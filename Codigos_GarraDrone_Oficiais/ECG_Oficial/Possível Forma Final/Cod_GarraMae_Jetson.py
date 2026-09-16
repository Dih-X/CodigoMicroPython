import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

PORTA_SERIAL = '/dev/ttyTHS1'
BAUDRATE = 9600

CMD_ABRIR = b'O\n'
CMD_FECHAR = b'F\n'

class GarraJetsonNode(Node):
    def __init__(self):
        super().__init__('garra_jetson_node')

        self.serial_arbotix = serial.Serial(PORTA_SERIAL, BAUDRATE, timeout=1)

        self.subscription = self.create_subscription(
            Int32,
            '/garra/comando',
            self.callback_comando,
            10
        )

        self.get_logger().info(
            f'Conectado ao ArbotiX-M em {PORTA_SERIAL}, aguardando comando em /garra/comando'
        )

    def callback_comando(self, msg):
        if msg.data == 1:
            self.serial_arbotix.write(CMD_ABRIR)
            self.get_logger().info('Comando ABRIR enviado...')
        elif msg.data == 0:
            self.serial_arbotix.write(CMD_FECHAR)
            self.get_logger().info('Comando FECHAR enviado...')
        else:
            self.get_logger().warn(f"Valor invalido recebido: {msg.data} (use 0 ou 1)")

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