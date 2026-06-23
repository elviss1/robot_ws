import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped

class DistanceDriver(Node):
    def __init__(self):
        super().__init__('distance_driver')
        self.target_distance = 1.0
        self.start_x = None
        self.start_y = None

        self.subscription = self.create_subscription(
            Odometry, 
            '/odom', 
            self.odom_callback, 
            10
        )

        self.publisher = self.create_publisher(
            TwistStamped,
            'cmd_vel',
            10
        )

    def odom_callback(self, msg):
        
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y

        if self.start_x == None:
            self.start_x = current_x
            self.start_y = current_y

        dx = current_x - self.start_x
        dy = current_y - self.start_y


        distance_moved = math.sqrt(dx * dx + dy * dy)

        cmd_msg = TwistStamped()

        if distance_moved < self.target_distance:
            cmd_msg.twist.linear.x = 0.2
            cmd_msg.twist.angular.z = 0.0
            status = "driving"
        else:
            cmd_msg.twist.linear.x = 0.0
            cmd_msg.twist.angular.z = 0.0
            status = "stopped"

        self.publisher.publish(cmd_msg)

        self.get_logger().info(
            f'distance: {distance_moved:.2f} m, '
            f'target: {self.target_distance:.2f} m, '
            f'status: {status}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = DistanceDriver()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()        
        

        #qx = msg.pose.pose.orientation.x
        #qy = msg.pose.pose.orientation.y
        #qz = msg.pose.pose.orientation.z
        #qw = msg.pose.pose.orientation.w
