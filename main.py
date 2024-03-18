import cv2
import pickle
import face_recognition
import numpy as np

#Width and Height as per dimensions used in UI of SnapTrack
cap_width=640
cap_height=480

cap=cv2.VideoCapture(0)
cap.set(3,cap_width) 
cap.set(4,cap_height)

#Loading the encoded file
file=open('EncodedFile.p','rb')
encodedListWithID=pickle.load(file)
file.close()
encodedList,idList=encodedListWithID

while True:
    success, img=cap.read()

    #Downsizing image to save computation power
    scaled_image=cv2.resize(img,(0,0),None,0.25,0.25)

    scaled_image=cv2.cvtColor(scaled_image,cv2.COLOR_BGR2RGB)

    faceCurrFrame=face_recognition.face_locations(scaled_image)

    encodedCurrFrame=face_recognition.face_encodings(scaled_image,faceCurrFrame)

    for encodedFace, faceLocation in zip(encodedCurrFrame,faceCurrFrame):
        
        matches=face_recognition.compare_faces(encodedList,encodedFace)
        faceDistances=face_recognition.face_distance(encodedList,encodedFace)
        
        matchIndex=np.argmin(faceDistances)

        if(matches[matchIndex]):
            y1,x2,y2,x1=faceLocation
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255, 0, 0),2)

    cv2.imshow("SnapTrack", img)
    cv2.waitKey(1)