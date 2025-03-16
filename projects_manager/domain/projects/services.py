from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from projects_manager.domain.projects.models import Project
from projects_manager.handlers import ErrorMessages


async def get_project_by_id(project_id: UUID, db: Session) -> Project:
    project: Project | None = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PROJECT_NOT_FOUND,
        )
    return project
