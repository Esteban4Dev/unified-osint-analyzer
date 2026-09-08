import httpx

from app.core.config import settings
from app.core.i18n import t

BASE_URL = "https://haveibeenpwned.com/api/v3"


async def lookup_email(email: str, lang: str = "es") -> dict:
    """Busca brechas asociadas a un email. Requiere API key de pago de HIBP."""
    if not settings.hibp_api_key:
        return {"configured": False, "error": t("hibp_key_missing", lang)}

    url = f"{BASE_URL}/breachedaccount/{email}"
    headers = {"hibp-api-key": settings.hibp_api_key, "user-agent": "osint-dashboard"}

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, headers=headers, params={"truncateResponse": "false"})
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code == 404:
        return {"configured": True, "breaches": [], "message": t("hibp_no_breaches", lang)}
    if resp.status_code != 200:
        return {"configured": True, "error": t("hibp_http_error", lang, code=resp.status_code)}

    breaches = resp.json()
    return {
        "configured": True,
        "breaches": [
            {"name": b.get("Name"), "date": b.get("BreachDate"), "data_classes": b.get("DataClasses")}
            for b in breaches
        ],
    }
