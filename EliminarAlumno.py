import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            ConditionExpression='attribute_exists(alumno_id)'
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
        'mensaje': 'Alumno eliminado'
    }
