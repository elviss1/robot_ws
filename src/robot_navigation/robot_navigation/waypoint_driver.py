import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan


class WaypointDriver(Node):
    def __init__(self):
        super().__init__('waypoint_driver')

        self.waypoints = [(2.0,2.0), (3.1,3.1), (4.5, 3.9)]
        self.current_waypoints = 0
        self.distance_tolerance = 0.1
        self.heading_tolerance = 0.1
        self.closest_obstacle_distance = float("inf")
        self.safety_distance = 0.5
        self.state = "ROTATING"

        
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

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


    def scan_callback(self, msg):
        front_angle = math.radians(30)

        front_ranges = []

        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i *msg.angle_increment

            if -front_angle <= angle <= front_angle:
                if msg.range_min <= r <= msg.range_max:
                    front_ranges.append(r)
        ranges = list(msg.ranges)

        if front_ranges:
            self.closest_obstacle_distance = min(front_ranges)
        else:
            self.closest_obstacle_distance = float("inf")

    def normalize_angle(self,angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
    
    def odom_callback(self, msg):
        
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        current_yaw = math.atan2(
            2.0 * (qw * qz + qx * qy),
            1.0 - 2.0 * (qy * qy + qz * qz)
        )
        target_x, target_y = self.waypoints[self.current_waypoints]

        dx = target_x - current_x
        dy = target_y - current_y 

        distance_to_goal = math.sqrt(dx * dx + dy * dy)
        desired_heading = math.atan2(dy,dx)
        heading_error = self.normalize_angle(desired_heading - current_yaw)

        cmd_msg = TwistStamped()

        # -------------------------
        # Phase 1: Choose state
        # -------------------------

        if distance_to_goal <= self.distance_tolerance:
            if self.current_waypoints == len(self.waypoints) - 1:
                self.state = "MISSION_COMPLETE"
            else:
                self.current_waypoints += 1
                self.state = "ROTATING"

        elif self.closest_obstacle_distance < self.safety_distance:
            self.state = "BLOCKED"

        elif abs(heading_error) > self.heading_tolerance:
            self.state = "ROTATING"

        else:
            self.state = "DRIVING"


        # -------------------------
        # Phase 2: Execute state
        # -------------------------

        if self.state == "MISSION_COMPLETE":
            cmd_msg.twist.linear.x = 0.0
            cmd_msg.twist.angular.z = 0.0

        elif self.state == "BLOCKED":
            cmd_msg.twist.linear.x = 0.0
            cmd_msg.twist.angular.z = 0.0

        elif self.state == "ROTATING":
            cmd_msg.twist.linear.x = 0.0

            if heading_error > 0:
                cmd_msg.twist.angular.z = 0.4
            else:
                cmd_msg.twist.angular.z = -0.4

        elif self.state == "DRIVING":
            gain = 0.5
            cmd_msg.twist.linear.x = 0.2
            cmd_msg.twist.angular.z = gain * heading_error
        # status = "unknown"

        # if distance_to_goal <= self.distance_tolerance:
        #     if self.current_waypoints == 2:
        #         cmd_msg.twist.linear.x = 0.0
        #         cmd_msg.twist.angular.z = 0.0
        #         status = "stopped"
        #     else:
        #         self.current_waypoints += 1
        #         status = "next_waypoint"

        # elif self.closest_obstacle_distance < self.safety_distance:
        #     cmd_msg.twist.linear.x = 0.0
        #     cmd_msg.twist.angular.z = 0.0
        #     status = "blocked_by_obstacle"
    
        # elif abs(heading_error) > self.heading_tolerance:
        #     cmd_msg.twist.linear.x = 0.0

        #     if heading_error > 0:
        #         cmd_msg.twist.angular.z = 0.4
        #     else:
        #         cmd_msg.twist.angular.z = -0.4

        #     status = "rotating"

        # else:
        #     gain = 0.5
        #     cmd_msg.twist.linear.x = 0.2
        #     cmd_msg.twist.angular.z = gain * heading_error
        #     status = "driving_correcting"

        self.publisher.publish(cmd_msg)

        self.get_logger().info(
            f'current: ({current_x:.2f}, {current_y:.2f}), '
            f'target: ({target_x:.2f}, {target_y:.2f}), '
            f'distance: {distance_to_goal:.2f}, '
            f'yaw: {current_yaw:.2f}, '
            f'desired: {desired_heading:.2f}, '
            f'error: {heading_error:.2f}, '
            f'state: {self.state}, '
            f'obstacle: {self.closest_obstacle_distance:.2f}, '
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
