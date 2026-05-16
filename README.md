# Notizen-API

Eine einfache REST-API für die Verwaltung von Notizen.  
Das Projekt besteht aus einem **FastAPI Backend**, einem **Streamlit Frontend** und einer **SQLite Datenbank**.

**Kurs:** Angewandte Programmierung HS-Coburg  
**Version:** 3.0.0

---

## Was ist das Projekt?

In diesem Projekt geht es um eine kleine Notizen-App.

Mit der API kann man:

- Notizen erstellen
- Notizen anzeigen
- Notizen aktualisieren
- Notizen löschen
- Notizen filtern
- Statistiken anzeigen
- Tags und Kategorien benutzen

Zusätzlich gibt es ein kleines Frontend mit Streamlit.  
Dort kann man Notizen anzeigen und neue Notizen über ein Formular erstellen.

---

## Projektstruktur

```text
Applied-Programming-Course/
├── main.py
├── frontend.py
├── work-log.md
├── README.md
├── pyproject.toml
├── uv.lock
└── Exploration/
    ├── test_main.py
    ├── test_notes.py
    └── test_validation.py
```

### Wichtige Dateien

| Datei | Beschreibung |
|---|---|
| `main.py` | FastAPI Backend mit Endpoints, Datenbank und Validierung |
| `frontend.py` | Streamlit Frontend zum Anzeigen und Erstellen von Notizen |
| `work-log.md` | Work Log für den Kurs |
| `Exploration/test_main.py` | Große Testdatei aus dem Kurs |
| `Exploration/test_notes.py` | Eigene praktische API-Tests |
| `Exploration/test_validation.py` | Eigene Tests für Validierung und Fehlerfälle |

Die Datei `notes.db` wird automatisch lokal erstellt, wenn das Backend gestartet wird.  
Sie enthält lokale Testdaten und muss nicht auf GitHub hochgeladen werden.

---

## Verwendete Technologien

Dieses Projekt benutzt:

- **Python**
- **FastAPI** für das Backend
- **Pydantic** für Validierung
- **SQLModel** für die Datenbank-Modelle
- **SQLite** als lokale Datenbank
- **Streamlit** für das Frontend
- **requests** für HTTP-Anfragen
- **pytest** für Tests
- **uv** zum Starten und Verwalten des Projekts

---

## Schnell starten

### 1. Projektordner öffnen

In PowerShell in den Projektordner wechseln:

```powershell
cd C:\Users\Lenovo\Desktop\Programmierung\Applied-Programming-Course
```

---

### 2. Abhängigkeiten installieren

Normalerweise reicht:

```powershell
uv sync
```

Die Abhängigkeiten stehen in `pyproject.toml`.

Falls ein Paket fehlt, kann man es mit `uv add` installieren, zum Beispiel:

```powershell
uv add fastapi sqlmodel streamlit requests pytest
```

---

### 3. Backend starten

```powershell
uv run fastapi dev main.py
```

Das Backend läuft dann unter:

```text
http://127.0.0.1:8000
```

Die automatische API-Dokumentation ist hier verfügbar:

```text
http://127.0.0.1:8000/docs
```

Über `/docs` kann man die API auch direkt im Browser testen.

---

### 4. Frontend starten

Ein zweites Terminal öffnen und starten:

```powershell
uv run streamlit run frontend.py
```

Wichtig:  
Das Backend muss laufen, bevor das Frontend Notizen laden oder erstellen kann.

---

## Wie funktioniert das Projekt?

Die App hat drei Teile:

```text
Streamlit Frontend  --->  FastAPI Backend  --->  SQLite Datenbank
```

Das Frontend schickt HTTP-Anfragen an das Backend.

Zum Beispiel werden Notizen so geladen:

```python
requests.get(f"{API_URL}/notes")
```

Neue Notizen werden so erstellt:

```python
requests.post(f"{API_URL}/notes", json=note_data)
```

Das Backend empfängt die Anfrage, prüft die Daten und speichert oder liest die Daten aus der SQLite-Datenbank.

---

# Erklärung von `main.py`

