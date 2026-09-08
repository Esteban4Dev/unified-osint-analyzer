import httpx

from app.core.config import settings
from app.core.i18n import t

BASE_URL = "https://www.virustotal.com/api/v3"


def _headers() -> dict:
    return {"x-apikey": settings.virustotal_api_key}


async def lookup_domain(domain: str, lang: str = "es") -> dict:
    if not settings.virustotal_api_key:
        return {"configured": False, "error": t("virustotal_key_missing", lang)}

    url = f"{BASE_URL}/domains/{domain}"
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, headers=_headers())
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code == 404:
        return {"configured": True, "error": t("virustotal_domain_not_found", lang)}
    if resp.status_code != 200:
        return {"configured": True, "error": t("virustotal_http_error", lang, code=resp.status_code)}

    attrs = resp.json().get("data", {}).get("attributes", {})
    stats = attrs.get("last_analysis_stats", {})
    return {
        "configured": True,
        "reputation": attrs.get("reputation"),
        "categories": attrs.get("categories", {}),
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
        "last_analysis_date": attrs.get("last_analysis_date"),
    }


async def lookup_ip(ip: str, lang: str = "es") -> dict:
    if not settings.virustotal_api_key:
        return {"configured": False, "error": t("virustotal_key_missing", lang)}

    url = f"{BASE_URL}/ip_addresses/{ip}"
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, headers=_headers())
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code != 200:
        return {"configured": True, "error": t("virustotal_http_error", lang, code=resp.status_code)}

    attrs = resp.json().get("data", {}).get("attributes", {})
    stats = attrs.get("last_analysis_stats", {})
    return {
        "configured": True,
        "reputation": attrs.get("reputation"),
        "asn": attrs.get("asn"),
        "as_owner": attrs.get("as_owner"),
        "country": attrs.get("country"),
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
    }
