# API - Documentacion de Endpoints

Base URL: `http://localhost:8000`  
Formato: JSON  
Autenticacion: Bearer token (`Authorization: Bearer <access_token>`)

## Modulos

| Archivo | Prefijo | Descripcion |
|---|---|---|
| [auth.md](endpoints/auth.md) | `/api/auth` | Registro, login, refresh y perfil |
| [verification.md](endpoints/verification.md) | `/api/verification` | Solicitud y confirmacion de codigo de verificacion |
| [users.md](endpoints/users.md) | `/api/users` | Creacion y consulta de usuarios |
| [transactions.md](endpoints/transactions.md) | `/api/transactions` | CRUD de transacciones |
| [categories.md](endpoints/categories.md) | `/api/categories` | CRUD de categorias |

## Endpoints de sistema

| Metodo | Ruta | Descripcion |
|---|---|---|
| `GET` | `/` | Nombre del proyecto |
| `GET` | `/health` | Estado del servidor y conexion a BD |

## Convenciones

- Los endpoints marcados con `[auth required]` requieren `Authorization: Bearer <access_token>`.
- Los timestamps se devuelven en ISO 8601 sin zona horaria (UTC implicito del servidor).
- Los errores siguen el formato `{ "detail": "mensaje" }`.
- Swagger interactivo disponible en `/docs`.

## Configuracion de correo y validacion

Para habilitar envio real de codigos de verificacion:

- En `.env` define `EMAIL_ENABLED=true`.
- Configura `SMTP_HOST`, `SMTP_PORT`, `SMTP_FROM_EMAIL`.
- Si tu proveedor requiere autenticacion, define `SMTP_USERNAME` y `SMTP_PASSWORD`.
- Usa solo una opcion de seguridad: `SMTP_USE_TLS=true` o `SMTP_USE_SSL=true`.
- Ajusta `SMTP_TIMEOUT_SECONDS` segun tu entorno de red.

Variables disponibles de correo (segun `core/config.py`):

- `EMAIL_ENABLED`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_USE_TLS`
- `SMTP_USE_SSL`
- `SMTP_FROM_EMAIL`
- `SMTP_FROM_NAME`
- `SMTP_TIMEOUT_SECONDS`

Flujo de validacion de usuario:

- `POST /api/auth/register` crea usuario y envia codigo de verificacion.
- `POST /api/verification/confirm` valida el codigo y marca `is_verified=true`.
- `POST /api/auth/login` solo funciona cuando la cuenta ya fue verificada.

Comportamiento por entorno:

- Desarrollo: `DEBUG=true` y `EMAIL_ENABLED=false` permite probar devolviendo `verification_code` en respuestas de registro/solicitud.
- Produccion: `DEBUG=false` y `EMAIL_ENABLED=true` envia correo real y no expone `verification_code`.
- Si `EMAIL_ENABLED=true` y faltan datos SMTP requeridos, la app falla al iniciar por validacion de configuracion.

Prueba rapida recomendada:

1. Configura SMTP en `.env` y reinicia la API.
2. Ejecuta `POST /api/auth/register`.
3. Verifica que llegue el correo con codigo.
4. Ejecuta `POST /api/verification/confirm`.
5. Ejecuta `POST /api/auth/login` y confirma acceso exitoso.
