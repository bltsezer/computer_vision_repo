import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import time


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
pytesseract

cap = cv2.VideoCapture(0)
cap.set(3,880)
cap.set(4,880)

while True:
    timer = cv2.getTickCount()
    isOk,img = cap.read()
    hImg, wImg,_ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
        cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)        
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    cv2.imshow("Result",img)
    cv2.waitKey(1)
