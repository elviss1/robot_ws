2026-06-06

Day 7: Add obstacle confirmation filter

Changes:
✓ Added obstacle_count state variable
✓ Robot now requires 3 consecutive detections
✓ Introduced memory across scans
✓ Reduced sensitivity to single bad readings

Learned:
✓ State vs local variables
✓ Sensor noise and false positives
✓ Filtering before decision-making



2026-06-07

Day 8: Perceive-Decide-Act Architecture

Built:
✓ perceive()
✓ decide()
✓ act()

Learned:
✓ Function outputs become inputs
✓ Separation of concerns
✓ Architecture emerges after building
✓ Don't solve the project, solve the next problem



2026-06-08
Day 9: First Vision Node

Built:
✓ Switched to waffle_pi
✓ Camera topic discovered
✓ Subscribed to /camera/image_raw
✓ Created robot_vision package

Learned:
✓ Image is the camera equivalent of LaserScan
✓ Sensors follow the same ROS pattern
✓ Camera publishes sensor_msgs/msg/Image
✓ Width and height represent image resolution
