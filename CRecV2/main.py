from machine import UART, Pin, mem32
import time

# --- Configuração da UART ---
uart = UART(0, baudrate=9600, tx=1, rx=3)

# --- Configuração dos pinos dos LEDs ---
gpios = [2, 4, 5, 18]

for gpio in gpios:
    Pin(gpio, Pin.OUT)

# Registrador de saída dos GPIOs de 0 a 31 do ESP32
GPIO_OUT = 0x3FF44004

# Função que monta a máscara de bits baseada nos pinos escolhidos
def montar_mascara(padrao_4bits):
    mascara = 0
    for i, gpio_ in enumerate(gpios):
        if (padrao_4bits >> i) & 1:
            mascara |= (1 << gpio_)   # Seta o bit do GPIO correspondente
    return mascara

# Mapeamento: Chave é o NÍVEL (0 a 4) -> Valor é o padrão de bits desejado (slide)
# 0b0001 (led 1), 0b0011 (led 1 e 2), 0b0111 (led 1, 2 e 3)...
valLEDS = {
    0: 0b0000,
    1: 0b0001,
    2: 0b0011,
    3: 0b0111,
    4: 0b1111,
}

print("Código de Ordens Iniciado...")

# Variável para guardar o último nível aplicado (evita reescrever o mem32 sem necessidade)
ultimo_nivel = -1

while True:
    if uart.any():
        # Lê 1 byte recebido
        dado = uart.read(1)
        nivel_recebido = dado[0] # Converte o byte de volta para inteiro (0 a 4)
        
        # Garante que o valor recebido está no escopo correto para evitar erros
        if nivel_recebido in valLEDS and nivel_recebido != ultimo_nivel:
            padrao_bits = valLEDS[nivel_recebido]
            
            # Aplica a máscara diretamente no registrador usando mem32
            mem32[GPIO_OUT] = montar_mascara(padrao_bits)
            
            print(f"[RX] Nível: {nivel_recebido} | Padrão Aplicado: {bin(padrao_bits)}")
            ultimo_nivel = nivel_recebido
            
    time.sleep(0.05)