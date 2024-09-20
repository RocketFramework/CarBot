#!/usr/bin/python3
import time

import cv2
import libcamera

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder
from motor_movement import move_horizontally as move_horizontally


# This is like opencv_face_detect_2.py, only we draw the face boxes on a
# recorded video. We have to use the "post_callback" to draw the faces because
# we want capture_buffer to get the image without face boxes, but then we
# want the boxes drawn before handing the image to the encoder.

face_detector = cv2.CascadeClassifier("/home/pi/Documents/haarcascade_frontalface_default.xml")

fx = None
motor_moving = False
MAX_QUEUE_LENGTH = 5  # Adjust the maximum length according to your requirements
my_queue = []

def distance(x1, x2):
    # Helper function to calculate the distance between two x values
    return abs(x1 - x2)

def enqueue(value, x_gap_threshold):
    global my_queue
    unique_list = []
    # Check if the queue is not empty and the new value is not too close to the last value
    if my_queue:
        if distance(value[0], my_queue[-1][0]) < x_gap_threshold:
            return
# """         elif len(value)>3:    
#             for v in value:
#                 if v not in unique_list:
#                     unique_list.append(v)
#     if len(unique_list)>0:          
#         value = unique_list   """                 
    if my_queue:
        print("new value ", value)
        print("old value ", my_queue[-1])
        
    my_queue.append(value)
    
    # Ensure the queue length does not exceed the maximum
    if len(my_queue) > MAX_QUEUE_LENGTH:
        my_queue = my_queue[-MAX_QUEUE_LENGTH:]

def filter_faces(faces, x_gap_threshold):
    """
    Remove x values that are close to each other based on the specified gap.

    Parameters:
    - faces: List of tuples where each tuple contains (x, y, w, h) values.
    - x_gap_threshold: The threshold to determine if x values are close.
    - w0, h0, w1, h1: Constants used in the calculation of (x, y, w, h).

    Returns:
    - Updated list of tuples with x values filtered based on the specified gap.
    """
    global my_queue

    result = []

    for f in faces:
        (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]

        # Enqueue the current tuple into the dynamic queue, considering the gap threshold
        enqueue((x, y, w, h), x_gap_threshold)

        # Append the last tuple in the queue to the result
        result.append(my_queue[-1])

    return result if len(result) > 0 else []

def draw_faces(request):
    global fx
    global i
    global motor_moving
    if motor_moving:
        pass
    
    with MappedArray(request, "main") as m:

        filtered_faces = filter_faces(faces, 70)
        
        for f in filtered_faces:
            print("value of f ", f)
            try:
                x, y, w, h = f
            except ValueError:
                x, y, w, h = f + [100]
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            #TODO: CHECK IF THE DESIRED MOVEMENT VALUES ARE RIGHT
            fx = x + w/2
            motor_moving = True
            if fx > SCREEN_WIDTH_PIXEL/2 + w/2:
                print("move left", fx), fx - SCREEN_WIDTH_PIXEL/2
                move_horizontally("right", SCREEN_WIDTH_PIXEL, fx - SCREEN_WIDTH_PIXEL/2)
            elif fx < SCREEN_WIDTH_PIXEL/2 - w/2:
                print("move right", fx, SCREEN_WIDTH_PIXEL/2 - fx)
                move_horizontally("left", SCREEN_WIDTH_PIXEL, SCREEN_WIDTH_PIXEL/2 - fx)
            time.sleep(0.01)
            motor_moving = False
            
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
SCREEN_WIDTH_PIXEL = 640
SCREEN_HEIGHT_PIXEL = 480
config = picam2.create_preview_configuration(main={"size": (SCREEN_WIDTH_PIXEL, SCREEN_HEIGHT_PIXEL)},
                                             lores={"size": (int(SCREEN_WIDTH_PIXEL/2), int(SCREEN_HEIGHT_PIXEL/2)), "format": "YUV420"})
config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
faces = []
picam2.post_callback = draw_faces

encoder = H264Encoder(10000000)
picam2.start_recording(encoder, "test.h264")

start_time = time.monotonic()
# Run for 10 seconds.
motor_moving = False
last_frame = None
while time.monotonic() - start_time < 1000:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1 * h1].reshape((h1, s1))
    
    # frame = grey
    # # Compare the current frame with the last frame
    # if last_frame is not None:
    #     difference = cv2.absdiff(last_frame, frame)
    #     motion = cv2.countNonZero(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))
    #     if motion < THRESHOLD:  # Adjust THRESHOLD based on your setup
    #         # Motion is below the threshold, endpoint reached
    #         print("Endpoint reached!")
    #         break
    # last_frame = frame
        
    faces = face_detector.detectMultiScale(grey, 1.1, 1)
    
picam2.stop_recording()