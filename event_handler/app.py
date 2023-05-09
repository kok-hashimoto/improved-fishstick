import base64
import json
import os
import uuid

import boto3

def lambda_handler(event, context):
    print(f"{event=}")
    print(f"{context=}")

    booking_table = os.environ["BOOKING_TABLE"]
    room_table = os.environ["ROOM_TABLE"]
    user_table = os.environ["USER_TABLE"]

    body = base64.b64decode(event["body"])
    params = json.loads(body)
    handler = params["handler"]
    if handler == "booking_add":
        resp = booking_add(booking_table, params)
    elif handler == "booking_list":
        resp = booking_list(booking_table)
    elif handler == "room_add":
        resp = room_add(room_table, params)
    elif handler == "room_list":
        resp = room_list(room_table)
    elif handler == "user_add":
        resp = user_add(user_table, params)
    elif handler == "user_list":
        resp = user_list(user_table)
    else:
        return {"statusCode": 500, "body": "no matching handler"}

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
    }


def booking_add(booking_table: str, params:dict[str, str]):
    id = str(uuid.uuid4())
    user_id = params["user_id"]
    room_id = params["room_id"]
    reserved_num = params["reserved_num"]
    begin_date_time = params["begin_date_time"]
    end_date_time = params["end_date_time"]
    new_booking = {"id":id, "user_id":user_id, "room_id":room_id, "reserved_num":reserved_num, "begin_date_time":begin_date_time, "end_date_time":end_date_time}

    table = boto3.resource("dynamodb").Table(booking_table)
    table.put_item(Item=new_booking)

    return new_booking

def booking_list(booking_table: str) -> list[dict[str, str]]:
    table = boto3.resource("dynamodb").Table(booking_table)
    items = table.scan()["Items"]
    bookings = []
    for item in items:
        bookings.append({"id":item["id"], "user_id":item["user_id"], "room_id":item["room_id", "reserved_num":item["reserved_num"], "begin_date_time":item["begin_date_time"], "end_date_time":item["end_date_time"]]})
    return bookings

def room_add(room_table: str, params: dict[str, str]):
    id = str(uuid.uuid4())
    name = params["name"]
    capacity = params["capacity"]
    new_room = {"id":id, "name":name, "capacity":capacity}

    table = boto3.resource("dynamodb").Table(room_table)
    table.put_item(Item=new_room)

    return new_room

def room_list(room_table: str) -> list[dict[str, str]]:
    table = boto3.resource("dynamodb").Table(room_table)
    items = table.scan()["Items"]
    rooms = []
    for item in items:
        rooms.append({"id":item["id"], "name":item["name"], "capacity":item["capacity"]})
    return rooms

def user_add(user_table: str, params: dict[str, str]):
    id = str(uuid.uuid4())
    name = params["name"]
    new_user = {"id":id, "name":name}

    table = boto3.resource("dynamodb").Table(user_table)
    table.put_item(Item=new_user)

    return new_user

def user_list(user_table: str) -> list[dict[str, str]]:
    table = boto3.resource("dynamodb").Table(user_table)
    items = table.scan()["Items"]
    users = []
    for item in items:
        users.append({"id":item["id"], "name":item["name"]})
    return users