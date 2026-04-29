# Users

Prefijo: `/api/users`  
Tag: `users`

> Estos endpoints no requieren autenticación. Fueron diseñados para el flujo de administración inicial. Para el registro de usuarios en el flujo normal, usar [`/api/auth/register`](auth.md).

---

## POST `/api/users/`

Crea un usuario directamente, sin devolver tokens.

**Autenticación:** ninguna

### Body

```json
{
  "name": "string",
  "second_name": "string (opcional, default '')",
  "paternal_last_name": "string",
  "maternal_last_name": "string (opcional, default '')",
  "email": "string",
  "password": "string",
  "age": "integer",
  "currency_code": "string (3 chars)",
  "user_type_id": "integer (opcional, default 2 = regular)"
}
```

### Respuesta `200 OK`

```json
{
  "id": 1,
  "name": "string",
  "second_name": "string",
  "paternal_last_name": "string",
  "maternal_last_name": "string",
  "email": "string",
  "age": 25,
  "currency_code": "USD",
  "user_type_id": 2
}
```

### Errores

| Código | Descripción |
|---|---|
| `400 Bad Request` | El usuario no pudo crearse |
| `422 Unprocessable Entity` | Validación del body fallida |

---

## GET `/api/users/{user_id}`

Obtiene un usuario por su ID.

**Autenticación:** ninguna

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `user_id` | integer | ID del usuario |

### Respuesta `200 OK`

```json
{
  "id": 1,
  "name": "string",
  "second_name": "string",
  "paternal_last_name": "string",
  "maternal_last_name": "string",
  "email": "string",
  "age": 25,
  "currency_code": "USD",
  "user_type_id": 2
}
```

### Errores

| Código | Descripción |
|---|---|
| `404 Not Found` | Usuario no encontrado |
