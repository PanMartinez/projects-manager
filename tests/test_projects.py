import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from data.samples import SAMPLE_GEOJSON


@pytest.mark.parametrize(
    "payload,expected_status",
    [
        (
            {
                "name": "New Project",
                "description": "New Project Description",
                "start_date": datetime.today().strftime("%Y-%m-%d"),
                "end_date": (datetime.today() + timedelta(days=30)).strftime(
                    "%Y-%m-%d"
                ),
                "area_of_interest": SAMPLE_GEOJSON,
            },
            200,
        ),
        (
            {
                "name": "New Project",
                "description": "New Project Description",
                "start_date": (datetime.today() + timedelta(days=30)).strftime(
                    "%Y-%m-%d"
                ),
                "end_date": datetime.today().strftime("%Y-%m-%d"),
                "area_of_interest": SAMPLE_GEOJSON,
            },
            422,
        ),
        ({}, 422),
        ({"name": "Only Name"}, 422),
        (
            {
                "name": "Test Project",
                "description": "Invalid Date Test",
                "start_date": (datetime.today() + timedelta(days=10)).strftime(
                    "%Y-%m-%d"
                ),
                "end_date": datetime.today().strftime("%Y-%m-%d"),
                "area_of_interest": SAMPLE_GEOJSON,
            },
            422,
        ),
        (
            {
                "name": "Test Project",
                "description": "Test description",
                "start_date": datetime.today().strftime("%Y-%m-%d"),
                "end_date": (datetime.today() + timedelta(days=30)).strftime(
                    "%Y-%m-%d"
                ),
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
                "name": "Test Project",
                "description": "Test description",
                "start_date": datetime.today().strftime("%Y-%m-%d"),
                "end_date": (datetime.today() + timedelta(days=30)).strftime(
                    "%Y-%m-%d"
                ),
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
    ],
)
def test_create_project(client, payload, expected_status):
    response = client.post("/api/projects/create", json=payload)
    assert response.status_code == expected_status


def test_get_projects_list(client, test_project):
    response = client.get("/api/projects/list")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["projects"]
    assert response_data["projects"][0]["id"] == str(test_project.id)
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


def test_update_project(client, test_project):
    project_update_payload = {
        "name": "Updated Project",
        "description": "Updated Project Description",
        "start_date": test_project.start_date.strftime("%Y-%m-%d"),
        "end_date": (test_project.end_date + timedelta(days=30)).strftime("%Y-%m-%d"),
        "area_of_interest": SAMPLE_GEOJSON,
    }
    response = client.patch(
        f"/api/projects/update/{test_project.id}", json=project_update_payload
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["id"] == str(test_project.id)
    assert response_data["name"] == "Updated Project"


def test_delete_project(client, test_project):
    list_projects_response = client.get("/api/projects/list")
    assert list_projects_response.status_code == 200
    assert list_projects_response.json()["total"] == 1

    delete_response = client.delete(f"/api/projects/delete/{test_project.id}")
    assert delete_response.status_code == 200

    list_projects_response = client.get("/api/projects/list")
    assert list_projects_response.status_code == 200
    assert list_projects_response.json()["total"] == 0
