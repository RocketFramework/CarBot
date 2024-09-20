
import time

import cv2
import numpy as np
from motor_movement import move_horizontally as move_horizontally

time.sleep(0.1)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)

while True:
     ret, frame = cap.read()
     flipped = cv2.flip(frame, flipCode = 0)
     frame1 = cv2.resize(flipped, (140, 140))
     font = cv2.FONT_HERSHEY_SIMPLEX

     gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
     boxes, weights = hog.detectMultiScale(gray, winStride=(1,1), padding=(1,1), scale=1.08)
     boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
     for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(gray, (xA, yA), (xB, yB),(0, 255, 0), 2)
        
        b=len(boxes)
        cv2.putText(gray, "peoplecount:" + str(b), (20,50), 0, 2, (255, 0, 0), 3)
        
        face_center = (xA + 20, yA)
        if face_center[0] < 75 and face_center[0] > 65:
            print("nothing", face_center[0])
            pass
        elif face_center[0] > 75:
            #move_horizontally("left")
            print("left", face_center[0])
        elif face_center[0] < 65:
            #move_horizontally("right")
            print("right", face_center[0])
        
     img = cv2.resize(gray,(640,480))
     cv2.imshow("Frame", img);
     key = cv2.waitKey(1) & 0xFF
     if key == ord("q"):
        break
    
# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)