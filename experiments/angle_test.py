import math

angles = [
    math.radians(179),
    math.radians(181),
    math.radians(-179),
    math.radians(-181),

]

def normalize(angle):
    while angle > math.pi:
        angle -= 2 * math.pi

    while angle < -math.pi:
        angle += 2 * math.pi
    
    return angle

print()
for angle in angles:
    normalized = normalize(angle)

    print(
        f"raw: {math.degrees(angle):7.2f}"
        f" normalized: {math.degrees(normalized):7.2f}"

        )