import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression='SET alumno_datos = :datos',
            ExpressionAttributeValues={':datos': alumno_datos},
            ConditionExpression='attribute_exists(alumno_id)',
            ReturnValues='ALL_NEW'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            # Salida (json)
            return {
                'statusCode': 404,
                'mensaje': 'Alumno no encontrado'
            }
        raise
    # Salida (json)
    return {
        'statusCode': 200,
        'mensaje': 'Alumno modificado',
        'alumno': response['Attributes']
    }
