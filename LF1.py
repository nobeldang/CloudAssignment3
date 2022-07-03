import boto3
import json
import requests



# Lambda execution starts here
def lambda_handler(event, context):
    region = "ENTER REGION es-####-1" 
    service = "es"
    credentials = boto3.Session().get_credentials()
    
    host = API_host_URL
    
    index = "posts"
    q = event["queryStringParameters"]["q"]

    url = host + "/" + index + "/_search?"
    url = url + "q={q}".format(q = q)
    
    # Make the signed HTTP request
    r = requests.get(url, auth=(username, password))
    
    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }
    
    idx = []
    res = json.loads(r.content.decode('utf-8'))
    for vals in res["hits"]["hits"]:
        idx.append(vals["_id"])
    
    if len(idx)==0:
        response['body'] = "No answers found for this category"
        return response
    dynamodb = boto3.resource('dynamodb', region_name="ENTER REGION NAME")
    table = dynamodb.Table('posts')
    
    result = []
    for val in idx:
        resp = table.get_item(Key = {"id": int(val)})
        if "Item" in resp.keys():
            result.append(resp["Item"][" posts"])
    print(len(result))
    if len(result)==0:
        response['body'] = "No answers found for this category"
        return 
    #Add the search results to the response
    response['body'] = str(result)
    return response