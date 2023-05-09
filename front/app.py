import datetime
import json
import os

import streamlit as st
import requests

def run():
    event_handler_url = os.environ["EVENT_HANDLER_URL"]
    page: str = st.sidebar.selectbox("Choose your page", ["booking", "room", "user"])
    page_map = {"booking":show_booking, "room":show_room, "user":show_user}
    page_map[page](event_handler_url)

def list_rooms(event_handler_url: str) -> list[dict[str, str]]:
    resp = requests.post(event_handler_url, data=json.dumps({"handler":"room_list"}))
    return resp.json()

def list_users(event_handler_url: str) -> list[dict[str, str]]:
    resp = requests.post(event_handler_url, data=json.dumps({"handler":"user_list"}))
    return resp.json()

def show_booking(event_handler_url: str):
    st.title("予約登録")

    users = list_users(event_handler_url)
    users_dict = {}
    for u in users:
        users_dict[u["name"]] = u["id"]
    st.write(users_dict)

    rooms = list_rooms(event_handler_url)
    rooms_dict = {}
    for r in rooms:
        rooms_dict[r["name"]] = {"id":r["id"], "capacity":r["capacity"]}
    st.write(rooms_dict)

    with st.form(key="booking"):
        user_id: int = "abc"
        room_id: int = "012"
        reserved_num: int = st.number_input("利用人数", min_value=1, step=1)
        date = st.date_input("日付", min_value=datetime.date.today())
        begin_time = st.time_input("開始時刻", value=datetime.time(hour=9))
        end_time = st.time_input("終了時刻", value=datetime.time(hour=20))
        submit_button = st.form_submit_button(label="submit")
        if submit_button:
            begin_date_time = datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=begin_time.hour,
                minute=begin_time.minute,
            ).isoformat()
            end_date_time = datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat()
            data = {
                "handler": "booking_add",
                "user_id": user_id,
                "room_id": room_id,
                "reserved_num": reserved_num,
                "begin_date_time": begin_date_time,
                "end_date_time": end_date_time,
            }
            resp = requests.post(event_handler_url, data=json.dumps(data))
            if resp.status_code == 200:
                st.success("登録成功")
            else:
                st.error("登録失敗")
            st.json(resp.json())


def show_room(event_handler_url: str):
    st.title("会議室登録")

    with st.form(key="room"):
        name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", min_value=1, step=1)
        submit_button = st.form_submit_button(label="登録")
        if submit_button:
            data = {
                "handler": "room_add",
                "name": name,
                "capacity": capacity,
            }
            resp = requests.post(event_handler_url, data=json.dumps(data))
            if resp.status_code == 200:
                st.success("登録成功")
            else:
                st.error("登録失敗")
            st.json(resp.json())

def show_user(event_handler_url: str):
    st.title("ユーザー登録")

    with st.form(key="user"):
        name: str = st.text_input("氏名", max_chars=12)
        submit_button = st.form_submit_button(label="登録")
        if submit_button:
            data = {
                "handler": "user_add",
                "name": name,
            }            
            resp = requests.post(event_handler_url, data=json.dumps(data))
            if resp.status_code == 200:
                st.success("登録成功")
            else:
                st.error("登録失敗")
            st.json(resp.json())

run()
