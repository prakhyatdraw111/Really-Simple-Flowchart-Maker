from pygame import *
from properties.backendClasses import *

init()
        
class Property:
    # load slider buttons (will be changed later)
    sliderUp = image.load("imgs/sliderUp.png")
    sliderDown = image.load("imgs/sliderDown.png")
    # text offset for y direction
    yTextOffset = 10-fnt.get_height()/2

    def __init__(self,pos,initialValue,propertyName,type,edgeCaseHigh=100,edgeCaseLow=0):      
        self.x, self.y = pos
        # load the property name
        self.propertyName = propertyName
        # load the render object of it
        self.pNameRender = fnt.render(self.propertyName,True,(255,255,255))
        # if property type = number
        #self.value = NoClass(self.x+235,self.y+20,10)
        self.value = ColourClass(self.x+170,self.y+10,initialValue) if type == "col" else NoClass(self.x+240,self.y+10,initialValue,edgeCaseHigh,edgeCaseLow)
        
    def display(self,s):
        # display the box
        draw.rect(s,(255,125,0),(self.x,self.y,380,20))
        # display the property name
        s.blit(self.pNameRender,(self.x+75-self.pNameRender.get_width()/2,self.y+self.yTextOffset))
        # display the separation bar
        draw.line(s,(255,255,255),(self.x+150,self.y),(self.x+150,self.y+20),5)
        # display the no class
        self.value.display(s)      

class PropertyWindow:
    closeImg = image.load("imgs/closeButton.png") # load close button img
    isClosed = True # for showing/not showing the properties window
    def __init__(self,x,y,*properties): 
        # init pos
        self.x = x
        self.y = y
        # init properties
        self.properties = list(properties)
        # clickable coords
        self.clickableCoords = lambda x: x[0] > self.x and x[1] > self.y-25 and x[0] < self.x+410 and x[1] < self.y+self.getHeight()+25
    
    def getHeight(self): return len(self.properties)*22.5+2.5

    def addProperty(self,property): self.properties.append(property)

    def chkCloseBtn(self):
        # initialise mouse 
        mousePressed = mouse.get_pressed()[0]
        mousePos = mouse.get_pos()
        # close if the button is pressed
        if mousePressed and mousePos[0] > self.x+385 and mousePos[1] > self.y-25 and mousePos[0] < self.x+410 and mousePos[1] < self.y: self.isClosed = True

    def chkSelected(self): 
        # check each property
        for property in self.properties:
            
            # return true of the property is selected
            if property.value.getSelection(): return True
        # if for loop is finished
        return False
    
    def display(self,s):
        # display everything if the window is open
        if not self.isClosed:
            draw.rect(s,(255,255,255),(self.x,self.y,385,self.getHeight()),border_radius=5) # draw exterior rectangle
            for i in self.properties: i.display(s) # draw the properties
            s.blit(self.closeImg,(self.x+385,self.y-25)) # draw close button
            self.chkCloseBtn() # check if close button is pressed

if __name__ == "__main__":
    s = display.set_mode((1280,720))
    c = time.Clock()

    property = PropertyWindow(97.5,97.5, # actual pos including the white border
                              Property((100,100),90,"text size","no",1000000),
                              Property((100,122.5),(255,0,0),"text colour","col"),
                              Property((100,145),(0,255,0),"body colour","col")
                              )
    
    property.__setattr__("isClosed",False)

    while 1:
        c.tick(60)

        for i in event.get():
            if i.type == QUIT: 
                quit()
                exit()

        s.fill((0,0,0))

        property.display(s)
        
        display.update()