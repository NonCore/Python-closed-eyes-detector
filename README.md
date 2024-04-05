Facial Landmarks and Eye State Detection
------------------------------------------------------------------
This repository contains a Python script that uses OpenCV, Dlib, and Pygame to detect facial landmarks and determine if the eyes are closed or open. The script uses a pre-trained model to detect faces and facial landmarks, and it plays an alarm sound when the eyes are closed for a certain period of time.

Dependencies
--------------------------------------------------------------------------------
To run the script, you need to install the following dependencies:

-OpenCV

-Dlib

-Pygame

Install using:

	pip install opencv-python dlib pygame

Usage	
----------------------------------------------------------------

To use the script, follow these steps:

-Download the shape predictor file from this link: https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat

-Download audio of choice and name as alarm.mp3

-Place the shape predictor file and audio file in the same directory as the script.

-Run the script using the following command:

	python 'filename'.py

-The script will open a window displaying the video feed from your webcam. It will detect faces and facial landmarks, and it will play an alarm sound when the eyes are closed for a certain period of time.

-Press the escape key to exit the script.

Algorithm
-----------------------------------------------------------------------
-The script uses the following algorithm to detect facial landmarks and determine if the eyes are closed or open:

-Capture the video feed from the webcam using OpenCV.

-Convert the video feed to grayscale.

-Detect faces in the video feed using the Dlib face detector.

-Approximate the eye positions using the Dlib shape predictor.

-Measure the lengths of the horizontal and vertical lines around the eyes.

-Calculate the ratio of the vertical lines to the horizontal lines.

-If the ratio is below a certain threshold, the eyes are considered closed.

-If the eyes are closed for a certain period of time, the script plays an alarm sound and turns the screen red.
