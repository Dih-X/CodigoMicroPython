#include <HardwareSerial.h>

HardwareSerial SerialArbotix(2); // Use UART1

#define RX_PIN 16
#define TX_PIN 17

void moverServo(byte id, int posicao){
    if(posicao<0) posicao = 0;
    if(posicao>1023) posicao = 1023;

    byte posMSB = (posicao >> 8) & 0xFF;
    byte posLSB = posicao & 0xFF;

    SerialArbotix.write(id);
    SerialArbotix.write(posMSB);
    SerialArbotix.write(posLSB);
}

void setup() {
  Serial.begin(115200);
  SerialArbotix.begin(57600, SERIAL_8N1, RX_PIN, TX_PIN); // Initialize UART1 with specified baud rate and pins
}

void loop(){
    Serial.println("Servo para 200");
    moverServo(1, 200);
    delay(2000);

    Serial.println("Servo para 800");
    moverServo(1, 800);
    delay(2000);
}