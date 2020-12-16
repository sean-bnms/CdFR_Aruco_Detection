# CdFR_Aruco_Detection
<p align='justify'>

Python script to detect the orientation of the Aruco marker located in the compass of the playground during a game of the 2021 French Robotic Cup edition on the theme Sail The World

## How to use the files ?

### Boussole folder

In this folder, there is a code to generate the Boussole Aruco Tag (4x4, id 17) as well as this marker in .png format

### Images folder

In this folder, 10 images of a rough reprodution of the compass of the playground, taken with a PiCamera v2. You can find the Python scripts to calibrate the camera using a Charuco Board on this repository : https://github.com/sean-bnms/PiCamera_Calibration.git

### .txt files

The usefullLinks.txt file contains the links that helped me build the python codes in this repository.

### .py file

The tagDetection.py file enables to capture frames of the Boussole's Aruco tag and for each one, determine the rotational vectors of the tag. <br/>
Then it converts these vectors in degree angles wich are used to determine if the compass is indicating North or South, in order for the robot to know in which harbour it needs to be at the end of the game. 

</p>
