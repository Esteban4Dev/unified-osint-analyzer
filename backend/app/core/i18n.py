"""Mensajes traducibles usados por los servicios y rutas del backend."""

MESSAGES = {
    "shodan_key_missing": {
        "es": "SHODAN_API_KEY no configurada",
        "en": "SHODAN_API_KEY not configured",
    },
    "virustotal_key_missing": {
        "es": "VIRUSTOTAL_API_KEY no configurada",
        "en": "VIRUSTOTAL_API_KEY not configured",
    },
    "hibp_key_missing": {
        "es": "HIBP_API_KEY no configurada (HaveIBeenPwned requiere una key paga)",
        "en": "HIBP_API_KEY not configured (HaveIBeenPwned requires a paid key)",
    },
    "securitytrails_key_missing": {
        "es": "SECURITYTRAILS_API_KEY no configurada",
        "en": "SECURITYTRAILS_API_KEY not configured",
    },
    "network_error": {
        "es": "Error de red: {detail}",
        "en": "Network error: {detail}",
    },
    "shodan_not_found": {
        "es": "No hay información en Shodan para este host",
        "en": "No information available on Shodan for this host",
    },
    "shodan_http_error": {
        "es": "Shodan devolvió HTTP {code}",
        "en": "Shodan returned HTTP {code}",
    },
    "shodan_resolve_failed": {
        "es": "No se pudo resolver el dominio",
        "en": "Could not resolve the domain",
    },
    "virustotal_domain_not_found": {
        "es": "Dominio no encontrado en VirusTotal",
        "en": "Domain not found on VirusTotal",
    },
    "virustotal_http_error": {
        "es": "VirusTotal devolvió HTTP {code}",
        "en": "VirusTotal returned HTTP {code}",
    },
    "hibp_http_error": {
        "es": "HIBP devolvió HTTP {code}",
        "en": "HIBP returned HTTP {code}",
    },
    "hibp_no_breaches": {
        "es": "No se encontraron brechas",
        "en": "No breaches found",
    },
    "securitytrails_http_error": {
        "es": "SecurityTrails devolvió HTTP {code}",
        "en": "SecurityTrails returned HTTP {code}",
    },
    "dns_not_applicable": {
        "es": "No aplica a IPs",
        "en": "Not applicable to IPs",
    },
    "username_not_connected": {
        "es": "Búsqueda por username aún no tiene una fuente conectada. Puedes agregar una en app/services/.",
        "en": "Username search doesn't have a connected source yet. You can add one in app/services/.",
    },
}


def t(key: str, lang: str = "es", **kwargs) -> str:
    """Traduce un mensaje. Si el idioma no existe, cae a español."""
    entry = MESSAGES.get(key, {})
    template = entry.get(lang) or entry.get("es") or key
    return template.format(**kwargs) if kwargs else template
