import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CampusEvents')

def lambda_handler(event, context):
    try: 
        body = json.loads(event.get('body') or '{}')

        item = { 
            'eventID': str(uuid.uuid4()),
            'title': body.get('title'),
            'category': body.get('category'),
            'description': body.get('description'),
            'dateTime': body.get('dateTime'),
            'location': body.get('location'),
            'creatorId': body.get('creatorId', 'admin'),
            'createdAt': datetime.utcnow().isoformat()
        }

        item = {k: v for k, v in item.items() if v is not None}

        table.put_item(Item=item)

        ses = boto3.client('ses', region_name='us-east-1')
        ses.send_email(
            Source='lippycody45@gmail.com',
            Destination={'ToAddresses': ['lippycody45@gmail.com']},
            Message={
                'Subject': {'Data': 'New Campus Event Posted!'},
                'Body': {
                    'Text': {'Data': f'A new event has been posted: {item.get("title")} on {item.get("dateTime", "TBD")}'},
                    'Html': {'Data': f'<h1>New Event!</h1><p>A new event has been posted: <strong>{item.get("title")}</strong> on {item.get("dateTime", "TBD")}</p>'}
                }
            }
        )

        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE,PUT'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE,PUT'
            },
            'body': json.dumps({'error': str(e)})
        }