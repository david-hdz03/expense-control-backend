# Expense Control — Backend API

API REST desarrollada con **FastAPI** y **SQLAlchemy 2.0** para el sistema de control de gastos personales.

---

## 📋 Requisitos

- **Python 3.11.x o superior** (recomendado: **3.12** o **3.13**)
  - Verifica tu versión: `python --version`
  - Descarga desde: https://www.python.org/downloads/

- **pip** (gestor de paquetes Python)
  - Generalmente incluido con Python
  - Verifica: `pip --version`

- **git** (para clonar/actualizar repositorio)

---

## 🚀 Instalación y Setup

### 1. Crear y Activar Entorno Virtual

```bash
# Desde la carpeta backend/
python -m venv .venv

# Activar según tu SO y shell:

# Windows (Git Bash / MSYS)
source .venv/Scripts/activate

# Windows (CMD)
# .venv\Scripts\activate.bat

# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate
```

Verifica que está activo: deberías ver `(.venv)` en el prompt de terminal.

### 2. Instalar Dependencias

```bash
# Con el entorno virtual activado:
pip install -r requirements.txt

# (Opcional) Verifica las dependencias:
pip list
```

**Tiempo esperado:** 2-5 minutos (según velocidad de red)

### 3. Configurar Variables de Entorno

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env y rellena estos valores:
```

**Archivo `.env` — Ejemplo para desarrollo con SQLite:**

```env
# Base de Datos
DATABASE_URL=sqlite:///./expense_control.db

# App
APP_NAME=Expense Control
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8080

# JWT (generar clave: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=tu-clave-secreta-minimo-32-caracteres-aleatorio
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Archivo `.env` — Ejemplo para PostgreSQL (local o remoto):**

```env
# Base de Datos
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/expense_control

# App
APP_NAME=Expense Control
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8080

# JWT
JWT_SECRET_KEY=tu-clave-secreta-minimo-32-caracteres-aleatorio
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Valores obligatorios:**
- `DATABASE_URL` — URL de conexión a la base de datos
- `JWT_SECRET_KEY` — Clave para firmar tokens (mínimo 32 caracteres, idealmente aleatoria)

### 4. Inicializar Base de Datos

La base de datos se crea automáticamente al arrancar el servidor (usando `Base.metadata.create_all()`).

**No necesitas ejecutar migraciones manuales — simplemente arranca el servidor.**

### 5. Ejecutar el Servidor de Desarrollo

```bash
# Con el entorno virtual activado:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

---

## 🌐 Verificar que Funciona

### Health Check
```bash
# En otra terminal:
curl http://localhost:8000/health
# Respuesta esperada: {"status": "healthy"}
```

### Documentación Interactiva (Swagger UI)
Abre en tu navegador: **http://localhost:8000/docs**

Desde aquí puedes:
- Ver todos los endpoints disponibles
- Leer documentación de cada endpoint
- Probar endpoints (autenticación incluida)

### Documentación Alternativa (ReDoc)
**http://localhost:8000/redoc**

---

## 📡 Endpoints Principales

### Autenticación

| Método | Ruta                      | Descripción                      | Requiere Auth |
|--------|---------------------------|----------------------------------|---------------|
| POST   | `/api/auth/register`      | Registra un nuevo usuario        | ❌ No        |
| POST   | `/api/auth/login`         | Inicia sesión, devuelve token    | ❌ No        |
| POST   | `/api/auth/refresh`       | Renueva token de acceso          | ✅ Sí        |

### Gastos (Expenses)

| Método | Ruta                    | Descripción                  | Requiere Auth |
|--------|-------------------------|------------------------------|---------------|
| GET    | `/api/expenses`         | Lista todos los gastos       | ✅ Sí        |
| POST   | `/api/expenses`         | Crea un nuevo gasto          | ✅ Sí        |
| GET    | `/api/expenses/{id}`    | Obtiene un gasto específico  | ✅ Sí        |
| PATCH  | `/api/expenses/{id}`    | Actualiza un gasto           | ✅ Sí        |
| DELETE | `/api/expenses/{id}`    | Elimina un gasto             | ✅ Sí        |

**Nota:** Para endpoints que requieren autenticación, incluye el token en el header:
```
Authorization: Bearer <tu-access-token>
```

---

## 🧪 Ejecutar Tests

```bash
# Con el entorno virtual activado:
pytest

# Opciones útiles:
pytest -v                    # Verbose (muestra cada test)
pytest -v --tb=short        # Muestra errores condensados
pytest tests/test_auth.py    # Ejecuta tests específicos
pytest -k "test_login"       # Ejecuta tests que coincidan con el patrón
```

---

## 📦 Dependencias Clave

- **FastAPI** (0.115.8) — Framework web asincrónico
- **SQLAlchemy** (2.0.48) — ORM para base de datos
- **Pydantic** (2.12.5) — Validación de datos
- **PyJWT** (2.11.0) — Soporte para tokens JWT
- **Uvicorn** (0.34.0) — Servidor ASGI
- **asyncpg** (0.31.0) — Driver async para PostgreSQL
- **bcrypt** (5.0.0) — Hashing de contraseñas
- **pytest** (9.0.2) — Testing

Ver `requirements.txt` para la lista completa.

---

