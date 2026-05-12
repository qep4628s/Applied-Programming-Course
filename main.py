from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional




app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Simple note management API",
    version="1.0.0"
)


####################################################################
#### Day 1: Basic FastAPI Endpoints
####################################################################

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/status")
def get_status():
    return {
        "status": "online",
        "version": "0.1.0",
        "day": 1
    }


@app.get("/about")
def get_about():
    return {
        "project": "My First API",
        "author": "Maryam",
        "course": "Applied Programming"
    }


@app.get("/square/{number}")
def calculate_square(number: int):
    result = number * number

    return {
        "number": number,
        "square": result,
        "calculation": f"{number} × {number} = {result}"
    }


@app.get("/student")
def student_info():
    return {
        "name": "Maryam",
        "semester": 1,
        "course": "Wirtschaftsinformatik",
        "university": "HS Coburg"
    }


@app.get("/double/{number}")
def double_numbers(number: int):
    result = number * 2

    return {
        "number": number,
        "double": result,
        "calculation": f"{number} * 2 = {result}"
    }


####################################################################
#### Day 2 and Day 3: Note API + Homework
####################################################################

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []
    created_at: str


NOTES_FILE = Path("data/notes.json")


def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    notes_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, "r") as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            if notes_db:
                notes_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, notes_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, "w") as f:
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
    """Create a new note"""

    notes_db, notes_id_counter = load_notes()

    new_note = Note(
        id=notes_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=note.tags,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    notes_db.append(new_note)
    save_notes(notes_db)

    return new_note


@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
) -> list[Note]:
    """Get a list of all notes with optional filters"""

    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        if category and note.category != category:
            continue

        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()

            if not (title_match or content_match):
                continue

        if tag and tag not in note.tags:
            continue

        if created_after and note.created_at < created_after:
            continue

        if created_before and note.created_at > created_before:
            continue

        filtered_notes.append(note)

    return filtered_notes

@app.get("/notes/stats")
def get_notes_stats():
    """Get statistics about notes"""

    notes_db, _ = load_notes()

    categories = {}
    tags_count = {}
    all_tags = set()

    for note in notes_db:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1

        for tag in note.tags:
            all_tags.add(tag)

            if tag in tags_count:
                tags_count[tag] += 1
            else:
                tags_count[tag] = 1

    sorted_tags = sorted(
        tags_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_tags = []

    for tag, count in sorted_tags[:5]:
        top_tags.append({
            "tag": tag,
            "count": count
        })

    return {
        "total_notes": len(notes_db),
        "by_category": categories,
        "top_tags": top_tags,
        "unique_tags_count": len(all_tags)
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    """Get a specific note by ID"""

    notes_db, _ = load_notes()

    for note in notes_db:
        if note.id == note_id:
            return note

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    """Update an existing note"""

    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at
            )

            notes_db[i] = updated_note
            save_notes(notes_db)

            return updated_note

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate) -> Note:
    """Partially update a note"""

    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title if note_update.title is not None else note.title,
                content=note_update.content if note_update.content is not None else note.content,
                category=note_update.category if note_update.category is not None else note.category,
                tags=note_update.tags if note_update.tags is not None else note.tags,
                created_at=note.created_at
            )

            notes_db[i] = updated_note
            save_notes(notes_db)

            return updated_note

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    """Delete a note"""

    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.get("/tags")
def list_tags() -> list[str]:
    """Get all unique tags from all notes"""

    notes_db, _ = load_notes()

    all_tags = set()

    for note in notes_db:
        for tag in note.tags:
            all_tags.add(tag)

    return sorted(list(all_tags))


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    """Get all notes with a specific tag"""

    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        if tag_name in note.tags:
            filtered_notes.append(note)

    return filtered_notes


@app.get("/categories")
def list_categories() -> list[str]:
    """Get all unique categories from all notes"""

    notes_db, _ = load_notes()

    categories = set()

    for note in notes_db:
        categories.add(note.category)

    return sorted(list(categories))


@app.get("/categories/{category_name}/notes")
def get_notes_by_category_name(category_name: str) -> list[Note]:
    """Get all notes in a specific category"""

    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        if note.category == category_name:
            filtered_notes.append(note)

    return filtered_notes


####################################################################
#### Day 3: Query Parameter Practice
####################################################################

@app.get("/queryparameters")
def query_parameters(param1: str = "", param2: int = None) -> dict:
    namen = ["Maryam", "Max", "Mina", "Ali", "Fati"]
    namen_gefiltert = []

    if not param1:
        return {
            "param1": param1,
            "param2": param2,
            "namen": namen
        }

    for name in namen:
        if param1.lower() in name.lower():
            namen_gefiltert.append(name)

    return {
        "param1": param1,
        "param2": param2,
        "namen": namen_gefiltert
    }


####################################################################
#### Day 3: Test Endpoints for Path Parameters
####################################################################

@app.get("/test/123")
def test_fixed():
    return {
        "message": "Hello, you!"
    }


@app.get("/test/{name}/test2/{city}")
def test_two_values(name: str, city: str):
    return {
        "name": name,
        "city": city
    }


@app.get("/test/{value}")
def test_value(value: str):
    return {
        "value": value
    }