from pygame import *
from numpy import array
from shapes.shape import *

class Diamond(Shape):
    def __init__(self,pos,colour,width):
        super().__init__(pos,colour)
        # properties
        self.width = width
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.pos[0]-self.width and x[0] < self.pos[0]+self.width and x[1] > self.pos[1]-self.width and x[1] < self.pos[1]+self.width                       
    
    def display(self,s):  
        # update clickable coords
        self.offsetArray = array((
            array((self.width+20,0)),
            -array((self.width+20,0)),
            -array((0,self.width+20)),
            array((0,self.width+20))
            ))
        # normal shape
        self.top = self.pos-array((0,self.width))
        self.left = self.pos-array((self.width,0))
        self.right = self.pos+array((self.width,0))
        self.bottom = self.pos+array((0,self.width))
        # spl shape
        self.specialShape(s)

        draw.polygon(s,self.colour,(self.top,self.left,self.bottom,self.right))

        # writing the text
        displayText(s,self.text,self.pos,(0,15),self.font,self.textColour, round((2*self.width)/self.getLengthOfW())+1 )

        # property function
        if self.isSelected: self.displayPropertyWindow(s)

    def resizeFunction(self,diff,dir):
        if (diff[0] >= 0 and dir == RIGHT) or (diff[1] >= 0 and dir == DOWN) or (diff[0] <= 0 and dir == LEFT) or (diff[1] <= 0 and dir == UP): self.width += 2
        else: self.width -= 2
    
    def specialShape(self,s):
        self.splTop = self.pos-array((0,self.width+2.5))
        self.splLeft = self.pos-array((self.width+2.5,0))
        self.splRight = self.pos+array((self.width+2.5,0))
        self.splBottom = self.pos+array((0,self.width+2.5))

        # drawing spl shape then normal shape
        if self.isSelected: 
            draw.polygon(s,WHITE,(self.splTop,self.splLeft,self.splBottom,self.splRight))
            self.displayObjectIndicator(s,self.objectIndicator,self.offsetArray)
