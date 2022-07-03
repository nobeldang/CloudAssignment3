import json
import boto3
from time import gmtime, strftime
from uuid import uuid1
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("posts")

now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    id = uuid1().int
    
    pos = event["posts"]
    
    print(event)
    response = table.put_item(
        Item={
            "id": id,
            "date":now,
            "posts":pos
            })
    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps("Added successfully with id " + str(id))
    }