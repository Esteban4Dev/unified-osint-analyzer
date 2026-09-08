import httpx

from app.core.config import settings
from app.core.i18n import t

BASE_URL = "https://api.shodan.io"


async def lookup_ip(ip: str, lang: str = "es") -> dict:
    """Consulta información de un host (IP) en Shodan."""
    if not settings.shodan_api_key:
        return {"configured": False, "error": t("shodan_key_missing", lang)}

    url = f"{BASE_URL}/shodan/host/{ip}"
    params = {"key": settings.shodan_api_key}

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, params=params)
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code == 404:
        return {"configured": True, "error": t("shodan_not_found", lang)}
    if resp.status_code != 200:
        return {"configured": True, "error": t("shodan_http_error", lang, code=resp.status_code)}

    data = resp.json()
    return {
        "configured": True,
        "ip": data.get("ip_str"),
        "org": data.get("org"),
        "os": data.get("os"),
        "ports": data.get("ports", []),
        "hostnames": data.get("hostnames", []),
        "country": data.get("country_name"),
        "isp": data.get("isp"),
        "vulns": list(data.get("vulns", [])) if data.get("vulns") else [],
        "last_update": data.get("last_update"),
    }


async def resolve_domain(domain: str, lang: str = "es") -> dict:
    """Resuelve un dominio a IP usando la API de DNS de Shodan y consulta esa IP."""
    if not settings.shodan_api_key:
        return {"configured": False, "error": t("shodan_key_missing", lang)}

    url = f"{BASE_URL}/dns/resolve"
    params = {"hostnames": domain, "key": settings.shodan_api_key}

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, params=params)
        except httpx.RequestError as exc:
            return {"configured": True, "error": t("network_error", lang, detail=str(exc))}

    if resp.status_code != 200:
        return {"configured": True, "error": t("shodan_http_error", lang, code=resp.status_code)}

    data = resp.json()
    ip = data.get(domain)
    if not ip:
        return {"configured": True, "error": t("shodan_resolve_failed", lang)}

    host_info = await lookup_ip(ip, lang)
    host_info["resolved_ip"] = ip
    return host_info
