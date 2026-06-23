Phase 1: Foundations
--------------------
Perceive
Decide
Act

Phase 2: Domain Sampling
------------------------
Perception
✓

Navigation
NEXT

Manipulation

Planning

Systems

Phase 3: Choose 1-2 Domains
------------------------
Phase 4: Deep Projects
------------------------
Phase 5: Hardware
------------------------


Checkpoints For The Roadmap
This is more important than the timeline itself.

Phase 1 — Foundations
Goal:
Understand robot architecture.
Checkpoint:
Can you explain from memory:
Sensor
↓
Perceive
↓
Decide
↓
Act

Can you build:
Subscriber
↓
Logic
↓
Publisher
without looking at notes?
If yes:
Pass.

Phase 2 — Domain Sampling
Goal:
Touch the major domains.
Checkpoint:
Could you explain to a beginner:
Perception

Navigation

Manipulation

Planning

Systems
in plain English?
Could you build a tiny project in each?
If yes:
Pass.

Phase 3 — Domain Selection
Goal:
Choose 1-2 domains.
Checkpoint:
Can you answer:
What am I best at?
What do I enjoy?
What does industry need?
If you cannot answer all three:
Don't specialize yet.

Phase 4 — Deep Projects
Goal:
Build portfolio-worthy work.
Checkpoint:
Could a recruiter spend 5 minutes on your GitHub and say:
This person can build robots.
If not:
Project isn't deep enough.

Phase 5 — First Job Readiness
[certain]
This is the real checkpoint.
Not:
Did I finish the roadmap?
But:

Can I sit in a robotics team's standup
and understand the conversation?
Topics mentioned:

ROS

Topics

Nodes

Sensors

Localization

Navigation

Transforms

Control

Simulation

If those are familiar rather than intimidating:
You're close.

My current assessment:

Phase 1:
~90-95% complete

Job readiness:
~10-15%

Reason:
You understand architecture now.

You do not yet understand navigation,
localization,
planning,
deployment,
or hardware integration.

That's not a criticism.

That's actually good news.

The hardest part for most beginners is reaching the point where robotics stops looking like magic.

You're crossing that boundary now. The next domains build on the same mental model rather than replacing it.



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


2026-06-16
Day 10-11: First Vision Node
Camera
↓
ROS Image
↓
OpenCV Image
↓
Average BGR
↓
Dominant Color
↓
Decision
↓
Motion Command

✓ Camera subscriber
✓ ROS Image → OpenCV conversion
✓ Average BGR extraction
✓ Dominant color detection
✓ Vision-based decision
✓ Vision-based actuation

Pipeline:

Perceive
↓
Camera
↓
Dominant color

Decide
↓
Choose velocities

Act


2026-06-18
Day 13 Artifact

Image
↓
HSV
↓
Mask
↓
Left / Center / Right
↓
Target Region
↓
Motion Command
↓
Publish /cmd_vel



2026-06-19
Day 14 – Navigation: Odometry and Robot State

Built an odometry reader node.

Key concepts:
- Odometry
- Position
- Velocity
- Reference frames

Key takeaway:
Odometry describes where the robot is and how it is moving relative to a reference frame.

Can inspect ROS message definitions and extract useful fields independently.



2026-06-20
Day 15 – Navigation: Pose Tracking

Built an odometry-based pose tracker.

Key concepts:
- Position (x, y)
- Orientation (quaternion)
- Yaw (human-readable heading)

Key takeaway:
Pose = Position + Orientation

Can interpret robot heading and describe robot state relative to the odom frame.




2026-06-21
Day 16 – Navigation: Motion and Pose Evolution

Observed how velocity commands affect robot pose over time.

Key concepts:
- Linear velocity
- Angular velocity
- Pose evolution

Key takeaway:
Translation changes position.
Rotation changes orientation.

Can interpret odometry changes as physical robot movement.



2026-06-22
Day 17 – Navigation: Distance-Based Motion

Built a distance driver using odometry.

Key concepts:
- Distance traveled
- Goal condition
- State-based decision making

Key takeaway:
Navigation behaviors can be driven by robot state rather than direct sensor reactions.

Can command the robot to move a target distance and stop automatically.
