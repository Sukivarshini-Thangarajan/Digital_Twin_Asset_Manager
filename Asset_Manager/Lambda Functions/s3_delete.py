import json
import boto3
import urllib.parse

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = "xr-asset-storage"

def lambda_handler(event, context):
    try:
        # Extract filename from path parameters
        path_params = event.get('pathParameters') or {}
        raw_filename = path_params.get('filename')

        if not raw_filename:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Filename required"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            }

        # Decode URL-encoded filename
        filename = urllib.parse.unquote(raw_filename)

        # Delete the object from S3
        s3.delete_object(Bucket=BUCKET, Key=filename)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Deleted '{filename}' successfully"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        }
