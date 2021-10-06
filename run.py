import cv2
import numpy
import time
from camera import Camera
from detector import Detector
from pid import PI

def main():

    # Sample time
    dt = 1.0 / 30.0

    # Camera
    camera = Camera('./assets/obj_000005.obj', dt)

    # Detector
    detector = Detector()

    # Target
    target = numpy.array([camera.width / 2, camera.height / 2])

    # Controller
    pi_x = PI(0.01, 0.0, dt)
    pi_y = PI(0.01, 0.0, dt)

    # Total time
    t = 0.0

    while True:

        # Input image
        rgb = camera.rgb()

        # Detector
        feedback = detector.detect(rgb)

        # Error
        error = target - feedback

        # Control
        x_dot = pi_x.control(error[1])
        y_dot = pi_y.control(error[0])
        camera.move(x_dot, y_dot)

        cv2.imshow('Viewer', rgb)

        cv2.waitKey(int(dt * 1000))

        if t > 4.0:
            camera.randomize_object()
            rgb = camera.rgb()
            cv2.imshow('Viewer', rgb)
            cv2.waitKey(3000)
            t = 0.0
        else:
            t += dt


if __name__ == '__main__':
    main()
