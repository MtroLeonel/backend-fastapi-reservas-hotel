# First Project - FastAPI Hotel API

Proyecto backend construido con FastAPI para exponer una API REST enfocada, por ahora, en la gestion de hoteles. El estado actual del repositorio cubre una primera base funcional con persistencia en PostgreSQL, migraciones con Alembic y ejecucion con Docker Compose.

## Estado actual

Actualmente el proyecto implementa:

- API REST con FastAPI.
- CRUD completo del recurso `hotels`.
- Persistencia con SQLAlchemy.
- Base de datos PostgreSQL.
- Migracion inicial con Alembic.
- Configuracion por variables de entorno.
- Ejecucion local con Docker y Docker Compose.
- Manejo centralizado de errores de dominio para la API.

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
		schemas.py           # Esquemas Pydantic
		routes.py            # Endpoints CRUD de hoteles
alembic/
	versions/
		f853a3f688a5_initial_tables_creation.py
docs/
	arquiteture.md         # No refleja el alcance actual
Dockerfile
docker-compose.yml
requirements.txt
```

## Endpoints disponibles

La aplicacion registra el modulo de hoteles bajo el prefijo ` /api/v1 `, por lo que hoy estan disponibles estas rutas:

- `GET /` estado basico de la aplicacion.
- `POST /api/v1/hotels/` crear hotel.
- `GET /api/v1/hotels/` listar hoteles.
- `GET /api/v1/hotels/{hotel_id}` obtener hotel por id.
- `PUT /api/v1/hotels/{hotel_id}` reemplazar un hotel.
- `PATCH /api/v1/hotels/{hotel_id}` actualizar parcialmente un hotel.
- `DELETE /api/v1/hotels/{hotel_id}` eliminar un hotel.

El listado de hoteles permite filtrar por ciudad mediante el query parameter `city`.

## Reglas implementadas hoy

- El nombre del hotel debe ser unico.
- `name` y `city` no pueden ser cadenas vacias.
- Si un hotel no existe, la API responde con error controlado.
- Los errores de dominio usan una respuesta JSON consistente.

## Configuracion

El proyecto utiliza variables de entorno. Entre las que el codigo espera o soporta se encuentran:

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

- ` /docs `
- ` /redoc `
- ` /openapi.json `

## Alcance actual

Este repositorio aun no implementa otros modulos de negocio fuera de hoteles. La base actual sirve como punto de partida para crecer hacia nuevos recursos y procesos, pero la documentacion de este README describe unicamente lo que existe hoy en codigo.

## Documento tecnico

Para una descripcion mas tecnica del proyecto y de sus componentes actuales, revisar `docs/proyecto-actual.md`.
