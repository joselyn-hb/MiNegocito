from database import obtener_conexion
from mysql.connector import Error
from datetime import datetime, date, timedelta
from decimal import Decimal, InvalidOperation


def generar_fechas_periodos(fecha_inicio, frecuencia, cantidad_periodos):
    # Importa las herramientas necesarias para manejar fechas
    import calendar

    # Comprueba que la cantidad de periodos sea válida
    if cantidad_periodos < 1:
        raise ValueError("La cantidad de periodos debe ser mayor que cero.")

    # Convierte la fecha recibida si viene como texto
    if isinstance(fecha_inicio, str):
        fecha_inicio = date.fromisoformat(fecha_inicio)

    # Guarda la fecha inicial
    fechas = []

    # Genera las fechas para la frecuencia semanal
    if frecuencia == "SEMANAL":

        for periodo in range(cantidad_periodos):

            # Cada periodo semanal suma siete días
            fecha_periodo = fecha_inicio + timedelta(days=7 * periodo)

            fechas.append(fecha_periodo)

    # Genera las fechas para la frecuencia quincenal
    elif frecuencia == "QUINCENAL":

        # Comienza con el mes y año de la fecha inicial
        anio = fecha_inicio.year
        mes = fecha_inicio.month

        while len(fechas) < cantidad_periodos:

            # Obtiene el último día del mes
            ultimo_dia = calendar.monthrange(anio, mes)[1]

            # Las fechas quincenales son el 15 y el 30
            # En febrero se utiliza su último día
            dias_mes = [15, min(30, ultimo_dia)]

            for dia in dias_mes:

                fecha_periodo = date(anio, mes, dia)

                # No incluye fechas anteriores al inicio
                if fecha_periodo >= fecha_inicio:
                    fechas.append(fecha_periodo)

                    # Detiene el cálculo al completar los periodos
                    if len(fechas) == cantidad_periodos:
                        break

            # Avanza al siguiente mes
            if mes == 12:
                mes = 1
                anio += 1
            else:
                mes += 1

    # Genera las fechas para la frecuencia mensual
    elif frecuencia == "MENSUAL":

        for periodo in range(cantidad_periodos):

            # Calcula el año y el mes correspondientes
            mes_total = fecha_inicio.month - 1 + periodo
            anio = fecha_inicio.year + mes_total // 12
            mes = mes_total % 12 + 1

            # Ajusta el día si el mes tiene menos días
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            dia = min(fecha_inicio.day, ultimo_dia)

            # Construye la fecha del periodo
            fecha_periodo = date(anio, mes, dia)

            fechas.append(fecha_periodo)

    else:
        # Rechaza cualquier frecuencia no reconocida
        raise ValueError("La frecuencia del Susú no es válida.")

    # Devuelve todas las fechas calculadas
    return fechas


def asignar_turnos_susu(participantes, metodo_asignacion, orden_manual=None):
    # Importa la herramienta para realizar sorteos aleatorios
    import random

    # Comprueba que existan participantes
    if not participantes:
        raise ValueError("El Susú no tiene participantes inscritos.")

    # Comprueba que el método de asignación sea válido
    if metodo_asignacion not in ("SORTEO", "INSCRIPCION", "MANUAL"):
        raise ValueError("El método de asignación no es válido.")

    # Copia la lista para no modificar la lista original
    participantes = list(participantes)

    # Asigna los turnos mediante sorteo aleatorio
    if metodo_asignacion == "SORTEO":

        # Mezcla las inscripciones individualmente
        random.SystemRandom().shuffle(participantes)

    # Asigna los turnos según el orden de inscripción
    elif metodo_asignacion == "INSCRIPCION":

        # Ordena por fecha de inscripción e identificador
        participantes.sort(
            key=lambda p: (
                p["fecha_inscripcion"],
                p["id_participante_susu"]
            )
        )

    # Asigna los turnos manualmente
    elif metodo_asignacion == "MANUAL":

        # Comprueba que se hayan proporcionado los turnos
        if orden_manual is None:
            raise ValueError("Debes indicar el orden manual de los turnos.")

        # Comprueba que todos los participantes tengan un turno
        if len(orden_manual) != len(participantes):
            raise ValueError("La cantidad de turnos manuales no coincide.")

        # Crea un diccionario para identificar cada inscripción
        participantes_por_id = {
            p["id_participante_susu"]: p
            for p in participantes
        }

        # Comprueba que no existan inscripciones repetidas
        if len(set(orden_manual)) != len(orden_manual):
            raise ValueError("No puedes asignar dos veces la misma inscripción.")

        # Comprueba que todas las inscripciones estén incluidas
        if set(orden_manual) != set(participantes_por_id):
            raise ValueError("La asignación manual contiene inscripciones inválidas.")

        # Organiza las inscripciones según el orden indicado
        participantes = [
            participantes_por_id[id_participante]
            for id_participante in orden_manual
        ]

    # Prepara el resultado con el número de turno
    turnos = []

    for numero_turno, participante in enumerate(participantes, start=1):

        # Guarda el identificador de la inscripción y su turno
        turnos.append({
            "id_participante_susu": participante["id_participante_susu"],
            "numero_turno": numero_turno
        })

    # Devuelve todos los turnos asignados
    return turnos