## 🗂️ Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación FastAPI + routers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuración (variables de entorno)
│   │   └── security.py            # Funciones de seguridad y JWT
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                # DeclarativeBase de SQLAlchemy
│   │   ├── session.py             # Engine y session factory
│   │   └── init_db.py             # Inicialización de tablas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # Modelo User (ORM)
│   │   ├── expense.py             # Modelo Expense (ORM)
│   │   └── oauth_account.py       # Modelo OAuthAccount (ORM)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                # Schemas User (Pydantic)
│   │   ├── expense.py             # Schemas Expense (Pydantic)
│   │   └── auth.py                # Schemas Auth (Pydantic)
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── auth.py            # Router de autenticación
│           └── expenses.py        # Router de gastos
├── tests/                         # Pruebas unitarias e integración
├── .env.example                   # Template de variables de entorno
├── .gitignore
├── alembic.ini                    # Configuración de Alembic (migraciones)
├── requirements.txt               # Dependencias de Python
└── README.md                      # Este archivo
```

---

## ⚙️ Configuración Avanzada

### Cambiar Puerto

```bash
uvicorn app.main:app --reload --port 9000
# API disponible en http://localhost:9000
```

### Escuchar en Todas las Interfaces

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Útil para acceder desde otra máquina en la red
# Dirección: http://<tu-ip-local>:8000
```

### Modo Producción (sin --reload)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Para deployment final (no reinicia con cambios en código)
```

---

## 🛠️ Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'app'`
```bash
# Verifica estar en la carpeta backend/
cd backend

# Verifica que el entorno virtual está activado
source .venv/Scripts/activate    # (.venv) debe aparecer en prompt

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: `Cannot find a matching version for [driver]`
```bash
# Verifica tu DATABASE_URL en .env
# Opciones válidas:
# - sqlite:///./expense_control.db
# - postgresql+asyncpg://user:pass@localhost:5432/db
# - mysql+pymysql://user:pass@localhost:3306/db
```

### Error: `KeyError: 'DATABASE_URL'` o similar
```bash
# Verifica que .env existe en backend/
ls -la .env

# Rellena todos los campos requeridos en .env
cat .env

# Si faltan valores, edita el archivo
```

### Error: `CORS` en navegador (frontend no conecta)
```bash
# Verifica CORS_ORIGINS en .env
# Debe incluir la URL del frontend:
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8080

# En desarrollo, puedes usar un valor amplio:
CORS_ORIGINS=http://localhost:*
```

### La base de datos no se crea
```bash
# Verifica que la carpeta backend/ es escribible
# Prueba crear un archivo de prueba:
touch test.txt
rm test.txt

# Si usas SQLite, verifica la ruta:
# DATABASE_URL=sqlite:///./expense_control.db    # Correcto
# DATABASE_URL=sqlite:///expense_control.db      # También válido
```

---

## 📚 Flujo de Desarrollo Típico

### Terminal 1: Ejecutar el servidor
```bash
cd backend
source .venv/Scripts/activate    # Windows bash
uvicorn app.main:app --reload
```

### Terminal 2: Ejecutar tests (mientras editas)
```bash
cd backend
source .venv/Scripts/activate    # Windows bash
pytest --watch                   # O pytest -v repetidamente
```

### Verificar en navegador
1. Abre http://localhost:8000/docs
2. Prueba endpoints en Swagger UI
3. Ve los cambios en tiempo real

---

## 🔐 Seguridad en Desarrollo

⚠️ **Importante para desarrollo local:**

- `DEBUG=true` muestra errores detallados (útil para desarrollo, ❌ **NO en producción**)
- `JWT_SECRET_KEY` debe ser aleatoria y segura (usa: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `CORS_ORIGINS` está abierto a localhost (ajusta para producción)
- `.env` contiene secretos — **nunca commitear** a git (ya está en `.gitignore`)

---

## 📝 Variables de Entorno Completas

| Variable                      | Tipo    | Requerida | Default | Descripción |
|-------------------------------|---------|-----------|---------|-------------|
| `DATABASE_URL`                | string  | ✅ Sí    | —       | URL de conexión a BD |
| `JWT_SECRET_KEY`              | string  | ✅ Sí    | —       | Clave para firmar JWT (32+ chars) |
| `APP_NAME`                    | string  | ❌ No    | Expense Control | Nombre de la aplicación |
| `DEBUG`                       | boolean | ❌ No    | true    | Modo debug (mostrar errores) |
| `CORS_ORIGINS`                | string  | ❌ No    | localhost:3000,... | URLs permitidas (separadas por coma) |
| `JWT_ALGORITHM`               | string  | ❌ No    | HS256   | Algoritmo para firmar tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | integer | ❌ No    | 15      | Minutos antes de expirar token acceso |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | integer | ❌ No    | 7       | Días antes de expirar token refresh |

---

## 🚀 Próximos Pasos

1. **Completa el setup** siguiendo los pasos 1-5 de esta guía
2. **Verifica la conexión** abriendo http://localhost:8000/docs
3. **Prueba autenticación**:
   - Registra un usuario en `/api/auth/register` (POST)
   - Inicia sesión en `/api/auth/login` (POST)
   - Copia el `access_token`
4. **Crea tu primer gasto**:
   - Haz click en "Authorize" (arriba a la derecha de Swagger)
   - Pega: `Bearer <tu-token>`
   - Usa POST `/api/expenses` para crear un gasto
5. **Integra con el frontend** — el frontend conectará automáticamente

---

## 📖 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pytest](https://docs.pytest.org/)

---

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección **"Solución de Problemas"** arriba
2. Verifica que estás en la rama correcta: `git branch`
3. Actualiza dependencias: `pip install --upgrade -r requirements.txt`
4. Limpia cache de Python: `find . -type d -name __pycache__ -exec rm -r {} +`
5. Consulta la documentación oficial de FastAPI

---

**Última actualización:** 2026-04-18  
**Versión recomendada de Python:** 3.11+ (probado con 3.12, 3.13)  
**Framework:** FastAPI 0.115.8  
**ORM:** SQLAlchemy 2.0.48
