import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit
import wikipedia
import sounddevice as sd
import scipy.io.wavfile as wav
import sys

from urllib.parse import quote
from datetime import datetime

# =========================
# CONFIGURACIÓN INICIAL
# =========================

if sys.platform == "win32":
    engine = pyttsx3.init(driverName="sapi5")
else:
    engine = pyttsx3.init()

wikipedia.set_lang("es")

# Buscar una voz en español
voces = engine.getProperty("voices")

for voz in voces:
    if "spanish" in voz.name.lower() or "es" in voz.id.lower():
        engine.setProperty("voice", voz.id)
        break

engine.setProperty("rate", 180)

# =========================
# FUNCIONES
# =========================

def hablar(texto):
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()


def escuchar():

    fs = 44100
    segundos = 8

    print("\nEscuchando...")

    try:

        audio_grabado = sd.rec(
            int(segundos * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write(
            "temporal.wav",
            fs,
            audio_grabado
        )

    except Exception as e:

        print(f"\n[Error de Micrófono]: {e}")

        hablar(
            "No pude acceder al micrófono."
        )

        return ""

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(
            "temporal.wav"
        ) as source:

            audio = recognizer.record(
                source
            )

        comando = recognizer.recognize_google(
            audio,
            language="es-MX"
        )

        comando = comando.lower()

        print(f"Usuario: {comando}")

        return comando

    except sr.UnknownValueError:

        print("No entendí el audio.")
        return ""

    except Exception as e:

        print(f"Error reconocimiento: {e}")
        return ""


# =========================
# COMANDOS
# =========================

def ejecutar_comando(comando):

    # WORD

    if (
        "abrir word" in comando
        or "abre word" in comando
        or comando == "word"
    ):

        hablar("Abriendo Microsoft Word")
        os.system("start winword")

    # EXCEL

    elif (
        "abrir excel" in comando
        or "abre excel" in comando
        or comando == "excel"
    ):

        hablar("Abriendo Microsoft Excel")
        os.system("start excel")

    # POWERPOINT

    elif (
        "abrir powerpoint" in comando
        or "abre powerpoint" in comando
        or comando == "powerpoint"
    ):

        hablar("Abriendo PowerPoint")
        os.system("start powerpnt")

    # BLOC DE NOTAS

    elif (
        "abrir bloc de notas" in comando
        or "abre bloc de notas" in comando
        or "bloc de notas" in comando
    ):

        hablar("Abriendo bloc de notas")
        os.system("start notepad")

    # CALCULADORA

    elif (
        "abrir calculadora" in comando
        or "abre calculadora" in comando
        or "calculadora" in comando
    ):

        hablar("Abriendo calculadora")
        os.system("start calc")

    # GOOGLE

    elif (
        "abrir google" in comando
        or "abre google" in comando
    ):

        hablar("Abriendo Google")
        webbrowser.open("https://www.google.com")

    # YOUTUBE

    elif (
        "abrir youtube" in comando
        or "abre youtube" in comando
    ):

        hablar("Abriendo YouTube")
        webbrowser.open("https://www.youtube.com")

    # REPRODUCTOR WINDOWS

    elif (
        "abrir reproductor de video" in comando
        or "abre reproductor de video" in comando
        or "abrir reproductor de música" in comando
        or "abre reproductor de música" in comando
        or comando == "reproductor"
    ):

        hablar("Abriendo Windows Media Player")
        os.system("start wmplayer")

    # REPRODUCIR EN YOUTUBE

    elif "reproduce" in comando:

        cancion = comando.replace(
            "reproduce",
            ""
        ).strip()

        if cancion:

            hablar(
                f"Reproduciendo {cancion}"
            )

            pywhatkit.playonyt(
                cancion
            )

        else:

            hablar(
                "Debes indicar qué deseas reproducir."
            )

    # BUSCAR

    elif (
        "buscar" in comando
        or "busca" in comando
    ):

        consulta = (
            comando
            .replace("buscar", "")
            .replace("busca", "")
            .replace("en wikipedia", "")
            .strip()
        )

        if len(consulta) < 3:

            hablar(
                "Debes decirme qué deseas buscar."
            )

            return True

        hablar(
            f"Buscando {consulta}"
        )

        consulta_url = quote(
            consulta
        )

        webbrowser.open(
            f"https://www.google.com/search?q={consulta_url}"
        )

        try:

            resultado = wikipedia.summary(
                consulta,
                sentences=2
            )

            hablar(
                "Encontré la siguiente información."
            )

            hablar(
                resultado
            )

        except wikipedia.exceptions.DisambiguationError:

            hablar(
                "La búsqueda tiene varios significados. Sé más específico."
            )

        except wikipedia.exceptions.PageNotFoundError:

            hablar(
                "No encontré información en Wikipedia."
            )

        except Exception:

            hablar(
                "Abrí la búsqueda, pero no pude leer un resumen."
            )

    # HORA

    elif (
        "qué hora es" in comando
        or "que hora es" in comando
        or "dime la hora" in comando
    ):

        hora = datetime.now().strftime(
            "%H:%M"
        )

        hablar(
            f"Son las {hora}"
        )

    # FECHA

    elif (
        "qué fecha es" in comando
        or "que fecha es" in comando
        or "qué día es hoy" in comando
        or "que día es hoy" in comando
    ):

        fecha = datetime.now().strftime(
            "%d de %B de %Y"
        )

        hablar(
            f"Hoy es {fecha}"
        )

    # APAGAR

    elif (
        "apagar equipo" in comando
        or "apaga el equipo" in comando
        or "apaga la computadora" in comando
    ):

        hablar(
            "Apagando el equipo en sesenta segundos."
        )

        os.system(
            "shutdown /s /t 60"
        )

        return False

    # CANCELAR APAGADO

    elif (
        "cancelar apagado" in comando
    ):

        os.system(
            "shutdown /a"
        )

        hablar(
            "Apagado cancelado."
        )

    # SALIR

    elif (
        "salir" in comando
        or "adiós" in comando
        or "adios" in comando
        or "hasta luego" in comando
        or "bay bay" in comando
    ):

        hablar(
            "Asistente finalizado. Hasta luego."
        )

        return False

    # COMANDO DESCONOCIDO

    else:

        hablar(
            "No entendí ese comando."
        )

    return True


# =========================
# PROGRAMA PRINCIPAL
# =========================

hablar(
    "Asistente virtual iniciado y listo para recibir instrucciones."
)

activo = True

while activo:

    comando = escuchar()

    if comando != "":
        activo = ejecutar_comando(comando)