reservas-hotel/
├── app/
│   ├── __init__.py
│   ├── database.py       # Conexión a la base de datos
│   ├── main.py           # Archivo central de la API
│   │
│   ├── hotels/           # Módulo de Hoteles
│   │   ├── __init__.py
│   │   ├── models.py     # Tabla Hotel (SQLAlchemy)
│   │   ├── schemas.py    # Validación Pydantic para Hoteles
│   │   └── routes.py     # Endpoints de Hoteles
│   │
│   ├── rooms/            # Módulo de Habitaciones
│   │   ├── __init__.py
│   │   ├── models.py     # Tabla Habitacion
│   │   ├── schemas.py    # Validación Pydantic para Habitaciones
│   │   └── routes.py     # Endpoints de Habitaciones
│   │
│   └── bookings/         # Módulo de Reservas
│       ├── __init__.py
│       ├── models.py     # Tabla Reserva
│       ├── schemas.py    # Validación Pydantic para Reservas
│       └── routes.py     # Endpoints de Reservas

Notas actuales del modulo bookings:

- `booking_code` se genera automaticamente en backend y es unico.
- `status` se almacena como string (sin ENUM en base de datos) con valores permitidos:
	- `confirmed`
	- `checked_in`
	- `checked_out`
	- `cancelled`
	- `no_show`
- `total_price` se calcula automaticamente desde backend:
	- `noches = (check_out - check_in).days`
	- `total_price = noches * room.price`
- Se evita solapamiento de reservas activas para la misma habitacion en el rango de fechas.

Cadena de migraciones actual:

- `f853a3f688a5_initial_tables_creation.py` -> `hotels`
- `ebad12904087_create_rooms_table.py` -> `rooms`
- `7a560d25d820_create_bookings_table.py` -> `bookings`

