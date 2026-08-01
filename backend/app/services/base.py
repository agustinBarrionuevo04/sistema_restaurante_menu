from dataclasses import dataclass, field
from typing import Any, TypeVar

from fastapi import HTTPException
from sqlmodel import Session, SQLModel

_T = TypeVar("_T", bound=SQLModel)


@dataclass
class BaseService:
    """Servicio base que encapsula acceso a la sesión y helpers comunes.

    Heredar de esta clase da acceso a :attr:`session` y a :meth:`get_or_404`,
    útil para cualquier recurso persistido en la base de datos.
    """

    session: Session = field(default_factory=Session)

    def get_or_404(self, model: type[_T], id: Any, detail: str) -> _T:
        """Devuelve la entidad por id o lanza HTTPException 404."""
        obj = self.session.get(model, id)
        if obj is None:
            raise HTTPException(status_code=404, detail=detail)
        return obj

    def commit_refresh(self, obj: _T) -> _T:
        """Persiste el objeto y lo refresca para devolver valores cargados."""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
