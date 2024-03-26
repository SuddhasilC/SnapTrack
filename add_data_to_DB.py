import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import db

dbURL=''

cred = credentials.Certificate("../Key/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': dbURL
})

ref=db.reference('Attendees')

data={
    "20CS8040":
    {
        "Name":"JRL",
        "Major":"CSE",
        "Total Attendance":5,
        "Last Attended Date":"2024-02-11 13:11:45"
    },
    "20CS8049":
    {
        "Name":"SC",
        "Major":"CSE",
        "Total Attendance":6,
        "Last Attended Date":"2024-02-11 13:07:55"
    }
}

for key,value in data.items():
    ref.child(key).set(value)