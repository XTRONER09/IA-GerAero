#include <Wire.h>
#include "HX711.h"

#define DOUT  18
#define CLK   19

HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando ESP32 HX711...");

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare();

  Serial.println("Listo para leer peso");
}

void loop() {
  if (scale.is_ready()) {
    float peso = scale.get_units(10); // promedio 10 lecturas
    // Enviar peso en gramos por serial
    Serial.println(peso);
  } else {
    Serial.println("Balanza no lista");
  }

  delay(500); // cada 0.5s
}
