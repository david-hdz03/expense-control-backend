# Categories

Prefijo: `/api/categories`  
Tag: `categories`

Las categorías tienen dos orígenes:

- **Predeterminadas** (`is_default: true`): creadas por el sistema al iniciar (`created_by = null`). Visibles para todos los usuarios. No se pueden editar ni eliminar por el usuario.
- **Personalizadas** (`is_default: false`): creadas por el usuario. Solo visibles y editables por quien las creó.

Categorías predeterminadas iniciales: `Comida`, `Salud`, `Transporte`, `Streaming`, `Entretenimiento`, `Educación`, `Hogar`, `Salario`, `Freelance`, `Inversiones`.

---

## GET `/api/categories` 🔒

Lista todas las categorías visibles para el usuario: las predeterminadas más las propias. Las predeterminadas aparecen primero, el resto ordenado por nombre.

**Autenticación:** Bearer token requerido

### Respuesta `200 OK`

```json
[
  {
    "id": 1,
    "name": "Comida",
    "is_default": true,
    "created_at": "2026-04-25T00:00:00"
  },
  {
    "id": 11,
    "name": "Gimnasio",
    "is_default": false,
    "created_at": "2026-04-25T12:00:00"
  }
]
```

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |

---

## POST `/api/categories` 🔒

Crea una categoría personalizada para el usuario autenticado.

**Autenticación:** Bearer token requerido

### Body

```json
{
  "name": "string (1–100 chars)"
}
```

### Respuesta `201 Created`

```json
{
  "id": 11,
  "name": "Gimnasio",
  "is_default": false,
  "created_at": "2026-04-25T12:00:00"
}
```

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `409 Conflict` | Ya existe una categoría con ese nombre (predeterminada o propia, insensible a mayúsculas) |
| `422 Unprocessable Entity` | Nombre vacío o mayor a 100 chars |

---

## PATCH `/api/categories/{category_id}` 🔒

Actualiza el nombre de una categoría personalizada propia.

**Autenticación:** Bearer token requerido

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `category_id` | integer | ID de la categoría |

### Body

```json
{
  "name": "string (1–100 chars)"
}
```

### Respuesta `200 OK`

```json
{
  "id": 11,
  "name": "Gym",
  "is_default": false,
  "created_at": "2026-04-25T12:00:00"
}
```

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `404 Not Found` | Categoría no encontrada o no pertenece al usuario (incluye predeterminadas) |
| `409 Conflict` | Nombre en conflicto con otra categoría visible del usuario |
| `422 Unprocessable Entity` | Nombre vacío o mayor a 100 chars |

---

## DELETE `/api/categories/{category_id}` 🔒

Elimina una categoría personalizada propia.

**Autenticación:** Bearer token requerido

### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `category_id` | integer | ID de la categoría |

### Respuesta `204 No Content`

Sin body.

### Errores

| Código | Descripción |
|---|---|
| `401 Unauthorized` | Token ausente o inválido |
| `404 Not Found` | Categoría no encontrada o no pertenece al usuario (incluye predeterminadas) |
