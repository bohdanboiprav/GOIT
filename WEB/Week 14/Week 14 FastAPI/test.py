import json
from datetime import datetime


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'time': json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'body': json.dumps('Hello from Lambda!')
    }


print(lambda_handler(1, 2))
