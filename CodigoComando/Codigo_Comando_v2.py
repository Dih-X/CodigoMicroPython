from machine import UART, Pin
import time

# --- Configuração da UART ---
uart = UART(0, baudrate=9600, tx=1, rx=3)

# --- Configuração dos Botões ---
btn_subir = Pin(26, Pin.IN, Pin.PULL_UP)
btn_descer = Pin(27, Pin.IN, Pin.PULL_UP)
btn_zerar = Pin(13, Pin.IN, Pin.PULL_UP)

b_subir_ant = 1
b_descer_ant = 1
b_zerar_ant = 1

# Nível começa em 0 e vai até 4 (para 4 leds)
nivel = 0

print("Código de Comando Iniciado (Controle de Níveis)...")

while True:
    b_subir_at = btn_subir.value()
    b_descer_at = btn_descer.value()
    b_zerar_at = btn_zerar.value()
    
    # Botão Subir (Máximo nível 4)
    if b_subir_ant == 1 and b_subir_at == 0:
        if nivel < 4:
            nivel += 1
        time.sleep(0.05) # Debounce
        
    # Botão Descer (Mínimo nível 0)
    if b_descer_ant == 1 and b_descer_at == 0:
        if nivel > 0:
            nivel -= 1
        time.sleep(0.05) # Debounce
        
    # Botão Zerar
    if b_zerar_ant == 1 and b_zerar_at == 0:
        nivel = 0
        time.sleep(0.05) # Debounce
        
    b_subir_ant = b_subir_at
    b_descer_ant = b_descer_at
    b_zerar_ant = b_zerar_at

    # Envia o nível atual como um byte bruto (ex: b'\x00', b'\x01', etc.)
    # bytes([nivel]) transforma o número inteiro em um byte
    uart.write(bytes([nivel]))
    
    time.sleep(0.1)