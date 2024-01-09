import boto3

from settings import settings

dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
                          aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY)
test_table = dynamodb.Table('test')

# test_table.put_item(
#     Item={
#         'name': 'johndoe',
#         'sale': '25',
#     }
# )

response = test_table.get_item(
    Key={
        'name': 'johndoe',
        'sale': '25',
    }
)

item = response['Item']
print(item)
print(item['name'])
