from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from sqlalchemy import select

from app.models.scan import ScanRecord
from app.utils.db import async_session
from app.utils.report_generator import to_json_bytes, to_pdf_bytes

router = APIRouter()


@router.get("/{record_id}/{fmt}")
async def export_report(record_id: int, fmt: str):
    if fmt not in ("pdf", "json"):
        raise HTTPException(400, "Formato no soportado, usa 'pdf' o 'json'")

    async with async_session() as session:
        record = await session.get(ScanRecord, record_id)

    if not record:
        raise HTTPException(404, "Registro no encontrado")

    data = record.to_dict()

    if fmt == "json":
        content = to_json_bytes(data["query"], data["query_type"], data["result"])
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=reporte_{record_id}.json"},
        )

    content = to_pdf_bytes(data["query"], data["query_type"], data["result"])
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=reporte_{record_id}.pdf"},
    )
