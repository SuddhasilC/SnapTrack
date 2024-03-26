import cv2
import pickle
import face_recognition
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

dbURL=''
sbURL=''

cred = credentials.Certificate("../Key/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': dbURL,
    'storageBucket': sbURL
}) 

bucket=storage.bucket()

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

counter=0
id=-1
attendeeImg=[]

while True:
    success, img=cap.read()

    #Downsizing image to save computation power
    scaled_image=cv2.resize(img,(0,0),None,0.25,0.25)

    scaled_image=cv2.cvtColor(scaled_image,cv2.COLOR_BGR2RGB)

    faceCurrFrame=face_recognition.face_locations(scaled_image)

    encodedCurrFrame=face_recognition.face_encodings(scaled_image,faceCurrFrame)

    if faceCurrFrame:

        for encodedFace, faceLocation in zip(encodedCurrFrame,faceCurrFrame):
            
            matches=face_recognition.compare_faces(encodedList,encodedFace)
            faceDistances=face_recognition.face_distance(encodedList,encodedFace)
            
            matchIndex=np.argmin(faceDistances)

            if(matches[matchIndex]):
                y1,x2,y2,x1=faceLocation
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(255, 0, 0),2)
                id=idList[matchIndex]

                if counter==0:
                    counter=1
        
        if counter!=0:
            if counter==1:
                #Get Attendee data from DB
                attendeeInfo=db.reference(f'Attendees/{id}').get()
                
                #Get Attendee Image from storage
                blob=bucket.get_blob(f'Attendee_Image_DB/{id}.jpg')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                attendeeImg=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                
                #Update attendance data
                dateTimeObject=datetime.strptime(attendeeInfo['Last Attended Date'],"%Y-%m-%d %H:%M:%S")
                secondsElapsed=(datetime.now()-dateTimeObject).total_seconds()

                period=10

                if secondsElapsed >= period :    
                    ref=db.reference(f'Attendees/{id}') 
                    ref.child('Last Attended Date').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    attendeeInfo['Total Attendance']+=1
                    ref.child('Total Attendance').set(attendeeInfo['Total Attendance'])



            counter+=1
            cv2.putText(img,str(attendeeInfo['Name']),(120,320),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            cv2.putText(img,str("ID: "+str(id)),(120,360),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            cv2.putText(img,"Total Attendance: "+str(attendeeInfo['Total Attendance']),(120,400),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

    else:

        counter=0

    cv2.imshow("SnapTrack", img)
    cv2.waitKey(1)