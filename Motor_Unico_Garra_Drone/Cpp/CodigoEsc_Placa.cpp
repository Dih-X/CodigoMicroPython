#include <ax12.h>
#include <BioloidController.h>

BioloidController bioloid = BioloidController(1000000);

void setup(){
    Serial.begin(115200);
}

void loop(){
    if (Serial.available()>=3){

        int id = Serial.read();
        int posMSB = Serial.read();
        int posLSB = Serial.read();
        int posicao = (posMSB << 8) + posLSB;
        SetPosition(id, posicao);
        
    }
}