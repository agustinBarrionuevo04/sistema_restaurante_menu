# Sistema de Carta Digital para Restaurante

Sistema completo para gestionar y publicar la carta digital de un restaurante:
una **carta pública** (solo lectura, mobile-first) que ven los clientes, y un
**panel de administración** protegido por JWT para el CRUD de categorías,
productos y adicionales, más la configuración del layout de la carta.

## Stack

| Capa       | Tecnología                                                            |
|------------|-----------------------------------------------------------------------|
| Front      | React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui (`@menu/ui`)  |
| Backend    | Python 3.11+ / FastAPI + SQLModel + Pydantic v2                        |
| Base datos | SQLite (desarrollo) / PostgreSQL (producción) + Alembic (migraciones) |
| Auth       | JWT (python-jose) + bcrypt (passlib)                                   |

Monorepo gestionado con **pnpm workspaces**.

## Estructura del proyecto

```
/
├── apps/
│   ├── carta/                # App pública, solo lectura, mobile-first
│   └── admin/                # Panel CRUD con auth JWT
├── packages/
│   ├── types/                # Tipos TypeScript compartidos
│   ├── api-client/           # Funciones fetch tipadas hacia el backend
│   └── ui/                   # Componentes shadcn/ui compartidos
├── backend/                  # FastAPI + SQLModel + PostgreSQL/SQLite
│   ├── app/
│   │   ├── main.py           # Factory create_app(), monta routers y migraciones
│   │   ├── config.py         # Clase Settings (pydantic-settings)
│   │   ├── db.py             # Engine + get_session
│   │   ├── models/           # SQLModel: Category, Product, AddOn, ProductAddOn, AppSettings
│   │   ├── schemas.py        # Pydantic: Create/Update/Out por dominio
│   │   ├── deps.py           # Proveedores de servicios (inyección por Depends)
│   │   ├── services/         # Capa de negocio (clases @dataclass)
│   │   └── routers/          # Endpoints HTTP (delegan en services)
│   ├── alembic/              # Migraciones de base de datos
│   └── tests/                # Unit tests (pytest)
└── docker-compose.yml        # PostgreSQL para producción
```

## Arquitectura elegida

El backend sigue una arquitectura por **capas** con un **Service Layer**:

```
Routers (HTTP)  →  Services (negocio)  →  Models/Session (persistencia)
     │                   │
     └── Schemas (validación Pydantic)  ←─ configuración central (Settings)
```

- **Routers**: funciones finas que capturan el request HTTP, validan con
  schemas y delegan toda la lógica en un servicio. No contienen lógica de
  negocio.
- **Services**: clases `@dataclass` que encapsulan la lógica de cada dominio
  (categorías, productos, adicionales, settings, auth, uploads). Se inyectan
  por dependencia (`Depends`) y reciben la `Session` de base de datos.
- **Models**: entidades `SQLModel` que representan las tablas.
- **Schemas**: modelos `Pydantic` de entrada/salida (Create/Update/Out).
- **Config**: clase `Settings` (`pydantic-settings`) que centraliza todas las
  variables de entorno y flags del sistema; se inyecta por dependencia.

### ¿Por qué esta arquitectura?

1. **Separación de responsabilidades**: cada capa cumple una sola función;
   cambiar la fuente de datos o el framework HTTP no obliga a reescribir la
   lógica de negocio.
2. **Lógica testeable**: al extraer la lógica a servicios con dependencias
   inyectadas, cada función se puede probar de forma **aislada** con una base
   de datos en memoria (ver Tests). Es lo que permite cubrir unitariamente
   todo el comportamiento del sistema.
3. **Consistencia y mantenibilidad**: los `Update` usan `model_dump(exclude_unset)`
   para aplicar solo los campos enviados; el patrón `get_or_404` y los
   `@dataclass` hacen el código uniforme y fácil de extender.
4. **Configuración tipada y centralizada**: lejos de `os.getenv` dispersos, la
   clase `Settings` valida y documenta cada variable de entorno.
5. **Migraciones reales**: Alembic versiona el esquema (en vez de `create_all`),
   permitiendo evolucionar la base de datos de forma reproducible.
6. **Frontend compartido**: `@menu/ui` y `@menu/types` se reutilizan entre la
   carta y el panel de administración, evitando duplicación.

### Flujo de una petición de ejemplo

`GET /products?status=active` →
router `products.list_products` →
`ProductService.list()` (filtros) + `ProductService.to_out()` (ensambla
adicionales) →
respuesta JSON validada por `ProductOut`.

---

## Cómo correr el programa completo

### Requisitos
- Node.js >= 18 y **pnpm**
- Python >= 3.11 (venv)
- Docker + Docker Compose (solo si querés PostgreSQL)

### 1. Base de datos (opcional para producción)

```bash
docker compose up -d
```

Para desarrollo se usa SQLite por defecto (`sqlite:///./menu.db`), sin necesidad
de Docker.

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"   # incluye pytest, httpx2, ruff

# Aplicar migraciones
alembic upgrade head

# Iniciar API (puerto 8000)
uvicorn app.main:app --reload
```

### 3. Seed de datos de demostración (opcional)

Genera categorías, adicionales y productos de ejemplo:

```bash
cd backend
source .venv/bin/activate
python seed.py
```

### 4. Frontend (dos procesos)

```bash
# Carta pública (puerto 5173)
pnpm dev:carta

# Panel de administración (puerto 5174)
pnpm dev:admin
```

Accesos:
- Carta pública: <http://localhost:5173>
- Panel admin: <http://localhost:5174> — credenciales por defecto `admin` / `admin123`

### Variables de entorno del backend (`.env` en `backend/`)

```bash
DATABASE_URL=sqlite:///./menu.db        # o postgresql://...
JWT_SECRET=change-me-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_ENDPOINT=
R2_BUCKET=
R2_PUBLIC_URL=
```

En frontend: `VITE_API_URL` (default `http://localhost:8000`) en `apps/*/.env`.

---

## Tests

Los tests son **unitarios** sobre la capa de servicios, usando una base de
datos SQLite **en memoria**, aislada por test (no tocan `menu.db`).

```bash
cd backend
source .venv/bin/activate
pytest            # o: python -m pytest
```

Para ver la salida detallada por test: `pytest -v`.

### Qué se cubre
- `SettingsService`: obtención por defecto, actualización y patrón singleton.
- `CategoryService`: CRUD, ordenamiento y protección 409 al borrar categorías
  con productos.
- `ProductService`: CRUD, filtros (categoría / estado), ensamblado de
  adicionales y validaciones 404/409.
- `AddOnService`: CRUD y protección 409 cuando está en uso.
- `AuthService`: login, emisión/validación de tokens, contraseñas y tokens
  inválidos/expirados.
- `UploadService`: generación de presign y guardado local de imágenes.

---

## Lint y formato

El backend usa **ruff** (check + format) con configuración en `pyproject.toml`:

```bash
cd backend
source .venv/bin/activate
ruff check app tests
ruff format --check app tests
```

---

## Endpoints principales

- **Categorías**: `GET/POST /categories`, `PATCH/DELETE /categories/{id}`
- **Productos**: `GET/POST /products`, `GET/PATCH/DELETE /products/{id}`,
  `POST/DELETE /products/{id}/addons[/{addon_id}]`
- **Adicionales**: `GET/POST /addons`, `PATCH/DELETE /addons/{id}`
- **Configuración**: `GET /settings` (público), `PUT /settings` (protegido)
- **Uploads**: `POST /uploads/presign`, `POST /uploads/local`
- **Auth**: `POST /auth/login`

Documentación interactiva de la API en <http://localhost:8000/docs>.
