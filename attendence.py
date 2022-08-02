import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path="images"
images=[]
personName=[]
mylist=os.listdir(path)
print(list) #['kalpna1.jpg', 'modi2.png', 'pratik.png']

for cu_img in mylist:
    #print(i,end=",")   #kalpna1.jpg,modi2.png,pratik.png,
    current_Img=cv2.imread(f'{path}/{cu_img}')
    #print(current_img)
    images.append(current_Img)
    #print(img)
    personName.append(os.path.splitext(cu_img)[0])
print(personName)

def faceEencoding(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodelistKnown=faceEencoding(images)
print("all encoding sucssesful....")

def attendance(name):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split()
            nameList.append(entry[0])

        if name not in nameList:
            time_now = datetime.now()
            tstr= time_now.strftime('%H:%M:%S')
            dstr= time_now.strftime('%d/%m/%y')
            f.writelines(f'{name},{tstr},{dstr}''\n')

cap=cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame,(0,0),None,0.25,0.25)
    faces= cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodeCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)

    for encodeface, faceloc in zip(encodeCurrentFrame,facesCurrentFrame):
        matches = face_recognition.compare_faces(encodelistKnown,encodeface)
        facedis = face_recognition.face_distance(encodelistKnown,encodeface)

        matchindex = np.argmin(facedis)

        if matches[matchindex]:
            name = personName[matchindex].upper()
            print(name)
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),3)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,0,255),3)
            cv2.putText(frame, name, (x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            attendance(name)

    cv2.imshow("camara",frame)
    if cv2.waitKey(10)==13:
        break
cap.release()
cv2.distroyAllwindows()

