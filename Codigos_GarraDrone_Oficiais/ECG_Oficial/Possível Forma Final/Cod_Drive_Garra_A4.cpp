/*
Esta versão consegue retornar a localização atual do servo

Requer a biblioteca ax12.h
Pacote (ArbotiX Sensor and Servo Library) da Trossen Robotics

Ligação(nesta praca(placa)):
D0/D1 (RX/TX) ->  ESP32 (via divisor de tensão no sentido ArbotiX -> ESP32)
Servo AX-12A  ->  Um dos 3 conectores brancos (AX/S1 bus)
*/

#include <ax12.h>

#define GRIPPER_ID 1           // ID do servo
#define POS_ABERTA 200         // Posição aberta (0-1023)
#define POS_FECHADA 800        // Posição fechada (0-1023)
#define VELOCIDADE 100         // Velocidade de movimento (aparentemente vai de 0-1023 tbm)
#define TOLERANCIA 10          // margem de erro aceita como "chegou no destino"
#define INTERVALO_FEEDBACK 100 // ms entre leituras da poisicao durante o movimento

int posicao_alvo = POS_ABERTA;
bool em_movimento = false;
unsigned long ultimo_feedback = 0;

void setup(){
    Serial.begin(9600);
    ax12Init(1000000);

    SetSpeed(GRIPPER_ID, VELOCIDADE);
    SetPosition(GRIPPER_ID, POS_ABERTA);
    posicao_alvo = POS_ABERTA;
}

void loop(){
    if (Serial.available()){
        char cmd = Serial.read();
        
        if (cmd == 'O'){
            posicao_alvo = POS_ABERTA;
            SetPosition(GRIPPER_ID, POS_ABERTA);
            em_movimento = true;
        }
        else if (cmd == 'F'){
            posicao_alvo = POS_FECHADA;
            SetPosition(GRIPPER_ID, POS_FECHADA);
            em_movimento = true;
        }

        if(em_movimento && (millis() - ultimo_feedback >= INTERVALO_FEEDBACK)){
            ultimo_feedback = millis();
            
            int pos_atual = GetPosition(GRIPPER_ID);

            if(pos_atual < 0){
                return; // erro na leitura da posição
            }

        Serial.print("POS:");
        Serial.println(pos_atual);

        if(abs(pos_atual - posicao_alvo) <= TOLERANCIA){
            em_movimento = false;
            Serial.print("DONE:")
            Serial.println(pos_atual);
        }
    }
}