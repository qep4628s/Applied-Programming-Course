from fastapi import FastAPI, HTTPException, Depends
from pydantic import (
    BaseModel,
    ConfigDict,
    Field as PydanticField,
    field_validator,
)
from sqlmodel import (
    SQLModel,
    Field as SQLField,
    Session,
    create_engine,
    Relationship,
    select,
    or_,
    col,
)
from datetime import datetime
from typing import Optional, Annotated
import re


app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Note API with SQLite database and validation",
    version="3.0.0"
)


ALLOWED_CATEGORIES = {"work", "personal", "school", "ideas", "general"}
TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")


# ============================================================================
# Database Models
# ============================================================================

class NoteTagLink(SQLModel, table=True):
    __tablename__ = "notelink"

    note_id: Optional[int] = SQLField(
        default=None,
        foreign_key="notes.id",
        primary_key=True
    )
    tag_id: Optional[int] = SQLField(
        default=None,
        foreign_key="tags.id",
        primary_key=True
    )


class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = SQLField(default_factory=datetime.now)

    tags: list["Tag"] = Relationship(
        back_populates="notes",
        link_model=NoteTagLink
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    name: str = SQLField(unique=True, index=True)

    notes: list[Note] = Relationship(
        back_populates="tags",
        link_model=NoteTagLink
    )

    @field_validator("name")
    @classmethod
    def clean_tag_name(cls, value: str) -> str:
        value = value.strip().lower()

        if len(value) < 2:
            raise ValueError("tag name must be at least 2 characters")

        if len(value) > 30:
            raise ValueError("tag name must be at most 30 characters")

        if not TAG_PATTERN.match(value):
            raise ValueError(
                "tag name must contain only lowercase letters, digits, and dashes"
            )

        return value


# ============================================================================
# Database Setup
# ============================================================================

engine = create_engine("sqlite:///notes.db")

SQLModel.metadata.create_all(engine)


def get_session():
    """Create a new database session for each request"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# ============================================================================
# API Input / Output Models
# ============================================================================

class NoteCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: str = PydanticField(
        min_length=3,
        max_length=100,
        description="Short note title",
        examples=["Shopping list"]
    )
    content: str = PydanticField(
        min_length=1,
        max_length=10_000,
        description="Note content",
        examples=["Buy milk and bread"]
    )
    category: str = PydanticField(
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+$",
        description="Category: work, personal, school, ideas or general",
        examples=["work"]
    )
    tags: list[str] = PydanticField(
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

            if len(tag) > 30:
                raise ValueError("tags must be at most 30 characters")

            if not TAG_PATTERN.match(tag):
                raise ValueError(
                    "tags must contain only lowercase letters, digits, and dashes"
                )

            if tag in seen:
                continue

            seen.add(tag)
            cleaned.append(tag)

        return cleaned


class NoteUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: Optional[str] = PydanticField(
        default=None,
        min_length=3,
        max_length=100
    )
    content: Optional[str] = PydanticField(
        default=None,
        min_length=1,
        max_length=10_000
    )
    category: Optional[str] = PydanticField(
        default=None,
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+$"
    )
    tags: Optional[list[str]] = PydanticField(
        default=None,
        max_length=10
    )

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

            if len(tag) > 30:
                raise ValueError("tags must be at most 30 characters")

            if not TAG_PATTERN.match(tag):
                raise ValueError(
                    "tags must contain only lowercase letters, digits, and dashes"
                )

            if tag in seen:
                continue

            seen.add(tag)
            cleaned.append(tag)

        return cleaned


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Helper Functions
# ============================================================================

def note_to_response(note: Note) -> NoteResponse:
    """Convert database Note object to response model"""
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat()
    )


def validate_tag_name(tag_name: str) -> str:
    """Validate and normalize a tag name before saving it"""
    tag_name = tag_name.strip().lower()

    if len(tag_name) < 2:
        raise HTTPException(
            status_code=422,
            detail="tag name must be at least 2 characters"
        )

    if len(tag_name) > 30:
        raise HTTPException(
            status_code=422,
            detail="tag name must be at most 30 characters"
        )

    if not TAG_PATTERN.match(tag_name):
        raise HTTPException(
            status_code=422,
            detail="tag name must contain only lowercase letters, digits, and dashes"
        )

    return tag_name


def get_or_create_tags(tag_names: list[str], session: Session) -> list[Tag]:
    """Get existing tags or create new ones"""

    tag_objects = []
    seen_tags = set()

    for tag_name in tag_names:
        tag_name = validate_tag_name(tag_name)

        if tag_name in seen_tags:
            continue

        seen_tags.add(tag_name)

        statement = select(Tag).where(Tag.name == tag_name)
        existing_tag = session.exec(statement).first()

        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name)
            session.add(new_tag)
            tag_objects.append(new_tag)

    return tag_objects


# ============================================================================
# Basic Endpoint
# ============================================================================

@app.get("/")
def root():
    return {
        "message": "Note API with SQLite database and validation is running"
    }


# ============================================================================
# Notes Endpoints
# ============================================================================

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note in database"""

    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )

    tag_objects = get_or_create_tags(note.tags, session)
    db_note.tags = tag_objects

    session.add(db_note)
    session.commit()
    session.refresh(db_note)

    return note_to_response(db_note)


