import base64
import json
import os
import uuid

import boto3

def lambda_handler(event, context):
    print(f"{event=}")
    print(f"{context=}")

    room_table = os.environ["ROOM_TABLE"]

    id = str(uuid.uuid4())
    body = base64.b64decode(event["body"])
    params = json.loads(body)
    name = params["name"]
    capacity = params["capacity"]
    new_room = {"id":id, "name":name, "capacity":capacity}

    table = boto3.resource("dynamodb").Table(room_table)
    table.put_item(Item=new_room)

    return {
        "statusCode": 200,
        "body": json.dumps(new_room),
    }
