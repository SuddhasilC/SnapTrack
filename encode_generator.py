import cv2
import face_recognition
import pickle
import os
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

#Importing Attendee Images and corrosponding IDs
folderPath= 'Attendee_Image_DB'
pathList=os.listdir(folderPath)
imgList=[]
idList=[] 
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    idList.append(path.split('.')[0])
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)

#Encoding Generator
def findEncodings(imgList): 
    encodedList=[]
    for img in imgList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encoding=face_recognition.face_encodings(img)[0]
        encodedList.append(encoding)
    return encodedList

#Encoding Attendee Images
encodedList=findEncodings(imgList)

#Saving encoded images of attendees along with corrosponding IDs in a list
encodedListWithID=[encodedList,idList]

file=open('EncodedFile.p','wb')
pickle.dump(encodedListWithID,file)
file.close()


