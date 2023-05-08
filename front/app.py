import json

import streamlit as st
import requests

st.title("API test user")

with st.form(key="user"):
    name: str = st.text_input("user name", max_chars=12)
    data = {
        "name": name,
    }
    submit_button = st.form_submit_button(label="submit")
    if submit_button:
        resp = requests.post("https://67fjv4ts3tw6frlsl2elf4gm5u0uewji.lambda-url.ap-northeast-1.on.aws/", data=json.dumps(data))
        st.json(resp.json())