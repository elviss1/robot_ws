import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped

class WaypointDriver(Node):
    def __init__(self):
        super().__init__('waypoint_driver')
        self.target_x = 2.0
        self.target_y = 1.0
        self.tolerance = 0.1

        self.subscription = self.create_subscription(
            Odometry, 
            '/odom', 
            self.odom_callback, 
            10
        )

        self.publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

    def odom_callback(self, msg):
        
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y

        dx = current_x - self.target_x
        dy = current_y - self.target_y

        distance_to_target = math.sqrt(dx * dx + dy * dy)

        cmd_msg = TwistStamped()

        if distance_to_target > self.tolerance:
            cmd_msg.twist.linear.x = 0.2
            cmd_msg.twist.angular.z = 0.0
            status = "driving"
        else:
            cmd_msg.twist.linear.x = 0.0
            cmd_msg.twist.angular.z = 0.0
            status = "stopped"

        self.publisher.publish(cmd_msg)

        self.get_logger().info(
            f'current: ({current_x:.2f}, {current_y:.2f}), '
            f'target: ({self.target_x:.2f}, {self.target_y:.2f}), '
            f'distance_to_target: {distance_to_target:.2f} m, '
            f'status: {status}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = WaypointDriver()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()        
        

        #qx = msg.pose.pose.orientation.x
        #qy = msg.pose.pose.orientation.y
        #qz = msg.pose.pose.orientation.z
        #qw = msg.pose.pose.orientation.w
