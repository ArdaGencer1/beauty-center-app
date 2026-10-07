"""Static tag surface of the served site.

Reads what a browser would actually receive: which tag assets each page pulls
and in what order, which Google Ads conversion labels the JavaScript is able to
fire, and whether the pre-compressed ``.gz`` twin nginx may serve still matches
the plain file.

Read-only.  Nothing here touches the network or the Google Ads account.
"""
from __future__ import annotations

import gzip
import re
from dataclasses import dataclass, field
from pathlib import Path

from adsai import config

# public_html is a symlink into releases/; resolve so mtimes and .gz twins are
# read from the release that is actually being served.
SITE_DIR = (config.ROOT_DIR.parent / "public_html").resolve()

# A page is a candidate only if it is the live file.  The tree carries hundreds
# of .bak-* and .gz twins next to every page; counting those as pages would
# report coverage against files no browser can request.
_BACKUP = re.compile(r"\.(bak|gz|rollback|backup)(\b|[-.])", re.IGNORECASE)

LABEL_RE = re.compile(r"AW-\d+/[A-Za-z0-9_-]+")
AW_ID_RE = re.compile(r"AW-\d{6,}")
GA4_ID_RE = re.compile(r"G-[A-Z0-9]{6,}")
GTM_ID_RE = re.compile(r"GTM-[A-Z0-9]{5,}")
SCRIPT_SRC_RE = re.compile(r"<script[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
GTAG_LOADER_RE = re.compile(r"googletagmanager\.com/gtag/js")
GTM_LOADER_RE = re.compile(r"googletagmanager\.com/gtm\.js")
CONSENT_DEFAULT_RE = re.compile(r"""consent['"]?\s*,\s*['"]default""")
# gtag(js, ...) instead of gtag('js', ...): a bare identifier where a string
# belongs.  It throws a ReferenceError on the first call, so every later
# gtag() in that block -- including the AW- config -- never runs.
UNQUOTED_GTAG_RE = re.compile(r"gtag\(\s*(?!['\"])(?:js|config|event|set|consent)\b")

# Assets every ad landing page is expected to carry.  Absence is not a style
# problem: a page without the loader records nothing at all for the ad traffic
# that lands on it.
EXPECTED_ASSETS = ("consent-bootstrap.js", "script.js", "ads-tracking.js")


def is_live_file(path: Path) -> bool:
    return not _BACKUP.search(path.name)


# A file on disk is not a page a browser can reach.  21 of the 128 .html files
# in this tree are never served: 17 are redirected to a different page by the
# organic-SEO consolidation map, and 4 directory index.html files lose to a
# root-level file of the same name.  Auditing them produced three confident
# criticals about measurement that no visitor can experience -- including
# "epilasyon.html loads no Google tag", whose URL 301s to /laser-signature,
# and "the site fires into a REMOVED conversion action", whose only reference
# lived in koru-protez-tirnak.html, which 301s to /protez-tirnak.
NGINX_REDIRECT_SNIPPET = Path("/etc/nginx/snippets/sgb_organic_redirects.conf")
_REWRITE_RE = re.compile(r"^\s*rewrite\s+(\S+)\s+(\S+)\s+permanent\s*;", re.MULTILINE)


def redirect_rules(snippet: Path | None = None) -> list[tuple[re.Pattern[str], str]]:
    """The nginx rules that send a path somewhere other than its own file."""
    path = snippet or NGINX_REDIRECT_SNIPPET
    try:
        text = path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        # Unreadable config is not evidence that nothing is redirected, so the
        # caller keeps every page rather than silently trusting an empty map.
        return []
    rules: list[tuple[re.Pattern[str], str]] = []
    for pattern, target in _REWRITE_RE.findall(text):
        try:
            rules.append((re.compile(pattern), target))
        except re.error:
            continue
    return rules


def canonical_path(page: Path, site_dir: Path | None = None) -> str:
    """The URL nginx canonicalises this file to (extensionless)."""
    rel = page.relative_to(site_dir or SITE_DIR).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    return "/" + rel[: -len(".html")]


def unserved_reason(
    page: Path,
    site_dir: Path | None = None,
    rules: list[tuple[re.Pattern[str], str]] | None = None,
) -> str | None:
    """Why no browser receives this file, or None when it is really served."""
    root = site_dir or SITE_DIR
    rel = page.relative_to(root).as_posix()

    # `rewrite ^/(.+)/index\.html/?$ -> /$1` then resolves /$1 to $1.html, so a
    # root-level twin always wins over the directory index.
    if rel.endswith("/index.html"):
        stem = rel[: -len("/index.html")]
        if (root / f"{stem}.html").is_file():
            return f"golgelendi: /{stem} -> {stem}.html"

    url = canonical_path(page, root)
    for pattern, target in (redirect_rules() if rules is None else rules):
        if pattern.search(url) or pattern.search(url + ".html"):
            if not target.rstrip("/").endswith(url):
                return f"301 -> {target}"
    return None


def unserved_pages(site_dir: Path | None = None) -> dict[Path, str]:
    """Every .html file on disk that no browser can reach, with the reason."""
    root = site_dir or SITE_DIR
    rules = redirect_rules()
    out: dict[Path, str] = {}
    for path in sorted(root.rglob("*.html")):
        if not is_live_file(path):
            continue
        reason = unserved_reason(path, root, rules)
        if reason:
            out[path] = reason
    return out


def pages(site_dir: Path | None = None) -> list[Path]:
    """Every served page, including the ones in subdirectories.

    `iletisim/`, `cilt-bakimi/`, `kalici-makyaj/` and `bolgesel-incelme/` each
    hold an `index.html` that ads land on. A top-level glob misses all four and
    reports a clean sheet for pages it never opened.
    """
    root = site_dir or SITE_DIR
    rules = redirect_rules()
    return sorted(
        p
        for p in root.rglob("*.html")
        if is_live_file(p) and not unserved_reason(p, root, rules)
    )


def scripts(site_dir: Path | None = None) -> list[Path]:
    root = site_dir or SITE_DIR
    return sorted(p for p in root.rglob("*.js") if is_live_file(p))


def page_name(path: Path, site_dir: Path | None = None) -> str:
    """Path relative to the site root -- four files are called index.html."""
    root = site_dir or SITE_DIR
    try:
        return str(path.relative_to(root))
    except ValueError:
        return path.name


@dataclass
class PageTags:
    """What one page would load, with the line each fact was found on."""

    name: str
    gtag_loader_line: int | None = None
    gtm_loader_line: int | None = None
    consent_default_line: int | None = None
    aw_ids: list[str] = field(default_factory=list)
    ga4_ids: list[str] = field(default_factory=list)
    gtm_ids: list[str] = field(default_factory=list)
    assets: list[tuple[str, int]] = field(default_factory=list)
    labels: list[tuple[str, int]] = field(default_factory=list)
    unquoted_gtag: list[int] = field(default_factory=list)

    @property
    def asset_names(self) -> set[str]:
        """Basenames of the site's own scripts.

        Third-party loaders are excluded: they are tracked by their own fields,
        and taking the basename of a URL like ``gtag/js?id=`` would otherwise
        enter a phantom asset called ``js`` into every page.
        """
        return {
            Path(s.split("?")[0]).name
            for s, _ in self.assets
            if not s.startswith(("http://", "https://", "//"))
        }

    @property
    def missing_assets(self) -> list[str]:
        have = self.asset_names
        return [a for a in EXPECTED_ASSETS if a not in have]

    @property
    def consent_before_loader(self) -> bool | None:
        """Consent Mode v2 requires the default state to be set before the tag
        loads.  Setting it afterwards means the first hit of every session
        leaves under the wrong consent state, which cannot be repaired later.

        None when there is no loader to be ordered against.
        """
        if self.gtag_loader_line is None:
            return None
        if self.consent_default_line is None:
            return False
        return self.consent_default_line < self.gtag_loader_line

    def to_dict(self) -> dict:
        return {
            "page": self.name,
            "gtag_loader_line": self.gtag_loader_line,
            "gtm_loader_line": self.gtm_loader_line,
            "consent_default_line": self.consent_default_line,
            "consent_before_loader": self.consent_before_loader,
            "aw_ids": self.aw_ids,
            "ga4_ids": self.ga4_ids,
            "gtm_ids": self.gtm_ids,
            "assets": [{"src": s, "line": n} for s, n in self.assets],
            "labels": [{"label": l, "line": n} for l, n in self.labels],
            "missing_assets": self.missing_assets,
            "unquoted_gtag_lines": self.unquoted_gtag,
        }


def scan_page(path: Path, site_dir: Path | None = None) -> PageTags:
    tags = PageTags(name=page_name(path, site_dir))
    seen_aw, seen_ga4, seen_gtm = set(), set(), set()
    # consent-bootstrap.js sets the default state, so the asset's own <script>
    # line counts as the consent point even though the call lives in the file.
    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if tags.gtag_loader_line is None and GTAG_LOADER_RE.search(line):
            tags.gtag_loader_line = lineno
        if tags.gtm_loader_line is None and GTM_LOADER_RE.search(line):
            tags.gtm_loader_line = lineno
        if tags.consent_default_line is None and (
            CONSENT_DEFAULT_RE.search(line) or "consent-bootstrap.js" in line
        ):
            tags.consent_default_line = lineno
        for src in SCRIPT_SRC_RE.findall(line):
            tags.assets.append((src, lineno))
        for label in LABEL_RE.findall(line):
            tags.labels.append((label, lineno))
        if UNQUOTED_GTAG_RE.search(line):
            tags.unquoted_gtag.append(lineno)
        for rex, bag, out in (
            (AW_ID_RE, seen_aw, tags.aw_ids),
            (GA4_ID_RE, seen_ga4, tags.ga4_ids),
            (GTM_ID_RE, seen_gtm, tags.gtm_ids),
        ):
            for found in rex.findall(line):
                if found not in bag:
                    bag.add(found)
                    out.append(found)
    return tags


@dataclass
class LabelSite:
    """One place in the JavaScript where a conversion label can be sent."""

    label: str
    file: str
    line: int
    via_variable: str | None = None
    used_lines: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "where": f"{self.file}:{self.line}",
            "via_variable": self.via_variable,
            "sent_on_lines": self.used_lines,
        }


