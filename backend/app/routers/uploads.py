import os
import uuid
import shutil

from fastapi import APIRouter, UploadFile, File

from app.schemas import PresignRequest, PresignResponse

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "products")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/presign", response_model=PresignResponse)
def presign_upload(data: PresignRequest):
    ext = data.filename.rsplit(".", 1)[-1] if "." in data.filename else "jpg"
    key = f"products/{uuid.uuid4()}.{ext}"

    upload_url = f"/uploads/local/{key}"
    public_url = f"http://localhost:8000{upload_url}"
    return PresignResponse(upload_url=upload_url, public_url=public_url)


@router.post("/local")
async def upload_local(file: UploadFile = File(...)):
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"upload_url": f"/uploads/local/products/{filename}", "public_url": f"http://localhost:8000/uploads/local/products/{filename}"}
