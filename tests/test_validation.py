import requests


BASE_URL = "http://127.0.0.1:8000"


def create_valid_note():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Valid note",
        "content": "This is valid content",
        "category": "general",
        "tags": ["test"]
    })
    assert response.status_code == 201
    return response.json()


def test_create_note_rejects_short_title():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "",
        "content": "Some content",
        "category": "general",
        "tags": []
    })

    assert response.status_code == 422


def test_create_note_rejects_unknown_category():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Valid title",
        "content": "Some content",
        "category": "banana",
        "tags": []
    })

    assert response.status_code == 422


def test_create_note_normalizes_tags():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Team sync",
        "content": "Discuss roadmap",
        "category": "WORK",
        "tags": ["WORK", "urgent", "URGENT", " meeting "]
    })

    assert response.status_code == 201
    data = response.json()

    assert data["category"] == "work"
    assert data["tags"] == ["work", "urgent", "meeting"]


def test_create_note_forbids_extra_fields():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Valid title",
        "content": "Some content",
        "category": "general",
        "tagz": ["typo"]
    })

    assert response.status_code == 422


def test_work_note_requires_work_tag():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Work meeting",
        "content": "Discuss work tasks",
        "category": "work",
        "tags": ["urgent"]
    })

    assert response.status_code == 422


def test_patch_with_empty_body_succeeds():
    note = create_valid_note()
    note_id = note["id"]

    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == note_id


def test_patch_with_invalid_title_fails():
    note = create_valid_note()
    note_id = note["id"]

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={"title": ""}
    )

    assert response.status_code == 422


def test_tag_name_rejects_uppercase_or_invalid_format():
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Invalid tag",
        "content": "Testing invalid tag format",
        "category": "general",
        "tags": ["BAD TAG"]
    })

    assert response.status_code == 422