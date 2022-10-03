from xml.etree.ElementTree import tostring
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyA0DEgr1k4-X_sK55XnWaPLdWHy8ZBeOmk",
  "authDomain": "car-detect-f215f.firebaseapp.com",
  "databaseURL": "https://car-detect-f215f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "car-detect-f215f",
  "storageBucket": "car-detect-f215f.appspot.com",
  "messagingSenderId": "1071578086388",
  "appId": "1:1071578086388:web:a79d04fac059d9548717a1"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

db.child("AutoPark").child("Main").child("nearestSlot").set("A1")







