import cv2
import time
import mediapipe as mp
import numpy
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
p=volume.GetVolumeRange()
minvol=p[0]
maxvol=p[1]
volbar = 400


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    def handpos(a):
        lmlist=[]
        if results.multi_hand_landmarks:
                        
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                lmlist.append([id,cx,cy])  
                
        return lmlist[a]
    
    
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    #print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    # print(id,cx,cy)
                    if id ==4 or id==8:
                        cv2.circle(img, (cx,cy), 13, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    
    # print(handpos(4),handpos(8))
    
    x1, y1 = handpos(4)[1], handpos(4)[2]
    x2, y2= handpos(8)[1], handpos(8)[2]
    ccx, ccy = (x1 + x2) // 2, (y1+y2) // 2
    lenth = math.hypot(x2-x1,y2-y1)
    # print(lenth)
    


    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    cv2.circle(img, (ccx,ccy), 13, (255,0,255), cv2.FILLED)


    vol =numpy.interp(lenth, [30, 300], [-65, 10])
    volbar =numpy.interp(lenth, [30, 300], [400, 100])
    print(vol)
    volume.SetMasterVolumeLevel(vol, None)


    if lenth<30:
        cv2.circle(img, (ccx,ccy), 13, (0,255,0), cv2.FILLED)
        
        
        
        
    cv2.rectangle(img, (50, 130), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
    