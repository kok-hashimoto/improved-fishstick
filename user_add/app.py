import base64
import json
import os
import uuid

import boto3

def lambda_handler(event, context):
    print(f"{event=}")
    print(f"{context=}")

    user_table: str = os.environ["USER_TABLE"]

    id = str(uuid.uuid4())
    body = base64.b64decode(event["body"])
    params = json.loads(body)
    name = params["name"]
    new_user = {"id":id, "name":name}

    table = boto3.resource("dynamodb").Table(user_table)
    table.put_item(Item=new_user)

    return {
        "statusCode": 200,
        "body": json.dumps(new_user),
    }
