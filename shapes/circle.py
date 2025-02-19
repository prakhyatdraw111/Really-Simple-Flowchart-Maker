from pygame import *
from shapes.shape import *
from numpy import array

class Circle(Shape):
    def __init__(self,pos,colour,radius):
        super().__init__(pos,colour)
        # properties
        self.radius = radius 
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.pos[0]-self.radius and x[0] < self.pos[0]+self.radius and x[1] > self.pos[1]-self.radius and x[1] < self.pos[1]+self.radius
    
    def display(self,s): 
        # update offset array
        self.offsetArray = array((array((20+self.radius,0)),
                                  -array((20+self.radius,0)),
                                  -array((0,20+self.radius)),
                                  array((0,20+self.radius))))

        # draw spl shape
        self.specialShape(s)

        # normal shape
        draw.circle(s,self.colour,self.pos,self.radius)

        # writing the text
        displayText(s,self.text,self.pos,array((0,0)),self.font,self.textColour, round((2*self.radius)/self.getLengthOfW())+1 )

        # property function
        if self.isSelected: self.displayPropertyWindow(s)


    def resizeFunction(self,diff,dir):
        if (diff[0] >= 0 and dir == RIGHT) or (diff[1] >= 0 and dir == DOWN) or (diff[0] <= 0 and dir == LEFT) or (diff[1] <= 0 and dir == UP): self.radius += 2
        else: self.radius -= 2

    def specialShape(self,s):
        self.splRadius = self.radius+2.5
        if self.isSelected: 
            draw.circle(s,WHITE,self.pos,self.splRadius)
            # for displaying the indicator
            self.displayObjectIndicator(s,self.objectIndicator,self.offsetArray)
