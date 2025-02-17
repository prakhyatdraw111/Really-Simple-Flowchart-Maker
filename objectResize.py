from pygame import Rect,draw,mouse
from numpy import array

class objectResizeIndicator:
    # for recording coords
    initCoords = None
    finalCoords = None
    difference = None

    # for recording initCoords only once 
    initCoordsUnlock = True

    # for checking hover
    hoverStatus = False

    def __init__(self,pos,colour,objectAction,direction):
        # properties
        self.pos = pos
        self.colour = array((255,255,255))-colour 
        self.objectAction = objectAction
        self.direction = direction
        # colour types
        self.inverseColour = colour
        self.normalColour = array((255,255,255))-colour
        #
        self.rect = Rect(*self.pos,10,10)
        # if it is clicked
        self.isSelected = False
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.pos[0] and x[0] < self.pos[0]+10 and x[1] > self.pos[1] and x[1] < self.pos[1]+10

    def getClickableCoords(self): return self.clickableCoords        
    
    def getPos(self): return self.pos
    def setPos(self,value): self.pos = value

    def getColour(self): return self.colour
    def setColour(self,value): self.colour = value

    def getSelected(self): return self.isSelected
    def setSelected(self,value): self.isSelected = value

    def changeColourAndSelected(self,colour,selection):
        self.setColour(colour)
        self.setSelected(selection)

    def checkHover(self): 
        # initiate mouse
        mousePos = mouse.get_pos()
        # check if it is in clickable coords
        self.hoverStatus = True if self.clickableCoords(mousePos) or self.isSelected else False

    def clickAction(self):
        # initiate the mouse
        mousePressed = mouse.get_pressed()[0]
        mousePos = mouse.get_pos()

        # check if it is pressed 
        if mousePressed:
            # check if it is pressed in clickable coords
            if self.clickableCoords(mousePos):
                # changing colour and selected
                self.changeColourAndSelected(self.inverseColour,True)
                
                # for recording initial coords
                if self.initCoordsUnlock:
                    self.initCoords = array(mousePos)
                    self.initCoordsUnlock = False 

        else: self.changeColourAndSelected(self.normalColour,False)

    def actionWhenSelected(self):
        if self.getSelected(): 
            self.finalCoords = array(mouse.get_pos())

            self.difference = self.finalCoords-self.initCoords

            if self.direction in (1,2): self.pos[0] = self.finalCoords[0] # increase x of pos
            elif self.direction in (3,4): self.pos[1] = self.finalCoords[1] # increase y of pos 
            
            self.objectAction(self.difference)
        # to release initCoordsUnlock when not selected
        else: self.initCoordsUnlock = True

    def display(self,s):
        # set cursor if it is hovered
        self.checkHover()
        # check if the small rect is clicked
        self.clickAction()
        # do action when selected
        self.actionWhenSelected()
        # display the rect
        self.rect = Rect(*self.pos,10,10) # updating the rect
        draw.rect(s,self.colour,self.rect)
