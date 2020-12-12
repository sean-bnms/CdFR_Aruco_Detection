import picamera
import cv2
import numpy as np 
import cv2.aruco as aruco
import math
import time
import os

#Constants
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_4X4_50)
RESOLUTION =  (1280, 960)
FRAMERATE = 30
MARKER_EDGE = 0.06 #boussole tag, 6cm large
parameters = aruco.DetectorParameters_create() #used in aruco;detectMarkers()

#Image collection
WORKDIR = 'Images/' 
TIME_INTERVAL = 3
NUMBER_OF_IMAGES = 10

#PiCamera V2 calibration parameters
CAMERA_MATRIX = np.array([[1.08608589e+03, 0.0, 7.26988003e+02],[0.0, 1.08608589e+03, 4.95638330e+02],[0.0, 0.0, 1.0]])
DISTORTION_COEFFS = np.array([[-1.62571333e-01],[-6.49672199e-01],[2.63050461e-02],[1.69642196e-03],[-6.53119443],[-1.28073078e-01],[-1.69046274],[-3.61436053],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])


#Detection of markers : return the id of the tag ArUco and the rotation vectors usefull to determine the angle of rotation on the z-axis of the marker
def find_marker(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    marker_corners, marker_ids, rejectedImgPoints = aruco.detectMarkers(image=gray, dictionary=ARUCO_DICT, parameters = parameters)
    rotation_vec, traslation_vec, _objpoints = aruco.estimatePoseSingleMarkers(corners = marker_corners,markerLength = MARKER_EDGE,cameraMatrix = CAMERA_MATRIX,distCoeffs = DISTORTION_COEFFS) 
    return rotation_vec, marker_ids


def angles_from_rvec(rvec):
    r_mat, _jacobian = cv2.Rodrigues(rvec)
    a = math.atan2(r_mat[2][1], r_mat[2][2])
    b = math.atan2(-r_mat[2][0], math.sqrt(math.pow(r_mat[2][1],2)) + math.sqrt(math.pow(r_mat[2][2],2)))
    c = math.atan2(r_mat[1][0], r_mat[0][0])
    return[a,b,c]

def calc_heading(rvec):
    angles = angles_from_rvec(rvec)
    degree_angle = math.degrees(angles[2])
    if degree_angle < 0 :
        degree_angle += 360
        return degree_angle

#return the boussole heading, assuming that the initial position (no rotation) <=> N
def boussole_direction(angle):
    if 90 < angle and angle < 270 :
        return 'S'
    else:
        return 'N'

def video_to_image():
    #Initialize the camera
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.framerate = FRAMERATE
        camera.start_preview()
        try : 
            for i, filename in enumerate(camera.capture_continuous('imageBoussole_{counter:02d}.png')):
                print(filename)
                time.sleep(TIME_INTERVAL)
                if i == NUMBER_OF_IMAGES - 1 :
                    break
        finally : 
            camera.stop_preview()

#video_to_image()
    
def harbour_identification():
    #Collect captures by order of numerotation
    images = np.array([WORKDIR + file for file in os.listdir(WORKDIR) if file.startswith("imageBoussole") and file.endswith(".png")])
    order = np.argsort([int(p.split(".")[-2].split("_")[-1]) for p in images])
    images = images[order]
    print(images)
    result =[]
    for image in images :
        frame = cv2.imread(image)
        rvec, ids = find_marker(frame)
        print('Ids detected :', ids)
        if ids == None :
            result.append((image, 'Error : marker detection'))
        else :
            boussole_angle = calc_heading(rvec)
            print('Angle associé :', boussole_angle)
            if boussole_angle == None :
                result.append((image, 'Error : angle calculus' ,boussole_angle))
            else :
                harbour = boussole_direction(boussole_angle)
                result.append((image, harbour, boussole_angle))
    return result

result = harbour_identification()
print("Final result: ",result)

