import cv2
from handdetector import HandDetector
from shaper import Rect
import numpy as np

   
class VirtualKeyApp:
    def __init__(self):
        self.capture=cv2.VideoCapture(0)

        self.detector=HandDetector(detectionCon=0.8)
        
        self.capture.set(3,960)
        self.capture.set(4,720)

        self.rectList=[]
        
            
    def start(self):
        for x in range(3):
            r=Rect([150*x+180,180])
            self.rectList.append(r)
        
        cColor=(200,80,80)
        while True:
            isOk,frame = self.capture.read()
            frame=cv2.flip(frame,1)
            frame = self.detector.findHands(frame)
            landmarks,bbox = self.detector.findPosition(frame)

            if landmarks:
                L,_,_ =self.detector.findDistance(8,12,frame)
                
                if L<30:
                    cursor=landmarks[8]
                    for i in self.rectList:
                        i.update(cursor)

            view=np.zeros_like(frame,np.uint8)
            for R in self.rectList:
                X,Y = R.pos
                H,W = R.size
                cv2.rectangle(
                    frame,
                    (X-W//2,Y-H//2),
                    (X+W//2,Y+H//2),
                    cColor,
                    cv2.FILLED)
            #*************************************
            #cv2.circle(frame,(w1+150, h1+150),30,cColor,cv2.FILLED)
            cv2.imshow("Test",frame)
            cv2.waitKey(1)

        #self.capture.release()

test=VirtualKeyApp()
test.start()
