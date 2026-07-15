# Proyecto Actual - Descripcion Tecnica

## Objetivo actual

El repositorio implementa una API backend para gestion hotelera con tres modulos funcionales activos:

- `hotels`
- `rooms`
- `bookings`

El documento describe exclusivamente lo implementado hoy en codigo.

## Resumen tecnico

- Framework HTTP: FastAPI.
- Servidor ASGI: Uvicorn.
- ORM: SQLAlchemy.
- Base de datos: PostgreSQL.
- Migraciones: Alembic.
- Configuracion: variables de entorno con `python-dotenv`.
- Contenerizacion: Docker y Docker Compose.

## Componentes actuales

### 1. Punto de entrada de la aplicacion

`app/main.py` centraliza:

- carga de variables de entorno,
- configuracion dinamica de `title`, `debug` y documentacion OpenAPI,
- registro del manejador global de excepciones,
- inclusion de routers bajo el prefijo `/api/v1` para hoteles, habitaciones y reservas,
- endpoint raiz de verificacion basica.

### 2. Capa de acceso a datos

`app/database.py` define:

- `engine` usando `DATABASE_URL`,
- `SessionLocal` para sesiones transaccionales,
- `Base` como clase declarativa,
- `get_db()` como dependencia por request.

### 3. Manejo de errores

`app/errors.py` implementa:

- `HotelAPIException`
- `ResourceNotFoundException`
- `DuplicateHotelException`
- `BadRequestException`

El handler global responde en formato JSON consistente:

```json
{
  "success": false,
  "error": "mensaje"
}
```

### 4. Modulo hotels

`app/hotels/` contiene CRUD completo de hoteles.

Modelo `Hotel`:

- `id` (PK)
- `name` (unico, indexado)
- `city` (indexado)

Rutas activas:

- `POST /api/v1/hotels/`
- `GET /api/v1/hotels/`
- `GET /api/v1/hotels/{hotel_id}`
- `PUT /api/v1/hotels/{hotel_id}`
- `PATCH /api/v1/hotels/{hotel_id}`
- `DELETE /api/v1/hotels/{hotel_id}`

### 5. Modulo rooms

`app/rooms/` contiene CRUD completo de habitaciones.

Modelo `Room`:

- `id` (PK)
- `number`
- `room_type`
- `capacity`
- `price`
- `is_available`
- `hotel_id` (FK a `hotels.id`, `ondelete=CASCADE`)

Rutas activas:

- `POST /api/v1/rooms/`
- `GET /api/v1/rooms/`
- `GET /api/v1/rooms/{room_id}`
- `PUT /api/v1/rooms/{room_id}`
- `PATCH /api/v1/rooms/{room_id}`
- `DELETE /api/v1/rooms/{room_id}`

### 6. Modulo bookings

`app/bookings/` contiene CRUD completo de reservas.

Modelo `Booking`:

- `id` (PK)
- `booking_code` (unico, indexado)
- `guest_name`
- `guest_email` (indexado)
- `check_in` (Date)
- `check_out` (Date)
- `total_price` (calculado por backend)
- `status` (String con valores permitidos por validacion de aplicacion)
- `room_id` (FK a `rooms.id`, `ondelete=CASCADE`)

Estados permitidos para reservas:

- `confirmed`
- `checked_in`
- `checked_out`
- `cancelled`
- `no_show`

Rutas activas:

- `POST /api/v1/bookings/`
- `GET /api/v1/bookings/`
- `GET /api/v1/bookings/{booking_id}`
- `PUT /api/v1/bookings/{booking_id}`
- `PATCH /api/v1/bookings/{booking_id}`
- `DELETE /api/v1/bookings/{booking_id}`

## Reglas de negocio implementadas

Hoteles:

- nombre unico,
- `name` y `city` obligatorios,
- filtro por ciudad en listado.

Habitaciones:

- `number` y `room_type` obligatorios,
- `capacity > 0`,
- `price >= 0`,
- no se repite `number` dentro del mismo hotel.

Reservas:

- `booking_code` se genera automaticamente,
- no hay solapamiento de fechas en la misma habitacion para reservas activas,
- `status` restringido por validacion de aplicacion a 5 valores,
- `total_price` se calcula automaticamente con:
  - `noches = (check_out - check_in).days`
  - `total_price = noches * room.price`

## Persistencia y migraciones

Versiones de esquema registradas:

- `f853a3f688a5_initial_tables_creation.py` crea `hotels`.
- `ebad12904087_create_rooms_table.py` crea `rooms` y FK a `hotels`.
- `7a560d25d820_create_bookings_table.py` crea `bookings` y FK a `rooms`.

## Ejecucion en contenedores

`Dockerfile`:

- base `python:3.11-slim`,
- instala dependencias,
- copia codigo,
- ejecuta Uvicorn en `8000`.

`docker-compose.yml`:

- servicio `web` (FastAPI),
- servicio `db` (PostgreSQL 15 Alpine),
- puertos `8000` y `5432`,
- carga variables desde `.env`,
- modo desarrollo con `--reload`.

## Variables de entorno observadas en el codigo

- `DATABASE_URL`
- `APP_ENV`
- `APP_TITLE`
- `DEBUG`
- `ENABLE_DOCS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Alcance actual

El proyecto ya cubre el flujo principal de inventario y reserva (hotel -> habitacion -> reserva) con reglas de negocio base. Aun no incorpora autenticacion, pruebas automatizadas ni pipeline CI/CD.