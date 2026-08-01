from fastapi import APIRouter, Depends, File, UploadFile

from app.deps import get_upload_service
from app.schemas import PresignRequest, PresignResponse
from app.services import UploadService

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/presign", response_model=PresignResponse)
def presign_upload(
    data: PresignRequest, service: UploadService = Depends(get_upload_service)
):
    """Genera las URLs de subida y pública para una imagen nueva."""
    return service.presign(data)


@router.post("/local")
def upload_local(
    file: UploadFile = File(...), service: UploadService = Depends(get_upload_service)
):
    """Guarda una imagen en disco y devuelve sus URLs."""
    return service.save_local(file)
