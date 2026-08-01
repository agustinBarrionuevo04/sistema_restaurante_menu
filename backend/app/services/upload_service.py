import os
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile

from app.config import Settings
from app.schemas import PresignRequest, PresignResponse


@dataclass
class UploadService:
    """Servicio de gestión de imágenes de productos (subida local y presign)."""

    settings: Settings

    def _upload_dir(self) -> Path:
        base = Path(self.settings.uploads_dir)
        if not base.is_absolute():
            base = Path(__file__).resolve().parent.parent / "static" / "products"
        base.mkdir(parents=True, exist_ok=True)
        return base

    def _extension(self, filename: str) -> str:
        return filename.rsplit(".", 1)[-1] if "." in filename else "jpg"

    def presign(self, data: PresignRequest) -> PresignResponse:
        """Genera un nombre de archivo y su URL pública de destino."""
        ext = self._extension(data.filename)
        key = f"products/{uuid.uuid4()}.{ext}"
        upload_url = f"/uploads/local/{key}"
        public_url = f"{self.settings.public_base_url}{upload_url}"
        return PresignResponse(upload_url=upload_url, public_url=public_url)

    def save_local(self, file: UploadFile) -> PresignResponse:
        """Guarda un archivo subido en disco y devuelve sus URLs."""
        ext = self._extension(file.filename or "jpg")
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = self._upload_dir() / filename

        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)

        upload_url = f"/uploads/local/products/{filename}"
        public_url = f"{self.settings.public_base_url}{upload_url}"
        os.chmod(filepath, 0o644)
        return PresignResponse(upload_url=upload_url, public_url=public_url)
