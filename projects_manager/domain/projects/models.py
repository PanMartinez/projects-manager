from __future__ import annotations

from sqlalchemy import String, Text, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column

from projects_manager.domain.common.models import Base


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    end_date: Mapped[str] = mapped_column(Date, nullable=False)
    area_of_interest: Mapped[str] = mapped_column(JSON, nullable=False)
