# TEST LITERATURA
# ESTE PROGRAMA HACE CUESTIONARIOS
# XIMENA MUÑOZ CRUZ

import os
import random
import re

# ---------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------
RUTA_ORIGINAL = "D:\\LENGUAJE DE PROGRAMACION\\PREGUNTAS EJERCICIO 10.txt"
NOMBRE_ARCHIVO = "PREGUNTAS EJERCICIO 10.txt"
PUNTOS_POR_ACIERTO = 10
LETRAS_VALIDAS = ["A", "B", "C", "D"]
ANCHO = 45

# Variable global para el puntaje acumulado
puntaje_acumulado = 0

# Patrones para reconocer el contenido del archivo
RE_OPCION = re.compile(r"^\s*\(?([A-Da-d])\s*[\)\.\:\-]\s*(.+)$")
RE_RESPUESTA = re.compile(
    r"^\s*(?:respuesta(?:\s+correcta)?|resp\.?|correcta|clave|answer)"
    r"\s*[:\-=]?\s*\(?([A-Da-d])\)?(?:[\s\)\.\-:].*)?$",
    re.IGNORECASE,
)
RE_LETRA_SOLA = re.compile(r"^\s*\(?([A-Da-d])\)?\s*\.?\s*$")
RE_NUMERO = re.compile(r"^\s*\d+\s*[\)\.\-]\s*")


# ---------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------
def linea_separadora(caracter="="):
    return caracter * ANCHO


def buscar_archivo():
    """Busca el archivo: ruta original, junto al programa o carpeta actual."""
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        RUTA_ORIGINAL,
        os.path.join(carpeta_script, NOMBRE_ARCHIVO),
        os.path.join(os.getcwd(), NOMBRE_ARCHIVO),
    ]
    for ruta in candidatos:
        if os.path.isfile(ruta):
            return ruta
    return None


def leer_texto(ruta):
    """Lee el archivo probando varias codificaciones."""
    for codificacion in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(ruta, "r", encoding=codificacion) as archivo:
                return archivo.read()
        except UnicodeDecodeError:
            continue
    return ""


# ---------------------------------------------------------------
# Lectura del archivo (acepta varios formatos)
#
# Formato 1 (una pregunta por línea):
#   Pregunta|A) op1|B) op2|C) op3|D) op4|B
#
# Formato 2 (varias líneas por pregunta):
#   ¿Quién escribió Don Quijote?
#   A) Lorca
#   B) Cervantes
#   C) Borges
#   D) Neruda
#   Respuesta: B
# ---------------------------------------------------------------
def _normalizar_opcion(texto, indice):
    texto = texto.strip()
    coincidencia = RE_OPCION.match(texto)
    if coincidencia:
        return f"{coincidencia.group(1).upper()}) {coincidencia.group(2).strip()}"
        return f"{LETRAS_VALIDAS[indice]}) {texto}"


def _resolver_letra(campo, opciones):
    campo = campo.strip()
    coincidencia = RE_RESPUESTA.match(campo) or RE_LETRA_SOLA.match(campo)
    if coincidencia:
        return coincidencia.group(1).upper()

    # La respuesta puede venir escrita como el texto de la opción
    for opcion in opciones:
        if campo.lower() == opcion[3:].strip().lower():
            return opcion[0]
    return None


def _parsear_linea_completa(partes):
    """Una línea con 6 campos separados por '|'."""
    pregunta = RE_NUMERO.sub("", partes[0]).strip()
    opciones = [_normalizar_opcion(o, i) for i, o in enumerate(partes[1:5])]
    letra = _resolver_letra(partes[5], opciones)

    if not pregunta or letra is None:
        return None
    return pregunta, opciones, letra


