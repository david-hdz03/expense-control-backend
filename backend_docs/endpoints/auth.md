# Auth

Prefijo: `/api/auth`  
Tag: `auth`

---

## POST `/api/auth/register`

Crea un nuevo usuario y genera un codigo de verificacion de correo.

**Autenticacion:** ninguna

### Body

```json
{
  "name": "string (1-100)",
  "second_name": "string (opcional, default '')",
  "paternal_last_name": "string (requerido)",
  "maternal_last_name": "string (opcional, default '')",
  "email": "string",
  "password": "string (min 8 chars, requiere mayuscula, digito y simbolo)",
  "age": "integer (> 0)",
  "currency_code": "string (exactamente 3 chars, ej: 'USD')"
}
```

### Respuesta `201 Created`

```json
{
  "detail": "User registered. Verify your email before login",
  "requires_verification": true,
  "verification_expires_at": "2026-01-01T00:15:00",
  "verification_code": "123456"
}
```

`verification_code` solo se devuelve cuando `DEBUG=true`.
Si `DEBUG=false`, nunca se expone en la respuesta.

### Errores

| Codigo | Descripcion |
|---|---|
| `409 Conflict` | El email ya esta registrado |
| `503 Service Unavailable` | Usuario creado, pero no se pudo enviar el correo de verificacion (SMTP no disponible o mal configurado) |
| `422 Unprocessable Entity` | Validacion fallida (contrasena debil, edad invalida, etc.) |

---

## POST `/api/auth/login`

Autentica a un usuario con email y contrasena.

**Autenticacion:** ninguna

### Body

```json
{
  "email": "string",
  "password": "string"
}
```

### Respuesta `200 OK`

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Errores

| Codigo | Descripcion |
|---|---|
| `401 Unauthorized` | Credenciales invalidas |
| `403 Forbidden` | Cuenta no verificada |

---

## POST `/api/auth/refresh`

Genera nuevos tokens a partir de un refresh token valido.

**Autenticacion:** ninguna (el refresh token va en el body)

### Body

```json
{
  "refresh_token": "string"
}
```

### Respuesta `200 OK`

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Errores

| Codigo | Descripcion |
|---|---|
| `401 Unauthorized` | Token expirado, invalido o usuario inactivo |
| `403 Forbidden` | Cuenta no verificada |

---

## GET `/api/auth/me` [auth required]

Devuelve el perfil del usuario autenticado.

**Autenticacion:** Bearer token requerido

### Respuesta `200 OK`

```json
{
  "id": 1,
  "name": "string",
  "email": "string",
  "is_verified": true,
  "is_active": true,
  "currency_code": "USD",
  "created_at": "2026-01-01T00:00:00"
}
```

### Errores

| Codigo | Descripcion |
|---|---|
| `401 Unauthorized` | Token ausente, expirado o invalido |
| `403 Forbidden` | Cuenta no verificada |

---

## POST `/api/auth/token` *(solo Swagger)*

Endpoint OAuth2 en formato `application/x-www-form-urlencoded`. Usado internamente por la interfaz `/docs` para el flujo de autenticacion interactiva. No esta documentado en el schema publico (`include_in_schema=False`).

| Campo form | Tipo | Descripcion |
|---|---|---|
| `username` | string | Email del usuario |
| `password` | string | Contrasena |
