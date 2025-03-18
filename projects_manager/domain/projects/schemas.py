from uuid import UUID
from datetime import date
from typing import Dict, Any
from pydantic import field_validator
from pydantic import BaseModel, Field

from projects_manager.domain.common.schemas import OrmBaseModel


class AreaOfInterest(BaseModel):
    type: str
    properties: Dict[str, Any] = {}
    geometry: Dict[str, Any]

    @field_validator("geometry", mode="before")
    @classmethod
    def validate_geometry(cls, v):
        if not isinstance(v, dict):
            raise ValueError("geometry must be a dictionary")

        if v.get("type") != "MultiPolygon":
            raise ValueError("Only 'MultiPolygon' geometry type is allowed")

        if "coordinates" not in v or not isinstance(v["coordinates"], list):
            raise ValueError("geometry must contain a 'coordinates' list")

        if not all(
            isinstance(polygon, list)
            and all(isinstance(area, list) and len(area) >= 4 for area in polygon)
            for polygon in v["coordinates"]
        ):
            raise ValueError(
                "Invalid 'MultiPolygon' structure. Each polygon must contain at least one area with 4+ points."
            )

        return v


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    description: str | None = None
    start_date: date
    end_date: date
    area_of_interest: AreaOfInterest


class ProjectDetailsSchema(ProjectBase, OrmBaseModel):
    id: UUID


class ProjectCreateSchema(ProjectBase):
    @field_validator("end_date", mode="before")
    @classmethod
    def validate_end_date(cls, v, values):
        values_data = values.data

        if "start_date" in values_data and v < values_data["start_date"].strftime(
            "%Y-%m-%d"
        ):
            raise ValueError("end_date must be after start_date")
        return v


class ProjectUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=32)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    area_of_interest: AreaOfInterest | None = None

    @field_validator("end_date", mode="before")
    @classmethod
    def validate_end_date(cls, v, values):
        values_data = values.data
        if (
            values_data["start_date"] is not None
            and v
            and v < values_data["start_date"].strftime("%Y-%m-%d")
        ):
            raise ValueError("end_date must be after start_date")
        return v
