from __future__ import annotations

import gzip
import tempfile
import unittest
from pathlib import Path

from adsai import tag_surface


class TagCtxCoreTest(unittest.TestCase):
    def test_page_requires_consent_before_loader_and_expected_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "index.html"
            page.write_text(
                """<script src='/consent-bootstrap.js'></script>
<script async src='https://www.googletagmanager.com/gtag/js?id=AW-11538067972'></script>
<script src='/script.js'></script>
<script src='/ads-tracking.js'></script>
""",
                encoding="utf-8",
            )
            result = tag_surface.scan_page(page, root)
            self.assertTrue(result.consent_before_loader)
            self.assertEqual([], result.missing_assets)
            self.assertIn("AW-11538067972", result.aw_ids)

    def test_unquoted_gtag_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "broken.html"
            page.write_text("<script>gtag(js, new Date());</script>", encoding="utf-8")
            result = tag_surface.scan_page(page, root)
            self.assertEqual([1], result.unquoted_gtag)

    def test_script_scan_survives_control_bytes_and_follows_variable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "ads-tracking.js"
            script.write_bytes(
                b"const WA_LABEL='AW-11538067972/abc_DEF-123';\n"
                b"const clean=/[\x00-\x1f]/;\n"
                b"gtag('event','conversion',{send_to:WA_LABEL});\n"
            )
            sites = tag_surface.scan_script(script, root)
            self.assertEqual(1, len(sites))
            self.assertEqual("AW-11538067972/abc_DEF-123", sites[0].label)
            self.assertEqual([3], sites[0].used_lines)

    def test_stale_gzip_twin_is_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plain = root / "script.js"
            plain.write_bytes(b"new")
            plain.with_name("script.js.gz").write_bytes(gzip.compress(b"old"))
            twins = tag_surface.gz_twins(root)
            self.assertEqual(1, len(twins))
            self.assertFalse(twins[0].matches)
            self.assertIn("STALE", twins[0].reason)


if __name__ == "__main__":
    unittest.main()
