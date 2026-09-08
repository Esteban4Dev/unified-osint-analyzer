import datetime
import json

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class ScanRecord(Base):
    """Un registro de historial: qué se consultó y qué se obtuvo."""

    __tablename__ = "scan_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    query: Mapped[str] = mapped_column(String(255))
    query_type: Mapped[str] = mapped_column(String(20))  # domain | ip | email | username
    result_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "query": self.query,
            "query_type": self.query_type,
            "result": json.loads(self.result_json),
            "created_at": self.created_at.isoformat(),
        }
