import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CampusEvents')

def lambda_handler(event, context):
    # Parse the incoming request body
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    event_id = body.get('eventID')

    if not event_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing eventID in request')
        }

    # Fetch the event from DynamoDB
    response = table.get_item(
        Key={'eventID': event_id}
    )

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps(f'No event found with ID: {event_id}')
        }

    event_name = item.get('title', 'Unnamed Event')
    event_date = item.get('dateTime', 'TBD')

    # Send the email
    ses = boto3.client('ses', region_name='us-east-1')

    ses.send_email(
        Source='lippycody45@gmail.com', #christopher.falcone@quinnipiac.edu
        Destination={
            'ToAddresses': ['lippycody45@gmail.com'] #christopherjofalcone@gmail.com
        },
        Message={
            'Subject': {'Data': 'Event Notification'},
            'Body': {
                'Text': {'Data': f'You have an upcoming event {event_name} on {event_date}'},
                'Html': {'Data': f'<h1>Hello!</h1><p>You have an upcoming event <strong>{event_name}</strong> on {event_date}</p>'}
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Email sent for event: {event_name} on {event_date}')
    }