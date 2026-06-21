import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomReader(Node):
    def __init__(self):
        super().__init__('odom_reader')


        self.subscription = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )

    def odom_callback(self, msg):
        
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        linear_x = msg.twist.twist.linear.x
        angular_z = msg.twist.twist.angular.z  

        yaw = math.atan2(
            2.0 * (qw * qz + qx * qy),
            1.0 - 2.0 * (qy * qy + qz * qz)
        )
        
        self.get_logger().info(
            f'x: {x:.2f}, '
            f'y: {y:.2f}, '
            f'yaw: {yaw:.2f} rad'
            f'linear_x: {linear_x: .2f}, '
            f'angular_z: {angular_z: .2f}, '
        )
        # self.get_logger().info(
        #     f'x: {x: .2f}, '
        #     f'y: {y: .2f}, '
        #     f'linear_x: {linear_x: .2f}, '
        #     f'angular_z: {angular_z: .2f}, '
        # )

       # 
def main(args=None):

    rclpy.init(args=args)

    node = OdomReader()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()