def parsear_texto(texto):
    """Convierte el texto del archivo en una lista de
    (pregunta, opciones, letra_correcta). Devuelve también avisos."""
    preguntas = []
    avisos = []

    pregunta = []
    opciones = []

    def cerrar_bloque(num, letra):
        nonlocal pregunta, opciones
        letras_presentes = [op[0] for op in opciones]
        if pregunta and len(opciones) >= 2 and letra in letras_presentes:
            preguntas.append((" ".join(pregunta), opciones, letra))
        else:
            avisos.append(f"Se ignoró una pregunta incompleta cerca de la línea {num}.")
        pregunta, opciones = [], []

    def descartar_pendiente(num):
        nonlocal pregunta, opciones
        if pregunta or opciones:
            avisos.append(f"Se ignoró una pregunta sin respuesta cerca de la línea {num}.")
        pregunta, opciones = [], []

    for num, linea in enumerate(texto.splitlines(), start=1):
        linea = linea.strip()
        if not linea:
            continue

        partes = [p.strip() for p in linea.split("|")]

        # Formato 1: pregunta completa en una sola línea
        if len(partes) == 6:
            completa = _parsear_linea_completa(partes)
            if completa:
                descartar_pendiente(num)
                preguntas.append(completa)
                continue

        # Formato 2: se procesa cada trozo como una línea independiente
        for trozo in partes:
            if not trozo:
                continue

            if RE_RESPUESTA.match(trozo) or (
                len(opciones) >= 2 and RE_LETRA_SOLA.match(trozo)
            ):
                letra = (RE_RESPUESTA.match(trozo) or RE_LETRA_SOLA.match(trozo)).group(1).upper()
                cerrar_bloque(num, letra)

            elif RE_OPCION.match(trozo):
                coincidencia = RE_OPCION.match(trozo)
                opciones.append(f"{coincidencia.group(1).upper()}) {coincidencia.group(2).strip()}")

            else:
                # Texto de pregunta; si ya había opciones sin respuesta, es otra pregunta
                if opciones:
                    descartar_pendiente(num)
                pregunta.append(RE_NUMERO.sub("", trozo).strip())

    descartar_pendiente(len(texto.splitlines()))
    return preguntas, avisos


# ---------------------------------------------------------------
# Función 1: Carga las preguntas desde el archivo
# ---------------------------------------------------------------
def cargar_preguntas(nombre_archivo=None):
    if nombre_archivo is None:
        nombre_archivo = buscar_archivo()

    if nombre_archivo is None:
        print(f"\nError: No se encontró el archivo '{NOMBRE_ARCHIVO}'.")
        ruta = input("Escribe la ruta completa del archivo (Enter para cancelar): ").strip().strip('"')
        if not ruta or not os.path.isfile(ruta):
            print("No se pudo abrir el archivo.\n")
            return []
        nombre_archivo = ruta

    try:
        texto = leer_texto(nombre_archivo)
    except OSError as error:
        print(f"\nError al leer el archivo: {error}\n")
        return []

    preguntas, avisos = parsear_texto(texto)

    for aviso in avisos:
        print(f"Advertencia: {aviso}")

    if not preguntas:
        print("\nNo se pudo leer ninguna pregunta. Revisa que el archivo tenga este formato:")
        print("  Pregunta|A) opción|B) opción|C) opción|D) opción|B\n")
        return []

    print(f"\nSe cargaron {len(preguntas)} preguntas correctamente.")
    return preguntas


# ---------------------------------------------------------------
# Función 2: Muestra UNA pregunta con sus opciones (sin la respuesta)
# ---------------------------------------------------------------
def mostrar_pregunta(numero, total, pregunta, opciones):
    print("\n" + linea_separadora())
    print(f"Pregunta {numero} de {total}\n")
    print(pregunta + "\n")

    for opcion in opciones:
        print(opcion)

    print("\n" + linea_separadora())


# ---------------------------------------------------------------
# Función 3: Pide la respuesta (repite hasta que sea A, B, C o D)
# ---------------------------------------------------------------
def pedir_respuesta():
    while True:
        respuesta = input("\nTu respuesta (A, B, C o D): ").strip().upper()
        if respuesta in LETRAS_VALIDAS:
            return respuesta
        print("Opción no válida. Escribe solo A, B, C o D.")


# ---------------------------------------------------------------
# Función 4: Compara la respuesta del usuario con la correcta
# ---------------------------------------------------------------
def comparar_respuestas(respuesta_usuario, respuesta_correcta):
    return respuesta_usuario == respuesta_correcta.strip().upper()


