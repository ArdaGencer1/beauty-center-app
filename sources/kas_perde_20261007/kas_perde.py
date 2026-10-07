#!/usr/bin/env python3
"""Kaş "Beş Perde" görselleri (plan: plans/claude/20261007/kas-yuz-hikaye-scroll.md).

İşlenmiş 1200w yarımlardan türetir; ham Instagram dosyası gerekmez.
Dürüstlük kuralları:
- Bir çiftin iki yarısına aynı kırpım ve aynı renk ayarı uygulanır.
- Kırpım yalnız "ALTIN ORAN KAŞ" hapını, imzayı ve komşu panel şeridini atar.
- Büyütme, cilt pürüzsüzleştirme, kıl koyulaştırma yok; kaş üstündeki monogram kalır.

Kullanım: python3 sources/kas_perde_20261007/kas_perde.py website/m/ig OUT_DIR
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

# slug -> (kaynak, kırpım [x0, y0, x1, y1] oran olarak)
BAND = (0.0, 0.0, 1.0, 0.69)  # etiket hapı tüm "sonra" yarılarında y≈0.70'te başlıyor
ITEMS = {
    "kas-perde-okuma": ("kas-altin-oran-once-1200.webp", BAND),
    "kas-perde-sonuc": ("kas-altin-oran-sonra-1200.webp", BAND),
    "kas-perde-harita": ("kas-kina-once-1200.webp", BAND),
    "kas-perde-alim": ("kas-kina-sonra-1200.webp", BAND),
    "kas-perde-gur-once": ("kas-cift-2-once-1200.webp", BAND),
    "kas-perde-gur": ("kas-cift-2-sonra-1200.webp", BAND),
    # dikey kapanış: hap ve imza alttan, boş yastık soldan kırpılır → 4:5
    "kas-profil-4x5": ("kas-profil-1200.webp", (0.15, 0.024, 1.0, 0.82)),
}
SIZES = (800, 1200)


def grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Color(im).enhance(1.02)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=3))


def main(src: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for slug, (name, (x0, y0, x1, y1)) in ITEMS.items():
        im = Image.open(src / name).convert("RGB")
        w, h = im.size
        im = grade(im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h))))
        for size in SIZES:
            if size > im.width:
                continue  # büyütme yok
            k = size / im.width
            im.resize((size, round(im.height * k)), Image.LANCZOS).save(
                out / f"{slug}-{size}.webp", quality=82, method=6
            )
        print(slug, im.size)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
