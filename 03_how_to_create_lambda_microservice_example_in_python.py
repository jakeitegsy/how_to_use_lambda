import boto3
import json

print('Loading function')
dynamodb = boto3.client('dynamodb')

def respond(error, response=None):
	return {
		'statusCode': '400' if error else '200',
		'body': error.message if error else json.dumps(response),
		'headers': {
			'Content-Type': 'application/json',
		}
	}

def lambda_handler(event, context):
	operations= {
		'DELETE': lambda dynamodb, x: dynamodb.delete_item(**x),
		'GET': lambda dynamodb, x: dynamodb.scan(**x),
		'POST': lambda dynamodb, x: dynamodb.put_item(**x),
		'PUT': lambda dynamodb, x: dynamodb.update_item(**x)
	}

	operation = event['httpMethod']

	if operation in operations:
		payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
		return respond(None, operations[operation](dynamodb, payload))
	else:
		return respond(ValueError('Unsupport method "{}"'.format(operation))