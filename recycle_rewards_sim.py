import time
import cv2
import random
from ultralytics import YOLO

# Simulación: Sin cámara física, usamos una imagen estática o generamos datos
# Para probar, descarga una imagen de botella o usa una de prueba
IMAGE_PATH = ''  # Cambia por una imagen real o deja vacío para simular

# Modelo YOLO
model = YOLO('yolov8n.pt')

# Simulación de báscula: Genera peso aleatorio (sin hardware)
def leer_peso_simulado():
    return random.uniform(100, 500)  # Peso en gramos, aleatorio

# Simulación de recompensa: Imprime en consola (sin API)
def enviar_recompensa_simulada(usuario_id, puntos, peso, tipo):
    print(f" Recompensa simulada para {usuario_id}: +{puntos} puntos por {peso:.1f}g de {tipo}")
    print(f"Total puntos acumulados: {puntos} (en simulación)")

# Clases reciclables
RECICLABLES = {'bottle', 'can', 'carton', 'paper', 'plastic', 'glass'}
PUNTOS_POR_PIEZA = 2

def main():
    puntos_acumulados = 0

    print(" Iniciando simulación del sistema de reciclaje...")
    print("Presiona 'q' para salir. (Sin cámara física, usa imagen estática)")

    while True:
        # Simulación: Carga imagen estática o genera datos
        if IMAGE_PATH:
            frame = cv2.imread(IMAGE_PATH)
            if frame is None:
                print(f"Imagen no encontrada: {IMAGE_PATH}. Usando simulación completa.")
                frame = None
        else:
            frame = None  # Simulación sin imagen

        if frame is not None:
            # Detección real con YOLO
            results = model(frame)
            annotated = results[0].plot()
        else:
            # Simulación: Genera detección aleatoria
            print("Simulando detección (sin imagen)...")
            reciclable_detectado = random.choice([True, False])
            tipo_objeto = 'reciclable' if reciclable_detectado else 'no_reciclable'
            annotated = None  # Sin imagen para mostrar

        if frame is not None:
            # Mostrar imagen con detecciones
            cv2.putText(annotated, f'Puntos: {puntos_acumulados}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Simulación Recycle Rewards', annotated)

            # Verificar detecciones reales
            reciclable_detectado = False
            tipo_objeto = 'no_reciclable'
            for box in results[0].boxes:
                clase_idx = int(box.cls[0])
                nombre = model.names.get(clase_idx, '').lower()
                if nombre in RECICLABLES:
                    reciclable_detectado = True
                    tipo_objeto = 'reciclable'
                    break
        else:
            # Usar simulación aleatoria
            reciclable_detectado = random.choice([True, False])
            tipo_objeto = 'reciclable' if reciclable_detectado else 'no_reciclable'

        if reciclable_detectado:
            peso = leer_peso_simulado()
            puntos_acumulados += PUNTOS_POR_PIEZA
            enviar_recompensa_simulada('usuario_simulado', PUNTOS_POR_PIEZA, peso, tipo_objeto)
            print(f"Objeto {tipo_objeto} detectado. Peso: {peso:.1f}g")
        else:
            print("Objeto no reciclable detectado (o ninguno en simulación).")

        # Espera 2 segundos entre simulaciones
        time.sleep(2)

        # Salir si hay imagen y se presiona 'q'
        if frame is not None and cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif frame is None:
            # En simulación sin imagen, salir después de unas iteraciones
            input("Presiona Enter para continuar simulación, o Ctrl+C para salir...")

    if frame is not None:
        cv2.destroyAllWindows()
    print(f"Simulación terminada. Puntos totales: {puntos_acumulados}")

if __name__ == '__main__':
    main()