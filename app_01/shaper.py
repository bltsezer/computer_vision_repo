import cv2
import numpy as np

class Circle:
    def __init__(self,radius=5,coordinates=[50,50]):
        self.radius = radius
        self.X = coordinates[0]
        self.Y = coordinates[1]

    def update(self,cursor):
        cColor= (200,20,20)
        x = self.X
        y = self.Y
        r =self.radius
        
        if (x-r)<cursor[0]<(x+r) and (y-r)<cursor[1]<(y+r):
            cColor=20,200,20
            self.X=cursor[0]
            self.Y=cursor[1]
        else:
            cColor=(200,20,20)

class Rect:
    def __init__(self,pos,size=[100,100]):
        self.pos = pos
        self.size = size

    def update(self,cursor):
        cColor= (200,20,20)
        X,Y = self.pos
        W,H = self.size
        
        if (X-W//2)<cursor[0]<(X+W//2) and (Y-H//2)<cursor[1]<(Y+H//2):
            self.pos=cursor
        
        
