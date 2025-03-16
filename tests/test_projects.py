from datetime import datetime, timedelta
from data.samples import SAMPLE_GEOJSON


def test_create_project(client):
    today = datetime.today()
    project_create_payload = {
        "name": "New Project",
        "description": "New Project Description",
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
        "area_of_interest": SAMPLE_GEOJSON,
    }
    response = client.post("/api/projects/create", json=project_create_payload)
    assert response.status_code == 200


def test_get_projects_list(client, test_project):
    response = client.get("/api/projects/list")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["projects"]
    assert response_data["projects"][0]["id"] == str(test_project.id)
    assert response.json()["total"] == 1


def test_get_project_details(client, test_project):
    response = client.get(f"/api/projects/details/{test_project.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data
    assert response_data["id"] == str(test_project.id)


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
