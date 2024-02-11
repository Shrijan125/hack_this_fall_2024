import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

width,height=1280,720
folderPath="Presentation"

cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

pathImages=sorted(os.listdir(folderPath),key=len)
print(pathImages)

imgNumbers=0
hs,ws=int(120*1.2),int(213*1.0)
gestureThreshold=300
buttonPressed=False
buttonCounter=0
buttonDelay=20
annotations=[[]]
annotationNumber=0
annotationStart=False
# HandDetector
detector=HandDetector(detectionCon=0.8,maxHands=1)



while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    pathFullImage=os.path.join(folderPath,pathImages[imgNumbers])
    imgCurrent=cv2.imread(pathFullImage)

    hands,img=detector.findHands(img,flipType=False)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)
    if hands and buttonPressed==False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        llmlist=hand['lmList']
        indexFinger=llmlist[8][0],llmlist[8][1]
        xVal=np.interp(llmlist[8][0],[width//2,width],[0,width])
        yVal=np.interp(llmlist[8][1],[150,height-150],[height,0])
        indexFinger=xVal,yVal
        # print(fingers)
        if cy<=gestureThreshold:
            annotationStart=False
            if fingers==[1,0,0,0,0]:
                print("LEFT")
                annotationStart=False
                if imgNumbers>0:
                    annotations=[[]] 
                    annotationNumber=0   
                    buttonPressed=True
                    imgNumbers-=1

            if fingers==[0,0,0,0,1]:
                print("RIGHT")
                annotationStart=False
                if imgNumbers<len(pathImages)-1:
                    annotations=[[]]
                    annotationNumber=0
                    buttonPressed=True
                    imgNumbers+=1
            
            if fingers==[0,1,1,0,0]:
                cv2.circle(imgCurrent,indexFinger,12,(255,0,255),cv2.FILLED )
                annotationStart=False
            
            if fingers==[0,1,0,0,0]:
                if annotationStart==False:
                    annotationStart=True
                    annotationNumber+=1 
                    annotations.append([])  
                cv2.circle(imgCurrent,indexFinger,12,(255,0,255),cv2.FILLED )
                annotations[annotationNumber].append(indexFinger)
            else:
                annotationStart=False
            
            if fingers==[0,1,1,1,0]:
                if annotations:
                    if annotationNumber>=0:
                        annotations.pop(-1)
                        annotationNumber-=1
                        buttonPressed=True

    if buttonPressed:
        buttonPressed+=1
        if buttonPressed>buttonDelay:
            buttonCounter=0
            buttonPressed=False
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if i!=0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)

    imgSmall=cv2.resize(img,(ws,hs))
    h,w,_=imgCurrent.shape
    imgCurrent[0:hs,w-ws:w]=imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)

    key=cv2.waitKey(1)
    if key==ord('q'):
        break
