import numpy as np
import math

def lidar_point_world(
    robot_x,
    robot_y,
    robot_yaw,
    distance,
    beam_angle
):
    
    world_angle = robot_yaw + beam_angle
    world_x = robot_x + distance * math.cos(world_angle)
    world_y = robot_y + distance * math.sin(world_angle)

    return world_x, world_y

world_x, world_y = lidar_point_world(
    robot_x = 2.0,
    robot_y = 3.0,
    robot_yaw = 0.0,
    distance = 4.0,
    beam_angle = math.radians(60)

)

#print(obstacle_x, obstacle_y)

grid = np.zeros((20,20), dtype = int)
resolution = 1.0
origin_x = 0.0
origin_y = 0.0

grid_x = int((world_x - origin_x)/resolution)
grid_y = int((world_y - origin_y)/resolution)

grid[grid_y][grid_x] += 1

print(grid)
print(grid_x.shape)