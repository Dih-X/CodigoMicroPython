from machine import UART, Pin, mem32, ADC
import time, machine

uart = UART(0, baudrate=9600)   # UART0 livre na placa física
#botao = Pin(13, Pin.IN, Pin.PULL_UP)
#estado_anterior = 1

#//////////////////////////////////////////////////////////////////////////////

pinoAnalogico = machine.Pin(34)
ADC = machine.ADC(pinoAnalogico)
ADC.atten(machine.ADC.ATTN_11DB)

#//////////////////////////////////////////////////////////////////////////////

while True:
    uart.write(b'\x01')

    subvalorADC = ADC.read()
    valorADC = subvalorADC

    time.sleep(0.1)