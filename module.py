# full arm leg yoga
import numpy as np
import mediapipe as mp
import cv2
import math
from keras.models import load_model 
import time

import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):#shoulder, elbow, wrist
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle >180.0:
        angle = 360-angle    
    return angle

def calculate_distance(a,b):
    a = np.array(a)
    b = np.array(b)
    print(a)
    print(b)
    
    #distance = ((((b[0] - a[0])**(2)) - ((b[1] - a[1])**(2)))**(0.5))
    distance = math.hypot(b[0] - a[0], b[1] - a[1])
    
    return distance

def capture_frame_fullbody():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    inputGoal = 3
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:    
        while cap.isOpened():
            _,frame=cap.read()
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                # Calculate angle
                angle = calculate_angle(shoulder_l, elbow_l, wrist_l)
                
                # Get coordinates of right hand
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                # Calculate angle
                angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
                # Curl counter logic for left
                if angle > 160:
                    stage = "Down"
                if angle < 30 and stage =='Down':
                    stage="Up"
                    counter +=1

                # Curl counter logic for right
                if angle_r > 160:
                    stage_r = "Down"
                if angle_r < 30 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1                      
            
            except:
                pass
            
            cv2.rectangle(res, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'BICEP CURLS', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)

            # Render curl counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            
            # Render curl counter for left hand
            # Setup status box for left 
            cv2.rectangle(res, (1280-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1280-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1280-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter), (1280-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1280-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage, (1280-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            #for the instructor
            cv2.rectangle(res, (700,720-60), (1280,720), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(res, 'Do Left arm next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(res, 'Do Right arm next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter >= inputGoal and counter_r >= inputGoal:
                cv2.putText(res, 'GOOD JOB', (720,960-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            #do your processing here
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                img = cv2.imread("./assets/Workout Completed.jpg", cv2.IMREAD_COLOR)
                cv2.imshow("Hello", img)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()
    # /////////////////////////////////////////////////

    cap = cv2.VideoCapture('./assets/Countdown5.mp4')
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, res1 = cap.read()
        if ret == True:
            _,buffer=cv2.imencode(".jpg",res1)
            res1=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res1+b'\r\n')
        else: 
            break
    cap.release()
    cv2.destroyAllWindows()
        
        
    # ////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    inputGoal=3
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image1 to RGB
            image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the image1
            image1.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(image1) #We are using the pose estimation model 
            # Recolor back to BGR
            image1.flags.writeable = True
            image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # Calculate angle of left full
                angle = calculate_angle(hip_l, knee_l, ankle_l)
                
                
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                # Calculate angle
                angle_r = calculate_angle(hip_r, knee_r, ankle_r)
                
                # Curl counter logic for left
                if angle > 140:
                    stage = "Down"
                if angle < 120 and stage =='Down':
                    stage="Up"
                    counter +=1
                    print("Left : ",counter)

                # Curl counter logic for right
                if angle_r > 140:
                    stage_r = "Down"
                if angle_r < 120 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1
                    print("Right : ",counter_r)                       
            
            except:
                pass
            cv2.rectangle(image1, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(image1, 'HIGH KNEES', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)

            # Render curl counter for right hand
            # Setup status box for right hand
            cv2.rectangle(image1, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(image1, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(image1, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(image1, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image1, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(image1, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image1, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            
            # Render curl counter for left hand
            # Setup status box for left 
            cv2.rectangle(image1, (1280-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(image1, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(image1, (1280-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(image1, 'REPS', (1280-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image1, str(counter), (1280-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(image1, 'STAGE', (1280-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image1, stage, (1280-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            #for the instructor
            cv2.rectangle(image1, (700,720-60), (1280,720), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(image1, 'Do Left leg next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(image1, 'Do Right leg next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter >= inputGoal and counter_r >= inputGoal:
                cv2.putText(image1, 'GOOD JOB', (720,960-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2, cv2.LINE_AA)
                
            # Render detections
            mp_drawing.draw_landmarks(image1, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
                
            _,buffer=cv2.imencode(".jpg",image1)
            image1=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+image1+b'\r\n')
            
            
            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                img = cv2.imread("./assets/Workout Completed.jpg", cv2.IMREAD_COLOR)
                cv2.imshow("Hello", img)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()
    
    # ////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1000)
    cap.set(4,700)
    inputGoal = 3
    back_angle_r = 90
    #initializing variables to count repetitions
    counter_r=0
    stage_r=None  
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:            
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                # Get coordinates of right hand
                shoulder= [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                foot= [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                

                back_angle_r = calculate_angle(shoulder,hip,foot)
                # Curl counter logic for right

                if back_angle_r <= 120: 
                    stage_r = "Down"
                if back_angle_r > 120 and back_angle_r <= 180 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1

            except:
                pass
            cv2.rectangle(res, (340,0), (740,60), (0,0,0), -1)
            cv2.putText(res, 'TOE TOUCH', (360,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Render pushup counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )         
            
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if int(counter_r) >= int(inputGoal):
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    
    # //////////////////////////////////////////
    cap = cv2.VideoCapture('./assets/Workout Completed.jpg')
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, res1 = cap.read()
        if ret == True:
            _,buffer=cv2.imencode(".jpg",res1)
            res1=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res1+b'\r\n')
        else: 
            break
    cap.release()
    cv2.destroyAllWindows()
    # /////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    stage = None
    inputGoal = 5
    basepoints = 0
    basePointList = []
    hip_cord_l = 0
    hip_cord_r = 0 
    shoulder_angle = 0
    shoulder_angle_r = 0 
    # Curl counter variables
    counter = 0 
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                # Get coordinates
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                hip_cord_l = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                # Calculate angle
                shoulder_angle = calculate_angle(hip_l,shoulder_l,wrist_l)
                
                # Get coordinates of right hand
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                hip_cord_r = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
                # Calculate angle
                shoulder_angle_r = calculate_angle(hip_r,shoulder_r,wrist_r)
                
            except:
                pass
            cv2.rectangle(res, (320,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'JUMP 2 to 3 times', (340,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)

            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            cv2.putText(res, str(hip_cord_l), (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            basePointList.append(hip_cord_l)
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if shoulder_angle > 90 and shoulder_angle_r > 90:
                basepoints = ((hip_cord_r + hip_cord_l)/2)
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    jumpPoint = min(basePointList)
    print("Jump height : ", jumpPoint )
    print("Base Point : ", basepoints)
    time.sleep(3)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                # Get coordinates
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                hip_cord_l = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                # Calculate angle
                shoulder_angle = calculate_angle(hip_l,shoulder_l,wrist_l)
                
                # Get coordinates of right hand
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                hip_cord_r = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
                # Calculate angle
                shoulder_angle_r = calculate_angle(hip_r,shoulder_r,wrist_r)
                
            except:
                pass
            
            if hip_cord_l < jumpPoint:
                stage = "Jump"
            if hip_cord_l > jumpPoint and stage =='Jump':
                stage="Stand"
                counter += 1
            

            cv2.rectangle(res, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'JUMP COUNTER', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            cv2.line(res, (0,int(700*jumpPoint)), (1280,int(700*jumpPoint)), (0, 255, 0), 3)
            cv2.line(res, (0,int(700*basepoints)), (1280,int(700*basepoints)), (0, 0, 255), 3)

            cv2.rectangle(res, (0,0), (100,70), (0,0,0), -1)
            cv2.putText(res, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            cv2.putText(res, str(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y), (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            cv2.putText(res, str(hip_cord_l), (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if int(inputGoal) <= int(counter):
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    
    # ///////////////////crunches
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    back_angle_r = 90
    inputGoal = 3
    #initializing variables to count repetitions
    counter_r=0
    stage_r=None  
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:            
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                # Get coordinates of right hand
                shoulder= [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                knee= [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                hip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                back_angle_r = calculate_angle(shoulder,hip,knee)

                if back_angle_r <= 90: 
                    stage_r = "Down"
                if back_angle_r > 90 and back_angle_r <= 180 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1  

            except:
                pass
            cv2.rectangle(res, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'CRUNCHES', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Render pushup counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            cv2.putText(res, str(back_angle_r), (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )  
            
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')

            if int(counter_r) >= int(inputGoal):
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
    
    # ////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    inputGoal = 3
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
        
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
        
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            

            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # Calculate angle
                angle = calculate_angle(hip_l, knee_l, ankle_l)
                
                
                # Get coordinates of right hand
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                # Calculate angle
                angle_r = calculate_angle(hip_r, knee_r, ankle_r)
                
                # Curl counter logic for left
                if angle > 150:
                    stage ="Up"
                if angle < 60 and stage == "Up":
                    stage = "Down"
                    counter += 1
                    print("Left :", counter)

                # Curl counter logic for right
                if angle_r > 150:
                    stage_r = "Up"
                if angle_r < 60 and stage_r =="Up":
                    stage_r="Down"
                    counter_r +=1
                    print("Right : ",counter_r)                            
            except:
                pass
            cv2.rectangle(res, (440,0), (860,60), (0,0,0), -1)
            cv2.putText(res, 'SIT UPS/SQUATS', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Render pushup counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            # Render curl counter for left hand
            # Setup status box for left hand
            cv2.rectangle(res, (1280-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1280-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1280-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter), (1280-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1280-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage, (1280-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(res, 'Do Left arm next', (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(res, 'Do Right arm next', (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)

            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')

            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                break
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def capture_frame_arm():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    inputGoal = 3
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:    
        while cap.isOpened():
            _,frame=cap.read()
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                # Calculate angle
                angle = calculate_angle(shoulder_l, elbow_l, wrist_l)
                
                # Get coordinates of right hand
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                # Calculate angle
                angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
                # Curl counter logic for left
                if angle > 160:
                    stage = "Down"
                if angle < 30 and stage =='Down':
                    stage="Up"
                    counter +=1

                # Curl counter logic for right
                if angle_r > 160:
                    stage_r = "Down"
                if angle_r < 30 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1                      
            
            except:
                pass
            
            cv2.rectangle(res, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'BICEP CURLS', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)

            # Render curl counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            
            # Render curl counter for left hand
            # Setup status box for left 
            cv2.rectangle(res, (1280-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1280-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1280-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter), (1280-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1280-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage, (1280-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            #for the instructor
            cv2.rectangle(res, (700,720-60), (1280,720), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(res, 'Do Left arm next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(res, 'Do Right arm next', (720,720-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter >= inputGoal and counter_r >= inputGoal:
                cv2.putText(res, 'GOOD JOB', (720,960-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            #do your processing here
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                img = cv2.imread("./assets/Workout Completed.jpg", cv2.IMREAD_COLOR)
                cv2.imshow("Hello", img)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()
    # /////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    inputGoal = 3
    # Curl counter variables
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                # Calculate angle
                angle = calculate_angle(shoulder_l, elbow_l, wrist_l)
                hip_angle = calculate_angle(hip_l,shoulder_l,elbow_l)
                
                # Get coordinates of right hand
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                # Calculate angle
                angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
                hip_angle_r = calculate_angle(hip_r,shoulder_r,elbow_r)
                
                # Visualize angle
                cv2.putText(res, str(angle),
                            tuple(np.multiply(elbow_l, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Curl counter logic for left
                if hip_angle > 160:
                    if angle < 40:
                        stage = "Down"
                    if angle > 160 and stage =='Down':
                        stage="Up"
                        counter +=1
                else:
                    comment = "PUSH your Left elbow back"

                # Curl counter logic for right
                if hip_angle_r > 160:
                    if angle_r < 40:
                        stage_r = "Down"
                    if angle_r > 160 and stage_r =='Down':
                        stage_r="Up"
                        counter_r +=1
                else:
                    comment = "PUSH your Left elbow back"                     
            
            except:
                pass
            
            cv2.rectangle(res, (440,0), (840,60), (0,0,0), -1)
            cv2.putText(res, 'TRICEP CURLS', (460,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)

            # Render curl counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            
            # Render curl counter for left hand
            # Setup status box for left 
            cv2.rectangle(res, (1280-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1280-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1280-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter), (1280-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1280-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage, (1280-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            #for the instructor
            cv2.rectangle(res, (730,960-60), (1280,960), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(res, 'Do Left arm next', (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(res, 'Do Right arm next', (750,960-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter == inputGoal and counter_r == inputGoal:
                cv2.putText(res, 'GOOD JOB', (540,960-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2, cv2.LINE_AA)
                
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
                
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')

            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    # //////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1000)
    cap.set(4,700)
    inputGoal = 3
    back_angle_r = 90
    #initializing variables to count repetitions
    counter_r=0
    counter_l=0
    stage_l= None
    stage_r=None  
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:            
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                # Get coordinates of right hand
                shoulder= [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                foot= [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                wrist =[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                
                shoulder_r= [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip_r= [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                foot_r= [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                wrist_r =[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                back_angle_l = calculate_angle(hip,shoulder,wrist)
                # Curl counter logic for right
                back_angle_r = calculate_angle(hip_r,shoulder_r,wrist_r)
                
                if back_angle_r <= 80: 
                    stage_r = "Down"
                if back_angle_r > 80 and back_angle_r <= 180 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1
                
                if back_angle_l <= 80: 
                    stage_l = "Down"
                if back_angle_l > 80 and back_angle_l <= 180 and stage_l =='Down':
                    stage_l="Up"
                    counter_l +=1

            except:
                pass
            cv2.rectangle(res, (340,0), (740,60), (0,0,0), -1)
            cv2.putText(res, 'PUNCH COUNTER', (360,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Render pushup counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            cv2.rectangle(res, (1000-220,0), (1280-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1000-145,0), (1280,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1000-220+5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_l), (1000-220+10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1000-220+80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_l, (1000-220+80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')
            
            if int(counter_r) >= int(inputGoal):
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

def capture_frame_leg():
    # ////////////////////////////////////////////////
    cap = cv2.VideoCapture(0)
    cap.set(3,1000)
    cap.set(4,700)
    inputGoal = 3
    # Curl counter variables
    counter = 0 
    counter_r = 0
    stage = None
    stage_r = None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor res to RGB
            res = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting BGR to RGB so that it becomes easier for library to read the res
            res.flags.writeable = False #this step is done to save some memoery
            # Make detection
            results = pose.process(res) #We are using the pose estimation model 
            # Recolor back to BGR
            res.flags.writeable = True
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # Calculate angle of left full
                angle = calculate_angle(hip_l, knee_l, ankle_l)
                
                
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                # Calculate angle
                angle_r = calculate_angle(hip_r, knee_r, ankle_r)
                
                # Curl counter logic for left
                if angle > 140:
                    stage = "Down"
                if angle < 120 and stage =='Down':
                    stage="Up"
                    counter +=1
                    print("Left : ",counter)

                # Curl counter logic for right
                if angle_r > 140:
                    stage_r = "Down"
                if angle_r < 120 and stage_r =='Down':
                    stage_r="Up"
                    counter_r +=1
                    print("Right : ",counter_r)                       
            
            except:
                pass
            cv2.rectangle(res, (300,0), (600,60), (0,0,0), -1)
            cv2.putText(res, 'KICK COUNTER', (320,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Render curl counter for right hand
            # Setup status box for right hand
            cv2.rectangle(res, (0,0), (70,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (75,0), (220,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (5,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter_r), (10,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (80,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage_r, (80,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            
            # Render curl counter for left hand
            # Setup status box for left 
            cv2.rectangle(res, (1000-220,0), (1000-150,80), (0,0,0), -1)
            # cv2.rectangle(res, (0,35), (220,80), (245,117,16), -1)
            cv2.rectangle(res, (1000-145,0), (1000,80), (0,0,0), -1)
            # Rep data
            cv2.putText(res, 'REPS', (1000-220,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, str(counter), (1000-220,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            # Stage data
            cv2.putText(res, 'STAGE', (1000-220+75,25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(res, stage, (1000-220+70,65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 1, cv2.LINE_AA)
            
            #for the instructor
            cv2.rectangle(res, (600,700-60), (1000,700), (0,0,0), -1)
            if counter > counter_r:
                cv2.putText(res, 'Do Left Leg next', (630,700-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter_r > counter:
                cv2.putText(res, 'Do Right Leg next', (630,700-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255), 2, cv2.LINE_AA)
            elif counter == inputGoal and counter_r == inputGoal:
                cv2.putText(res, 'GOOD JOB', (540,960-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2, cv2.LINE_AA)
                
            # Render detections
            mp_drawing.draw_landmarks(res, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
                
            _,buffer=cv2.imencode(".jpg",res)
            res=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res+b'\r\n')

            if int(counter) >= int(inputGoal) and int(counter_r) >= int(inputGoal):
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release
    cv2.destroyAllWindows()

def capture_frame_yoga():
    def inFrame(lst):
        if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
            return True 
        return False

    model  = load_model("./static/model_yoga.h5")
    label = np.load("./static/labels_yoga.npy")

    holistic = mp.solutions.pose
    holis = holistic.Pose()
    drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,700)
    time = 0
    
    while True:
        time += 1
        lst = []

        _, frm = cap.read()

		# window = np.zeros((940,940,3), dtype="uint8")

        frm = cv2.flip(frm, 1)

        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

        frm = cv2.blur(frm, (4,4))
        if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
            for i in res.pose_landmarks.landmark:
                lst.append(i.x - res.pose_landmarks.landmark[0].x)
                lst.append(i.y - res.pose_landmarks.landmark[0].y)

            lst = np.array(lst).reshape(1,-1)

            p = model.predict(lst)
            pred = label[np.argmax(p)]

            if p[0][np.argmax(p)] > 0.75:
                cv2.putText(frm, pred , (100,100),cv2.FONT_ITALIC, 1, (0,255,225),3)

            else:
                cv2.putText(frm, "Asana is either wrong not trained" , (100,100),cv2.FONT_ITALIC, 0.8, (0,255,255),3)

        else: 
            cv2.putText(frm, "Make Sure Full body visible", (100,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255),3)


        drawing.draw_landmarks(frm, res.pose_landmarks, holistic.POSE_CONNECTIONS,
								connection_drawing_spec=drawing.DrawingSpec(color=(255,255,255), thickness=6 ),
								landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), circle_radius=3, thickness=3))


		# window[420:900, 170:810, :] = frm
        _,buffer=cv2.imencode(".jpg",frm)
        frm=buffer.tobytes()
        yield(b' --frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n'+frm+b'\r\n')
        
def lol():
# //////////////////////////////////////////
    cap = cv2.VideoCapture('./assets/Workout Completed.jpg')
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, res1 = cap.read()
        if ret == True:
            _,buffer=cv2.imencode(".jpg",res1)
            res1=buffer.tobytes()
            yield(b' --frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+res1+b'\r\n')
        else: 
            break
    cap.release()
    cv2.destroyAllWindows()
# /////////////////////////////////////////////////////////////////