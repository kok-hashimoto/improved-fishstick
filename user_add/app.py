import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"{event=}")
    logger.info(f"{context=}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
