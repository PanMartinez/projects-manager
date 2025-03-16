from uuid import UUID
from datetime import datetime
from typing import Dict, Any, List
from pydantic import field_validator
from pydantic import BaseModel, Field

from projects_manager.domain.common.schemas import OrmBaseModel


class AreaOfInterest(BaseModel):
    type: str
    properties: Dict[str, Any] = {}
    geometry: Dict[str, Any]


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    description: str | None = None
    start_date: datetime
    end_date: datetime
    area_of_interest: AreaOfInterest


class ProjectDetailsSchema(ProjectBase, OrmBaseModel):
    id: UUID


class ProjectListSchema(BaseModel):
    items: List[ProjectDetailsSchema]
    total: int


class ProjectActionBase(ProjectBase):
    @field_validator("end_date", mode="before")
    @classmethod
    def end_date_must_be_after_start_date(cls, v, values):
        values_data = values.data

        if "start_date" in values_data and v < values_data["start_date"].strftime(
            "%Y-%m-%d"
        ):
            raise ValueError("end_date must be after start_date")
        return v


class ProjectCreateSchema(ProjectActionBase):
    pass


class ProjectUpdateSchema(ProjectBase):
    pass
