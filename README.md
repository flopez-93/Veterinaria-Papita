# Papita Veterinaria

Sistema web de gestión de turnos para una veterinaria, desarrollado como Trabajo Práctico Integrador de Ingeniería de Software.

## Tecnologías utilizadas

* Python
* FastAPI
* SQLite
* SQLAlchemy
* HTML
* CSS
* JavaScript

## Funcionalidades principales

* Registro e inicio de sesión de usuarios
* Gestión de mascotas
* Reserva y gestión de turnos
* Consulta de disponibilidad horaria
* Registro de historial médico
* Calificación de atención
* Paneles según rol: cliente, veterinario y administrativo
* Exportación de datos en CSV

## Estructura del proyecto

* `main.py`: define los endpoints principales de la API.
* `models.py`: contiene las tablas y relaciones de la base de datos.
* `schemas.py`: define los modelos de entrada y salida.
* `crud.py`: contiene la lógica de consulta, alta, modificación y baja.
* `database.py`: configura la conexión con SQLite.
* `seed.py`: carga datos iniciales para la demo.
* `papita_veterinaria_front_conectado_api.html`: frontend del sistema.

## Cómo ejecutar el proyecto

1. Crear un entorno virtual:

```bash
python -m venv venv
```

2. Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install fastapi uvicorn sqlalchemy pydantic email-validator
```

4. Cargar datos iniciales:

```bash
python seed.py
```

5. Levantar la API:

```bash
python -m uvicorn main:app --reload
```

6. Abrir el frontend en el navegador:

```text
papita_veterinaria_front_conectado_api.html
```

## Documentación de la API

Una vez levantado el backend, la documentación automática de FastAPI se puede consultar en:

```text
http://127.0.0.1:8000/docs
```

## Usuarios de prueba

Cliente:

```text
Email: maria@mail.com
Contraseña: 123
```

Veterinario:

```text
Email: carlos@vet.com
Contraseña: 123
```

Administrativo:

```text
Email: laura@mail.com
Contraseña: 123
```

## Integrantes

* Lucas Martínez
* Magali Rodríguez
* Melina Gramajo
* Juan Díaz
* Franco López

