# API REST Alumnos y Profesores

API REST con Flask para gestionar alumnos y profesores.

## Referencia rápida de endpoints

### Alumnos
| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/alumnos` | Lista todos los alumnos |
| GET | `/alumnos/<id>` | Obtiene un alumno por ID |
| POST | `/alumnos` | Crea un alumno (campos: `nombres`, `apellidos`, `matricula`, `promedio`) |
| PUT | `/alumnos/<id>` | Actualiza completamente un alumno existente |
| DELETE | `/alumnos/<id>` | Elimina un alumno |


### Profesores
| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/profesores` | Lista todos los profesores |
| GET | `/profesores/<id>` | Obtiene un profesor por ID |
| POST | `/profesores` | Crea un profesor (campos: `numeroEmpleado`, `nombres`, `apellidos`, `horasClase`) |
| PUT | `/profesores/<id>` | Actualiza completamente un profesor existente |
| DELETE | `/profesores/<id>` | Elimina un profesor |






