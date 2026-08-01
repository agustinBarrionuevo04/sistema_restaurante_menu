from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import Settings, get_settings

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class AuthService:
    """Servicio de autenticación: login, emisión y validación de tokens JWT."""

    settings: Settings

    def _secret_key(self) -> str:
        return self.settings.jwt_secret

    def _hash_password(self, plain: str) -> str:
        return pwd_context.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verifica una contraseña contra su hash almacenado."""
        return pwd_context.verify(plain, hashed)

    def create_access_token(self, subject: str) -> str:
        """Genera un JWT firmado con expiración configura."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.settings.access_token_expire_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(
            payload, self._secret_key(), algorithm=self.settings.jwt_algorithm
        )

    def login(self, username: str, password: str) -> str | None:
        """Autentica credenciales de admin y devuelve un token, o None si fallan."""
        if username != self.settings.admin_username:
            return None
        if not self.verify_password(
            password, self._hash_password(self.settings.admin_password)
        ):
            return None
        return self.create_access_token(username)

    def validate_token(self, credentials: HTTPAuthorizationCredentials) -> str:
        """Valida un token Bearer y devuelve el usuario, o lanza 401."""
        token = credentials.credentials
        try:
            payload = jwt.decode(
                token, self._secret_key(), algorithms=[self.settings.jwt_algorithm]
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido") from None

        username = payload.get("sub")
        if username != self.settings.admin_username:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username


def get_auth_service(settings: Settings = Depends(get_settings)) -> AuthService:
    """Dependencia que provee una instancia de AuthService configurada."""
    return AuthService(settings=settings)


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> str:
    """Dependencia de protección de rutas; devuelve el usuario autenticado."""
    return auth_service.validate_token(credentials)
