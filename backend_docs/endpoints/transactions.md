# Transactions

Prefijo: `/api/transactions`  
Tag: `transactions`

Todos los endpoints de transacciones (excepto `/types`) requieren autenticación. Cada usuario solo puede ver y modificar sus propias transacciones.

---

## GET `/api/transactions/types`

Lista los tipos de transacción disponibles (ej: ingreso, gasto).

**Autenticación:** ninguna

### Respuesta `200 OK`

```json
[
  { "id": 1, "name": "ingreso" },
  { "id": 2, "name": "gasto" }
]
```

---

## GET `/api/transactions` 🔒

Lista las transacciones del usuario autenticado con filtros opcionales.

**Autenticación:** Bearer token requerido

### Query params

| Parámetro | Tipo | Requerido | Descripción |
|---|---|---|---|
| `transaction_type_id` | integer | no | Filtra por tipo de transacción |
| `category_id` | integer | no | Filtra por categoría |

### Respuesta `200 OK`

```json
[
  {
    "id": 1,
    "amount": 5000,
    "transaction_type": { "id": 1, "name": "ingreso" },
    "category": { "id": 3, "name": "Salario" },
    "user_id": 7,
    "created_at": "2026-04-25T00:00:00",
    "updated_at": "2026-04-25T00:00:00"
  }
]
```

> `category` puede ser `null` si la transacción no tiene categoría asignada.  
> `amount` se almacena como entero (centavos o unidad entera según la moneda del usuario).

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |

---

## POST `/api/transactions` 🔒

Crea una nueva transacción para el usuario autenticado.

**Autenticación:** Bearer token requerido

### Body

```json
{
  "amount": 5000,
  "transaction_type_id": 1,
  "category_id": 3
}
```

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `amount` | integer | sí | Monto de la transacción |
| `transaction_type_id` | integer | sí | ID del tipo de transacción |
| `category_id` | integer | no | ID de la categoría (puede ser `null`) |

### Respuesta `201 Created`

```json
{
  "id": 1,
  "amount": 5000,
  "transaction_type": { "id": 1, "name": "ingreso" },
  "category": { "id": 3, "name": "Salario" },
  "user_id": 7,
  "created_at": "2026-04-25T00:00:00",
  "updated_at": "2026-04-25T00:00:00"
}
```

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `422 Unprocessable Entity` | Validación del body fallida |

---

## GET `/api/transactions/{tx_id}` 🔒

Obtiene una transacción por ID. Solo devuelve transacciones del usuario autenticado.

**Autenticación:** Bearer token requerido

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tx_id` | integer | ID de la transacción |

### Respuesta `200 OK`

```json
{
  "id": 1,
  "amount": 5000,
  "transaction_type": { "id": 1, "name": "ingreso" },
  "category": { "id": 3, "name": "Salario" },
  "user_id": 7,
  "created_at": "2026-04-25T00:00:00",
  "updated_at": "2026-04-25T00:00:00"
}
```

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `404 Not Found` | Transacción no encontrada o pertenece a otro usuario |

---

## PATCH `/api/transactions/{tx_id}` 🔒

Actualiza parcialmente una transacción. Solo se envían los campos a modificar.

**Autenticación:** Bearer token requerido

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tx_id` | integer | ID de la transacción |

### Body (todos los campos son opcionales)

```json
{
  "amount": 6000,
  "transaction_type_id": 2,
  "category_id": 4
}
```

### Respuesta `200 OK`

Transacción actualizada con el mismo formato que `GET /{tx_id}`.

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `404 Not Found` | Transacción no encontrada o pertenece a otro usuario |
| `422 Unprocessable Entity` | Validación del body fallida |

---

## DELETE `/api/transactions/{tx_id}` 🔒

Elimina una transacción. Solo puede eliminar transacciones propias.

**Autenticación:** Bearer token requerido

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tx_id` | integer | ID de la transacción |

### Respuesta `204 No Content`

Sin body.

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `404 Not Found` | Transacción no encontrada o pertenece a otro usuario |
