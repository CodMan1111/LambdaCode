import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CampusEvents')  

def lambda_handler(event, context):
    event_id = event.get('queryStringParameters', {}).get('eventId')

    if not event_id:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'eventId is required'})
        }

    table.delete_item(
        Key={'eventID': event_id}  
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'Event deleted successfully'})
    }