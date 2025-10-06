import json
import boto3

# Initialize S3 client with region (ensure this matches your bucket's region)
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = "xr-asset-storage"

def lambda_handler(event, context):
    try:
        # Extract query parameters
        params = event.get('queryStringParameters') or {}
        filename = params.get('filename')
        content_type = params.get('contentType')  # Expecting MIME type from frontend

        # Validate required parameters
        if not filename or not content_type:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Both 'filename' and 'contentType' are required"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            }

        # Generate pre-signed PUT URL with Content-Type
        upload_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET,
                'Key': filename,
                'ContentType': content_type
            },
            ExpiresIn=300  # 5 minutes
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"uploadURL": upload_url}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        }
