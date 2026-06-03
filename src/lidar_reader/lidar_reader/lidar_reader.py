import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped                                                                                                                                                                                                               


class LidarReader(Node):

    def __init__(self):
        super().__init__('lidar_reader')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.publisher = self.create_publisher(
            TwistStamped, 
            '/cmd_vel', 
            10    
        )

    def scan_callback(self, msg):

        valid_ranges = [
            r for r in msg.ranges
            if r > 0.0 and math.isfinite(r)
        ]
                                                                                                        
        if len(valid_ranges) > 0:
            nearest = min(valid_ranges)
            nearest_index = msg.ranges.index(nearest)

            angle = (
                msg.angle_min
                + nearest_index * msg.angle_increment
            )
            if nearest < 0.75:

                stop_msg = TwistStamped()

                stop_msg.twist.linear.x = 0.0
                stop_msg.twist.angular.z = 0.0

                self.publisher.publish(stop_msg)

                self.get_logger().info(
                    'Obstacle detected! STOP command sent'
                )

            self.get_logger().info(
                f'Nearest obstacle: {nearest:.2f} m, '
                f'Beam Index: {nearest_index}, '
                f'Angle: {angle:.2f} rad'
            )


def main(args=None):
    rclpy.init(args=args)

    node = LidarReader()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
