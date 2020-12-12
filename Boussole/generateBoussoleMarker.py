#Imports
import numpy as np
import matplotlib.pyplot as plt
import cv2
import cv2.aruco as aruco


#Constantes
ID_TAG_BOUSSOLE=17
ARUCO_DICT=aruco.Dictionary_get(aruco.DICT_4X4_50)
PIXEL_SIZE=200



#Figure
fig = plt.figure()

TAG_IMG=aruco.drawMarker(ARUCO_DICT,ID_TAG_BOUSSOLE,200)
plt.imshow(TAG_IMG,cmap='gray')
plt.axis('off')
print(TAG_IMG)
plt.savefig("tagAruco/Boussole/boussole_marker.jpeg")

plt.show()

print(ARUCO_DICT)




