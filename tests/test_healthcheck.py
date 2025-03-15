from projects_manager.domain.projects.models import Project


def test_healthcheck(test_project: Project):
    assert test_project.name == "Test Project"
