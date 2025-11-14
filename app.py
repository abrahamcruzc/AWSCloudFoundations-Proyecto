from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

alumnos = []
profesores = []


def generar_id(items):
    """Obtiene el siguiente ID incremental para la colección indicada."""
    return (max((item["id"] for item in items), default=0) + 1)


def buscar_por_id(items, entity_id):
    """Devuelve el elemento cuyo id coincida o None si no existe."""
    return next((item for item in items if item["id"] == entity_id), None)


def validar_alumno(data, requiere_id=False):
    requeridos = ["nombres", "apellidos", "matricula", "promedio"]
    if requiere_id:
        requeridos.append("id")

    for campo in requeridos:
        if campo not in data:
            return False, f"Campo '{campo}' es requerido"

    # Validar ID si se requiere
    if requiere_id:
        if not isinstance(data["id"], int) or data["id"] <= 0:
            return False, "El campo 'id' debe ser un entero positivo"

    try:
        promedio = float(data["promedio"])
    except (TypeError, ValueError):
        return False, "El campo 'promedio' debe ser un número"

    if promedio < 0 or promedio > 100:
        return False, "El promedio debe estar entre 0 y 100"

    if not isinstance(data["nombres"], str) or not data["nombres"].strip():
        return False, "Campo 'nombres' debe ser string no vacío"

    if not isinstance(data["apellidos"], str) or not data["apellidos"].strip():
        return False, "Campo 'apellidos' debe ser string no vacío"

    if not isinstance(data["matricula"], str) or not data["matricula"].strip():
        return False, "Campo 'matricula' debe ser string no vacío"

    alumno_validado = {
        "nombres": data["nombres"].strip(),
        "apellidos": data["apellidos"].strip(),
        "matricula": data["matricula"].strip(),
        "promedio": promedio,
    }

    if requiere_id:
        alumno_validado["id"] = data["id"]

    return True, alumno_validado


def validar_profesor(data, requiere_id=False):
    requeridos = ["numeroEmpleado", "nombres", "apellidos", "horasClase"]
    if requiere_id:
        requeridos.append("id")

    for campo in requeridos:
        if campo not in data:
            return False, f"Campo '{campo}' es requerido"

    # Validar ID si se requiere
    if requiere_id:
        if not isinstance(data["id"], int) or data["id"] <= 0:
            return False, "El campo 'id' debe ser un entero positivo"

    # Validar numeroEmpleado (puede ser int o string)
    try:
        numero_empleado = int(data["numeroEmpleado"])
        if numero_empleado <= 0:
            return False, "El campo 'numeroEmpleado' debe ser un entero positivo"
    except (TypeError, ValueError):
        return False, "El campo 'numeroEmpleado' debe ser un entero positivo"

    if not isinstance(data["nombres"], str) or not data["nombres"].strip():
        return False, "Campo 'nombres' debe ser string no vacío"

    if not isinstance(data["apellidos"], str) or not data["apellidos"].strip():
        return False, "Campo 'apellidos' debe ser string no vacío"

    # Validar horasClase
    horas = data["horasClase"]
    if isinstance(horas, bool):
        return False, "El campo 'horasClase' debe ser un entero positivo"
    try:
        horas_int = int(horas)
    except (TypeError, ValueError):
        return False, "El campo 'horasClase' debe ser un entero positivo"

    if horas_int < 0:
        return False, "El campo 'horasClase' debe ser un entero positivo o cero"

    profesor_validado = {
        "numeroEmpleado": numero_empleado,
        "nombres": data["nombres"].strip(),
        "apellidos": data["apellidos"].strip(),
        "horasClase": horas_int,
    }

    if requiere_id:
        profesor_validado["id"] = data["id"]

    return True, profesor_validado


def obtener_json():
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValueError("El cuerpo de la petición debe ser JSON válido")
    return payload


@app.errorhandler(ValueError)
def handle_value_error(err):
    return jsonify({"error": str(err)}), 400


