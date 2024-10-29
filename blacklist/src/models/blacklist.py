from uuid import uuid4

from sqlalchemy import func, UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import db


class Blacklist(db.Model):
    __tablename__ = "blacklists"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, nullable=False)
    client_id: Mapped[UUID] = mapped_column(UUID(as_uuid=False), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