@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
) -> list[NoteResponse]:
    """List notes with optional filters"""

    statement = select(Note)

    if category:
        category = category.strip().lower()
        statement = statement.where(Note.category == category)

    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%")
            )
        )

    if tag:
        tag_lower = tag.lower().strip()
        statement = statement.join(Note.tags).where(Tag.name == tag_lower)

    if created_after:
        try:
            created_after_date = datetime.fromisoformat(created_after)
            statement = statement.where(Note.created_at >= created_after_date)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="created_after must be ISO format, for example 2026-05-01"
            )

    if created_before:
        try:
            created_before_date = datetime.fromisoformat(created_before)
            statement = statement.where(Note.created_at <= created_before_date)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="created_before must be ISO format, for example 2026-05-30"
            )

    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]


@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    """Get statistics about notes"""

    notes = session.exec(select(Note)).all()
    all_tags_from_table = session.exec(select(Tag)).all()

    categories = {}
    tags_count = {}

    for note in notes:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1

        for tag in note.tags:
            if tag.name in tags_count:
                tags_count[tag.name] += 1
            else:
                tags_count[tag.name] = 1

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
        "total_notes": len(notes),
        "by_category": categories,
        "top_tags": top_tags,
        "unique_tags_count": len(all_tags_from_table)
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    """Get a specific note by ID"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found"
        )

    return note_to_response(note)


@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    note_update: NoteCreate,
    session: SessionDep
) -> NoteResponse:
    """Update an existing note"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found"
        )

    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.tags = get_or_create_tags(note_update.tags, session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return note_to_response(note)


@app.patch("/notes/{note_id}")
def partial_update_note(
    note_id: int,
    note_update: NoteUpdate,
    session: SessionDep
) -> NoteResponse:
    """Partially update a note"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found"
        )

    if note_update.title is not None:
        note.title = note_update.title

    if note_update.content is not None:
        note.content = note_update.content

    if note_update.category is not None:
        note.category = note_update.category

    if note_update.tags is not None:
        note.tags = get_or_create_tags(note_update.tags, session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return note_to_response(note)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found"
        )

    session.delete(note)
    session.commit()

    return


# ============================================================================
# Tag Endpoints
# ============================================================================

@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags from the Tag table"""

    statement = select(Tag)
    tags = session.exec(statement).all()

    return sorted([tag.name for tag in tags])


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(
    tag_name: str,
    session: SessionDep
) -> list[NoteResponse]:
    """Get all notes with specific tag"""

    tag_lower = tag_name.lower().strip()

    statement = select(Tag).where(Tag.name == tag_lower)
    tag = session.exec(statement).first()

    if not tag:
        return []

    return [
        note_to_response(note)
        for note in tag.notes
    ]


# ============================================================================
# Category Endpoints
# ============================================================================

@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    """Get all unique categories from all notes"""

    statement = select(Note.category)
    categories = session.exec(statement).all()

    return sorted(list(set(categories)))


@app.get("/categories/{category_name}/notes")
def get_notes_by_category_name(
    category_name: str,
    session: SessionDep
) -> list[NoteResponse]:
    """Get all notes in a specific category"""

    category_name = category_name.strip().lower()

    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]