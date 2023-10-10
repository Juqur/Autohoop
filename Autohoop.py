import datetime
import time
from openni import openni2
from primesense import _openni2 as c_api
import matplotlib.pyplot as plt
import numpy as np
import cv2
import serial

GRAY_COLOR = (64, 64, 64)
CAPTURE_SIZE_KINECT = (512, 424)
CAPTURE_SIZE_OTHERS = (640, 480)

MIN_DEPTH_CAPTURE_DISTANCE = 0.35
MAX_DEPTH_CAPTURE_DISTANCE = 0.1
MAX_DISTANCE = 440

MAX_HORIZONTAL_DISTANCE = 478
HORIZONTAL_SCREEN_SIZE = 512

MAX_VERTICAL_DISTANCE = 346
VERTICAL_SCREEN_SIZE = 424

MAX_DISTANCE_FROM_CENTER_X = 50
MIN_SHOT_HEIGHT = MAX_VERTICAL_DISTANCE - 100

LENGTH = 38
HEIGHT = 41

CAMERA_ANGLE = np.radians(-20)
CAMERA_POSITION = np.array([30, 125, -30])

ser = serial.Serial('COM3', 9600)

def rotate_x():
    c = np.cos(CAMERA_ANGLE)
    s = np.sin(CAMERA_ANGLE)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def transform_coordinates(coords):
    translated_coords = coords - CAMERA_POSITION
    rotation_matrix = rotate_x()
    rotated_coords = np.dot(rotation_matrix, translated_coords)
    final_coords = rotated_coords
    return final_coords


def predict_position(x0, x1, y0, y1, z0, z1, dt):
    vx = (x1 - x0) / dt
    vy = (y1 - y0) / dt
    vz = (z1 - z0) / dt
    a = -0.5 * 9.81 * pow(10, -12) #dt is in microseconds
    tz = (MAX_DISTANCE - z0) / vz #time it takes to reach the hoop
    x = x0 + vx * tz
    y = y0 + vy * tz + a*(pow(tz, 2))
    if abs(x - MAX_HORIZONTAL_DISTANCE / 2) <= MAX_DISTANCE_FROM_CENTER_X and y > MIN_SHOT_HEIGHT:
        x = (1 - (((x - MAX_HORIZONTAL_DISTANCE / 2) + MAX_DISTANCE_FROM_CENTER_X) / (
                    MAX_DISTANCE_FROM_CENTER_X * 2))) * 100
        y = (MAX_VERTICAL_DISTANCE - y)/(MAX_VERTICAL_DISTANCE - MIN_SHOT_HEIGHT) * 100
        position_data = f"{x},{y}\n"
        ser.write(position_data.encode())

    print(f"Speeds (vx, vy, vz): ({vx:.4f}, {vy:.4f}, {vz:.4f})")
    print(f"Time Difference (dt): {dt:.2f}")
    print(f"Initial Position (x0, y0, z0): ({x0:.2f}, {y0:.2f}, {z0:.2f})")
    print(f"Initial Position (x1, y1, z1): ({x1:.2f}, {y1:.2f}, {z1:.2f})")
    print(f"Predicted Position: x = {x:.2f}, y = {y:.2f}")
    print("-------------------")


def get_position():
    openni2.initialize()
    if (openni2.is_initialized()):
        print
        "openNI2 initialized"
    else:
        print
        "openNI2 not initialized"

    ## Register the device
    dev = openni2.Device.open_any()

    ## Create the streams stream
    depth_stream = dev.create_depth_stream()

    ## Configure the depth_stream -- changes automatically based on bus speed
    # print 'Get b4 video mode', depth_stream.get_video_mode() # Checks depth video configuration
    depth_stream.set_video_mode(
        c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320,
                           resolutionY=240, fps=30))

    ## Start the streams
    depth_stream.start()

    x_array = []
    y_array = []
    z_array = []

    start_time = datetime.datetime.now()

    i = 0
    while True:
        delta_time = datetime.datetime.now() - start_time
        dmap = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(240,
                                                                                                        320)  # Works & It's FAST
        d4d = np.uint8(dmap.astype(float) * 255 / 2 ** 12 - 1)  # Correct the range. Depth images are 12bits
        d4d = cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
        # Define the threshold for white color (adjust this value as per your requirement)
        white_threshold = 70
        # Transform colors that are too white into pitch black
        white_pixels = np.all(d4d < white_threshold, axis=-1)
        d4d[white_pixels] = [255, 255, 255]

        # Invert the image
        d4d = 255 - d4d
        y, x, _ = np.unravel_index(np.argmax(d4d), d4d.shape)
        z = d4d.max()
        d4d[y, x] = [255, 255, 0]
        x = x / 320
        y = y / 240
        z = z / 255
        depth = z * MAX_DISTANCE
        width = (x * MAX_HORIZONTAL_DISTANCE * z)
        height = ((1 - y) * MAX_VERTICAL_DISTANCE * z)
        print(transform_coordinates(np.array([width, height, depth])), np.array(np.array([width, height, depth])))
        time.sleep(0.25)
        if (depth > 315):
            x_array.append(width)
            y_array.append(depth)
            z_array.append(height)
            if (len(x_array) > 2):
                i += 1
                predict_position(x_array[-2], x_array[-1], z_array[-2], z_array[-1], y_array[-2], y_array[-1],
                                delta_time.microseconds)
                if (i == 5):
                    break

        cv2.imshow('depth', d4d)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    depth_stream.stop()
    openni2.unload()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([MAX_HORIZONTAL_DISTANCE / 2], [MAX_DISTANCE], [MAX_VERTICAL_DISTANCE], c='red', marker='o', s=100,
               label='Camera')
    ax.scatter(x_array, y_array, z_array, c=np.arange(len(x_array)), cmap='cool')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    ax.set_zlim(0, 500)
    plt.show()
    ser.close()


if __name__ == '__main__':
    get_position()
