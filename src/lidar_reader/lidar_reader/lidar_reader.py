import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarReader(Node):

    def __init__(self):
        super().__init__('lidar_reader')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):

        valid_ranges = [r for r in msg.ranges if r > 0.0]

        if len(valid_ranges) > 0:
            nearest = min(valid_ranges)
            self.get_logger().info(
                f'Nearest obstacle: {nearest:.2f} m'
            )


def main(args=None):
    rclpy.init(args=args)

    node = LidarReader()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
