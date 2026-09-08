import ipaddress
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.i18n import t
from app.models.scan import ScanRecord
from app.utils.db import get_session
from app.services import (
    shodan_service,
    virustotal_service,
    hibp_service,
    securitytrails_service,
    dnsdumpster_service,
)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    lang: str = "es"  # "es" o "en"


def _detect_query_type(query: str) -> str:
    query = query.strip()
    try:
        ipaddress.ip_address(query)
        return "ip"
    except ValueError:
        pass
    if "@" in query:
        return "email"
    if "." in query:
        return "domain"
    return "username"


@router.get("/sources")
async def sources_status():
    """Indica qué fuentes están configuradas con API key."""
    return settings.configured_sources()


@router.post("/search")
async def unified_search(payload: SearchRequest, session: AsyncSession = Depends(get_session)):
    query = payload.query.strip()
    lang = payload.lang if payload.lang in ("es", "en") else "es"
    qtype = _detect_query_type(query)

    result: dict = {}

    if qtype == "ip":
        result["shodan"] = await shodan_service.lookup_ip(query, lang)
        result["virustotal"] = await virustotal_service.lookup_ip(query, lang)
        result["dns"] = {"configured": False, "error": t("dns_not_applicable", lang)}
    elif qtype == "domain":
        result["shodan"] = await shodan_service.resolve_domain(query, lang)
        result["virustotal"] = await virustotal_service.lookup_domain(query, lang)
        result["securitytrails"] = await securitytrails_service.lookup_domain(query, lang)
        result["dns"] = await dnsdumpster_service.lookup_domain(query)
    elif qtype == "email":
        result["hibp"] = await hibp_service.lookup_email(query, lang)
    else:
        result["message"] = {"configured": True, "note": t("username_not_connected", lang)}

    record = ScanRecord(query=query, query_type=qtype, result_json=json.dumps(result))
    session.add(record)
    await session.commit()
    await session.refresh(record)

    return record.to_dict()


@router.get("/history")
async def get_history(limit: int = 20, session: AsyncSession = Depends(get_session)):
    stmt = select(ScanRecord).order_by(ScanRecord.id.desc()).limit(limit)
    rows = (await session.execute(stmt)).scalars().all()
    return [row.to_dict() for row in rows]