@app.get('/alumnos')
def listar_alumnos():
    try:
        return jsonify(alumnos), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.get('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    try:
        alumno = buscar_por_id(alumnos, alumno_id)
        if alumno is None:
            return jsonify({"error": f"Alumno con id {alumno_id} no encontrado"}), 404
        return jsonify(alumno), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.post('/alumnos')
def crear_alumno():
    try:
        payload = obtener_json()
        es_valido, alumno_data = validar_alumno(payload, requiere_id=True)
        if not es_valido:
            return jsonify({"error": alumno_data}), 400

        # Verificar si ya existe un alumno con ese ID
        if buscar_por_id(alumnos, alumno_data["id"]) is not None:
            return jsonify({"error": f"Ya existe un alumno con id {alumno_data['id']}"}), 400

        alumnos.append(alumno_data)
        return jsonify(alumno_data), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.put('/alumnos/<int:alumno_id>')
def actualizar_alumno(alumno_id):
    try:
        alumno = buscar_por_id(alumnos, alumno_id)
        if alumno is None:
            return jsonify({"error": f"Alumno con id {alumno_id} no encontrado"}), 404

        payload = obtener_json()
        es_valido, alumno_data = validar_alumno(payload)
        if not es_valido:
            return jsonify({"error": alumno_data}), 400

        alumno.update(alumno_data)
        return jsonify(alumno), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.delete('/alumnos/<int:alumno_id>')
def eliminar_alumno(alumno_id):
    try:
        alumno = buscar_por_id(alumnos, alumno_id)
        if alumno is None:
            return jsonify({"error": f"Alumno con id {alumno_id} no encontrado"}), 404

        alumnos.remove(alumno)
        return jsonify({"message": f"Alumno con id {alumno_id} eliminado"}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.get('/profesores')
def listar_profesores():
    try:
        return jsonify(profesores), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.get('/profesores/<int:profesor_id>')
def obtener_profesor(profesor_id):
    try:
        profesor = buscar_por_id(profesores, profesor_id)
        if profesor is None:
            return jsonify({"error": f"Profesor con id {profesor_id} no encontrado"}), 404
        return jsonify(profesor), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.post('/profesores')
def crear_profesor():
    try:
        payload = obtener_json()
        es_valido, profesor_data = validar_profesor(payload, requiere_id=True)
        if not es_valido:
            return jsonify({"error": profesor_data}), 400

        # Verificar si ya existe un profesor con ese ID
        if buscar_por_id(profesores, profesor_data["id"]) is not None:
            return jsonify({"error": f"Ya existe un profesor con id {profesor_data['id']}"}), 400

        profesores.append(profesor_data)
        return jsonify(profesor_data), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.put('/profesores/<int:profesor_id>')
def actualizar_profesor(profesor_id):
    try:
        profesor = buscar_por_id(profesores, profesor_id)
        if profesor is None:
            return jsonify({"error": f"Profesor con id {profesor_id} no encontrado"}), 404

        payload = obtener_json()
        es_valido, profesor_data = validar_profesor(payload)
        if not es_valido:
            return jsonify({"error": profesor_data}), 400

        profesor.update(profesor_data)
        return jsonify(profesor), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.delete('/profesores/<int:profesor_id>')
def eliminar_profesor(profesor_id):
    try:
        profesor = buscar_por_id(profesores, profesor_id)
        if profesor is None:
            return jsonify({"error": f"Profesor con id {profesor_id} no encontrado"}), 404

        profesores.remove(profesor)
        return jsonify({"message": f"Profesor con id {profesor_id} eliminado"}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.get('/health')
def health_check():
    """Endpoint simple para verificar que el servicio está en ejecución."""
    return jsonify({"status": "ok"}), 200


@app.get('/')
def root_message():
    """Mensaje inicial mientras se implementan los endpoints REST completos."""
    return jsonify({"message": "API REST para alumnos y profesores"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
