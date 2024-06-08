import boto3
import json
import requests

print('Loading function')
dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    
    map_response_to_json()

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

def map_response_to_json():
    baseUrl = "https://beetle-curious-longhorn.ngrok-free.app"
    endpoint = "/energyUsage/"
    user = "user/mfkzen@gmail.com"
    frequency = "/frequency/hourly"
    url = baseUrl+endpoint+user+frequency
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()

        # Generate a response with the parsed JSON data
        response_data = {
            "status": "success",
            "message": "Request processed successfully",
            "data": response_json
        }
    else:
        # Generate an error response
        response_data = {
            "status": "error",
            "message": "Failed to fetch data",
            "data": None
        }

    # Convert the response data to JSON format
    response_json = json.dumps(response_data)

    return response_json

