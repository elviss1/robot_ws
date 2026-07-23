import math

def lidar_point_world(
    robot_x,
    robot_y,
    robot_yaw,
    distance,
    beam_angle
):
    
    world_angle = robot_yaw + beam_angle
    obstacle_x = robot_x + distance * math.cos(world_angle)
    obstacle_y = robot_y + distance * math.sin(world_angle)

    return obstacle_x, obstacle_y

obstacle_x, obstacle_y = lidar_point_world(
    robot_x = 2.0,
    robot_y = 3.0,
    robot_yaw = 0.0,
    distance = 4.0,
    beam_angle = math.radians(60)

)

print(obstacle_x, obstacle_y)