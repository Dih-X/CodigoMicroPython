from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=1, rx=3)

btn_subir = Pin(26, Pin.IN, Pin.PULL_UP)
btn_descer = Pin(27, Pin.IN, Pin.PULL_UP)
btn_zerar = Pin(13, Pin.IN, Pin.PULL_UP)

b_subir_ant = 1
b_descer_ant = 1
b_zerar_ant = 1

nivel = 0

#print("Código de Comando Iniciado (Controle de Níveis)...")

while True:
    b_subir_at = btn_subir.value()
    b_descer_at = btn_descer.value()
    b_zerar_at = btn_zerar.value()
    
    if b_subir_ant == 1 and b_subir_at == 0:
        if nivel < 4:
            nivel += 1
        time.sleep(0.05) # Debounce

    if b_descer_ant == 1 and b_descer_at == 0:
        if nivel > 0:
            nivel -= 1
        time.sleep(0.05) # Debounce
        
    if b_zerar_ant == 1 and b_zerar_at == 0:
        nivel = 0
        time.sleep(0.05) # Debounce
        
    b_subir_ant = b_subir_at
    b_descer_ant = b_descer_at
    b_zerar_ant = b_zerar_at

    uart.write(bytes([nivel]))
    
    time.sleep(0.1)