// Código para Arduino: Control de compuerta inteligente
// Recibe señales del script de Python vía serial para activar la compuerta

#define GATE_PIN 9  // Pin para el servo o relé de la compuerta
#define SENSOR_PIN A0  // Pin para sensor de entrada (opcional)
#define LEVEL_SENSOR_PIN A1  // Pin para sensor de nivel del bote

#include <Servo.h>

Servo gateServo;

void setup() {
  Serial.begin(9600);  // Comunicación serial con Python
  gateServo.attach(GATE_PIN);
  gateServo.write(0);  // Posición inicial (cerrada)
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LEVEL_SENSOR_PIN, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'O') {  // Abrir compuerta para botella
      gateServo.write(90);  // Abrir
      delay(2000);  // Mantener abierto 2 segundos
      gateServo.write(0);  // Cerrar
    } else if (command == 'C') {  // Cerrar o para otros residuos
      gateServo.write(0);
    }
  }

  // Monitoreo de sensores (opcional, enviar datos a Python)
  int entryDetected = digitalRead(SENSOR_PIN);
  int level = analogRead(LEVEL_SENSOR_PIN);

  if (entryDetected == HIGH) {
    Serial.println("Entrada detectada");
  }

  if (level > 500) {  // Umbral para nivel alto
    Serial.println("Bote casi lleno");
  }

  delay(100);
}