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

