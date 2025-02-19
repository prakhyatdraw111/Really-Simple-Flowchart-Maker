from pygame import *
init()

# initialise the font
fnt = font.Font("font.ttf",15)

class NoClass:
    # ------FOR COUNTDOWN-----
    countDownTime = 10
    locked = False
    # ------------------------

    # ------FOR NO SLIDER-----
    sliderUp = image.load("imgs/sliderUp.png")
    sliderDown = image.load("imgs/sliderDown.png")
    # ------------------------

    selected = False

    # init last key pressed
    lastKeyPressed = K_F15

    def __init__(self,x,y,value,edgeCaseHigh,edgeCaseLow):
        # initite pos
        self.x = x
        self.y = y
        # initiate value
        self.value = value 
        # initiate the edge cases
        self.edgeCaseHigh = edgeCaseHigh
        self.edgeCaseLow = edgeCaseLow
        # create the value render object
        self.updateValueRender()

    # ---------UTILITY FUNCTIONS---------
    def updateValueRender(self): 
        self.valueRender = fnt.render(f"{self.value}",True,(255,255,255)) # create/update the render
        self.xOffset = self.valueRender.get_width()/2 # load the offset
    
    def listenCountDown(self):
        # reduce the countdown by 1
        self.countDownTime -= 1
        # check if it is 0
        if self.countDownTime == 0: 
            self.countDownTime = 10 # reset count down time
            self.locked = False # unlock the system

    def getSelection(self): return self.selected
    # -----------------------------------

    def doSelection(self,s):
        # initialise mouse
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        # check if the area is pressed
        if pressed[0]:
            if pos[0] > self.x-self.xOffset and pos[1] > self.y-10 and pos[0] < self.x+self.xOffset and pos[1] < self.y+10: self.selected = True
            else: self.selected = False
        # draw a box when it's pressed
        if self.selected: draw.polygon(s,(255,0,0),width=3,points=( (self.x-self.xOffset, self.y-10), (self.x+self.xOffset,self.y-10), (self.x+self.xOffset,self.y+10), (self.x-self.xOffset,self.y+10) ))
    
    def checkText(self):
        # check if a key is pressed
        getPressed = key.get_pressed()

        # do the following only if the system is unlocked or one char is being repeatedly pressed
        if not self.locked or not getPressed[self.lastKeyPressed]:
            # create all the pressable keys
            keysList = {K_0: "0", K_1: "1", K_2: "2", K_3: "3",
                        K_4: "4", K_5: "5", K_6: "6", K_7: "7",
                        K_8: "8", K_9: "9"}

            # check if any key from above is pressed
            keysPressed = filter(lambda x: getPressed[x], keysList)

            # edit the value
            self.value = str(self.value) # convert it to string
            for Key in keysPressed: 
                self.value += keysList[Key] # add the desired value
                self.lastKeyPressed = Key # update last key pressed

            # check if backspace is pressed
            if getPressed[K_BACKSPACE]: 
                self.lastKeyPressed = K_BACKSPACE # update last key pressed
                self.value = self.value[:-1] # slice all chars but the last
                # check if the string is blank
                if not self.value.isdigit(): self.value = self.edgeCaseLow # convert value to 0
                else: self.value = int(self.value) # convert it back to int

            self.value = int(self.value) # restore it to int
            if self.value > self.edgeCaseHigh: self.value = self.edgeCaseHigh # put it to the max value if the value is too high
            if self.value < self.edgeCaseLow: self.value = self.edgeCaseLow   # ---- '' ----- min value -------- '' ------- low
            self.updateValueRender() # update the render object

            # lock the system 
            self.locked = True

        # start the countdown if it is locked
        elif self.locked: self.listenCountDown()

    def sliderFunction(self):
        # function to update render object
        def updateValueAndRender(value):
            # + value
            self.value += value
            # update render object
            self.updateValueRender()

        # initiate mouse
        mousePressed = mouse.get_pressed()[0]
        mousePosX = mouse.get_pos()[0]
        mousePosY = mouse.get_pos()[1]
        # check pressed and x coords
        if mousePressed and mousePosX > self.x+self.xOffset and mousePosX < self.x+self.xOffset+20:
            # check y coords for 1st button and less than edgecase
            if mousePosY > self.y-20 and mousePosY < self.y and self.value < self.edgeCaseHigh: updateValueAndRender(1)
            # check y coords for 2nd button and more than edgecase
            if mousePosY > self.y and mousePosY < self.y+20 and self.value > self.edgeCaseLow: updateValueAndRender(-1)
    
    def display(self,s):
        # ----------FOR TEXT---------
        # display value render object
        s.blit(self.valueRender,(self.x-self.xOffset, self.y-self.valueRender.get_height()/2))
        # check is mouse is clicked on text
        self.doSelection(s)
        # check if a key is pressed
        if self.selected: self.checkText()
        # ---------------------------

        # ------FOR NO SLIDER------
        # display buttons
        s.blit(self.sliderUp,(self.x+self.xOffset,self.y-10))
        s.blit(self.sliderDown,(self.x+self.xOffset,self.y))
        # check if buttons are pressed
        self.sliderFunction()

class ColourClass:
    # arrow mark
    arrow = image.load("imgs/arrow.png")
    def __init__(self,x,y,value): 
        # initiate pos
        self.x = x
        self.y = y
        # initiate value
        self.value = value
        # create 3 no. classes
        self.redClass = NoClass(self.x+30,self.y,self.value[0],255,0) # for red
        self.greenClass = NoClass(self.x+80,self.y,self.value[1],255,0) # for green
        self.blueClass = NoClass(self.x+130,self.y,self.value[2],255,0) # for blue

    def getSelection(self): return self.redClass.getSelection() or self.greenClass.getSelection() or self.blueClass.getSelection()

    def display(self,s):
        # drawing rectangle and no class
        def drawRectangleAndNoClass(x,y,colour,noClass=None):
            draw.rect(s,(255,255,255),(x,y,15,15)) # draw a white square
            draw.rect(s,colour,(x+2.5,y+2.5,10,10)) # draw the coloured square
            if noClass is not None: noClass.display(s) # display noClass only if it's given
    
        # display input rectangles and noClasses
        drawRectangleAndNoClass(self.x+2.5,self.y-7.5,(255,0,0),self.redClass) # for red
        drawRectangleAndNoClass(self.x+52.5,self.y-7.5,(0,255,0),self.greenClass) # for green
        drawRectangleAndNoClass(self.x+102.5,self.y-7.5,(0,0,255),self.blueClass) # for blue

        # resultant colour
        s.blit(self.arrow,(self.x+152.5,self.y-7.5)) # display arrow
        self.value = (self.redClass.value,self.greenClass.value,self.blueClass.value) # update value
        drawRectangleAndNoClass(self.x+175,self.y-7.5,self.value) # display resultant colour