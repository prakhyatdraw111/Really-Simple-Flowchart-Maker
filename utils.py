from pygame import *

class Button:
    def __init__(self,x,y,xSize,ySize,function,img):
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.function = function
        self.image = image.load(f"imgs/{img}.png")

    def display(self,s):
        # display the image
        s.blit(self.image,(self.x,self.y))
        # check if the button is clicked
        self.checkClick()

    def checkClick(self): 
        # load the mouse
        mousePressed = mouse.get_pressed()[0]
        mousePos = mouse.get_pos()
        # define the condition
        positionSatisfied = mousePos[0] > self.x and mousePos[1] > self.y and mousePos[0] < self.x+self.xSize and mousePos[1] < self.y+self.ySize
        # check the conditions
        if mousePressed and positionSatisfied: self.function()