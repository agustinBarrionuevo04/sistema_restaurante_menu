from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.schemas import TokenResponse
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """Autentica con credenciales de admin y devuelve un token JWT."""
    token = auth_service.login(data.username, data.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return TokenResponse(access_token=token)
