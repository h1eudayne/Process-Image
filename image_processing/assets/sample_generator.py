"""
Sample Image Generator
Creates a test image with shapes for learning exercises.
Run this script first to generate assets/sample.jpg
"""

import numpy as np
import cv2
import os

def generate_sample_image():
    """Create a 640x480 image with colorful shapes for testing."""
    img = np.ones((480, 640, 3), dtype=np.uint8) * 255

    cv2.rectangle(img, (50, 50), (200, 180), (255, 100, 0), -1)

    cv2.circle(img, (320, 240), 80, (0, 200, 0), -1)

    pts = np.array([[480, 100], [560, 280], [400, 280]], np.int32)
    cv2.fillPoly(img, [pts], (0, 0, 255))

    cv2.ellipse(img, (150, 380), (90, 50), 0, 0, 360, (0, 255, 255), -1)

    cv2.rectangle(img, (450, 330), (550, 430), (200, 0, 200), -1)

    cv2.putText(img, "OpenCV Learning", (150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    for x in range(640):
        color = (int(255 * x / 640), 0, int(255 * (640 - x) / 640))
        cv2.line(img, (x, 460), (x, 480), color, 1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "sample.jpg")
    cv2.imwrite(output_path, img)
    print(f"[OK] Anh mau da duoc tao: {output_path}")
    print(f"     Kich thuoc: {img.shape[1]}x{img.shape[0]} pixels")
    print(f"     Channels: {img.shape[2]} (BGR)")

    return output_path


if __name__ == "__main__":
    generate_sample_image()
