#include <Wire.h>

const int adcPin = A0;       // ADC-Pin
const int i2cAddress = 8;    // I2C-Adresse

void setup() {
  Wire.begin(i2cAddress);    // Starten der I2C-Kommunikation mit der angegebenen Adresse
  Wire.setClock(400000);
  analogReadResolution(12);  // Setze die Auflösung des ADCs auf 10 Bit
}

void loop() {
  byte data = 0;    // Variable zum Speichern des zu sendenden Bytes
  int bitCount = 0; // Zähler für die Anzahl der erzeugten Bits

  while (bitCount < 8) {
    // Lese ADC-Wert von Pin A0
    int adcValue = analogRead(adcPin);
  
    // Extrahiere das LSB
    byte newBit = adcValue & 0x01;
  
    // Shifte das LSB in das Byte
    data = (data << 1) | newBit;
  
    // Inkrementiere den Bit-Zähler
    bitCount++;
  }
  
  // Sende das Byte über I2C
  Wire.beginTransmission(i2cAddress);
  Wire.write(data);
  Wire.endTransmission();
  
  //delay(10); // Optionale Verzögerung für Stabilität
}
