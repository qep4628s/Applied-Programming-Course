import requests

BASE_URL = "http://127.0.0.1:8000"


def test_list_courses():
    response = requests.get(f"{BASE_URL}/courses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_course():
    course_data = {
        "code": "TEST101",
        "name": "Test Course",
        "semester": 1,
        "ects": 5,
        "lecturer": "Test Lecturer"
    }

    response = requests.post(f"{BASE_URL}/courses", json=course_data)

    assert response.status_code in [201, 409]