`main.py` ist die wichtigste Datei im Projekt.  
Dort ist das Backend.

In `main.py` gibt es:

- Imports
- FastAPI App
- Datenbank-Modelle
- Pydantic-Modelle
- Validierung
- Helper-Funktionen
- API-Endpoints

---

## Imports

Am Anfang werden die benötigten Pakete importiert:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, Field as PydanticField, field_validator
from sqlmodel import SQLModel, Field as SQLField, Session, create_engine, Relationship, select
```

Wichtige Imports:

- `FastAPI` erstellt die API
- `HTTPException` wird für Fehler wie `404` benutzt
- `Depends` wird für die Datenbank-Session benutzt
- `BaseModel` wird für Eingabe- und Ausgabe-Modelle benutzt
- `field_validator` prüft und bereinigt Eingaben
- `SQLModel` wird für Datenbank-Modelle benutzt
- `Session` wird für Datenbankzugriffe benutzt
- `Relationship` verbindet Notizen und Tags

---

## FastAPI App

Die App wird so erstellt:

```python
app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Note API with SQLite database and validation",
    version="3.0.0"
)
```

Dadurch bekommt die API einen Titel, eine Beschreibung und eine Version.

Diese Informationen sieht man auch in der automatischen Dokumentation unter:

```text
http://127.0.0.1:8000/docs
```

---

# Datenbank

Die Datenbank wird mit SQLite und SQLModel umgesetzt.

Es gibt drei wichtige Tabellen:

- `notes`
- `tags`
- `notelink`

---

## Note Model

Das `Note` Model beschreibt eine Notiz in der Datenbank.

Eine Notiz hat:

- `id`
- `title`
- `content`
- `category`
- `created_at`
- `tags`

Beispiel:

```json
{
  "id": 1,
  "title": "Team Meeting",
  "content": "Discuss project tasks",
  "category": "work",
  "tags": ["urgent", "meeting"],
  "created_at": "2026-05-16T14:30:00"
}
```

Die ID wird automatisch von der Datenbank erstellt.  
`created_at` speichert, wann die Notiz erstellt wurde.

---

## Tag Model

Das `Tag` Model beschreibt einen Tag.

Ein Tag hat:

- `id`
- `name`

Der Name ist einzigartig.  
Das bedeutet: derselbe Tag wird nicht immer wieder neu gespeichert.

Beispiele:

```text
urgent
meeting
school-task
```

---

## NoteTagLink Model

`NoteTagLink` verbindet Notizen und Tags.

Das ist nötig, weil:

- eine Notiz mehrere Tags haben kann
- ein Tag zu mehreren Notizen gehören kann

Beispiel:

```text
Note 1: "Team Meeting"  -> Tags: urgent, meeting
Note 2: "Shopping"      -> Tags: urgent, shopping
```

Der Tag `urgent` kann also mit mehreren Notizen verbunden sein.

Das ist eine Many-to-Many Beziehung.

---

## Datenbank erstellen

Die Datenbank wird mit diesem Code erstellt:

```python
engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)
```

Wenn `notes.db` noch nicht existiert, wird die Datei automatisch erstellt.

---

## Datenbank-Session

Die Funktion `get_session()` erstellt eine Datenbank-Session:

```python
def get_session():
    with Session(engine) as session:
        yield session
