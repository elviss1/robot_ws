import math
import numpy as np


def lidar_point_to_world(
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


resolution = 1.0
origin_x = -10.0
origin_y = -10.0

robot_x = 0.0
robot_y = 0.0
robot_yaw = 0.0

distances = [4.0, 4.0, 4.0, 4.0, 4.0]
beam_angles = [
    math.radians(-60),
    math.radians(-30),
    math.radians(0),
    math.radians(30),
    math.radians(60),
]

grid = np.zeros((20,20), dtype = int)

for distance, beam_angle in zip(distances, beam_angles):
    world_x, world_y = lidar_point_to_world(
    robot_x,
    robot_y,
    robot_yaw,
    distance,
    beam_angle
)
    grid_x = int((world_x - origin_x)/resolution)
    grid_y = int((world_y - origin_y)/resolution)
    if 0 <= grid_x < grid.shape[1] and 0 < grid_y <= grid.shape[0]:

        grid[grid_y][grid_x] += 1
print(grid)
print(np.argwhere(grid > 0))