# ---------------------------------------------------------------
# Función 5: Marca la opción correcta DESPUÉS de responder
# ---------------------------------------------------------------
def mostrar_resultado(opciones, respuesta_usuario, respuesta_correcta):
    print()
    for opcion in opciones:
        letra = opcion[0]
        if letra == respuesta_correcta:
            marca = "   <-- CORRECTA"
        elif letra == respuesta_usuario:
            marca = "   <-- tu respuesta"
        else:
            marca = ""
        print(opcion + marca)


# ---------------------------------------------------------------
# Función 6: Pregunta cuántas preguntas quiere responder
# ---------------------------------------------------------------
def pedir_cantidad(total):
    while True:
        entrada = input(f"\n¿Cuántas preguntas quieres responder? (1-{total}, Enter = todas): ").strip()

        if entrada == "":
            return total

        if entrada.isdigit() and 1 <= int(entrada) <= total:
            return int(entrada)

        print(f"Escribe un número entre 1 y {total}.")


# ---------------------------------------------------------------
# Función 7: Recorre las preguntas UNA POR UNA y lleva el puntaje
# ---------------------------------------------------------------
def resolver_preguntas():
    global puntaje_acumulado

    preguntas = cargar_preguntas()

    if not preguntas:
        return

    cantidad = pedir_cantidad(len(preguntas))
    seleccion = random.sample(preguntas, cantidad)

    puntaje_ronda = 0
    aciertos = 0

    for numero, (pregunta, opciones, respuesta_correcta) in enumerate(seleccion, start=1):
        mostrar_pregunta(numero, cantidad, pregunta, opciones)
        respuesta_usuario = pedir_respuesta()

        mostrar_resultado(opciones, respuesta_usuario, respuesta_correcta)

        if comparar_respuestas(respuesta_usuario, respuesta_correcta):
            print(f"\n¡Respuesta correcta! Sumas {PUNTOS_POR_ACIERTO} puntos.")
            puntaje_acumulado += PUNTOS_POR_ACIERTO
            puntaje_ronda += PUNTOS_POR_ACIERTO
            aciertos += 1
        else:
            print(f"\nRespuesta incorrecta. La correcta era: {respuesta_correcta}")

        if numero < cantidad:
            input("\nPresiona Enter para ver la siguiente pregunta...")

    porcentaje = (aciertos / cantidad) * 100

    print("\n" + linea_separadora())
    print("--- FIN DE LA RONDA ---")
    print(f"Aciertos: {aciertos} de {cantidad} ({porcentaje:.0f}%)")
    print(f"Puntaje obtenido en esta ronda: {puntaje_ronda}")
    print(f"Puntaje total acumulado: {puntaje_acumulado}")
    print(linea_separadora() + "\n")


# ---------------------------------------------------------------
# Función 8: Muestra el menú principal
# ---------------------------------------------------------------
def mostrar_menu():
    print("\n========== QUIZ GAME ==========")
    print("1. Jugar")
    print("2. Ver puntaje actual")
    print("3. Salir")

    opcion_raw = input("\nElige una opción: ").strip()

    if not opcion_raw.isdigit():
        raise ValueError("Debes ingresar un número entero válido (1, 2 o 3).")

    opcion = int(opcion_raw)

    if opcion not in [1, 2, 3]:
        raise ValueError("Opción fuera de rango. Selecciona entre 1, 2 o 3.")

    return opcion


# ---------------------------------------------------------------
# Función 9: Función principal
# ---------------------------------------------------------------
def main():
    while True:
        try:
            opcion = mostrar_menu()

            if opcion == 1:
                resolver_preguntas()

            elif opcion == 2:
                print(f"\nEl puntaje actual acumulado es: {puntaje_acumulado} puntos\n")

            elif opcion == 3:
                print(f"\nPuntaje final: {puntaje_acumulado} puntos.")
                print("¡Gracias por jugar! Hasta la próxima.")
                break

        except ValueError as ve:
            print(f"\nError de entrada: {ve}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nPrograma interrumpido. ¡Hasta la próxima!")
            break

        except Exception as e:
            print(f"\nOcurrió un error inesperado: {e}\n")


if __name__ == "__main__":
    main()