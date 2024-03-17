import cv2

#Width and Height as per dimensions used in UI of SnapTrack
cap_width=640
cap_height=480

cap = cv2.VideoCapture(0)
cap.set(3,cap_width) 
cap.set(4,cap_height)

while True:
    success, img= cap.read()
    cv2.imshow("SnapTrack", img)
    cv2.waitKey(1)