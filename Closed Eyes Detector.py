# Install first dependencies 
#pip install opencv-python dlib pygame
# Make sure all the necessary files are all in the same directory
# Download the shape predictor here:https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat 

# import necessary libraries
import cv2
import numpy as np
import dlib
from math import sqrt
import time
import pygame

#Set the video capturing and predictor variables
#cap = cv2.VideoCapture('http://192.168.8.106:4747/video')
cap = cv2.VideoCapture(1)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#initiate the pygame and locate the sound file that needs to play
pygame.init()
sound=pygame.mixer.Sound('alarm.mp3')

#finds the midpoint of a tuple and returns an integer
def midpoint(p1, p2):
    return (int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2))


#finds the distance between two points
def euclidean_distance(p1, p2):
    return sqrt(int(p2.x - p1.x)**2 + int(p2.y - p1.y)**2)


#converts tuple to integer for calculations
def ttp(tup):
    return dlib.point(int(tup[0]), int(tup[1]))


#sets initial boolean for counting and checking if eyes are closed
closed_eyes = False
closed_eyes_start = 0
closed_threshold = 0.3
closed_time = 3

#Loop function
while True:
    ret, frame = cap.read() #assign the video to the variable frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #get the grayscale of the image
    faces = detector(gray) #use the detector of dlib and assign it to the variable faces
    for face in faces:
        landmarks = predictor(gray, face) #use the predictor of dlib and assign it to landmarks to approximate eye extremities 

        # Draw a rectangle around the face
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        #based on the dataset, approximate the eye positions, right, left, top, bottom
        left_eyel = (landmarks.part(36).x, landmarks.part(36).y) #left eye left
        left_eyer = (landmarks.part(39).x, landmarks.part(39).y) #left eye right
        right_eyel = (landmarks.part(42).x, landmarks.part(42).y) #right eye left
        right_eyer = (landmarks.part(45).x, landmarks.part(45).y) #right eye right
        left_eyet = midpoint(landmarks.part(37), landmarks.part(38)) #left eye top
        left_eyeb = midpoint(landmarks.part(41), landmarks.part(40)) #left eye bottom
        right_eyet = midpoint(landmarks.part(43), landmarks.part(44)) #right eye top
        right_eyeb = midpoint(landmarks.part(47), landmarks.part(46)) #right eye bottom
        
        #Measure the line lengths to be used for conditional statements
        hline_left_length = euclidean_distance(ttp(left_eyer), ttp(left_eyel))
        hline_right_length = euclidean_distance(ttp(right_eyer), ttp(right_eyel))
        vline_left_length = euclidean_distance(ttp(left_eyet), ttp(left_eyeb))
        vline_right_length = euclidean_distance(ttp(right_eyet), ttp(right_eyeb))

        #ratio the vertical lines to the horizontal lines
        ratio_left = vline_left_length/hline_left_length
        ratio_right = vline_right_length/hline_right_length

        # Draw lines for eye landmarks
        hline_left = cv2.line(frame, left_eyer, left_eyel, (0, 255, 0), 2)
        hline_right = cv2.line(frame, right_eyer, right_eyel, (0, 255, 0), 2)
        vline_left = cv2.line(frame, left_eyet, left_eyeb, (0, 255, 0), 2)
        vline_right = cv2.line(frame, right_eyet, right_eyeb, (0, 255, 0), 2)

        # Print the lengths of the lines and ratios
        cv2.putText(frame, f'Left Ratio: {ratio_left:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f'Right Ratio: {ratio_right:.2f}', (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f'Left Vertical: {vline_left_length:.2f}', (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f'Right Vertical: {vline_right_length:.2f}', (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        #checks if eyes or closed or not
        if ratio_left < closed_threshold and ratio_right < closed_threshold:
            if not closed_eyes:
                closed_eyes_start = time.time()
                closed_eyes = True
                #print("if1")
        #changes boolean to true if eyes are open
        else:
            closed_eyes = False
            sound.stop()

        # If both eyes are still closed and enough time has passed, turn the screen red and play the alarm
        elapsed = time.time() - closed_eyes_start
        print(elapsed)
        print(closed_eyes)
        if elapsed >= closed_time and closed_eyes:
            frame[:] = (0, 0, 255)
            cv2.putText(frame, f"Eyes closed for at least {closed_time} seconds", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            sound.play()
            
    frame=cv2.resize(frame,(640,480)) #resize it to 640 by 480
    cv2.imshow("Frame", frame)  # Display the colored frame

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # exit when escape key is pressed
        break

cap.release()
cv2.destroyAllWindows()
