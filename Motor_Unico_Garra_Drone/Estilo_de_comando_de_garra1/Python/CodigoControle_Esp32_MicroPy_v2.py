import time
from machine import UART

uart = UART(2, baudrate=115200, tx=17, rx=16)

#comando => controla a garra, 0 = fecha, 1 = abre
comando = 0
espera = 2000

tempAnterior = time.ticks_ms()

def mover_servo(servo_id, posicao):
    if posicao < 0:
        posicao = 0
    elif posicao > 1023:
        posicao = 1023

    pos_msb = (posicao >> 8) & 0xFF
    pos_lsb = posicao & 0xFF

    pacote = bytes([servo_id, pos_msb, pos_lsb])
    uart.write(pacote)

while True:
    tempAtual = time.ticks_ms()

    if comando == 1:
        #abre
        if time.ticks_diff(tempAtual, tempAnterior) >= espera:
            mover_servo(servo_id = 1, posicao = 800)
            tempAnterior = tempAtual

    elif comando == 0:  
        #fecha
        if time.ticks_diff(tempAtual, tempAnterior) >= espera:
            mover_servo(servo_id = 1, posicao = 200)
            tempAnterior = tempAtual