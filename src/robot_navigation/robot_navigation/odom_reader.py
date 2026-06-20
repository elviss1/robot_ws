import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomReader(Node):
    def __init__(self):
        super().__init__('odom_reader')


        self.subscription = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )

    def odom_callback(self, msg):
        
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        linear_x = msg.twist.twist.linear.x
        angular_z = msg.twist.twist.angular.z  
        self.get_logger().info(
            f'x: {x: .2f}, '
            f'y: {y: .2f}, '
            f'linear_x: {linear_x: .2f}, '
            f'angular_z: {angular_z: .2f}, '
        )

       # 
def main(args=None):

    rclpy.init(args=args)

    node = OdomReader()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()