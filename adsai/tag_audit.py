"""Cross-reference the site's tag surface against the Google Ads account.

Neither side is trustworthy alone.  The account knows which conversion actions
exist and which of them bidding treats as a goal; the site knows which labels
can actually be sent.  Every expensive measurement failure this account has had
lives in the gap between the two: a goal that cannot fire, a tag that fires into
a deleted action, a page carrying no tag at all.

Read-only.  Produces findings; applies nothing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from adsai import config, tag_account, tag_surface

CRITICAL, WARN, INFO = "critical", "warn", "info"


def _dead_primary_fix(action, twins: list) -> str:
    """What to do about a goal that cannot fire.

    The obvious repair -- wire the label up -- is the wrong one when a live
    action already measures the same event in the same biddable goal: it would
    start counting every interaction twice.
    """
    if twins:
        names = ", ".join(f"{t.id} ({t.name})" for t in twins)
        return (
            f"Etiketi bağlama. {names} aynı olayı zaten ölçüyor ve aynı biddable "
            "hedefte; bağlamak çift sayım yaratır. Bunun yerine bu mükerreri "
            "kaldır ya da primary_for_goal'ünü düşür. Önce: ads_ctx.py guard + blast."
        )
    return (
        "Ya etiketi siteye bağla, ya primary_for_goal'ü kaldır. "
        "Karar öncesi: ads_ctx.py guard + blast."
    )
_ORDER = {CRITICAL: 0, WARN: 1, INFO: 2}


@dataclass
class Finding:
    id: str
    severity: str
    title: str
    evidence: list[str] = field(default_factory=list)
    cost: str = ""
    fix: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "severity": self.severity,
            "title": self.title,
            "evidence": self.evidence,
            "cost": self.cost,
            "fix": self.fix,
        }


# Words that say what a conversion action is actually measuring. Two ENABLED
# actions sharing a category and one of these are measuring the same event,
# whatever their names happen to be.
_INTENT_WORDS = {
    "whatsapp": "whatsapp",
    "wa": "whatsapp",
    "telefon": "phone",
    "phone": "phone",
    "call": "phone",
    "arama": "phone",
    "form": "form",
    "lead": "lead",
    "iletisim": "contact",
    "contact": "contact",
    "kisi": "contact",
    "randevu": "appointment",
    "payment": "payment",
    "odeme": "payment",
    "purchase": "payment",
}


def _intent_of(name: str) -> str | None:
    import unicodedata

    plain = "".join(
        c for c in unicodedata.normalize("NFKD", name.lower())
        if not unicodedata.combining(c)
    )
    for token in __import__("re").split(r"[^a-z0-9]+", plain):
        if token in _INTENT_WORDS:
            return _INTENT_WORDS[token]
    return None


def audit(offline: bool = False, site_dir: Path | None = None) -> dict:
    actions, as_of = tag_account.load(offline=offline)
    survey = tag_surface.survey(site_dir)

    # Where each label can be sent from, byte-safely -- grep misses these files.
    site_labels: dict[str, list[str]] = {}
    for page in survey["pages"]:
        for label, line in page.labels:
            site_labels.setdefault(label, []).append(f"{page.name}:{line}")
    for site in survey["label_sites"]:
        site_labels.setdefault(site.label, []).append(f"{site.file}:{site.line}")

    by_label = {lab: a for a in actions for lab in a.labels}
    findings: list[Finding] = []

    try:
        biddable = tag_account.biddable_categories()
        settings = tag_account.account_settings()
    except Exception:  # noqa: BLE001 - offline or API down; degrade, do not fail
        biddable, settings = set(), {}

    # Actions measuring the same thing inside the same biddable goal.
    intent_groups: dict[tuple[str, str], list] = {}
    for action in actions:
        if action.status != "ENABLED":
            continue
        # Only primary actions feed bidding, so only they can double-count it.
        # The four offline payment actions share the "payment" token while
        # measuring genuinely different payments -- they are secondary, and
        # filtering here keeps them out without special-casing them by name.
        if not action.primary_for_goal:
            continue
        intent = _intent_of(action.name)
        if intent and action.category in biddable:
            intent_groups.setdefault((action.category, intent), []).append(action)
    twins = {
        a.id: [o for o in group if o.id != a.id]
        for group in intent_groups.values()
        if len(group) > 1
        for a in group
    }

    # --- account side: goals that cannot fire ------------------------------
    for action in actions:
        if action.status != "ENABLED" or not action.is_tag_borne:
            continue
        where = [w for lab in action.labels for w in site_labels.get(lab, [])]
        if where:
            continue
        if action.primary_for_goal and action.conversions_30d == 0:
            findings.append(
                Finding(
                    id=f"dead_primary::{action.id}",
                    severity=CRITICAL,
                    title=f"{action.name} birincil hedef ama hiç fire edemiyor",
                    evidence=[
                        f"conversion_action/{action.id} status=ENABLED primary_for_goal=True",
                        f"labels={action.labels}",
                        "30 günde 0 dönüşüm; etiket hiçbir canlı html/js dosyasında yok",
                    ],
                    cost=(
                        "primary_for_goal olduğu için teklif algoritması bunu hedef sayar. "
                        "Yapısal olarak fire edemeyen bir hedef, Max Conversions kampanyalarına "
                        "sürekli 'bu dönüşüm hiç gelmiyor' sinyali verir."
                    ),
                    fix=_dead_primary_fix(action, twins.get(action.id, [])),
                )
            )
        else:
            findings.append(
                Finding(
                    id=f"orphan_label::{action.id}",
                    severity=WARN,
                    title=f"{action.name} etiketi sitede yok ama dönüşüm alıyor",
                    evidence=[
                        f"conversion_action/{action.id} labels={action.labels}",
                        f"30 günde {action.conversions_30d:.0f} dönüşüm",
                    ],
                    cost="Fire noktası site kodunda değil; GTM container'ından geliyor olabilir.",
                    fix="GTM envanteri (Faz 3) olmadan kaynağı kesinleştirilemez.",
                )
            )

    # --- site side: tags pointing nowhere ----------------------------------
    for label, where in sorted(site_labels.items()):
        action = by_label.get(label)
        if action is None:
            findings.append(
                Finding(
                    id=f"unknown_label::{label}",
                    severity=CRITICAL,
                    title=f"Site hesapta hiç bulunmayan bir etiketi gönderiyor: {label}",
                    evidence=where,
                    cost="Gönderilen her hit kayboluyor; o etkileşim hiçbir yerde sayılmıyor.",
                    fix="Etiketi canlı bir conversion action'ınkiyle değiştir ya da çağrıyı kaldır.",
                )
            )
        elif action.status == "REMOVED":
            findings.append(
                Finding(
                    id=f"ghost_label::{action.id}",
                    severity=CRITICAL,
                    title=f"Site silinmiş bir aksiyona ateş ediyor: {action.name}",
                    evidence=where + [f"conversion_action/{action.id} status=REMOVED"],
                    cost=(
                        "Silinmiş aksiyon hiçbir şey kaydetmez."
                        + (
                            " Üstelik WEBSITE_CALL: numara değiştirme (phone_conversion_number) "
                            "silinmiş bir aksiyona bağlı çalışıyor."
                            if action.type == "WEBSITE_CALL"
                            else ""
                        )
                    ),
                    fix="Çağrıyı kaldır ya da canlı bir aksiyonun etiketine taşı.",
                )
            )
        elif len({w.split(":")[0] for w in where}) > 1:
            findings.append(
                Finding(
                    id=f"label_split::{action.id}",
                    severity=WARN,
                    title=f"{action.name} etiketi birden fazla dosyadan gönderiliyor",
                    evidence=where,
                    cost="Her iki yol da çalışırsa aynı etkileşim iki kez sayılabilir.",
                    fix=(
                        "Tekilleştirme bayrağının (ör. SGB_GADS_WA_SENT) her iki yolda da "
                        "okunduğunu doğrula. Kesin cevabı runtime verir: "
                        "tagtools/tag_probe.mjs --scenario whatsapp, same_endpoint_repeats "
                        "alanına bak -- farklı uç noktalar tek dönüşümün taşıyıcılarıdır."
                    ),
                )
            )

    # --- page coverage -----------------------------------------------------
    for page in survey["pages"]:
        if page.gtag_loader_line is None:
            # A page with no gtag.js of its own is not necessarily untagged: the
            # GTM container loads the Google tag itself. Four pages under
            # iletisim/, cilt-bakimi/, kalici-makyaj/ and bolgesel-incelme/ look
            # bare here and were proven at runtime to configure AW correctly.
            # Only a page with neither is genuinely unmeasured.
            if page.gtm_ids or page.gtm_loader_line is not None:
                findings.append(
                    Finding(
                        id=f"page_tagged_via_gtm::{page.name}",
                        severity=INFO,
                        title=f"{page.name}: Google tag'i GTM üzerinden geliyor",
                        evidence=[
                            f"kendi gtag.js loader'i yok; GTM={page.gtm_ids or 'inline'}"
                        ],
                        cost="Statik olarak doğrulanamaz; ölçüm container'a bağlı.",
                        fix=f"./run tag_ctx.py verify --pages {page.name}",
                    )
                )
                continue
            findings.append(
                Finding(
                    id=f"page_untagged::{page.name}",
                    severity=CRITICAL,
                    title=f"{page.name} hiç Google tag'i yüklemiyor",
                    evidence=[
                        f"{page.name}: ne gtag.js ne GTM; eksik varlıklar={page.missing_assets}"
                    ],
                    cost="Bu sayfaya inen reklam trafiği ölçülmüyor; dönüşümü de atfedilemiyor.",
                    fix="Diğer sayfalardaki tag bloğunu ve varlık sırasını bu sayfaya da uygula.",
                )
            )
            continue
        if page.unquoted_gtag:
            findings.append(
                Finding(
                    id=f"broken_gtag::{page.name}",
                    severity=CRITICAL,
                    title=f"{page.name}: gtag çağrıları tırnaksız, blok çalışmadan patlıyor",
                    evidence=[
                        f"{page.name} satır {page.unquoted_gtag}: gtag(js, ...) -- gtag('js', ...) olmalı",
                        "ilk çağrı ReferenceError atar; sonraki gtag('config', 'AW-...') hiç çalışmaz",
                    ],
                    cost=(
                        "Sayfa gtag.js'i yükler ama ne GA4 ne Ads hedefi yapılandırılır. "
                        "O sayfadaki hiçbir etkileşim Ads'e atfedilemez."
                    ),
                    fix="gtag('js', new Date()); gtag('config', 'G-...'); gtag('config', 'AW-...');",
                )
            )
        if page.consent_before_loader is False:
            findings.append(
                Finding(
                    id=f"consent_order::{page.name}",
                    severity=CRITICAL,
                    title=f"{page.name}: consent default gtag.js'ten sonra",
                    evidence=[
                        f"consent satırı={page.consent_default_line}, loader satırı={page.gtag_loader_line}"
                    ],
                    cost="Oturumun ilk hit'i yanlış consent durumunda gider; sonradan düzeltilemez.",
                    fix="consent-bootstrap.js'i gtag.js loader'ından önceye al.",
                )
            )
        if page.missing_assets:
            findings.append(
                Finding(
                    id=f"page_partial::{page.name}",
                    severity=WARN,
                    title=f"{page.name}: eksik tag varlığı {page.missing_assets}",
                    evidence=[f"yüklenenler={sorted(page.asset_names)}"],
                    cost="Eksik dosyanın bağladığı tıklama dönüşümleri bu sayfada fire etmez.",
                    fix="Eksik <script> etiketlerini standart sıraya ekle.",
                )
            )

    # --- what nginx actually serves ----------------------------------------
    for twin in survey["gz_twins"]:
        if not twin.matches:
            findings.append(
                Finding(
                    id=f"stale_gz::{twin.name}",
                    severity=CRITICAL,
                    title=f"{twin.name}.gz düz dosyayla eşleşmiyor",
                    evidence=[twin.reason],
                    cost=(
                        "gzip_static açıksa nginx .gz'yi tercih eder: tarayıcılar eski tag kodunu "
                        "alırken diskteki dosya doğru görünür."
                    ),
                    fix="Düzenlemeden sonra .gz ikizini yeniden üret.",
                )
            )

    # --- the same event measured twice inside one biddable goal ------------
    for (category, intent), group in sorted(intent_groups.items()):
        if len(group) < 2:
            continue
        live = [a for a in group if a.conversions_30d > 0]
        dead = [a for a in group if a.conversions_30d == 0]
        findings.append(
            Finding(
                id=f"duplicate_intent::{category}::{intent}",
                severity=WARN,
                title=f"{category} hedefinde aynı olayı ölçen {len(group)} aksiyon",
                evidence=[
                    f"{a.id} {a.name} -- 30 günde {a.conversions_30d:.0f}"
                    for a in sorted(group, key=lambda x: -x.conversions_30d)
                ],
                cost=(
                    f"{category} biddable bir hedef; içindeki aksiyonlar toplanır. "
                    "Şu an yalnızca biri fire ettiği için toplam doğru, ama ikisi "
                    "birden fire ederse aynı etkileşim iki kez sayılır ve teklif "
                    "algoritması olduğundan iyi bir dönüşüm oranı görür."
                ),
                fix=(
                    "Mükerreri kaldır ya da primary_for_goal'ünü düşür. "
                    + (
                        f"Canlı olan: {live[0].id} ({live[0].name}). "
                        if live else ""
                    )
                    + (
                        f"Ölü olan: {', '.join(a.id for a in dead)}."
                        if dead else ""
                    )
                ),
            )
        )

    # --- an account switch nothing feeds -----------------------------------
    if settings.get("enhanced_conversions_for_leads"):
        feeders = [
            s for s in survey["label_sites"]
            if "user_data" in Path(tag_surface.SITE_DIR / s.file).read_bytes()
            .decode("utf-8", "replace")
        ]
        if not feeders:
            findings.append(
                Finding(
                    id="enhanced_conversions_unfed",
                    severity=WARN,
                    title="Enhanced conversions açık ama siteden user_data gitmiyor",
                    evidence=[
                        "customer.conversion_tracking_setting."
                        "enhanced_conversions_for_leads_enabled = True",
                        "dönüşüm gönderen hiçbir dosyada user_data geçmiyor",
                    ],
                    cost=(
                        "Ayar açık olduğu için eşleştirme bekleniyor; besleme "
                        "olmayınca dönüşümler hash'li kimlik olmadan gidiyor ve "
                        "modellenen dönüşüm kazancı hiç gerçekleşmiyor."
                    ),
                    fix="Dönüşüm çağrılarına user_data ekle, ya da ayarı kapat.",
                )
            )

    # --- destinations that are not there -----------------------------------
    try:
        from adsai import tag_endpoints

        for probe in tag_endpoints.survey()["probes"]:
            if probe.verdict not in ("unreachable", "missing", "error"):
                continue
            findings.append(
                Finding(
                    id="unreachable_endpoint::" + probe.target.url.split("://", 1)[-1],
                    severity=CRITICAL,
                    title=f"Ölçüm ucu ulaşılamıyor: {probe.target.url}",
                    evidence=[probe.detail, f"kaynak: {probe.target.source}"],
                    cost=(
                        "Gönderen taraf hatayı yutuyor; oraya giden her olay "
                        "hiçbir sinyal vermeden kayboluyor."
                    ),
                    fix="Ucu ayağa kaldır ya da gönderen yapılandırmayı kaldır.",
                )
            )
    except Exception as exc:  # noqa: BLE001
        findings.append(
            Finding(
                id="endpoint_probe_failed",
                severity=INFO,
                title="Uç nokta yoklaması çalışmadı",
                evidence=[f"{type(exc).__name__}: {exc}"],
            )
        )

    removed_tagged = [a for a in actions if a.status == "REMOVED" and a.labels]
    if removed_tagged:
        findings.append(
            Finding(
                id="inventory_clutter",
                severity=INFO,
                title=f"{len(removed_tagged)} silinmiş ama etiketli conversion action",
                evidence=[f"{a.id} {a.name}" for a in removed_tagged],
                cost="Etiketleri hâlâ eşleşebilir; hangi etiketin canlı olduğunu okumayı zorlaştırır.",
                fix="Envanteri denetimde referans olarak tut; hesapta temizlik gerekmez.",
            )
        )

    findings.sort(key=lambda f: (_ORDER[f.severity], f.id))
    return {
        "as_of": as_of,
        "site_dir": survey["site_dir"],
        "pages_scanned": survey["page_count"],
        "actions_scanned": len(actions),
        "counts": {
            sev: sum(1 for f in findings if f.severity == sev)
            for sev in (CRITICAL, WARN, INFO)
        },
        "findings": findings,
    }
