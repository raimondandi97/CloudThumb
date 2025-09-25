import json

import boto3
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends

from app.auth import get_current_user

router = APIRouter()

@router.post("/upload")
async def create_user(file: UploadFile = File(...), _: str = Depends(get_current_user)):
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
async def get_image_analysis(image_id: str, _: str = Depends(get_current_user)):
    lambda_client = boto3.client("lambda", region_name="us-east-1")
    payload = {"key": image_id}

    response = lambda_client.invoke(
        FunctionName="opencv_lambda",
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    result = json.loads(response["Payload"].read().decode("utf-8"))
    if "error" in result:
        if result["error"] == "Item not found":
            raise HTTPException(status_code=404, detail="Item not found")
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    return result