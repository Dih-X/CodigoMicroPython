import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
import serial

PORTA_SERIAL = '/dev/ttyTHS1'   # troque para '/dev/ttyUSB0' se usar adaptador FTDI
BAUDRATE = 9600                 # deve bater com o Serial.begin() no ArbotiX-M

CMD_ABRIR = b'O\n'
CMD_FECHAR = b'F\n'

# Devem bater com POS_ABERTA/POS_FECHADA definidos no arbotix_garra.ino
POS_ABERTA = 200
POS_FECHADA = 800
TOLERANCIA = 10


class GarraJetsonNode(Node):
    def __init__(self):
        super().__init__('garra_jetson_node')

        self.serial_arbotix = serial.Serial(PORTA_SERIAL, BAUDRATE, timeout=1)

        self.pub_posicao = self.create_publisher(Int32, '/garra/posicao', 10)
        self.pub_estado = self.create_publisher(String, '/garra/estado', 10)

        self.subscription = self.create_subscription(
            Int32, '/garra/comando', self.callback_comando, 10
        )

        self.em_movimento = False
        # thread separada para ler a serial sem bloquear o rclpy.spin()
        self.thread_leitura = threading.Thread(target=self.ler_serial, daemon=True)
        self.thread_leitura.start()

        self.get_logger().info(
            f'Conectado ao ArbotiX-M em {PORTA_SERIAL}, aguardando comandos em /garra/comando'
        )

    def callback_comando(self, msg):
        if self.em_movimento:
            self.get_logger().warn('Comando ignorado: garra ainda em movimento (aguardando DONE)')
            return

        if msg.data == 1:
            self.serial_arbotix.write(CMD_ABRIR)
            self.em_movimento = True
            self.get_logger().info('Comando ABRIR enviado ao ArbotiX-M')
        elif msg.data == 0:
            self.serial_arbotix.write(CMD_FECHAR)
            self.em_movimento = True
            self.get_logger().info('Comando FECHAR enviado ao ArbotiX-M')
        else:
            self.get_logger().warn(f'Valor invalido recebido: {msg.data} (use 0 ou 1)')

    def ler_serial(self):
        """Roda em thread separada, lendo continuamente o feedback do ArbotiX-M."""
        while rclpy.ok():
            try:
                linha = self.serial_arbotix.readline().decode('utf-8', errors='ignore').strip()
            except serial.SerialException:
                continue

            if not linha:
                continue

            if linha.startswith('POS:'):
                self.processar_posicao(linha[4:], final=False)
            elif linha.startswith('DONE:'):
                self.processar_posicao(linha[5:], final=True)

    def processar_posicao(self, valor_str, final):
        try:
            posicao = int(valor_str)
        except ValueError:
            return

        self.pub_posicao.publish(Int32(data=posicao))

        if final:
            self.em_movimento = False
            if abs(posicao - POS_ABERTA) <= TOLERANCIA:
                estado = 'ABERTA'
            elif abs(posicao - POS_FECHADA) <= TOLERANCIA:
                estado = 'FECHADA'
            else:
                estado = 'PARADA_FORA_DO_ALVO'
            self.get_logger().info(f'Garra confirmou posicao final: {posicao} ({estado})')
        else:
            estado = 'MOVENDO'

        self.pub_estado.publish(String(data=estado))

    def destroy_node(self):
        if self.serial_arbotix.is_open:
            self.serial_arbotix.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GarraJetsonNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()