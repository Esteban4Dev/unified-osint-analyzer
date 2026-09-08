import io
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def to_json_bytes(query: str, query_type: str, result: dict) -> bytes:
    payload = {"query": query, "query_type": query_type, "result": result}
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def to_pdf_bytes(query: str, query_type: str, result: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "OSINT Dashboard - Reporte")
    y -= 1 * cm

    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, y, f"Consulta: {query} ({query_type})")
    y -= 0.8 * cm

    c.setFont("Helvetica-Bold", 12)
    for source, data in result.items():
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, y, source.capitalize())
        y -= 0.6 * cm
        c.setFont("Helvetica", 9)
        for line in json.dumps(data, indent=2, ensure_ascii=False).splitlines():
            if y < 2 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 9)
            c.drawString(2.3 * cm, y, line[:110])
            y -= 0.45 * cm
        y -= 0.4 * cm

    c.save()
    return buffer.getvalue()
