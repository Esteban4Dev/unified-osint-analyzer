"""
DNS Dumpster no ofrece una API pública oficial (su web usa un token de sesión
pensado solo para uso interactivo). En vez de scrapear su sitio, este servicio
hace su propio reconocimiento DNS directo, lo cual es más estable y no
depende de terceros.
"""

import asyncio

import dns.resolver

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]


def _query_sync(domain: str) -> dict:
    records: dict[str, list[str]] = {}
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    for rtype in RECORD_TYPES:
        try:
            answers = resolver.resolve(domain, rtype)
            records[rtype] = [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            records[rtype] = []
        except Exception as exc:  # noqa: BLE001
            records[rtype] = [f"error: {exc}"]

    return records


async def lookup_domain(domain: str) -> dict:
    records = await asyncio.to_thread(_query_sync, domain)
    return {"configured": True, "records": records}
