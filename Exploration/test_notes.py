import requests

BASE_URL = "http://127.0.0.1:8000"


def create_test_note(
    title="Test Note",
    content="Test content",
    category="general",
    tags=None
):
    if tags is None:
        tags = ["test"]

    note_data = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert response.status_code == 201

    return response.json()


def test_create_note():
    note_data = {
        "title": "Test Note",
        "content": "Test content",
        "category": "general",
        "tags": ["test", "pytest"]
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test content"
    assert data["category"] == "general"
    assert data["tags"] == ["test", "pytest"]
    assert "id" in data
    assert "created_at" in data


def test_list_notes():
    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note_by_id():
    created_note = create_test_note(
        title="Find Me",
        content="This note should be found",
        category="general",
        tags=["find"]
    )

    note_id = created_note["id"]

    response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Find Me"


def test_update_note():
    created_note = create_test_note(
        title="Old Title",
        content="Old content",
        category="general",
        tags=["old"]
    )

    note_id = created_note["id"]

    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "personal",
        "tags": ["updated"]
    }

    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    assert data["category"] == "personal"
    assert data["tags"] == ["updated"]


def test_delete_note():
    created_note = create_test_note(
        title="Delete Me",
        content="This note will be deleted",
        category="general",
        tags=["delete"]
    )

    note_id = created_note["id"]

    delete_response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert delete_response.status_code == 204

    get_response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_response.status_code == 404


def test_filter_by_category():
    create_test_note(
        title="Work Note",
        content="Content for work",
        category="work",
        tags=["office"]
    )

    response = requests.get(f"{BASE_URL}/notes?category=work")

    assert response.status_code == 200

    notes = response.json()

    for note in notes:
        assert note["category"] == "work"


def test_filter_by_search():
    create_test_note(
        title="Meeting Note",
        content="Discuss project plan",
        category="work",
        tags=["meeting"]
    )

    response = requests.get(f"{BASE_URL}/notes?search=meeting")

    assert response.status_code == 200

    notes = response.json()

    for note in notes:
        text = note["title"].lower() + " " + note["content"].lower()
        assert "meeting" in text


def test_filter_by_tag():
    create_test_note(
        title="Urgent Note",
        content="Important task",
        category="work",
        tags=["urgent"]
    )

    response = requests.get(f"{BASE_URL}/notes?tag=urgent")

    assert response.status_code == 200

    notes = response.json()

    for note in notes:
        assert "urgent" in note["tags"]


def test_combined_filters():
    create_test_note(
        title="Meeting with client",
        content="Important meeting about project",
        category="work",
        tags=["urgent", "meeting"]
    )

    response = requests.get(
        f"{BASE_URL}/notes?category=work&tag=urgent&search=meeting"
    )

    assert response.status_code == 200

    notes = response.json()

    for note in notes:
        assert note["category"] == "work"
        assert "urgent" in note["tags"]

        text = note["title"].lower() + " " + note["content"].lower()
        assert "meeting" in text


def test_create_note_missing_field():
    invalid_note = {
        "title": "Only title"
    }

    response = requests.post(f"{BASE_URL}/notes", json=invalid_note)

    assert response.status_code == 422


def test_get_nonexistent_note():
    response = requests.get(f"{BASE_URL}/notes/999999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_note():
    updated_data = {
        "title": "Updated",
        "content": "Updated content",
        "category": "general",
        "tags": ["updated"]
    }

    response = requests.put(f"{BASE_URL}/notes/999999", json=updated_data)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_nonexistent_note():
    response = requests.delete(f"{BASE_URL}/notes/999999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_notes_statistics():
    create_test_note(
        title="Stats Note",
        content="Note for statistics",
        category="general",
        tags=["stats", "test"]
    )

    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_notes" in data
    assert "by_category" in data
    assert "top_tags" in data
    assert "unique_tags_count" in data
    assert isinstance(data["by_category"], dict)
    assert isinstance(data["top_tags"], list)


def test_list_categories():
    create_test_note(
        title="Category Note",
        content="Note for category endpoint",
        category="school",
        tags=["category"]
    )

    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200

    categories = response.json()

    assert isinstance(categories, list)
    assert "school" in categories


def test_notes_by_category():
    create_test_note(
        title="School Note",
        content="This is a school note",
        category="school",
        tags=["school"]
    )

    response = requests.get(f"{BASE_URL}/categories/school/notes")

    assert response.status_code == 200

    notes = response.json()

    for note in notes:
        assert note["category"] == "school"


def test_patch_note_title_only():
    created_note = create_test_note(
        title="Old Patch Title",
        content="Original content",
        category="general",
        tags=["patch"]
    )

    note_id = created_note["id"]

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={"title": "New Patch Title"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Patch Title"
    assert data["content"] == "Original content"
    assert data["category"] == "general"
    assert data["tags"] == ["patch"]


def test_patch_multiple_fields():
    created_note = create_test_note(
        title="Patch Multiple",
        content="Old content",
        category="general",
        tags=["old"]
    )

    note_id = created_note["id"]

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={
            "title": "Patched Title",
            "content": "Patched content"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Patched Title"
    assert data["content"] == "Patched content"
    assert data["category"] == "general"
    assert data["tags"] == ["old"]