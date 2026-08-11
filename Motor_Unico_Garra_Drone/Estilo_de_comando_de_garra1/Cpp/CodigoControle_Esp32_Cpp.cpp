//BROKEN

#include <HardwareSerial.h>

HardwareSerial SerialArbotix(2); // Use UART1

#define RX_PIN 16
#define TX_PIN 17

String comando = "";

void moverServo(byte id, int posicao){
    if(posicao < 0) posicao = 0;
    if(posicao > 1023) posicao = 1023;

    byte posMSB = (posicao >> 8) & 0xFF;
    byte posLSB = posicao & 0xFF;

    SerialArbotix.write(id);
    SerialArbotix.write(posMSB);
    SerialArbotix.write(posLSB);
}

void setup() {
  Serial.begin(115200);
  SerialArbotix.begin(57600, SERIAL_8N1, RX_PIN, TX_PIN);
  delay(1000);
}

void loop(){
    if (Serial.available()){                          // 'beffier' if command central script
        comando = Serial.readStringUntil('\n');      // cmds -> atv, zr, zpi, emr, esc
        comando.trim();                             // zu, zx, zy, zz, esczr
        comando.toLowerCase(); 

        if (comando == "atv"){
            //Serial.println("Servo para 200");
            moverServo(1, 200);
            delay(2000);
        }

        //Serial.println("Servo para 800");
        moverServo(1, 800);
        delay(2000);
    }
}