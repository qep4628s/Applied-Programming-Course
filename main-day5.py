from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing_extensions import Self
from typing import Optional
from datetime import datetime, timezone
from pathlib import Path
import json
import re


app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Simple note management API with validation",
    version="1.0.0"
)


ALLOWED_CATEGORIES = {"work", "personal", "school", "ideas", "general"}
TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")


class NoteCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: str = Field(
        min_length=3,
        max_length=100,
        description="Short note title",
        examples=["Shopping list"]
    )
    content: str = Field(
        min_length=1,
        max_length=10_000,
        description="Note content",
        examples=["Buy milk and bread"]
    )
    category: str = Field(
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+$",
        description="Category: work, personal, school, ideas or general",
        examples=["work"]
    )
    tags: list[str] = Field(
        default_factory=list,
        max_length=10,
        description="List of tags",
        examples=[["work", "urgent"]]
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 3:
            raise ValueError("title must be at least 3 characters")

        return value

    @field_validator("category")
    @classmethod
    def category_must_be_allowed(cls, value: str) -> str:
        value = value.strip().lower()

        if value not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"category must be one of {sorted(ALLOWED_CATEGORIES)}"
            )

        return value

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw: list[str]) -> list[str]:
        cleaned = []
        seen = set()

        for tag in raw:
            tag = tag.strip().lower()

            if not tag:
                raise ValueError("tags must not be empty strings")

            if len(tag) < 2:
                raise ValueError("tags must be at least 2 characters")

            if not TAG_PATTERN.match(tag):
                raise ValueError(
                    "tags must contain only lowercase letters, digits, and dashes"
                )

            if tag in seen:
                continue

            seen.add(tag)
            cleaned.append(tag)

        return cleaned

    @model_validator(mode="after")
    def work_notes_need_work_tag(self) -> Self:
        # This must be a model validator because it checks category and tags together.
        if self.category == "work" and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")

        return self


class NoteUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    content: Optional[str] = Field(default=None, min_length=1, max_length=10_000)
    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+$"
    )
    tags: Optional[list[str]] = Field(default=None, max_length=10)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if len(value) < 3:
            raise ValueError("title must be at least 3 characters")

        return value

    @field_validator("category")
    @classmethod
    def category_must_be_allowed(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip().lower()

        if value not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"category must be one of {sorted(ALLOWED_CATEGORIES)}"
            )

        return value

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw: Optional[list[str]]) -> Optional[list[str]]:
        if raw is None:
            return raw

        cleaned = []
        seen = set()

        for tag in raw:
            tag = tag.strip().lower()

            if not tag:
                raise ValueError("tags must not be empty strings")

            if len(tag) < 2:
                raise ValueError("tags must be at least 2 characters")

            if not TAG_PATTERN.match(tag):
                raise ValueError(
                    "tags must contain only lowercase letters, digits, and dashes"
                )

            if tag in seen:
                continue

            seen.add(tag)
            cleaned.append(tag)

        return cleaned


class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = Field(default_factory=list)
    created_at: str


NOTES_FILE = Path("data/notes.json")


def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    notes_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            if notes_db:
                notes_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, notes_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        notes_data = [note.model_dump() for note in notes_db]
        json.dump(notes_data, f, indent=2, ensure_ascii=False)


@app.get("/")
def root():
    return {
        "message": "Note API with validation is running"
    }


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

    if category:
        category = category.strip().lower()

    if tag:
        tag = tag.strip().lower()

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
    tag_name = tag_name.strip().lower()

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
    category_name = category_name.strip().lower()

    filtered_notes = []

    for note in notes_db:
        if note.category == category_name:
            filtered_notes.append(note)

    return filtered_notes