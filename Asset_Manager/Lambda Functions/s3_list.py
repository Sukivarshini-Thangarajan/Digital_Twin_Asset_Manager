import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = "xr-asset-storage"  # your bucket

def lambda_handler(event, context):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = []
        for obj in response.get('Contents', []):
            files.append({
                "name": obj['Key'],
                "size": obj['Size'],
                "last_modified": obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S")
            })

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
            },
            "body": json.dumps(files)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
