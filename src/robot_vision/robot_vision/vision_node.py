import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped
from cv_bridge import CvBridge    
import cv2                                                                                                                                                           


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

        hsv_image = cv2.cvtColor(
            cv_image,
            cv2.COLOR_BGR2HSV
        )

        lower_green = (40, 50, 50)
        upper_green = (80, 255, 255)

        green_mask = cv2.inRange(
            hsv_image,
            lower_green,
            upper_green
        )

        height, width = green_mask.shape
        third = width // 3

        left_region = green_mask[:, :third]
        center_region = green_mask[:, third:2 * third]
        right_region = green_mask[:, 2 * third:]

        left_count = cv2.countNonZero(left_region)
        center_count = cv2.countNonZero(center_region)
        right_count = cv2.countNonZero(right_region)
        centre_y = cv_image.shape[0] // 2
        centre_x = cv_image.shape[1] // 2

        centre_pixel = cv_image[centre_y, centre_x]


        target_region = self.find_target_region(
            left_count,
            center_count,
            right_count
        )
        linear, angular = self.decide(target_region)

        self.act(linear, angular)

        self.get_logger().info(
            f'Center pixel BGR: {centre_pixel}, '
            f'Image shape: {cv_image.shape}, '
            f'Mask shape: {green_mask.shape}, '
            f'Left: {left_count}, '
            f'Center: {center_count}, '
            f'Right: {right_count}, '
            f'Target: {target_region}, '
            f'Linear: {linear:.1f}, '
            f'Angular: {angular:.1f}'
        
)

    def find_target_region(self, left_count, center_count, right_count):

        if left_count == 0 and center_count == 0 and right_count == 0:
            return "none"

        if left_count > center_count and left_count > right_count:
            return "left"

        if center_count > left_count and center_count > right_count:
            return "center"

        if right_count > left_count and right_count > center_count:
            return "right"

        return "none"
     

    def decide(self, target_region):

        if target_region == "left":
            return 0.0, 1.0

        if target_region == "center":
            return 0.3, 0.0

        if target_region == "right":
            return 0.0, -1.0

        return 0.0, 0.0
    
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