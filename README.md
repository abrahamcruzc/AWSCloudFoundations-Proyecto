# API REST Alumnos y Profesores

API REST desarrollada con Flask para gestionar alumnos y profesores usando almacenamiento en memoria (listas).

## Requisitos
- Python 3.8 o superior
- Pip 20+

## Instalación y ejecución local
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

El servicio quedará expuesto en `http://0.0.0.0:3000` con los 10 endpoints solicitados, además de `GET /` y `GET /health`.

## Referencia rápida de endpoints

### Alumnos
| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/alumnos` | Lista todos los alumnos |
| GET | `/alumnos/<id>` | Obtiene un alumno por ID |
| POST | `/alumnos` | Crea un alumno (campos: `nombres`, `apellidos`, `matricula`, `promedio`) |
| PUT | `/alumnos/<id>` | Actualiza completamente un alumno existente |
| DELETE | `/alumnos/<id>` | Elimina un alumno |

Validaciones: strings no vacíos; `promedio` número entre 0 y 100.

### Profesores
| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/profesores` | Lista todos los profesores |
| GET | `/profesores/<id>` | Obtiene un profesor por ID |
| POST | `/profesores` | Crea un profesor (campos: `numeroEmpleado`, `nombres`, `apellidos`, `horasClase`) |
| PUT | `/profesores/<id>` | Actualiza completamente un profesor existente |
| DELETE | `/profesores/<id>` | Elimina un profesor |

Validaciones: strings no vacíos; `horasClase` entero positivo.

Todas las respuestas son JSON, se utilizan los códigos HTTP 200/201/400/404/500 según corresponda y los IDs se auto-generan en cada colección.

## Pruebas manuales con `curl`

```bash
# Crear un alumno
curl -X POST http://localhost:3000/alumnos \
	-H "Content-Type: application/json" \
	-d '{"nombres":"Juan","apellidos":"Pérez","matricula":"A001","promedio":85.5}'

# Consultar alumnos
curl http://localhost:3000/alumnos

# Crear un profesor
curl -X POST http://localhost:3000/profesores \
	-H "Content-Type: application/json" \
	-d '{"numeroEmpleado":"P100","nombres":"Ana","apellidos":"López","horasClase":10}'

# Consultar profesores
curl http://localhost:3000/profesores
```


