from uuid import UUID
from datetime import date
from typing import Dict, Any, List
from pydantic import field_validator
from pydantic import BaseModel, Field


class AreaOfInterest(BaseModel):
    type: str
    properties: Dict[str, Any] = {}
    geometry: Dict[str, Any]


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    description: str | None = None
    start_date: date
    end_date: date
    area_of_interest: AreaOfInterest

    @field_validator("end_date", mode="before")
    @classmethod
    def end_date_must_be_after_start_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class Project(ProjectBase):
    id: UUID

    class Config:
        orm_mode = True


class ProjectList(BaseModel):
    items: List[Project]
    total: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass
