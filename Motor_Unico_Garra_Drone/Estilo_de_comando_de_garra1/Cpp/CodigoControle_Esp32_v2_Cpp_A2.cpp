#include <HardwareSerial.h>

HardwareSerial SerialArbotix(2); // Use UART1
//#define SerialArbotix 2
//int SerialArbotix 2;

#define RX_PIN 16
#define TX_PIN 17

String comando = "";
unsigned long waitTime = 0;

void setup() {
    //Serial.begin(57600);
    Serial.begin(115200);

    SerialArbotix.begin(57600, SERIAL_8N1, RX_PIN, TX_PIN);
    //SerialArbotix.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);

    Serial.begin(9600);
    delay(100);
}

/*
void moverServo(byte id, int posicao){
    if(posicao < 0) posicao = 0;
    if(posicao > 1023) posicao = 1023;

    byte posMSB = (posicao >> 8) & 0xFF;
    byte posLSB = posicao & 0xFF;

    SerialArbotix.write(id);
    SerialArbotix.write(posMSB);
    SerialArbotix.write(posLSB);
}
*/

void loop(){
    if (Serial.available()){                          
        comando = Serial.readStringUntil('\n');      // cmds -> atv, ret
        comando.trim();                             
        comando.toLowerCase();

        waitTime = millis();

        if (comando == "atv"){
            if (millis() - waitTime >= 2000){
                //Serial.println("Servo para 200");
                moverServo(1, 1023);
                //delay(2000);
            }

        } else if (comando == "ret"){

            if (millis() - waitTime >= 2000){
                //Serial.println("Servo para 800");
                moverServo(1, 0);
                //delay(2000);
            }
        }
    }
}