from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=17, rx=16)

CMD_ABRIR = b'O/n'
CMD_FECHAR = b'F/n'

def abrir_garra():
    uart.write(CMD_ABRIR)
    print("Comando enviado: Abrir")

def fechar_garra():
    uart.write(CMD_FECHAR)
    print("Comando enivado: Fechar")

#botoes caso fosse fisico (tera de alterar para comandos eletricos)
botao_abrir = Pin(4, Pin.IN, Pin.PULL_UP)
botao_fechar = Pin(5, Pin.IN, Pin.PULL_UP)

estado_anterior_abrir = 1
estado_anterior_fechar = 1

print("System ready")

while True:
    estado_abrir = botao_abrir.value()
    estado_fechar = botao_fechar.value()

    if estado_abrir == 0 and estado_anterior_abrir == 1:
        abrir_garra()
        time.sleep(0.3)

    if estado_fechar == 0 and estado_anterior_fechar == 1:
        fechar_garra()
        time.sleep(0.3)

    estado_anterior_abrir = estado_abrir
    estado_anterior_fechar = estado_fechar

    time.sleep(0.02)
