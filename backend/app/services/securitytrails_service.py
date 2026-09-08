import httpx

from app.core.config import settings
from app.core.i18n import t

BASE_URL = "https://api.securitytrails.com/v1"


async def lookup_domain(domain: str, lang: str = "es") -> dict:
    if not settings.securitytrails_api_key:
        return {"configured": False, "error": t("securitytrails_key_missing", lang)}

    url = f"{BASE_URL}/domain/{domain}"
    headers = {"APIKEY": settings.securitytrails_api_key}

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code != 200:
        return {"configured": True, "error": t("securitytrails_http_error", lang, code=resp.status_code)}

    data = resp.json()
    return {
        "configured": True,
        "hostname": data.get("hostname"),
        "alexa_rank": data.get("alexa_rank"),
        "current_dns": data.get("current_dns", {}),
    }
