# Proyecto Actual - Descripcion Tecnica

## Objetivo actual

El repositorio implementa una API backend inicial para administrar hoteles. En este momento el dominio funcional real se limita al modulo `hotels`, con operaciones CRUD, validaciones basicas de negocio, persistencia relacional y soporte de migraciones.

No se documenta aqui una arquitectura futura ideal ni modulos planeados. Este documento refleja exclusivamente lo que existe hoy en el codigo.

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

El archivo `app/main.py` crea la instancia principal de FastAPI y centraliza estas responsabilidades:

- Carga de variables de entorno.
- Configuracion dinamica de `title`, `debug` y exposicion de documentacion OpenAPI.
- Registro del manejador global para excepciones de dominio.
- Inclusion del router de hoteles bajo el prefijo `/api/v1`.
- Definicion de un endpoint raiz de verificacion basica.

### 2. Capa de acceso a datos

El archivo `app/database.py` define:

- `engine` de SQLAlchemy usando `DATABASE_URL`.
- `SessionLocal` para crear sesiones transaccionales.
- `Base` como clase declarativa para los modelos.
- `get_db()` como dependencia de FastAPI para abrir y cerrar sesiones por request.

El proyecto depende de que `DATABASE_URL` exista y apunte a PostgreSQL.

### 3. Manejo de errores

El archivo `app/errors.py` implementa una jerarquia de excepciones propia:

- `HotelAPIException`
- `ResourceNotFoundException`
- `DuplicateHotelException`
- `BadRequestException`

Estas excepciones son capturadas por un exception handler global que devuelve respuestas JSON con esta estructura:

```json
{
  "success": false,
  "error": "mensaje"
}
```

Esto permite desacoplar la logica del dominio de la construccion manual de respuestas HTTP en cada endpoint.

### 4. Modulo hotels

El modulo `app/hotels/` contiene la implementacion funcional principal del sistema.

#### Modelo

`models.py` define la entidad `Hotel` con la tabla `hotels`:

- `id`: entero, clave primaria.
- `name`: string, unico e indexado.
- `city`: string, indexado.

#### Esquemas

`schemas.py` define los contratos de entrada y salida:

- `HotelBase`
- `HotelCreate`
- `HotelUpdate`
- `HotelResponse`

`HotelResponse` habilita `from_attributes`, por lo que puede serializar instancias ORM directamente.

#### Rutas y comportamiento

`routes.py` define un `APIRouter` con prefijo `/hotels` y etiqueta `Hotels`. Al incluirse desde `main.py` bajo `/api/v1`, la superficie HTTP efectiva es:

- `POST /api/v1/hotels/`
- `GET /api/v1/hotels/`
- `GET /api/v1/hotels/{hotel_id}`
- `PUT /api/v1/hotels/{hotel_id}`
- `PATCH /api/v1/hotels/{hotel_id}`
- `DELETE /api/v1/hotels/{hotel_id}`

La implementacion actual incluye funciones auxiliares privadas para:

- buscar hoteles por id,
- validar unicidad del nombre,
- validar strings vacios o con espacios.

## Reglas de negocio implementadas

Las reglas activas hoy son estas:

- un hotel debe tener `name` y `city` con contenido util,
- el nombre del hotel no puede repetirse,
- las actualizaciones parciales solo modifican los campos enviados,
- las busquedas por id responden con error de dominio si el registro no existe,
- el listado puede filtrarse por ciudad usando coincidencia `ILIKE`.

## Persistencia y migraciones

El proyecto ya cuenta con una migracion inicial en Alembic:

- crea la tabla `hotels`,
- crea indices para `id`, `city` y `name`,
- marca `name` como unico.

Esto indica que el esquema ya se encuentra versionado desde el inicio del proyecto, aunque por ahora solo cubre una entidad.

## Ejecucion en contenedores

### Dockerfile

El `Dockerfile` actual:

- parte de `python:3.11-slim`,
- instala dependencias desde `requirements.txt`,
- copia la carpeta `app/`,
- arranca Uvicorn en el puerto `8000`.

### docker-compose.yml

El archivo de Compose levanta dos servicios:

- `web`: aplicacion FastAPI.
- `db`: PostgreSQL 15 Alpine.

Tambien:

- publica el puerto `8000` para la API,
- publica el puerto `5432` para PostgreSQL,
- monta el repositorio dentro del contenedor `web`,
- inyecta variables desde `.env`,
- usa `--reload` para desarrollo.

## Variables de entorno observadas en el codigo

Las variables referenciadas directamente por el proyecto son:

- `DATABASE_URL`
- `APP_ENV`
- `APP_TITLE`
- `DEBUG`
- `ENABLE_DOCS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Alcance real del repositorio hoy

Actualmente el proyecto contiene una base tecnica valida para crecer, pero el alcance funcional implementado sigue siendo acotado. No se observan aun:

- autenticacion o autorizacion,
- pruebas automatizadas,
- separacion por capas de servicio o repositorio,
- multiples modulos de negocio,
- observabilidad avanzada,
- pipeline CI/CD,
- versionado adicional de la API mas alla del prefijo actual,
- modelos relacionales adicionales como habitaciones, reservas o usuarios.

## Valor de esta base actual

Aunque el alcance es pequeno, la base ya incorpora varios elementos utiles para escalar:

- estructura modular inicial,
- convenciones CRUD consistentes,
- manejo centralizado de errores,
- migraciones desde etapas tempranas,
- contenedorizacion para entorno local,
- configuracion desacoplada por entorno.

## Conclusion

Hoy el proyecto es una API inicial de gestion de hoteles, no una plataforma hotelera completa. Su contenido actual es suficiente para servir como base de aprendizaje, evolucion tecnica incremental y futura incorporacion de nuevos modulos, pero la documentacion debe entenderse en ese alcance acotado.