from __future__ import annotations

from datetime import date
from sqlalchemy import CheckConstraint, String, Text, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column

from projects_manager.domain.common.models import Base


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    area_of_interest: Mapped[dict] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="check_start_end_date"),
    )
