import shutil
from io import BytesIO
from pathlib import Path

import pytest
from app.config import Settings
from app.schemas import PresignRequest
from app.services import UploadService
from fastapi import UploadFile


@pytest.fixture()
def tmp_upload_service(tmp_path) -> UploadService:
    settings = Settings(
        database_url="sqlite://",
        public_base_url="http://test.local:8000",
        uploads_dir=str(tmp_path / "static" / "products"),
    )
    return UploadService(settings=settings)


def test_presign_generates_product_key_with_extension(tmp_upload_service):
    data = PresignRequest(filename="foto.png")

    result = tmp_upload_service.presign(data)

    assert result.upload_url.startswith("/uploads/local/products/")
    assert result.upload_url.endswith(".png")
    assert result.public_url == f"http://test.local:8000{result.upload_url}"


def test_presign_defaults_extension_when_missing(tmp_upload_service):
    data = PresignRequest(filename="sin_extension")

    result = tmp_upload_service.presign(data)

    assert result.upload_url.endswith(".jpg")


def test_presign_generates_unique_keys(tmp_upload_service):
    first = tmp_upload_service.presign(PresignRequest(filename="a.jpg"))
    second = tmp_upload_service.presign(PresignRequest(filename="b.jpg"))

    assert first.upload_url != second.upload_url


def test_save_local_writes_file_and_returns_urls(tmp_upload_service):
    file = UploadFile(
        filename="plato.jpg",
        file=BytesIO(b"datos-de-imagen"),
    )

    result = tmp_upload_service.save_local(file)

    saved_path = Path(tmp_upload_service._upload_dir()) / Path(result.upload_url).name
    assert saved_path.exists()
    assert saved_path.read_bytes() == b"datos-de-imagen"
    assert result.public_url.startswith("http://test.local:8000")


def test_extension_extraction(tmp_upload_service):
    assert tmp_upload_service._extension("foto.png") == "png"
    assert tmp_upload_service._extension("sin_ext") == "jpg"


def test_upload_dir_is_created(tmp_upload_service, tmp_path):
    target = tmp_path / "nuevo" / "dir"
    upload_service = UploadService(Settings(uploads_dir=str(target)))

    directory = upload_service._upload_dir()

    assert directory.exists()
    shutil.rmtree(directory)
