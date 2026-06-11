import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
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

        self.bridge = CvBridge()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(
        msg,
        desired_encoding='bgr8'
    )

        self.get_logger().info(
        f'OpenCV image shape: {cv_image.shape}'
    )

        self.get_logger().info(
            f'Width: {msg.width}'
            f'Height: {msg.height}'
            f'Encoding: {msg.encoding}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = VisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()