_ASSIGN_RE = re.compile(
    r"(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*['\"](AW-\d+/[A-Za-z0-9_-]+)['\"]"
)


def scan_script(path: Path, site_dir: Path | None = None) -> list[LabelSite]:
    """Find every conversion label a script can fire.

    Labels are rarely written at the call site -- they are assigned to a
    constant and that constant is passed as ``send_to``.  Matching only the
    literal would find the definition and miss whether anything actually sends
    it, so the variable is followed to its uses.
    """
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    found: dict[str, LabelSite] = {}

    for lineno, line in enumerate(lines, 1):
        for name, label in _ASSIGN_RE.findall(line):
            found[label] = LabelSite(label, page_name(path, site_dir), lineno, via_variable=name)
        for label in LABEL_RE.findall(line):
            if label not in found:
                found[label] = LabelSite(label, page_name(path, site_dir), lineno)

    for site in found.values():
        if site.via_variable:
            use = re.compile(r"send_to\s*:\s*" + re.escape(site.via_variable) + r"\b")
        else:
            use = re.compile(r"send_to\s*:\s*['\"]" + re.escape(site.label) + r"['\"]")
        site.used_lines = [n for n, line in enumerate(lines, 1) if use.search(line)]

    return sorted(found.values(), key=lambda s: (s.file, s.line))


