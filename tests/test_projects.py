import pytest
from uuid import uuid4
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError

from data.samples import SAMPLE_GEOJSON
from projects_manager.domain.projects.models import Project


def get_projects_parameters(create: bool = True):
    project_str = "New" if create else "Updated"
    test_cases = [
        (
            {
                "name": f"{project_str} Project",
                "description": f"{project_str} Project Description",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "area_of_interest": SAMPLE_GEOJSON,
            },
            200,
        ),
        (
            {
                "name": f"{project_str} Project",
                "description": f"{project_str} Project Invalid Date",
                "start_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "end_date": date.today().strftime("%Y-%m-%d"),
                "area_of_interest": SAMPLE_GEOJSON,
            },
            422,
        ),
        (
            {
                "name": f"{project_str} Project",
                "description": f"{project_str} Project No Coordinates",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "area_of_interest": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "InvalidType",
                        "coordinates": [],
                    },
                },
            },
            422,
        ),
        (
            {
                "name": f"{project_str} Project",
                "description": f"{project_str} Project Invalid Coordinates",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "area_of_interest": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [-52.8430645648562, -5.63351005831322],
                            [-52.8289481608136, -5.674529420529012],
                            [-52.8114438198008, -5.6661010219506664],
                        ],
                    },
                },
            },
            422,
        ),
    ]
    if create:
        test_cases.extend([({}, 422), ({"name": "Only Name"}, 422)])
    return test_cases


@pytest.mark.parametrize(
    "payload,expected_status",
    get_projects_parameters(create=True),
)
def test_create_project(client, payload, expected_status):
    response = client.post("/api/projects/create", json=payload)
    assert response.status_code == expected_status


def test_get_projects_list(client, test_project):
    response = client.get("/api/projects/list")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["items"]
    assert response_data["items"][0]["id"] == str(test_project.id)
    assert response.json()["total"] == 1


def test_get_project_details__valid_id(client, test_project):
    response = client.get(f"/api/projects/details/{test_project.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["id"] == str(test_project.id)


def test_get_project_details__invalid_id(client, test_project):
    response = client.get(f"/api/projects/details/{str(uuid4())}")
    assert response.status_code == 404
    assert response.json()["detail"] == "PROJECT_NOT_FOUND"


@pytest.mark.parametrize(
    "payload,expected_status",
    get_projects_parameters(create=False),
)
def test_update_project_full_payload(client, test_project, payload, expected_status):
    response = client.patch(f"/api/projects/update/{test_project.id}", json=payload)
    assert response.status_code == expected_status
    if expected_status == 200:
        response_data = response.json()
        assert response_data
        assert response_data["id"] == str(test_project.id)
        assert response_data["name"] == "Updated Project"


@pytest.mark.parametrize(
    "payload,expected_status,updated_field",
    [
        ({"name": "Updated Project Name"}, 200, "name"),
        ({"description": "New Description"}, 200, "description"),
        ({"start_date": date.today().strftime("%Y-%m-%d")}, 200, "start_date"),
        (
            {"end_date": (date.today() + timedelta(days=60)).strftime("%Y-%m-%d")},
            200,
            "end_date",
        ),
        ({"area_of_interest": SAMPLE_GEOJSON}, 200, "area_of_interest"),
        (
            {
                "area_of_interest": {
                    "type": "Feature",
                    "geometry": {"type": "InvalidType", "coordinates": []},
                }
            },
            422,
            None,
        ),
    ],
)
def test_update_project_not_full_payload(
    client, test_project, payload, expected_status, updated_field
):
    response = client.patch(f"/api/projects/update/{test_project.id}", json=payload)
    assert response.status_code == expected_status
    if expected_status == 200:
        response_data = response.json()
        assert response_data["id"] == str(test_project.id)
        for key, value in payload.items():
            assert response_data[key] == value

        project_response = client.get(f"/api/projects/details/{test_project.id}")
        assert project_response.status_code == 200
        project_data = project_response.json()
        assert project_data[updated_field] == payload[updated_field]


def test_delete_project(client, test_project):
    list_projects_response = client.get("/api/projects/list")
    assert list_projects_response.status_code == 200
    assert list_projects_response.json()["total"] == 1

    delete_response = client.delete(f"/api/projects/delete/{test_project.id}")
    assert delete_response.status_code == 200

    list_projects_response = client.get("/api/projects/list")
    assert list_projects_response.status_code == 200
    assert list_projects_response.json()["total"] == 0


def test_start_date_before_end_date(test_db):
    today = date.today()
    invalid_project: Project = Project(
        name="Invalid Project",
        description="Invalid description",
        start_date=today,
        end_date=today - timedelta(days=30),
        area_of_interest=SAMPLE_GEOJSON,
    )

    test_db.add(invalid_project)

    with pytest.raises(IntegrityError):
        test_db.commit()
