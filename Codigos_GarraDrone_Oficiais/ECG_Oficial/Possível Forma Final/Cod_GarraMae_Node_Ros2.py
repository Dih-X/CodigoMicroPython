import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

PORTA_SERIAL = '/dev/ttyACMO'
BAUDRATE = 115200

class GarraBridge(Node):
    def __init__(self):
        super().__init__('garra_bridge')
        self.subscription = self.create_subscription(
            Int32,
            '/garra/comando',
            self.listener_callback,
            self.callback_comando,
            10
        )
        self.get_logger().info(f'Conectando à Pico {PORTA_SERIAL} com baudrate {BAUDRATE}, aguardando comandos em garra/comando')

    def callback_comando(self, msg):
        if msg.data == 1:
            self.serial_pico.Write(b'1\n')
            self.get_logger().info('Comando: Abrir Garra')
        elif msg.data == 0:
            self.serial_pico.Write(b'0\n')
            self.get_logger().info('Comando: Fechar Garra')
        else:
            self.get_logger().warn('Comando inválido recebido {msg.data} (use 0 ou 1)')


    def main(args=None):
        rclpy.init(args=args)
        node = GarraBridge()

        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()

    if __name__ == '__main__':
        main()