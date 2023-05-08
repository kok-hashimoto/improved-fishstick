import base64
import json
import os
import uuid

import boto3

def lambda_handler(event, context):
    print(f"{event=}")
    print(f"{context=}")

    booking_table = os.environ["BOOKING_TABLE"]

    id = str(uuid.uuid4())
    body = base64.b64decode(event["body"])
    params = json.loads(body)
    user_id = params["user_id"]
    room_id = params["room_id"]
    reserved_num = params["reserved_num"]
    begin_date_time = params["begin_date_time"]
    end_date_time = params["end_date_time"]
    new_booking = {"id":id, "user_id":user_id, "room_id":room_id, "reserved_num":reserved_num, "begin_date_time":begin_date_time, "end_date_time":end_date_time}

    table = boto3.resource("dynamodb").Table(booking_table)
    table.put_item(Item=new_booking)

    return {
        "statusCode": 200,
        "body": json.dumps(new_booking),
    }
