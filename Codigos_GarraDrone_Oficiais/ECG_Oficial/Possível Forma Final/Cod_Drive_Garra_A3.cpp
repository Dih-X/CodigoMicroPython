
/*

Requer a biblioteca ax12.h
Pacote (ArbotiX Sensor and Servo Library) da Trossen Robotics

Ligação(nesta praca(placa)):
D0/D1 (RX/TX) ->  ESP32 (via divisor de tensão no sentido ArbotiX -> ESP32)
Servo AX-12A  ->  Um dos 3 conectores brancos (AX/S1 bus)

*/

#include <ax12.h>

#define GRIPPER_ID 1      // ID do servo
#define POS_ABERTA 200    // Posição aberta (0-1023)
#define POS_FECHADA 800   // Posição fechada (0-1023)
#define VELOCIDADE 100    // Velocidade de movimento (aparentemente vai de 0-1023 tbm)

void setup(){
    Serial.begin(9600);
    ax12Init(1000000);

    SetSpeed(GRIPPER_ID, VELOCIDADE);
    SetPosition(GRIPPER_ID, POS_ABERTA);
}

void loop(){
    if (Serial.available()){
        char cmd = Serial.read();
        
        if (cmd == 'O'){
            SetPosition(GRIPPER_ID, POS_ABERTA);
        }
        else if (cmd == 'F'){
            SetPosition(GRIPPER_ID, POS_FECHADA);
        }
    }
}