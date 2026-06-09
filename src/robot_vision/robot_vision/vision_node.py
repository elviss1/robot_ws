import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
                                                                                                                                                                                                       


class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

    def image_callback(self, msg):

        self.get_logger().info(
            f'Received image: '
            f'{msg.width}x{msg.height}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = VisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()