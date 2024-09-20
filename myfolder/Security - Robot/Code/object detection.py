#!/usr/bin/python3
import time

import cv2
from libcamera import Transform

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder

# This is like opencv_face_detect_2.py, only we draw the face boxes on a
# recorded video. We have to use the "post_callback" to draw the faces because
# we want capture_buffer to get the image without face boxes, but then we
# want the boxes drawn before handing the image to the encoder.

face_detector = cv2.CascadeClassifier("/home/pi/Documents/haarcascade_frontalface_default.xml")


def draw_faces(request):
    with MappedArray(request, "main") as m:
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))


picam2 = Picamera2()

picam2.start_preview(Preview.QTGL, transform=Transform(hflip=0, vflip=1))
config = picam2.create_preview_configuration(main={"size": (640, 480)},
                                             lores={"size": (320, 240), "format": "YUV420"})
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
while time.monotonic() - start_time < 1000:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1 * h1].reshape((h1, s1))
    faces = face_detector.detectMultiScale(grey, 1.1, 3)

picam2.stop_recording()