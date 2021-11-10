import numpy as np
import cv2 as cv
import imutils
from math import pi
class CircleWorker:

    def __init__(self, image_path):
        
        self.image_path = image_path
        self.minx = 100000
        self.maxx = 0
        self.miny = 100000
        self.maxy = 0
        self.getRad = False
        self.rad = 0
        self.extLeft = {}
        self.extRight = {}
        self.extTop = {}
        self.extBot = {}
        pass
    
    def __find_edge_points(self,contours):

        for cnt in contours:
                
            for c in cnt:
                if c[0] > self.maxx:
                    self.extRight[0] = c
                    self.maxx = c[0]

                if c[0] < self.minx:
                    self.extLeft[0] = c
                    self.minx = c[0]

                if c[1] > self.maxy:
                    self.extBot[0]=c
                    self.maxy = c[1]

                if c[1] < self.miny:
                    self.extTop[0] = c
                    self.miny = c[1]

        return self.extLeft, self.extRight, self.extTop, self.extBot

    def __getContours(self,mask):

        canny = imutils.auto_canny(mask)
        contours, _= cv.findContours(canny,  cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        max_len = 0
        largest_contour = None

        for cnt in contours:
            
            if len(cnt) > max_len:
             
                largest_contour = cnt
                max_len = len(cnt)

        largest_contour = np.array(largest_contour)
        
        return largest_contour

    def get_radius(self):
        if self.rad != 0 :
            return self.rad
        else:
            self.getRad = True
            radious = self.get_area(self.image_path)
            return radious

    def get_area(self,draw=False):
        
        self.image = cv.imread(self.image_path)
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        _ ,thresh1 = cv.threshold(gray,50,255,cv.THRESH_BINARY)
        canny = imutils.auto_canny(thresh1)
        self.contour = self.__getContours(canny)
        
        extLeft, extRight, extTop, extBot = self.__find_edge_points(self.contour)
        if draw == True:
            self.__drawExtremePoints(extLeft, extRight, extTop, extBot)
                       
        diameter = extBot[0][1]-extTop[0][1]

        self.rad = diameter/2
        if self.getRad == True:
            return self.rad

        area = pi*(diameter/2)**2

        return np.round(area,2)

    def __drawExtremePoints(self,LeftExt,RightExtPoint,TopExtreme,BotExtreme):

        new = np.zeros_like(self.image.copy())
        cv.drawContours(new, [self.contour], -1, (255, 255, 255), -1)
        cv.circle(new, LeftExt[0], 8, (0, 0, 255), -1)
        cv.circle(new, RightExtPoint[0], 8, (0, 255, 0), -1)
        cv.circle(new, TopExtreme[0], 8, (255, 0, 0), -1)
        cv.circle(new, BotExtreme[0], 8, (255, 255, 0), -1)
        cv.imshow('new',new)
        cv.waitKey(0)
        
        pass
        

    

if __name__ == '__main__':
    img = "circle.png"
    worker = CircleWorker(img)

    
    area = worker.get_area()
    radious = worker.get_radius()
    print(area, radious)
    # cv.imshow('img',circles)
    # cv.waitKey(0)
    


  