def crear_susu(nombre, descripcion, monto_cuota, frecuencia,
               fecha_inicio, cantidad_participantes, metodo_asignacion):

    # Establece la conexión con la base de datos
    conexion = obtener_conexion()

    # Comprueba si se pudo establecer la conexión
    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        # Elimina espacios innecesarios del nombre
        nombre = nombre.strip()

        # Comprueba que el nombre no esté vacío
        if not nombre:
            return False, "Debes ingresar el nombre del Susú."

        # Convierte la cuota a decimal con dos posiciones
        monto_cuota = Decimal(str(monto_cuota)).quantize(
            Decimal("0.01")
        )

        # Convierte la cantidad de participantes a entero
        cantidad_participantes = int(cantidad_participantes)

        # Comprueba que la cuota sea mayor que cero
        if monto_cuota <= 0:
            return False, "La cuota debe ser mayor que cero."

        # Comprueba que existan al menos dos participantes
        if cantidad_participantes < 2:
            return False, "El Susú debe tener al menos 2 participantes."

        # Valida la frecuencia de pago seleccionada
        if frecuencia not in ("SEMANAL", "QUINCENAL", "MENSUAL"):
            return False, "La frecuencia seleccionada no es válida."

        # Valida el método de asignación de turnos
        if metodo_asignacion not in ("SORTEO", "INSCRIPCION", "MANUAL"):
            return False, "El método de asignación no es válido."

        # Crea el cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        # Prepara la consulta para guardar el nuevo Susú
        consulta = """
            INSERT INTO susus (
                nombre,
                descripcion,
                monto_cuota,
                frecuencia,
                fecha_inicio,
                cantidad_participantes,
                metodo_asignacion,
                estado,
                fecha_creacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo', NOW())
        """
        # Ejecuta la consulta con los datos recibidos
        cursor.execute(
            consulta,
            (
                nombre,
                descripcion,
                monto_cuota,
                frecuencia,
                fecha_inicio,
                cantidad_participantes,
                metodo_asignacion
            )
        )

        # Obtiene el identificador del Susú recién creado
        id_susu = cursor.lastrowid

        # Confirma los cambios en la base de datos
        conexion.commit()

        # Devuelve el resultado y el identificador
        return True, f"Susú creado correctamente. ID: {id_susu}"

    except (Error, ValueError, InvalidOperation) as e:

        # Deshace los cambios si ocurre algún error
        conexion.rollback()

        # Muestra el error en la terminal
        print("Error al crear el Susú:", e)

        # Devuelve un mensaje de error
        return False, "No se pudo crear el Susú. Verifica los datos."

    finally:

        # Cierra el cursor si fue creado
        if cursor:
            cursor.close()

        # Cierra la conexión con MySQL
        conexion.close()


def listar_susus(estado=None):

    # Establece la conexión con la base de datos
    conexion = obtener_conexion()

    # Comprueba si se pudo establecer la conexión
    if conexion is None:
        return []

    cursor = None

    try:
        # Crea un cursor que devuelve los resultados como diccionarios
        cursor = conexion.cursor(dictionary=True)

        # Prepara la consulta para obtener los Susús
        consulta = """
            SELECT
                id_susu,
                nombre,
                descripcion,
                monto_cuota,
                frecuencia,
                fecha_inicio,
                fecha_fin,
                cantidad_participantes,
                metodo_asignacion,
                estado
            FROM susus
        """

        # Filtra los resultados si se especifica un estado
        if estado:
            consulta += " WHERE estado = %s"

        # Ordena los Susús desde el más reciente
        consulta += " ORDER BY id_susu DESC"

        # Ejecuta la consulta según el filtro seleccionado
        if estado:
            cursor.execute(consulta, (estado,))
        else:
            cursor.execute(consulta)

        # Devuelve todos los registros encontrados
        return cursor.fetchall()

    except Error as e:

        # Muestra el error en la terminal
        print("Error al consultar los Susús:", e)

        # Devuelve una lista vacía si ocurre un error
        return []

    finally:

        # Cierra el cursor si fue creado
        if cursor:
            cursor.close()

        # Cierra la conexión con MySQL
        conexion.close()


