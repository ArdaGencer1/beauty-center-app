"""Google Ads API client — .env uzerinden baglanti."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


def _env(key: str) -> str:
    return os.getenv(key, "").strip().strip('"')


def get_client() -> GoogleAdsClient:
    return GoogleAdsClient.load_from_dict(
        {
            "developer_token": _env("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": _env("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": _env("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": _env("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": _env("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True,
        }
    )


def get_customer_id() -> str:
    return _env("GOOGLE_ADS_CUSTOMER_ID").replace("-", "")
