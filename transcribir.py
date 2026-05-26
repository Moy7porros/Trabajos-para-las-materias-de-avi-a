import speech_recognition as sr 

filename = "WhatsApp Ptt 2026-05-25 at 7.14.13 PM.wav"
output_file = "transcripcion_audio.txt"

r = sr.Recognizer()

try:
    print("Procesando el archivo de audio...")
    full_transcription = ""
    fragmento_index = 1

    with sr.AudioFile(filename) as source:
        # Nota: quitamos source.DURATION porque rompe el código.
        # Simplemente leemos fragmentos de 10 segundos hasta que r.record() devuelva un audio vacío.
        while True:
            try:
                # Registra bloques de 10 segundos consecutivamente
                audio_data = r.record(source, duration=10)
                
                # Si r.record ya no lee nada (fin del archivo), salimos del bucle
                if len(audio_data.frame_data) == 0:
                    break
                
                text = r.recognize_google(audio_data, language="es-ES")
                full_transcription += text + "\n"
                print(f"Fragmento {fragmento_index}: {text}")
                
            except sr.UnknownValueError:
                print(f"Fragmento {fragmento_index}: No se pudo entender el audio.")
                full_transcription += "[No se pudo entender el audio]\n"
            except sr.RequestError as e: 
                print(f"Error al comunicarse con el servicio de Google: {e}")
                break
            
            fragmento_index += 1
        
        # Guardar el archivo final
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write(full_transcription)
        
        print(f"\nTranscripción completada y guardada en: {output_file}")

except FileNotFoundError:
    print(f"El archivo '{filename}' no se encontró. Asegúrate de que esté en la misma carpeta que este script.")
except ValueError as e:
    print(f"Error con el archivo de audio: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")