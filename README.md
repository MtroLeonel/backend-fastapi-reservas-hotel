# First Project - FastAPI Hotel API

Proyecto backend construido con FastAPI para exponer una API REST de gestion hotelera con tres modulos funcionales: hoteles, habitaciones y reservas.

## Estado actual

Actualmente el proyecto implementa:

- API REST con FastAPI.
- CRUD completo para `hotels`, `rooms` y `bookings`.
- Persistencia con SQLAlchemy sobre PostgreSQL.
- Migraciones versionadas con Alembic.
- Configuracion por variables de entorno.
- Ejecucion local con Docker y Docker Compose.
- Manejo centralizado de errores de dominio.

## Stack

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Alembic
- python-dotenv
- Docker / Docker Compose

## Estructura principal

```text
app/
	main.py                # Punto de entrada de FastAPI
	database.py            # Motor, sesion y base declarativa
	errors.py              # Excepciones personalizadas de la API
	hotels/
		models.py            # Modelo SQLAlchemy de hoteles
		schemas.py           # Esquemas Pydantic de hoteles
		routes.py            # Endpoints CRUD de hoteles
	rooms/
		models.py            # Modelo SQLAlchemy de habitaciones
		schemas.py           # Esquemas Pydantic de habitaciones
		routes.py            # Endpoints CRUD de habitaciones
	bookings/
		models.py            # Modelo SQLAlchemy de reservas
		schemas.py           # Esquemas Pydantic de reservas
		routes.py            # Endpoints CRUD de reservas
alembic/
	versions/
		f853a3f688a5_initial_tables_creation.py
		ebad12904087_create_rooms_table.py
		7a560d25d820_create_bookings_table.py
docs/
	arquiteture.md
	proyecto-actual.md
Dockerfile
docker-compose.yml
requirements.txt
```

## Endpoints disponibles

La aplicacion registra los routers bajo el prefijo `/api/v1`:

- `GET /` estado basico de la aplicacion.

Hoteles:
- `POST /api/v1/hotels/`
- `GET /api/v1/hotels/`
- `GET /api/v1/hotels/{hotel_id}`
- `PUT /api/v1/hotels/{hotel_id}`
- `PATCH /api/v1/hotels/{hotel_id}`
- `DELETE /api/v1/hotels/{hotel_id}`

Habitaciones:
- `POST /api/v1/rooms/`
- `GET /api/v1/rooms/`
- `GET /api/v1/rooms/{room_id}`
- `PUT /api/v1/rooms/{room_id}`
- `PATCH /api/v1/rooms/{room_id}`
- `DELETE /api/v1/rooms/{room_id}`

Reservas:
- `POST /api/v1/bookings/`
- `GET /api/v1/bookings/`
- `GET /api/v1/bookings/{booking_id}`
- `PUT /api/v1/bookings/{booking_id}`
- `PATCH /api/v1/bookings/{booking_id}`
- `DELETE /api/v1/bookings/{booking_id}`

## Reglas de negocio implementadas

Hoteles:
- El nombre del hotel debe ser unico.
- `name` y `city` no pueden estar vacios.

Habitaciones:
- `number` y `room_type` no pueden estar vacios.
- `capacity` debe ser mayor que 0.
- `price` no puede ser negativo.
- No se permiten numeros de habitacion duplicados dentro del mismo hotel.

Reservas:
- Se genera `booking_code` unico automaticamente.
- Estados permitidos: `confirmed`, `checked_in`, `checked_out`, `cancelled`, `no_show`.
- No se permiten solapamientos de fechas en la misma habitacion para reservas activas.
- `total_price` se calcula automaticamente con esta formula:
  - `noches = (check_out - check_in).days`
  - `total_price = noches * room.price`

## Configuracion

Variables de entorno usadas en el proyecto:

- `DATABASE_URL`
- `APP_ENV`
- `APP_TITLE`
- `DEBUG`
- `ENABLE_DOCS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Ejecucion con Docker Compose

```bash
docker compose up --build
```

La API queda expuesta en `http://localhost:8000` y PostgreSQL en `localhost:5432`.

## Documentacion interactiva

Si `ENABLE_DOCS` esta habilitado, FastAPI expone:

- `/docs`
- `/redoc`
- `/openapi.json`

## Documento tecnico

Para una descripcion tecnica detallada del estado actual, revisar `docs/proyecto-actual.md`.
