import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped
from cv_bridge import CvBridge                                                                                                                                                               


class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.publisher = self.create_publisher(
            TwistStamped, 
            '/cmd_vel', 
            10
        )

        self.bridge = CvBridge()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
)
        centre_y = cv_image.shape[0] // 2
        centre_x = cv_image.shape[1] // 2

        centre_pixel = cv_image[centre_y, centre_x]

        mean_bgr = cv_image.mean(axis=(0, 1))

        blue = mean_bgr[0]
        green = mean_bgr[1]
        red = mean_bgr[2]
        if green > blue and green > red:
            dominant_color = "green"
        elif blue > green and blue > red:
            dominant_color = "blue"
        else:
            dominant_color = "red/other"

        linear, angular = self.decide(dominant_color)
        self.act(linear, angular)
        
        self.get_logger().info(
            f'Blue: {blue:.1f}, '
            f'Green: {green:.1f}, '
            f'Red: {red:.1f}, '
            f'Dominant: {dominant_color}, '
            f'Linear: {linear:.1f}, '
            f'Angular: {angular:.1f}'
)
        

    def decide(self, dominant_color):
        if dominant_color == 'green':
            return 0.1, 0.2
        return 0.0,0.0
    
    def act(self, linear, angular):
        cmd_msg = TwistStamped()
        cmd_msg.twist.linear.x = linear
        cmd_msg.twist.angular.z = angular
        
        self.publisher.publish(cmd_msg)
        

        

def main(args=None):

    rclpy.init(args=args)

    node = VisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()