import cv2

# Hypothetical motor control functions
def move_horizontally(direction):

    # Move the horizontal motor in the specified direction 
    from motor_movement import move_horizontally as move_horizontally1
    move_horizontally1(direction, 26, 19, 13, 6)

def move_vertically(direction):
    # Move the vertical motor in the specified direction
    from motor_movement import move_horizontally as move_horizontally2
    move_horizontally2(direction, 21, 20, 16, 12)


class HumanTracker:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('/home/pi/Documents/haarcascade_frontalface_default.xml')   
        self.target_center = (0.5, 0.5) # Center of the frame   
        self.horizontal_tolerance = 0.1 # Tolerance for horizontal centering   
        self.vertical_tolerance = 0.1 # Tolerance for vertical centering
        
    def track_human(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center = (x + w // 2, y + h // 2)
            
            # Check horizontal alignment     
            if face_center[0] < self.target_center[0] - self.horizontal_tolerance: 
                move_horizontally("left")     
            elif face_center[0] > self.target_center[0] + self.horizontal_tolerance:       
                move_horizontally("right")
            # Check vertical alignment     
            if face_center[1] < self.target_center[1] - self.vertical_tolerance:       
                move_vertically("up")     
            elif face_center[1] > self.target_center[1] + self.vertical_tolerance:       
                move_vertically("down")
    def start_tracking(self, video_source=0):
        cap = cv2.VideoCapture(video_source)
        while True:
            ret, frame = cap.read()     
            if not ret:
                break
                
            self.track_human(frame)
            
            cv2.imshow('Video', frame)
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()   
        cv2.destroyAllWindows()