def editar_susu(id_susu, nombre, descripcion, monto_cuota,
                frecuencia, fecha_inicio, cantidad_participantes,
                metodo_asignacion):

    # Establece la conexión con MySQL
    conexion = obtener_conexion()

    # Comprueba la conexión
    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        # Limpia el nombre del Susú
        nombre = nombre.strip()

        # Convierte los valores a sus tipos correspondientes
        monto_cuota = Decimal(str(monto_cuota)).quantize(
            Decimal("0.01")
        )
        cantidad_participantes = int(cantidad_participantes)

        # Valida el nombre
        if not nombre:
            return False, "Debes ingresar el nombre del Susú."

        # Valida la cuota
        if monto_cuota <= 0:
            return False, "La cuota debe ser mayor que cero."

        # Valida la cantidad de participantes
        if cantidad_participantes < 2:
            return False, "Se necesitan al menos 2 participantes."

        # Valida la frecuencia
        if frecuencia not in ("SEMANAL", "QUINCENAL", "MENSUAL"):
            return False, "La frecuencia no es válida."

        # Valida el método de asignación
        if metodo_asignacion not in ("SORTEO", "INSCRIPCION", "MANUAL"):
            return False, "El método de asignación no es válido."

        # Comprueba que el Susú exista
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id_susu FROM susus WHERE id_susu = %s",
            (id_susu,)
        )

        if cursor.fetchone() is None:
            return False, "El Susú que deseas editar no existe."

        # Actualiza la información del Susú
        consulta = """
            UPDATE susus
            SET
                nombre = %s,
                descripcion = %s,
                monto_cuota = %s,
                frecuencia = %s,
                fecha_inicio = %s,
                cantidad_participantes = %s,
                metodo_asignacion = %s
            WHERE id_susu = %s
        """

        cursor.execute(
            consulta,
            (
                nombre,
                descripcion,
                monto_cuota,
                frecuencia,
                fecha_inicio,
                cantidad_participantes,
                metodo_asignacion,
                id_susu
            )
        )

        # Guarda los cambios
        conexion.commit()

        return True, "Susú actualizado correctamente."

    except (Error, ValueError, InvalidOperation) as e:

        # Revierte los cambios si ocurre un error
        conexion.rollback()

        print("Error al editar el Susú:", e)

        return False, "No se pudo actualizar el Susú."

    finally:

        # Cierra el cursor
        if cursor:
            cursor.close()

        # Cierra la conexión
        conexion.close()


def registrar_participante_susu(
    id_susu,
    nombre_participante,
    telefono=None,
    id_cliente=None
):
    # Establece la conexión con MySQL
    conexion = obtener_conexion()

    # Comprueba que exista una conexión
    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        # Limpia los datos recibidos
        nombre_participante = nombre_participante.strip()

        if telefono:
            telefono = telefono.strip()

        # Valida que se haya escrito el nombre
        if not nombre_participante:
            return False, "Debes ingresar el nombre del participante."

        # Abre el cursor para consultar la base de datos
        cursor = conexion.cursor(dictionary=True)

        # Comprueba que el Susú exista y esté activo
        cursor.execute(
            """
            SELECT cantidad_participantes, metodo_asignacion, estado
            FROM susus
            WHERE id_susu = %s
            """,
            (id_susu,)
        )

        susu = cursor.fetchone()

        if susu is None:
            return False, "El Susú seleccionado no existe."

        if susu["estado"] != "activo":
            return False, "No puedes agregar participantes a este Susú."

        # Cuenta los participantes que ya están inscritos
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM participantes_susu
            WHERE id_susu = %s
            AND estado = 'activo'
            """,
            (id_susu,)
        )

        total_inscritos = cursor.fetchone()["total"]

        # Comprueba que todavía haya cupos disponibles
        if total_inscritos >= susu["cantidad_participantes"]:
            return False, "Este Susú ya alcanzó el máximo de participantes."

        # Determina el turno cuando el método es por inscripción
        orden_entrega = None

        if susu["metodo_asignacion"] == "INSCRIPCION":
            orden_entrega = total_inscritos + 1

        # Registra al participante
        cursor.execute(
            """
            INSERT INTO participantes_susu (
                id_susu,
                id_cliente,
                nombre_participante,
                telefono,
                orden_entrega,
                fecha_inscripcion,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), 'activo')
            """,
            (
                id_susu,
                id_cliente,
                nombre_participante,
                telefono,
                orden_entrega
            )
        )

        # Guarda el registro en la base de datos
        conexion.commit()

        return True, "Participante registrado correctamente."

    except (Error, ValueError) as e:

        # Revierte los cambios si ocurre algún error
        conexion.rollback()

        print("Error al registrar participante:", e)

        return False, "No se pudo registrar el participante."

    finally:

        # Cierra el cursor si fue creado
        if cursor:
            cursor.close()

        # Cierra la conexión
        conexion.close()


def listar_participantes_susu(id_susu):
    # Establece la conexión con MySQL
    conexion = obtener_conexion()

    # Comprueba que exista una conexión
    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        # Crea el cursor para consultar los participantes
        cursor = conexion.cursor(dictionary=True)

        # Busca los participantes activos del Susú seleccionado
        consulta = """
            SELECT
                id_participante_susu,
                id_susu,
                id_cliente,
                nombre_participante,
                telefono,
                orden_entrega,
                fecha_inscripcion,
                estado
            FROM participantes_susu
            WHERE id_susu = %s
            AND estado = 'activo'
            ORDER BY fecha_inscripcion ASC, id_participante_susu ASC
        """

        cursor.execute(consulta, (id_susu,))

        # Recupera todos los participantes encontrados
        participantes = cursor.fetchall()

        return True, participantes

    except Error as e:

        # Muestra el error y devuelve un mensaje
        print("Error al consultar participantes:", e)

        return False, "No se pudieron consultar los participantes."

    finally:

        # Cierra el cursor
        if cursor:
            cursor.close()

        # Cierra la conexión
        conexion.close()

