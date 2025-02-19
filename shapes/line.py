from pygame import *
from numpy import array,delete
from shapes.shape import *
from properties.property import *

# constants
XPLUS = 1
YMINUS = 2
XMINUS = 3
YPLUS = 4

class Line(Shape):
    # for locking controls
    locked = False
    lockTime = 50
    # for the direction
    direction = 1
    # text offset
    textOffset = 0
    # thickness!!!!
    thickness = 5
    
    def __init__(self,pos,colour,text,length):
        super().__init__(pos,colour)
        # properties
        self.text = text
        self.length = length
        self.head = (pos, pos+array((self.length,0)))
        self.arrow1 = (pos+array(((7/8)*self.length,self.length//8)), pos+array((self.length,0)))
        self.arrow2 = (pos+array(((7/8)*self.length,self.length//-8)), pos+array((self.length,0)))
        # delete ORI UP & DOWN
        del self.resizeFunctionU, self.resizeFunctionD
        delete(self.objectIndicator,2)
        delete(self.objectIndicator,3)
        # add thickness property
        self.properties.addProperty(Property(self.pos+array((2.5,70)),5,"Thickness","no",30,1))
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.head[0][0] and x[0] < self.head[1][0] and x[1] > self.head[0][1]-self.length//8 and x[1] < self.head[0][1]+self.length//8
        # thickness property
        self.properties.addProperty(Property((self.pos[0]+2.5,self.pos[1]+70),5,"Line thickness","no",25,1))
    
    def actualResizeFunction(self,dirOfMouse,diffCond1,diffCond2,movingArray):
        if dirOfMouse == RIGHT:
            if diffCond1: self.length += 2 
            elif diffCond2 and self.length > 10: self.length -= 2  

        elif dirOfMouse == LEFT:
            if diffCond1: self.length -= 2; self.pos += movingArray
            elif diffCond2 and self.length > 10: self.length += 2; self.pos -= movingArray
    
    def resizeFunction(self,diff,dir): # check resize
        if self.direction == XPLUS: self.actualResizeFunction(dir, diff[0] > 0, diff[0] < 0, array((2,0))) 
        if self.direction == XMINUS: self.actualResizeFunction(dir, diff[0] < 0, diff[0] > 0, -array((2,0)))
        if self.direction == YPLUS: self.actualResizeFunction(dir, diff[1] > 0, diff[1] < 0, array((0,2)))
        if self.direction == YMINUS: self.actualResizeFunction(dir, diff[1] < 0, diff[1] > 0 , -array((0,2)))
    
    def display(self,s): 
        # initialise mouse
        mousePressed = mouse.get_pressed()
        mousePos = mouse.get_pos()
        # check if arrow keys are pressed
        self.checkArrow()
        # start the countdown when locked
        if self.locked: self.countDown()
        # set the pos of everything acc. to direction
        self.selectPos(s)
        # special rect
        self.specialShape(s)
        # display the normal shape
        self.normalShape(s)
        # display the text
        displayText(s,self.text,self.pos,array((self.length/2,self.length/4))+self.textOffset,self.font,self.textColour,1000000)
        # property function
        if self.isSelected: 
            self.displayPropertyWindow(s) # display it
            if mousePressed[2] and self.clickableCoords(mousePos): self.properties.addProperty(Property((self.pos[0]+2.5,self.pos[1]+70),self.thickness,"Line thickness","no",25,1)) # update property
        # change value of thickness
        self.thickness = self.properties.properties[3].value.value   
    
    def checkArrow(self): 
        # check if arrows are pressed
        if self.isSelected and not self.locked and not self.displayOnly and (key.get_pressed()[K_RIGHT] or key.get_pressed()[K_LEFT]):
            if key.get_pressed()[K_RIGHT]: 
                # subtract enum
                self.direction -= 1 if self.direction > XPLUS else -3
            if key.get_pressed()[K_LEFT]: 
                # add enum
                self.direction += 1 if self.direction < YPLUS else -3
            # lock the controls 
            self.locked = True
            
    def countDown(self):
        self.lockTime -= 1 # reduce lock time
        if self.lockTime == 0: 
            self.locked = False # unlock
            self.lockTime = 50 # reset

    def offset(self,endPoint,arrowOffset1,arrowOffset2,xGreater,xLesser,yGreater,yLesser):
        self.head = (self.pos, self.pos+endPoint)
        self.arrow1 = (self.pos+arrowOffset1, self.pos+endPoint)
        self.arrow2 = (self.pos+arrowOffset2, self.pos+endPoint)
        self.clickableCoords = lambda x: x[0] > xGreater and x[0] < xLesser and x[1] > yGreater and x[1] < yLesser

    def specialShapeOffset(self,s,width1start,width1end,width2start,width2end,length1start,length1end,length2start,length2end):
        draw.line(s,(255,255,255),self.pos+width1start,self.pos+width1end)
        draw.line(s,(255,255,255),self.pos+width2start,self.pos+width2end)
        draw.line(s,(255,255,255),self.pos+length1start,self.pos+length1end)
        draw.line(s,(255,255,255),self.pos+length2start,self.pos+length2end)
    
    def changeOffsetArray(self,coords,dir):
        self.offsetArray = coords
        for i in self.objectIndicator: i.direction = dir

    # order-
    # change offset
    # change special shape
    # change text offset
    # change clickable coords
    
    def selectPos(self,s):
        if not self.displayOnly and self.isSelected:
            if self.direction == XPLUS: 
                self.offset( array((self.length,0)),
                             array(((7/8)*self.length,self.length//8)),
                             array(((7/8)*self.length,self.length//-8)),
                             self.head[0][0],self.head[1][0],
                             self.head[0][1]-self.length//8,self.head[0][1]+self.length//8 )
                
                self.specialShapeOffset( s,-array((0,self.length//8)),
                                        array((0,self.length//8)),
                                        array((self.length+5,self.length//8)),
                                        array((self.length+5,self.length//-8)),
                                        array((0,self.length//8)),
                                        array((self.length+5,self.length//8)),
                                        -array((0,self.length//8)),
                                        array((self.length+5,self.length//-8)) )
                
                self.textOffset = 0
                
                self.changeOffsetArray( array((
                    array((self.length+20,0)),
                    -array((30,0))
                    )),1 )
            
            elif self.direction == XMINUS: 
                self.offset( -array((self.length,0)),
                            -array(((7/8)*self.length,self.length//-8)),
                            -array(((7/8)*self.length,self.length//8)),
                            self.pos[0]-self.head[1][0],self.head[0][0],
                            self.head[0][1]-self.length//8,self.head[0][1]+self.length//8 )
                
                self.specialShapeOffset( s,-array((0,self.length//8)),
                                        array((0,self.length//8)),
                                        array((-self.length-5,self.length//8)),
                                        -array((self.length+5,self.length//8)),
                                        array((0,self.length//8)),
                                        array((-self.length-5,self.length//8)),
                                        -array((0,self.length//8)),
                                        array((-self.length-5,self.length//-8)) )
                
                self.textOffset = -array((self.length,0))

                self.changeOffsetArray( array((
                    -array((self.length+20,0)),
                    array((10,0)) )),2 
                )
            
            elif self.direction == YMINUS: 
                self.offset(-array((0,self.length)),
                            -array((self.length//-8,(7/8)*self.length)),
                            -array((self.length//8,(7/8)*self.length)),
                            self.head[0][0]-self.length//8,
                            self.head[0][0]+self.length//8,
                            self.head[0][1]-self.length,self.head[0][1])
                
                self.specialShapeOffset(s,-array((self.length//8,0)),
                                        array((self.length//8,0)),
                                        -array((self.length//8,self.length+5)),
                                        array((self.length//8,-self.length-5)),
                                        -array((self.length//8,0)),
                                        -array((self.length//8,self.length+5)),
                                        array((self.length//8,0)),
                                        array((self.length//8,-self.length-5)))
                
                self.textOffset = -array((0,self.length/2))

                self.changeOffsetArray( array(( -array((0,self.length+20)),
                                                array((0,10)) )),3 )
            
            elif self.direction == YPLUS: 
                self.offset(array((0,self.length)),
                            array((self.length//8,(7/8)*self.length)),
                            array((self.length//-8,(7/8)*self.length)),
                            self.head[0][0]-self.length//8,
                            self.head[0][0]+self.length//8,
                            self.head[0][1],self.head[1][1])
                
                self.specialShapeOffset(s,-array((self.length//8,0)),
                                        array((self.length//8,0)),
                                        array((self.length//8,self.length+5)),
                                        array((self.length//-8,self.length+5)),
                                        array((self.length//8,0)),
                                        array((self.length//8,self.length+5)),
                                        -array((self.length//8,0)),
                                        array((self.length//-8,self.length+5)) )
                
                self.textOffset = array((0,self.length/2))

                self.changeOffsetArray( 
                    array(( array((0,self.length+20)),
                            -array((0,20))
                        )),4 
                    )

    def specialShape(self,s):
        if self.isSelected:
            # object resize indicator
            self.displayObjectIndicator(s,self.objectIndicator,self.offsetArray)
    
    def normalShape(self,s):
        # display
        draw.line(s,self.colour,*self.head,self.thickness)
        draw.line(s,self.colour,*self.arrow1,self.thickness)
        draw.line(s,self.colour,*self.arrow2,self.thickness)