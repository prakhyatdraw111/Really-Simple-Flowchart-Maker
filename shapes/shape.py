from pygame import *
from random import randint
from numpy import array
from sentenceBreaker import convert
from objectResize import objectResizeIndicator
from properties import property

init()

# directions

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

WHITE = (255,255,255)

Font = font.Font("font.ttf",16)

def displayText(s,text,pos,offset,fnt,colour,n=20):
    textRender = convert(text,fnt,colour,n)
    # to define the range of postions of each render object
    halfHeightOfText = (22 * len(textRender)) / 2 

    # displaying the text render list
    for i,j in zip(textRender,range(int(round(pos[1]-halfHeightOfText,0)), 
                                    int(round(pos[1]+halfHeightOfText,0)),fnt.get_height())):
        s.blit(i,array((pos[0],j))-array((i.get_width()/2,fnt.get_height()/2))+offset)

def generatePropertyFromORI(function, instance, x): # Ɐ x is map or filter
    returnArray = array(list(x(function,instance.objectIndicator)))

    return returnArray

class Shape:
    # -----------FOR PROPERTY WINDOW-------------
    propertyWindowTime = 60
    propertyWindowLocked = False
    # -------------------OTHER-------------------
    textColour = (255,255,255)

    def __init__(self,pos,colour):
        self.pos = array(pos)
        self.colour = array(colour)
        self.displayOnly = False
        self.isSelected = False
        self.isMoving = False
        self.collisionPos = None
        self.font = Font
        self.notMovingTime = 0
        self.id = randint(-2147483648,2147483647)
        self.text = ""
        # object resize functions
        self.resizeFunctionR = lambda diff: self.resizeFunction(diff,RIGHT)
        self.resizeFunctionL = lambda diff: self.resizeFunction(diff,LEFT)
        self.resizeFunctionU = lambda diff: self.resizeFunction(diff,UP)
        self.resizeFunctionD = lambda diff: self.resizeFunction(diff,DOWN)
        # object resize indicator
        self.objectIndicator = array((objectResizeIndicator(self.pos,self.colour,self.resizeFunctionR,RIGHT),
                                      objectResizeIndicator(self.pos,self.colour,self.resizeFunctionL,LEFT),
                                      objectResizeIndicator(self.pos,self.colour,self.resizeFunctionU,UP),
                                      objectResizeIndicator(self.pos,self.colour,self.resizeFunctionD,DOWN)))
        # property window
        self.properties = property.PropertyWindow(self.pos[0],self.pos[1],
            property.Property((self.pos[0]+2.5,self.pos[1]+2.5),(255,0,0),"Shape colour","col"),
            property.Property((self.pos[0]+2.5,self.pos[1]+25),(255,255,255),"Text colour","col"),
            property.Property((self.pos[0]+2.5,self.pos[1]+47.5),15,"Text size","no")
        )
    
    def getDisplayOnly(self): return self.displayOnly
    def setDisplayOnly(self,value): self.displayOnly = value

    def getSelected(self): return self.isSelected
    def setSelected(self,value): self.isSelected = value

    def getMoving(self): return self.isMoving
    def setMoving(self,value): self.isMoving = value

    def getCollisionPos(self): return self.collisionPos
    def setCollisionPos(self,value): self.collisionPos = value

    def getText(self): return self.text
    def setText(self,value): self.text = value

    def specialShape(self): pass

    def getLengthOfW(self): return self.font.render("A",True,(0,0,0)).get_width()

    def displayObjectIndicator(self,s,objectIndicators,offsetArray):
        for objectIndicator, offset in zip(objectIndicators,offsetArray):
            objectIndicator.setPos(self.pos+offset)
            objectIndicator.display(s)

    def displayPropertyWindow(self,s): 
        # initialise mouse
        mousePressed = mouse.get_pressed()
        mousePos = mouse.get_pos()
        # check if mouse is pressed
        if mousePressed[2] and self.clickableCoords(mousePos): 
            # update properties window
            self.properties = property.PropertyWindow(self.pos[0],self.pos[1],
                                property.Property((self.pos[0]+2.5,self.pos[1]+2.5),self.properties.properties[0].value.value,"Shape colour","col"),
                                property.Property((self.pos[0]+2.5,self.pos[1]+25),self.properties.properties[1].value.value,"Text colour","col"),
                                property.Property((self.pos[0]+2.5,self.pos[1]+47.5),self.properties.properties[2].value.value,"Text size","no")
                                )   
            # set window's is closed to false
            self.properties.isClosed = False

        # display property window
        self.properties.display(s)

        # change the values of the properties
        self.colour = array(self.properties.properties[0].value.value)
        self.font = font.Font("font.ttf",self.properties.properties[2].value.value)
        self.textColour = array(self.properties.properties[1].value.value)
            
                    

