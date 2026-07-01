from machine import UART, Pin, mem32, ADC
import time, machine

uart = UART(0, baudrate=9600)
#led  = Pin(2, Pin.OUT)
#led.value(0)

#//////////////////////////////////////////////////////////////////////////////
gpios = [2, 4, 5, 18]

for gpio in gpios:
    Pin(gpio, Pin.OUT)

GPIO_OUT = 0x3FF44004

#//////////////////////////////////////////////////////////////////////////////
def aplicar(nibble):
    for i, led in enumerate(leds):
        led.value((nibble >> i) & 1)

def montar_mascara(padrao_4bits):
    mascara = 0
    for i, gpio_ in enumerate(gpios):
        if (padrao_4bits >> i) & 1:
            mascara |= (1 << gpio_)   # seta o bit correspondente ao GPIO

    return mascara
#//////////////////////////////////////////////////////////////////////////////
valLEDS2 = {
    0    : 0b0000,  #0000  |  0b0000 0000   8 bits
    1023 : 0b0001,  #1024  |  0b0001 0001
    2047 : 0b0011,  #2048  |  0b0001 0011
    3071 : 0b0111,  #3072  |  0b0001 0111
    4095 : 0b1111,  #4096  |  0b0001 1111
}
#//////////////////////////////////////////////////////////////////////////////
while True:
    
    if uart.any():
        dado = uart.read(1)
        if dado == b'\x01':
            led.value(1)
            print("[RX] LED LIGADO")
        elif dado == b'\x00':
            led.value(0)
            print("[RX] LED DESLIGADO")
    time.sleep(0.02)
    
    #//////////////////////////////////////////////////////////////////////////////

    print(valorADC)
    if (valorADC <= 1023):
        resposta = valLEDS2[0]
        mem32[GPIO_OUT] = montar_mascara(resposta)
    elif ((valorADC > 1023) and (valorADC<2047)):
        resposta = valLEDS2[1023]
        mem32[GPIO_OUT] = montar_mascara(resposta)
    elif ((valorADC > 2047) and (valorADC<3071)):
        resposta = valLEDS2[2047]
        mem32[GPIO_OUT] = montar_mascara(resposta)
    elif ((valorADC > 3071) and (valorADC<4095)):
        resposta = valLEDS2[3071]
        mem32[GPIO_OUT] = montar_mascara(resposta)
    elif (valorADC >= 4095):
        resposta = valLEDS2[4095]
        mem32[GPIO_OUT] = montar_mascara(resposta)

    time.sleep(0.1)
