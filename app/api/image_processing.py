import boto3
import uuid
from fastapi import APIRouter, File, UploadFile


router = APIRouter()

@router.post("/upload")
async def create_user(file: UploadFile = File(...)):
    s3_client = boto3.client("s3")
    dynamodb = boto3.client('dynamodb')
    file_content = await file.read()
    s3_client.put_object(
        Bucket="cloud-thumb-bucket",
        Key=file.filename,
        Body=file_content,
        ContentType=file.content_type
    )
    dynamodb.put_item(
        TableName='CloudThumb-Table',
        Item={
            'UserId': {'S': str(uuid.uuid4())},
            'FileName': {'S': file.filename},
            'ContentType': {'S': file.content_type},
            'Headers': {'S': str(file.headers)}
    })
    return {"success: file uploaded successfully"}

@router.get("/analysis/{image_id}")
async def get_image_analysis(image_id: str):
    return {'message': 'Feature coming soon'}