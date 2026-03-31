from deepface import DeepFace
import json

# --- MESA DE TRABAJO: PERFILES DE HOGAR ---
perfiles = {
    "adulto_alborotado": {
        "luces": "ultravioleta 30%",
        "musica": "black metal",
        "temp": "22°C"
    },
    "niño_activo": {
        "luces": "brillantes 100%",
        "musica": "cocomelon",
        "temp": "24°C"
    }
}

def activar_hogar(perfil):
    config = perfiles[perfil]
    print(f"\n[SISTEMA]: Perfil '{perfil}' detectado.")
    print(f">> Ajustando luces a: {config['luces']}")
    print(f">> Reproduciendo: {config['musica']}")
    print(f">> Climatizando a: {config['temp']}")

try:
    # 1. Escanear rostro
    print("Escaneando entrada...")
    analisis = DeepFace.analyze(img_path = "rostro.jpg", 
                                actions = ['age'],
                                enforce_detection = False)
    
    edad = analisis[0]['age']
    print(f"Edad detectada: {edad} años")

    # 2. Lógica de decisión según el requerimiento
    if edad > 18:
        activar_hogar("adulto_alborotado")
    else:
        activar_hogar("niño_activo")

except Exception as e:
    print(f"Error en el sensor: {e}")

if edad > 18:
    activar_hogar("adulto_alborotado")
elif edad > 12:
    print("Perfil Adolescente detectado (sin configurar)")
else:
    activar_hogar("niño_active")