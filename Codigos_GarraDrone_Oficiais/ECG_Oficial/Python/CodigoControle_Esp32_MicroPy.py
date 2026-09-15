import time
from machine import UART

uart = UART(2, baudrate=115200, tx=17, rx=16)

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
    mover_servo(servo_id = 1, posicao = 200)
    time.sleep(2)

    mover_servo(servo_id = 1, posicao = 800)
    time.sleep(2)