from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from datetime import datetime
from typing import Optional, Annotated


app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Note API with SQLite database",
    version="2.0.0"
)


####################################################################
#### Task 6: Database Models
####################################################################

class NoteTagLink(SQLModel, table=True):
    __tablename__ = "notelink"

    note_id: Optional[int] = Field(
        default=None,
        foreign_key="notes.id",
        primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tags.id",
        primary_key=True
    )


class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)

    tags: list["Tag"] = Relationship(
        back_populates="notes",
        link_model=NoteTagLink
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    notes: list[Note] = Relationship(
        back_populates="tags",
        link_model=NoteTagLink
    )


# Create database engine
engine = create_engine("sqlite:///notes.db")


# Create tables
SQLModel.metadata.create_all(engine)


####################################################################
#### Task 6: Session Dependency
####################################################################

def get_session():
    """Create a new database session for each request"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


####################################################################
#### Task 6: API Input / Output Models
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


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

    class Config:
        from_attributes = True


####################################################################
#### Helper Functions
####################################################################

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


def get_or_create_tags(tag_names: list[str], session: Session) -> list[Tag]:
    """Get existing tags or create new ones"""

    tag_objects = []
    seen_tags = set()

    for tag_name in tag_names:
        tag_name_lower = tag_name.lower().strip()

        if not tag_name_lower or tag_name_lower in seen_tags:
            continue

        seen_tags.add(tag_name_lower)

        statement = select(Tag).where(Tag.name == tag_name_lower)
        existing_tag = session.exec(statement).first()

        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)

    return tag_objects


####################################################################
#### Basic Endpoint
####################################################################

@app.get("/")
def root():
    return {"message": "Note API with SQLite database is running"}


####################################################################
#### Notes Endpoints
####################################################################

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
                status_code=400,
                detail="created_after must be ISO format, for example 2026-05-01"
            )

    if created_before:
        try:
            created_before_date = datetime.fromisoformat(created_before)
            statement = statement.where(Note.created_at <= created_before_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="created_before must be ISO format, for example 2026-05-30"
            )

    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]


@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    """Get statistics about notes"""

    notes = session.exec(select(Note)).all()

    categories = {}
    tags_count = {}
    all_tags = set()

    for note in notes:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1

        for tag in note.tags:
            all_tags.add(tag.name)

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
        "unique_tags_count": len(all_tags)
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


####################################################################
#### Tag Endpoints
####################################################################

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


####################################################################
#### Category Endpoints
####################################################################

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

    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]