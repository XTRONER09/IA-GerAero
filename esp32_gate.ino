// Código para ESP32: Control de compuerta inteligente con WiFi
// Recibe comandos del script de Python vía HTTP para activar la compuerta

#include <WiFi.h>
#include <WebServer.h>
#include <Servo.h>

#define GATE_PIN 13  // Pin para el servo (GPIO 13)
#define SENSOR_PIN 34  // Pin para sensor de entrada (GPIO 34, ADC)
#define LEVEL_SENSOR_PIN 35  // Pin para sensor de nivel (GPIO 35, ADC)

const char* ssid = "TuSSID";  // Reemplaza con tu SSID WiFi
const char* password = "TuPassword";  // Reemplaza con tu contraseña WiFi

WebServer server(80);
Servo gateServo;

void setup() {
  Serial.begin(115200);
  gateServo.attach(GATE_PIN);
  gateServo.write(0);  // Posición inicial (cerrada)

  // Conectar a WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Definir rutas del servidor
  server.on("/open", HTTP_GET, []() {
    gateServo.write(90);  // Abrir compuerta
    delay(2000);
    gateServo.write(0);  // Cerrar
    server.send(200, "text/plain", "Compuerta abierta para botella");
  });

  server.on("/close", HTTP_GET, []() {
    gateServo.write(0);  // Cerrar compuerta
    server.send(200, "text/plain", "Compuerta cerrada");
  });

  server.on("/status", HTTP_GET, []() {
    int entry = analogRead(SENSOR_PIN);
    int level = analogRead(LEVEL_SENSOR_PIN);
    String response = "Entrada: " + String(entry) + ", Nivel: " + String(level);
    server.send(200, "text/plain", response);
  });

  server.begin();
  Serial.println("Servidor HTTP iniciado");
}

void loop() {
  server.handleClient();

  // Monitoreo adicional si es necesario
  delay(10);
}