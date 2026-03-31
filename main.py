import cv2
import time
from deepface import DeepFace
from config import PERFILES

# Variables de estado globales
perfil_actual = "BUSCANDO..."
color_actual = (255, 255, 255)
ultimo_analisis = 0

def aplicar_cambios_hogar(perfil_key):
    """Simula la activación física de los dispositivos"""
    datos = PERFILES[perfil_key]
    print(f"\n--- ACTIVANDO PERFIL: {datos['etiqueta']} ---")
    print(f"[*] Luces -> {datos['luces']}")
    print(f"[*] Música -> {datos['musica']}")
    print(f"[*] Clima -> {datos['temp']}")
    return datos['etiqueta'], datos['color']

# Inicializar Cámara
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX

while True:
    ret, frame = cap.read()
    if not ret: break

    # --- DISEÑO DEL DASHBOARD ---
    # Dibujar cabecera
    cv2.rectangle(frame, (0, 0), (400, 80), (40, 40, 40), -1)
    cv2.putText(frame, "SMART HOME AI v1.0", (20, 30), font, 0.7, (200, 200, 200), 1)
    
    # Mostrar Perfil Activo
    cv2.putText(frame, f"STATUS: ", (20, 60), font, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, perfil_actual, (110, 60), font, 0.8, color_actual, 2)

    # Instrucción en la parte inferior
    cv2.putText(frame, "[SPACE]: ESCANEAR | [Q]: SALIR", (20, frame.shape[0] - 20), font, 0.5, (255, 255, 255), 1)

    cv2.imshow("Sensor Bio-Metrico", frame)

    key = cv2.waitKey(1) & 0xFF

    # --- LÓGICA DE RECONOCIMIENTO ---
    if key == ord(' ') and (time.time() - ultimo_analisis) > 2:
        ultimo_analisis = time.time()
        perfil_actual = "ANALIZANDO..."
        cv2.imshow("Sensor Bio-Metrico", frame) # Forzar refresco visual
        
        cv2.imwrite("rostro.jpg", frame)
        
        try:
            # Analizar edad (usamos 'opencv' como detector por ser más veloz para Smart Home)
            resultado = DeepFace.analyze(
                img_path="rostro.jpg", 
                actions=['age'], 
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            edad = resultado[0]['age']
            print(f"Escaneo completado. Edad estimada: {edad}")

            if edad >= 18:
                perfil_actual, color_actual = aplicar_cambios_hogar("adulto_alborotado")
            else:
                perfil_actual, color_actual = aplicar_cambios_hogar("niño_activo")

        except Exception as e:
            print(f"Fallo en sensor: {e}")
            perfil_actual = "ERROR LECTURA"
            color_actual = (0, 0, 255)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()