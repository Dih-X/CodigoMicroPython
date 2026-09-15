import time
import sys
import uselect
from machine import UART

uart = UART(2, baudrate=57600, tx=17, rx=16)

comando = None
tempo_comando = time.ticks_ms()
espera = 2000

entrada = uselect.poll()
entrada.register(sys.stdin, uselect.POLLIN)


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
    eventos = entrada.poll(0)
    if eventos:
        texto = sys.stdin.readline()
        if texto:
            texto = texto.strip().lower()
            if texto in ("atv", "ret"):
                comando = texto
                tempo_comando = time.ticks_ms()

    if comando is not None and time.ticks_diff(time.ticks_ms(), tempo_comando) >= espera:
        posicao = 1023 if comando == "atv" else 0
        mover_servo(servo_id=1, posicao=posicao)
        comando = None