```

Die Session wird in den Endpoints benutzt, um Daten zu lesen oder zu speichern.

---

# Validierung

Die API prüft Daten, bevor sie gespeichert werden.

Dafür werden Pydantic-Modelle benutzt:

- `NoteCreate`
- `NoteUpdate`
- `NoteResponse`

---

## NoteCreate

`NoteCreate` wird benutzt, wenn eine neue Notiz erstellt wird.

Eine gültige Anfrage sieht so aus:

```json
{
  "title": "Team Meeting",
  "content": "Discuss project tasks",
  "category": "work",
  "tags": ["urgent", "meeting"]
}
```

Die API prüft:

- ob der Titel lang genug ist
- ob Content nicht leer ist
- ob die Kategorie erlaubt ist
- ob die Tags gültig sind

Wenn etwas nicht gültig ist, gibt die API `422` zurück.

---

## NoteUpdate

`NoteUpdate` wird für `PATCH` benutzt.

Bei `PATCH` müssen nicht alle Felder gesendet werden.

Beispiel:

```json
{
  "title": "New Title"
}
```

Dann wird nur der Titel geändert.  
Content, Kategorie und Tags bleiben gleich.

---

## NoteResponse

`NoteResponse` bestimmt, wie die Antwort der API aussieht.

Beispiel:

```json
{
  "id": 1,
  "title": "Team Meeting",
  "content": "Discuss project tasks",
  "category": "work",
  "tags": ["urgent", "meeting"],
  "created_at": "2026-05-16T14:30:00"
}
```

Dadurch ist die Antwort einfacher zu lesen.

---

## Kategorien

Erlaubte Kategorien sind:

```text
work
personal
school
ideas
general
```

Wenn eine andere Kategorie gesendet wird, gibt die API einen Fehler zurück.

Beispiel:

```text
banana -> 422
```

Kategorien werden automatisch bereinigt:

```text
WORK -> work
```

---

## Tags

Regeln für Tags:

- jeder Tag muss mindestens 2 Zeichen haben
- jeder Tag darf maximal 30 Zeichen haben
- maximal 10 Tags pro Notiz
- nur Kleinbuchstaben, Zahlen und Bindestriche
- Leerzeichen am Anfang und Ende werden entfernt
- Großbuchstaben werden zu Kleinbuchstaben
- doppelte Tags werden entfernt

Beispiel:

```text
Input:  ["WORK", "urgent", "URGENT", " meeting "]
Output: ["work", "urgent", "meeting"]
```

Ungültiges Beispiel:

```text
Input: ["BAD TAG"]
Result: 422
```

---

# Helper-Funktionen

Ich benutze Helper-Funktionen, damit die Endpoints nicht zu lang werden.

---

## note_to_response()

Diese Funktion wandelt eine Datenbank-Notiz in eine API-Antwort um.

In der Datenbank sind Tags Objekte.  
Die API soll aber nur die Namen der Tags zurückgeben.

Deshalb wird das hier benutzt:

```python
tags=[tag.name for tag in note.tags]
```

Die Antwort sieht dann einfach so aus:

```json
"tags": ["urgent", "meeting"]
```

---

## validate_tag_name()

Diese Funktion prüft, ob ein Tag gültig ist.

Sie prüft:

- Länge
- erlaubte Zeichen
- Format

Wenn der Tag ungültig ist, wird `422` zurückgegeben.

---

## get_or_create_tags()

Diese Funktion prüft, ob ein Tag schon existiert.

Wenn der Tag existiert, wird er wiederverwendet.  
Wenn nicht, wird er neu erstellt.

Beispiel:

```text
Erste Notiz benutzt: urgent
Zweite Notiz benutzt: urgent
```

In der Datenbank wird `urgent` trotzdem nur einmal gespeichert.

---

# API-Endpoints

## Health Check

```http
GET /
```

Prüft, ob die API läuft.

---

## Notiz erstellen

```http
POST /notes
```

Beispiel:

```json
{
  "title": "Team Meeting",
  "content": "Discuss Q2 goals",
  "category": "work",
  "tags": ["urgent", "meeting"]
}
```

Wenn die Notiz erfolgreich erstellt wurde, gibt die API `201` zurück.

---

## Alle Notizen anzeigen

```http
GET /notes
```

Dieser Endpoint gibt alle Notizen zurück.

Man kann auch filtern:

```http
GET /notes?category=work
GET /notes?tag=urgent
GET /notes?search=meeting
GET /notes?created_after=2026-05-01
GET /notes?created_before=2026-05-30
```

Filter können kombiniert werden:

```http
GET /notes?category=work&tag=urgent&search=meeting
```

---

## Eine Notiz anzeigen

```http
GET /notes/{note_id}
```

Beispiel:

```http
GET /notes/1
```

Wenn die Notiz existiert, wird sie zurückgegeben.  
Wenn nicht, gibt die API `404` zurück.

---

## Notiz vollständig aktualisieren

```http
PUT /notes/{note_id}
```

Bei `PUT` müssen alle Felder gesendet werden.

Beispiel:

```json
{
  "title": "Updated Note",
  "content": "Updated content",
  "category": "personal",
  "tags": ["updated"]
}
```

---

## Notiz teilweise aktualisieren

```http
PATCH /notes/{note_id}
```

Bei `PATCH` werden nur die Felder geändert, die gesendet werden.

Beispiel:

```json
{
  "title": "New Title"
}
```

Dann wird nur der Titel geändert.  
Die anderen Felder bleiben gleich.

---

## Notiz löschen

```http
DELETE /notes/{note_id}
```

Wenn die Notiz gelöscht wurde, gibt die API `204` zurück.

Wenn die Notiz nicht existiert, gibt die API `404` zurück.

---

## Tags

```http
GET /tags
GET /tags/{tag_name}/notes
```

`GET /tags` zeigt alle Tags.

`GET /tags/urgent/notes` zeigt alle Notizen mit dem Tag `urgent`.

---

## Kategorien

```http
GET /categories
GET /categories/{category_name}/notes
```

`GET /categories` zeigt alle verwendeten Kategorien.

`GET /categories/work/notes` zeigt alle Notizen aus der Kategorie `work`.

---

## Statistiken

```http
GET /notes/stats
```

Beispiel:

```json
{
  "total_notes": 5,
  "by_category": {
    "work": 2,
    "personal": 2,
    "school": 1
  },
  "top_tags": [
    {
      "tag": "urgent",
      "count": 3
    }
  ],
  "unique_tags_count": 6
}
```

Die Statistik zeigt:

- Anzahl aller Notizen
- Anzahl der Notizen pro Kategorie
- häufigste Tags
- Anzahl eindeutiger Tags

---

# Frontend

Das Frontend ist in `frontend.py`.

Es benutzt:

```python
import streamlit as st
import requests
```

`streamlit` wird für die Oberfläche benutzt.  
`requests` sendet Anfragen an das Backend.

---

## API URL

```python
API_URL = "http://127.0.0.1:8000"
```

Das Frontend erwartet also, dass das Backend auf Port `8000` läuft.

---

## Notizen anzeigen

Das Frontend lädt Notizen mit:

```python
response = requests.get(f"{API_URL}/notes")
```

Wenn die Anfrage funktioniert, werden die Notizen angezeigt.

Angezeigt werden:

- Titel
- Content
- Kategorie
- Tags

---

## Neue Notiz erstellen

Im Frontend kann man eingeben:

- Titel
- Content
- Kategorie
- Tags

Tags werden mit Komma getrennt eingegeben:

```text
urgent, meeting
```

Danach werden sie in eine Liste umgewandelt und an die API gesendet.

Die Daten sehen ungefähr so aus:

```python
note_data = {
    "title": title,
    "content": content,
    "category": category,
    "tags": tags
}
```

Gesendet wird mit:

```python
response = requests.post(f"{API_URL}/notes", json=note_data)
```

Nach dem Erstellen erscheint die neue Notiz in der Liste.

---

# Tests

Die Tests sind mit `pytest` geschrieben.

Ein Test sendet eine Anfrage an die API und prüft mit `assert`, ob das Ergebnis stimmt.

Beispiel:

```python
def test_list_notes():
    response = requests.get("http://127.0.0.1:8000/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

`assert` bedeutet:  
Wenn die Bedingung stimmt, ist der Test erfolgreich.  
Wenn nicht, schlägt der Test fehl.

---

## Wichtige Statuscodes

```text
200 = OK
201 = Created
204 = No Content
404 = Not Found
422 = Validation Error
```

---

## Tests ausführen

Wichtig:  
Das Backend muss laufen, bevor die Tests mit `requests` gestartet werden.

Terminal 1:

```powershell
uv run fastapi dev main.py
```

Terminal 2:

```powershell
uv run pytest Exploration/test_main.py -v
```

Die Option `-v` bedeutet verbose.  
Dann werden die Namen der einzelnen Tests angezeigt.

---

## Eigene Tests ausführen

```powershell
uv run pytest Exploration/test_notes.py -v
uv run pytest Exploration/test_validation.py -v
```

---

## Einzelnen Test ausführen

```powershell
uv run pytest Exploration/test_main.py::test_create_note_normalizes_tags -v
```

Das ist hilfreich, wenn nur ein bestimmter Test fehlschlägt.

---

## Was testen die Tests?

Die Tests prüfen zum Beispiel:

- Notizen erstellen
- Notizen anzeigen
- Notizen aktualisieren
- Notizen löschen
- Filter nach Kategorie
- Filter nach Tag
- Suche nach Titel oder Inhalt
- Statistik-Endpoint
- Fehlerfälle mit `404`
- Validierungsfehler mit `422`
- Tag-Normalisierung
- Kategorie-Normalisierung
- `PATCH` und `PUT`

Beim letzten Testlauf hat die große Testdatei bestanden:

```text
70 passed
```

---

## Beispiel: Tag-Normalisierung testen

Beispielinput:

```json
{
  "title": "Team sync",
  "content": "Discuss roadmap",
  "category": "WORK",
  "tags": ["WORK", "urgent", "URGENT", " meeting "]
}
```

Erwartetes Ergebnis:

```json
{
  "category": "work",
  "tags": ["work", "urgent", "meeting"]
}
```

Dabei wird geprüft, ob:

- Kategorie klein geschrieben wird
- Tags klein geschrieben werden
- Leerzeichen entfernt werden
- doppelte Tags entfernt werden

---

## Beispiel: Fehler testen

Beispielinput:

```json
{
  "title": "",
  "content": "Some content",
  "category": "general",
  "tags": []
}
```

Erwartetes Ergebnis:

```text
422
```

Das zeigt, dass die API ungültige Eingaben ablehnt.

---

# Häufige Probleme

## Backend läuft nicht

Wenn das Frontend keine Notizen laden kann, zuerst prüfen, ob das Backend läuft:

```powershell
uv run fastapi dev main.py
```

---

## Port 8000 ist schon belegt

Dann kann man einen anderen Port benutzen:

```powershell
uvicorn main:app --reload --port 8001
```

Dann muss aber auch im Frontend `API_URL` angepasst werden.

---

## Tests erreichen die API nicht

Die Tests mit `requests` brauchen ein laufendes Backend.

Also zuerst:

```powershell
uv run fastapi dev main.py
```

Dann in einem zweiten Terminal:

```powershell
uv run pytest Exploration/test_main.py -v
```

---

# Checklist vor der Abgabe

- [ ] Backend läuft ohne Fehler
- [ ] Frontend verbindet sich mit dem Backend
- [ ] Notiz erstellen funktioniert
- [ ] Notizen anzeigen funktioniert
- [ ] Notiz aktualisieren funktioniert
- [ ] Notiz löschen funktioniert
- [ ] Filter funktionieren
- [ ] Tests laufen mit `pytest`
- [ ] README ist aktuell
- [ ] Work Log ist aktuell
- [ ] Änderungen sind auf GitHub gepusht

---

# Was ich gelernt habe

In diesem Projekt habe ich gelernt:

- eine REST-API mit FastAPI zu bauen
- eine SQLite-Datenbank mit SQLModel zu verwenden
- Datenbank-Modelle zu erstellen
- eine Many-to-Many Beziehung umzusetzen
- Eingaben mit Pydantic zu validieren
- API-Endpoints für `GET`, `POST`, `PUT`, `PATCH` und `DELETE` zu schreiben
- Fehler mit `404` und `422` zu behandeln
- Tests mit pytest zu schreiben
- mit requests API-Tests auszuführen
- ein einfaches Frontend mit Streamlit zu bauen
- ein Projekt für GitHub zu organisieren

---

## Status

**Status:** Funktioniert lokal  
**Backend:** `main.py`  
**Frontend:** `frontend.py`  
**Tests:** pytest  
**Getestet:** 70 Tests bestanden  
**Bereit:** Zur Abgabe