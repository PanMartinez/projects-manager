import logging

from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from projects_manager.config.cache import InMemoryCache
from projects_manager.config.dependencies import get_db
from projects_manager.domain.projects.models import Project
from projects_manager.domain.projects.services import get_project_by_id
from projects_manager.domain.projects.schemas import (
    ProjectDetailsSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)

projects_router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    include_in_schema=True,
)

logger = logging.getLogger(__name__)
cache = InMemoryCache()


@projects_router.post("/create", response_model=ProjectDetailsSchema)
async def create_project(
    project_data: ProjectCreateSchema,
    db: Session = Depends(get_db),
) -> ProjectDetailsSchema:
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        area_of_interest=project_data.area_of_interest.model_dump(),
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return ProjectDetailsSchema.model_validate(new_project)


@projects_router.get("/list", response_model=Page[ProjectDetailsSchema])
async def list_projects(
    db: Session = Depends(get_db),
) -> Page[ProjectDetailsSchema]:
    return paginate(db, select(Project))


@projects_router.get("/details/{project_id}", response_model=ProjectDetailsSchema)
async def get_project_details(
    project_id: UUID,
    db: Session = Depends(get_db),
) -> ProjectDetailsSchema:
    cache_key = f"project_details:{project_id}"
    cached_project = cache.get(cache_key)
    if cached_project:
        return cached_project

    project = await get_project_by_id(project_id, db)
    project_data = ProjectDetailsSchema.model_validate(project)
    cache.set(cache_key, project_data)
    return project_data


@projects_router.patch("/update/{project_id}", response_model=ProjectDetailsSchema)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdateSchema,
    db: Session = Depends(get_db),
) -> ProjectDetailsSchema:
    project = await get_project_by_id(project_id, db)
    project.name = project_data.name
    if project_data.description:
        project.description = project_data.description
    project.start_date = project_data.start_date
    project.end_date = project_data.end_date
    project.area_of_interest = project_data.area_of_interest.model_dump()
    db.commit()
    db.refresh(project)

    updated_project = ProjectDetailsSchema.model_validate(project)
    cache.set(f"project_details:{project_id}", updated_project)
    return updated_project


@projects_router.delete("/delete/{project_id}")
async def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    project = await get_project_by_id(project_id, db)
    db.delete(project)
    db.commit()
    cache.clear(f"project_details:{project_id}")
