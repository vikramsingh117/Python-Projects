# Face-detection
this is my first project :D
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import numpy as np

import cv2

cap=cv2.VideoCapture(0)

aface=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip=0

facedata=[]

datapath="./data/"

filename=input("enter name of the user")

while True:

    ret,frame=cap.read()
    
    if ret==False:
        continue

    faces= aface.detectMultiScale(frame,1.3,5)
    faces=sorted(faces,key=lambda f:f[2]*f[3])


    for face in faces[-1:]:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        oddset=10
        faceselect=frame[y-oddset:y+h+oddset,x-oddset:x+w+oddset]
        faceselect=cv2.resize(faceselect,(100,100))

        skip+=1
        if skip%10==0:
            facedata.append(faceselect)
            print(len(facedata))

    cv2.imshow("faceselect",faceselect)
    cv2.imshow("video camera",frame)
    #cv2.imshow("video camera",gray)


    key=cv2.waitKey(1) & 0xFF
    #CHANGING THE BA;UE OF WAITKEY WILL MAKE THR VIFEO LAG BY THE MILISEC INPUTTED
    if key ==ord("q"):
        break

facedata= np.asarray(facedata)

facedata=facedata.reshape((facedata.shape[0],-1))

print(facedata.shape)

np.save(datapath+filename+".npy",facedata)

print("data saved at "+datapath+filename+".npy")

cap.release()
cv2.destroyAllWindows()

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import numpy as np
import cv2

datapath="./data/"


def distance(v1,v2):
    return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):

        dist=[]
        for i in range(train.shape[0]):
            ix=train[i, :-1]
            iy=train[i, -1]
            d = distance(test, ix)
            dist.append([d, iy])
        dk= sorted(dist, key=lambda x: x[0])[:k]
        labels= np.array(dk)[:, -1]

        output = np.unique(labels, return_counts=True)
        index= np.argmax(output[1])
        return output[0][index]

cap=cv2.VideoCapture(0)

aface=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip=0

facedata=[]

labels=[]

class_id=0

names={}



for fx in os.listdir(datapath):

    if fx.endswith(".npy"):
        names[class_id]=fx[:-4]
        print("loaded"+fx)
        data_item= np.load(datapath+fx)
        facedata.append(data_item)
        target= class_id*np.ones((data_item.shape[0],))
        class_id+=1
        labels.append(target)


facedataset= np.concatenate(facedata, axis=0)

facelabels= np.concatenate(labels, axis=0).reshape((-1,1))

print(facedataset.shape)

print(facelabels.shape)

trainset=np.concatenate((facedataset,facelabels),axis=1)

print(trainset.shape)




while True:

    ret,frame = cap.read()
    if ret == False:
        continue
    faces= aface.detectMultiScale(frame, 1.3,5)
    for face in faces:
        x,y,w,h=face

        offset=10
        faceselect=frame[y-offset:y+h+offset,x-offset:x+w+offset]
        faceselect=cv2.resize(faceselect,(100,100))
        out=knn(trainset,faceselect.flatten())
        predname=names[int(out)]
        cv2.putText(frame,predname,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,255),2)

    cv2.imshow("faces",frame)

    key=cv2.waitKey(1) & 0xFF
    if key==ord("q"):
        break
cap.release()

cv2.destroyAllWindows()
