from pygame import *
from shapes.shape import *
from numpy import array

class Rectangle(Shape):
    def __init__(self,pos,colour,dimx,dimy):
        super().__init__(pos,colour)
        # properties
        self.dimx = dimx
        self.dimy = dimy
        self.myRect = None
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.pos[0] and x[0] < self.pos[0]+self.dimx and x[1] > self.pos[1] and x[1] < self.pos[1]+self.dimy
    
    def resizeFunction(self,diff,dir):
        if dir == RIGHT:
            if diff[0] >= 0: self.dimx += 2       
            elif diff[0] < 0: self.dimx -= 2
        
        if dir == DOWN:            
            if diff[1] >= 0: self.dimy += 2       
            elif diff[1] < 0: self.dimy -= 2

        if dir == LEFT:
            if diff[0] > 0: self.dimx -= 2; self.pos += array((2,0))
            elif diff[0] <= 0: self.dimx += 2; self.pos -= array((2,0))

        if dir == UP:
            if diff[1] > 0: self.dimy -= 2; self.pos += array((0,2))
            elif diff[1] <= 0: self.dimy += 2; self.pos -= array((0,2))

    def display(self,s):
        # update offset array
        self.offsetArray = array((
            array((self.dimx+20,self.dimy/2)),
            array((-20,self.dimy/2)),
            array((self.dimx/2,-20)),
            array((self.dimx/2,self.dimy+20))
                                ))
        
        # normal shape
        self.myRect = Rect(*self.pos,self.dimx,self.dimy)
        # special shape
        self.specialShape(s)

        draw.rect(s,self.colour,self.myRect)
        # draw the inner rect (sub)
        self.drawInner(s)

        # writing the text
        displayText(s,self.text,self.pos,array((self.dimx/2,self.dimy/2)),self.font,self.textColour, round(self.dimx/self.getLengthOfW())+1 )
        
        # property function
        if self.isSelected: self.displayPropertyWindow(s)

    def drawInner(self,s): pass
        
    def specialShape(self,s):
        splShapeOffset = array((2.5,2.5))
        self.mySplRect = Rect(*self.pos-splShapeOffset,self.dimx+5,self.dimy+5)

        if self.isSelected: 
            draw.rect(s,WHITE,self.mySplRect) # drawing spl shape
            # for displaying the indicator
            self.displayObjectIndicator(s,self.objectIndicator,self.offsetArray)

class Subroutine(Rectangle):
    # creating that inner rectangle
    myInnerRect = None
    # override function
    def drawInner(self,s):
        self.myInnerRect = Rect(*(self.pos[0]+10,self.pos[1]),self.dimx-20,self.dimy)
        draw.rect(s,(self.colour[0]-20 if self.colour[0] >= 20 else 0,self.colour[1]-20 if self.colour[1] >= 20 else 0,self.colour[2]-20 if self.colour[2] >= 20 else 0),self.myInnerRect)