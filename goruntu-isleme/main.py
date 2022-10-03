from errno import EREMOTE
from operator import index
from turtle import write_docstringdict
from xml.dom.minidom import Document
import cv2
import pickle
from cv2 import resize
from cv2 import waitKey
import numpy as np
import cvzone

from xml.etree.ElementTree import tostring
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyA0DEgr1k4-X_sK55XnWaPLdWHy8ZBeOmk",
  "authDomain": "car-detect-f215f.firebaseapp.com",
  "databaseURL": "https://car-detect-f215f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "car-detect-f215f",
  "storageBucket": "car-detect-f215f.appspot.com",
  "messagingSenderId": "1071578086388",
  "appId": "1:1071578086388:web:a79d04fac059d9548717a1",
  "car_detect": "car_detect.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()



timer = 0

width, height = 40, 90
emptyPark = []
parkUniqueCode = []
parkCodeA = []
parkCodeB = []
parkCodeC = []
parkCodeD = []
gy1,gy2,gx1,gx2 = 10,10,10,10

try:
    with open('carParkPos','rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def defineParkCode(posList):   
    for pos in posList:
        x,y = pos
        x1 = x
        x2 = x+ width
        y1 = y
        y2 = y+height
        y1AKontrol = 114+30
        y2AKontrol = 204 -30
        
        y1BKontrol = 204 + 30
        y2BKontrol = 204 + height - 30

        y1CKontrol = 434 + 30
        y2CKontrol = 524 - 30

        y1DKontrol = 524 + 30
        y2DKontrol = 524 + height-30

        if(y1 < y1AKontrol and y2 > y2AKontrol):
            parkCodeA.append([y1,y2,x1,x2])
        elif (y1 < y1BKontrol and y2 > y2BKontrol):
            parkCodeB.append([y1,y2,x1,x2])
        elif (y1 < y1CKontrol and y2 > y2CKontrol):
            parkCodeC.append([y1,y2,x1,x2])
        elif (y1 < y1DKontrol and y2 > y2DKontrol):
            parkCodeD.append([y1,y2,x1,x2])
           

        gecici = 0
        for i in range(0,len(parkCodeA)):
            for j in  range(i+1,len(parkCodeA)):
                if parkCodeA[i][2] >parkCodeA[j][2]:
                    gecici = parkCodeA[i]
                    parkCodeA[i] = parkCodeA[j]
                    parkCodeA[j] = gecici
        gecici = 0
        for i in range(0,len(parkCodeB)):
            for j in  range(i+1,len(parkCodeB)):
                if parkCodeB[i][2] >parkCodeB[j][2]:
                    gecici = parkCodeB[i]
                    parkCodeB[i] = parkCodeB[j]
                    parkCodeB[j] = gecici                
        gecici = 0
        for i in range(0,len(parkCodeC)):
            for j in  range(i+1,len(parkCodeC)):
                if parkCodeC[i][2] >parkCodeC[j][2]:
                    gecici = parkCodeC[i]
                    parkCodeC[i] = parkCodeC[j]
                    parkCodeC[j] = gecici          
        gecici = 0
        for i in range(0,len(parkCodeD)):
            for j in  range(i+1,len(parkCodeD)):
                if parkCodeD[i][2] >parkCodeD[j][2]:
                    gecici = parkCodeD[i]
                    parkCodeD[i] = parkCodeD[j]
                    parkCodeD[j] = gecici  

    print(parkCodeA)
    print(len(parkCodeA))
    print(parkCodeB)
    print(len(parkCodeB))

defineParkCode(posList)

#Video feed
cap = cv2.VideoCapture('parking.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES,670)


    





def checkParkingSpace(imgPro):
    emptyParkCount = 0
    emptyPark = []
    string = ""
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:(y+height),x:(x+width)]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0,colorR=(0,0,255))

        if count < 800:
            sayac = 0
            color = (0,255,0)
            x1 = x
            x2 = x+width
            y1 = y
            y2 = y+height
            emptyPark.append([y1,y2,x1,x2])
            emptyParkCount = len(emptyPark)
            thickness = 4
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width,pos[1]+height),color, thickness)
        enkucuk = 10000
        sayacA = 0
        sayacB = 0
        sayacC = 0
        sayacD = 0
        for i in range(0,len(emptyPark)):
            y1,y2,x1,x2 = emptyPark[i]
            distance = np.sqrt((x1-gx1)^2+(y1-gy1)^2)
            if emptyPark[i] in parkCodeA:
                sayacA += 1
            if emptyPark[i] in parkCodeB:
                sayacB += 1
            if emptyPark[i] in parkCodeC:
                sayacC += 1
            if emptyPark[i] in parkCodeD:
                sayacD += 1    
            if enkucuk > distance:
                enkucuk = distance
                enYakinIndis = i
            sayac = 0
            if emptyPark[enYakinIndis] in parkCodeA:
                for alanA in parkCodeA:
                    sayac += 1
                    
                    if emptyPark[enYakinIndis] == alanA:
                        string = f"A-{sayac}"
                        print(f"En yakın boş park alanı: {string}")
                        break 
            sayac = 0
            if emptyPark[enYakinIndis] in parkCodeB:
                for alanB in parkCodeB:
                    sayac += 1
                    if emptyPark[enYakinIndis] == alanB:
                        string = f"B-{sayac}"
                        print(f"En yakın boş park alanı: {string}")
                        break 
            sayac = 0
            if emptyPark[enYakinIndis] in parkCodeC:
                for alanC in parkCodeC:
                    sayac += 1
                    if emptyPark[enYakinIndis] == alanC:
                        string = f"C-{sayac}"
                        print(f"En yakın boş park alanı: {string}")
                        break   
            sayac = 0
            if emptyPark[enYakinIndis] in parkCodeD:
                for alanD in parkCodeD:
                    sayac += 1
                    if emptyPark[enYakinIndis] == alanD:
                        string = f"D-{sayac}"
                        print(f"En yakın boş park alanı: {string}")
                        break            
        print(sayacA,sayacB,sayacC,sayacD,emptyParkCount)
    db.child("AutoPark").child("Main").child("totalSlotCount").set(len(emptyPark))
    db.child("AutoPark").child("Main").child("nearestSlot").set(string)
    db.child("AutoPark").child("SectionA").child("slotCount").set(sayacA)
    db.child("AutoPark").child("SectionB").child("slotCount").set(sayacB)
    db.child("AutoPark").child("SectionC").child("slotCount").set(sayacC)
    db.child("AutoPark").child("SectionD").child("slotCount").set(sayacD)             
    
        
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,670) 

    success, img = cap.read()
    img = cv2.resize(img,(1366,768))

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgThreshold = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,75,16)
    kernel = np.ones((2,2),np.int8)
    imgDilate = cv2.dilate(imgThreshold,kernel,iterations=1)

    checkParkingSpace(imgDilate)



    cv2.imshow("image",img)
    waitKey(10)