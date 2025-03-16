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
