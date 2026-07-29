import os
import uuid
import datetime

import boto3
from botocore.config import Config
from fastapi import APIRouter, Depends

from app.schemas import PresignRequest, PresignResponse

router = APIRouter(prefix="/uploads", tags=["uploads"])

R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "")
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "")
R2_BUCKET = os.getenv("R2_BUCKET", "")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "")


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


@router.post("/presign", response_model=PresignResponse)
def presign_upload(data: PresignRequest):
    ext = data.filename.rsplit(".", 1)[-1] if "." in data.filename else "jpg"
    key = f"products/{uuid.uuid4()}.{ext}"

    client = get_s3_client()
    upload_url = client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": R2_BUCKET,
            "Key": key,
            "ContentType": data.content_type,
        },
        ExpiresIn=3600,
    )

    public_url = f"{R2_PUBLIC_URL.rstrip('/')}/{key}"
    return PresignResponse(upload_url=upload_url, public_url=public_url)
