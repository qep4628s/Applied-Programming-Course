import streamlit as st
import requests

URL = "https://naas.isalman.dev/no"

def request_no():
    response = requests.get(URL)
    response_json = response.json()
    return response_json["reason"]

# Initialization
if "text1" not in st.session_state:
    st.session_state["text1"] = request_no()
    print("init Text1")

if "text" not in st.session_state:
    st.session_state["text"] = request_no()
    print("init Text")

if st.button("Neuer Text1"):
    st.session_state["text1"] = request_no()

st.write(st.session_state["text1"])

if st.button("Neuer Text"):
    st.session_state["text"] = request_no()

st.write(st.session_state["text"])

with st.expander("session_state"):
    st.write(st.session_state)