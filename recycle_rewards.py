import time
import cv2
import requests
import serial
from ultralytics import YOLO

# Configuración de cámara
cap = cv2.VideoCapture(0)

# Modelo de detección de objetos YOLO
model = YOLO('yolov8n.pt')  # Ajusta según tu modelo

# Balanza conectada por serial (ESP32/Arduino)
# Ajusta el puerto serial según tu sistema, p.ej. 'COM4' o '/dev/ttyUSB0'
SCALE_SERIAL = 'COM4'
BAUDRATE = 9600

# Configuración de servidor de recompensa (API de la app)
APP_API_URL = 'http://127.0.0.1:5000/reward'  # Cambia por tu API real
USER_ID = 'usuario123'

# Clases reciclables (puedes ajustar según dataset)
RECICLABLES = {'bottle', 'can', 'carton', 'paper', 'plastic', 'glass'}

# Puntos por pieza aceptada
PUNTOS_POR_PIEZA = 2

def leer_peso_de_bascula():
    try:
        with serial.Serial(SCALE_SERIAL, BAUDRATE, timeout=1) as ser:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                return None
            # Se espera un valor numérico (gramos o kg)
            return float(line)
    except Exception as e:
        print('Error balanza:', e)
        return None

def enviar_recompensa(usuario_id, puntos, peso, tipo):
    payload = {
        'user_id': usuario_id,
        'points': puntos,
        'weight': peso,
        'type': tipo,
        'timestamp': int(time.time())
    }
    try:
        r = requests.post(APP_API_URL, json=payload, timeout=2)
        if r.status_code == 200:
            print('Recompensa enviada:', payload)
        else:
            print('Error API:', r.status_code, r.text)
    except Exception as e:
        print('No se pudo enviar recompensa:', e)


def main():
    puntos_acumulados = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print('No hay imagen de la cámara')
            break

        results = model(frame)
        # Dibujar detecciones
        annotated = results[0].plot()

        reciclable_detectado = False
        tipo_objeto = 'no_reciclable'

        for box in results[0].boxes:
            clase_idx = int(box.cls[0])
            nombre = model.names.get(clase_idx, '').lower()

            if nombre in RECICLABLES:
                reciclable_detectado = True
                tipo_objeto = 'reciclable'
                # marca rápida, rompemos para no duplicar puntos en el mismo frame
                break

        if reciclable_detectado:
            peso = leer_peso_de_bascula()
            if peso is not None and peso > 0:
                puntos_acumulados += PUNTOS_POR_PIEZA
                enviar_recompensa(USER_ID, PUNTOS_POR_PIEZA, peso, tipo_objeto)
            else:
                print('Objeto reciclable detectado pero sin lectura de peso válida')

        cv2.putText(annotated, f'Puntos: {puntos_acumulados}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Recycle Rewards', annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