@dataclass
class GzTwin:
    """A pre-compressed file nginx may serve instead of the plain one."""

    name: str
    matches: bool
    reason: str

    def to_dict(self) -> dict:
        return {"file": self.name, "matches": self.matches, "reason": self.reason}


def gz_twins(site_dir: Path | None = None) -> list[GzTwin]:
    """Compare every live file against its ``.gz`` twin.

    With ``gzip_static`` on, nginx prefers the ``.gz``.  A twin left behind by
    an edit keeps serving the previous tag code to every client that sends
    ``Accept-Encoding: gzip`` -- which is all of them -- while the plain file on
    disk reads correct to anyone inspecting it.
    """
    root = site_dir or SITE_DIR
    out: list[GzTwin] = []
    for plain in sorted(
        list(root.rglob("*.html")) + list(root.rglob("*.js")) + list(root.rglob("*.css"))
    ):
        if not is_live_file(plain):
            continue
        twin = plain.with_name(plain.name + ".gz")
        if not twin.exists():
            continue
        try:
            same = gzip.decompress(twin.read_bytes()) == plain.read_bytes()
        except OSError as exc:
            out.append(GzTwin(page_name(plain, root), False, f"unreadable: {exc}"))
            continue
        out.append(
            GzTwin(
                page_name(plain, root),
                same,
                "identical" if same else "STALE -- .gz serves different bytes",
            )
        )
    return out


def survey(site_dir: Path | None = None) -> dict:
    """Everything the static side knows, in one pass."""
    root = site_dir or SITE_DIR
    page_tags = [scan_page(p, root) for p in pages(root)]
    label_sites: list[LabelSite] = []
    for js in scripts(root):
        label_sites.extend(scan_script(js, root))
    return {
        "site_dir": str(root),
        "page_count": len(page_tags),
        "pages": page_tags,
        "label_sites": label_sites,
        "gz_twins": gz_twins(root),
    }
