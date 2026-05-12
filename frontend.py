import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("My Notes App")

st.header("Show notes")

response = requests.get(f"{API_URL}/notes")

if response.status_code == 200:
    notes = response.json()

    if len(notes) == 0:
        st.write("No notes found.")
    else:
        for note in notes[-10:]:
            st.subheader(note["title"])
            st.write(note["content"])
            st.write("Category:", note["category"])
            st.write("Tags:", ", ".join(note["tags"]))
else:
    st.write("Could not load notes.")


st.header("Create a new note")

title = st.text_input("Title")
content = st.text_area("Content")
category = st.selectbox(
    "Category",
    ["general", "work", "personal", "school", "ideas"]
)
tags_input = st.text_input("Tags", placeholder="example: urgent, meeting")

if st.button("Create note"):
    tags = []

    if tags_input:
        tags = tags_input.split(",")

    note_data = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags
    }

    response = requests.post(f"{API_URL}/notes", json=note_data)

    if response.status_code == 201:
        st.success("Note created!")
        st.rerun()
    else:
        st.error("Something went wrong.")
        st.write(response.json())