# Verification

Prefijo: `/api/verification`  
Tag: `verification`

---

## POST `/api/verification/request`

Genera o reenvia un codigo de verificacion para una cuenta no verificada.

**Autenticacion:** ninguna

### Body

```json
{
  "email": "string"
}
```

### Respuesta `200 OK`

```json
{
  "detail": "Verification code generated",
  "expires_at": "2026-01-01T00:15:00",
  "verification_code": "123456"
}
```

`verification_code` solo se devuelve cuando `DEBUG=true`.
Si `DEBUG=false`, nunca se expone en la respuesta.

### Errores

| Codigo | Descripcion |
|---|---|
| `404 Not Found` | Usuario no encontrado |
| `409 Conflict` | Cuenta ya verificada |
| `503 Service Unavailable` | Codigo generado, pero no se pudo enviar correo (SMTP no disponible o mal configurado) |

---

## POST `/api/verification/confirm`

Confirma el codigo y marca la cuenta como verificada.

**Autenticacion:** ninguna

### Body

```json
{
  "email": "string",
  "code": "123456"
}
```

### Respuesta `200 OK`

```json
{
  "detail": "Email verified successfully",
  "verified": true
}
```

### Errores

| Codigo | Descripcion |
|---|---|
| `400 Bad Request` | Codigo invalido |
| `404 Not Found` | Usuario o codigo activo no encontrado |
| `410 Gone` | Codigo expirado |
