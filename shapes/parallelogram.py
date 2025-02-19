from pygame import *
from numpy import array
from shapes.shape import *

class Parallelogram(Shape):
    def __init__(self,pos,colour,base,height):
        super().__init__(pos,colour)
        # properties
        self.base = base
        self.height = height
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.pos[0]-20 and x[0] < self.pos[0]+self.base and x[1] > self.pos[1] and x[1] < self.pos[1]+self.height
        # object resize indicator
        self.offsetArray = None
    
    def resizeFunction(self,diff,dir): 
        if dir == RIGHT:
            if diff[0] >= 0: self.base += 2       
            elif diff[0] < 0: self.base -= 2
        
        if dir == DOWN:            
            if diff[1] >= 0: self.height += 2       
            elif diff[1] < 0: self.height -= 2

        if dir == LEFT:
            if diff[0] > 0: self.base -= 2; self.pos += array((2,0))
            elif diff[0] <= 0: self.base += 2; self.pos -= array((2,0))

        if dir == UP:
            if diff[1] > 0: self.height -= 2; self.pos += array((0,2))
            elif diff[1] <= 0: self.height += 2; self.pos -= array((0,2))  
    
    def display(self,s): 
        self.offsetArray = array((
            array((self.base+10,self.height/2)),
            array((-30,self.height/2)),
            array((self.base/2,-20)),
            array((self.base/2,self.height+10))
        ))
        # normal shape
        self.topRight = self.pos+array((self.base,0))
        self.bottomLeft = self.pos+array((-20,self.height))
        self.bottomRight = self.pos+array((self.base-20,self.height))
        # spl shape
        self.specialShape(s)

        # drawing normal shape
        draw.polygon(s,self.colour,(self.pos,self.topRight,self.bottomRight,self.bottomLeft))

        # writing the text
        displayText(s,self.text,self.pos,array((self.base/2,self.height/2)),self.font,self.textColour, round(self.base/self.getLengthOfW())+1 )

        # property function
        if self.isSelected: self.displayPropertyWindow(s)
    
    def specialShape(self,s):
        self.splTopLeft = self.pos-array((2.5,2.5))
        self.splTopRight = self.pos+array((2.5+self.base,-2.5))
        self.splBottomLeft = self.pos+array((-22.5,self.height+2.5))
        self.splBottomRight = self.pos+array((self.base-17.5,self.height+2.5))
        if self.isSelected: 
            draw.polygon(s,WHITE,(self.splTopLeft,self.splTopRight,self.splBottomRight,self.splBottomLeft))
            self.displayObjectIndicator(s,self.objectIndicator,self.offsetArray)
