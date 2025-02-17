# really simple flowchart maker v1
# author: me (prakhyat dr)

from pygame import *
from pygame import *
from shapes.shape import *
from shapes.circle import *
from shapes.rectangle import *
from shapes.diamond import *
from shapes.parallelogram import *
from shapes.line import *
from numpy import array
from utils import Button

init()

#-------------------------------------------------

# load common colours
WHITE = (255,255,255)

#-------------------------------------------------

# checking if caps lock is pressed
isCapsLock = False

#------------BUTTON STUFF AND SCENE CHANGE------------------

# creating enums
WORKSPACE = 1
GUIDE = 2

# creating a variable to switch thru guide and workspace
scene = WORKSPACE

# define their functions

def kFunction():
    # make scene var a global variable
    global scene
    # change scene to workspace
    scene = WORKSPACE

def guideFunction():
    # make scene var a global variable
    global scene
    # change scene to guide
    scene = GUIDE

# create the buttons

kButton = Button(530,505,220,70,kFunction,"kButton")
guideButton = Button(1068,0,220,70,guideFunction,"guideButton")

#--------------GUIDE-----------------

# load guide items

# load the font
largeFont = font.Font("century.ttf",48)
regularFont = font.Font("century.ttf",32)

# load the texts
title = largeFont.render("Guide",True,WHITE)

postulates = array((
    regularFont.render("Drag and drop the shape you want from the shapes below.",True,WHITE),
    regularFont.render("Click on it to select it.",True,WHITE),
    regularFont.render("Once selected, you can start typing to edit the box.",True,WHITE),
    regularFont.render("If you want to change the properties of the box, right click on the shape.",True,WHITE),
    regularFont.render("If you want to delete the shape, press delete.",True,WHITE),
    regularFont.render("If you want to rotate a line, use the left or right arrow keys.",True,WHITE)
))

# creating the guide interface
def guide(s):
    # display the title
    s.blit(title,(0,0))
    # display the texts
    for text,height in zip(postulates,range(100,1000,50)): s.blit(text,(0,height))
    # display k button
    kButton.display(s)

#----------MAIN FUNCTIONS------------

def drawLines(s):
    draw.line(s,WHITE,(0,570),(1280,570),5)
    draw.line(s,WHITE,(0,620),(1280,620),5)

    draw.line(s,WHITE,(256,620),(256,720),5)
    draw.line(s,WHITE,(512,620),(512,720),5)
    draw.line(s,WHITE,(768,620),(768,720),5)
    draw.line(s,WHITE,(1024,620),(1024,720),5)

def checkMultipleSelection(instanceList):
    selections = [] # for returning the items w/ selections
    for i in instanceList: # finding selections
        if i.getSelected(): selections.append(i)
    multipleNos = list(map(lambda x: x.notMovingTime,selections)) # for checking maximum of length
    if len(multipleNos) > 0: # before starting the game nothing will be there so only
        most = max(multipleNos) 
        indexMost = multipleNos.index(most)
        selections.pop(indexMost)
        for i in selections: 
            i.setSelected(False)
            i.setMoving(False)

def returnKey(eventSystem):
    # creating a dictionary so that corresponding key can be returned
    keys = {K_a:"a",K_b:"b",K_c:"c",K_d:"d",K_e:"e",K_f:"f",K_g:"g",K_h:"h",
            K_i:"i",K_j:"j",K_k:"k",K_l:"l",K_m:"m",K_n:"n",K_o:"o",K_p:"p",
            K_q:"q",K_r:"r",K_s:"s",K_t:"t",K_u:"u",K_v:"v",K_w:"w",K_x:"x",
            K_y:"y",K_z:"z",K_1:"1",K_2:"2",K_3:"3",K_4:"4",K_5:"5",K_6:"6",
            K_7:"7",K_8:"8",K_9:"9",K_0:"0", K_LEFTBRACKET:"[",K_RIGHTBRACKET:"]",
            K_MINUS:"-",K_EQUALS:"=",K_BACKSLASH:"\\",K_SEMICOLON:";",K_QUOTE:"'",K_COMMA:",",
            K_PERIOD:".",K_SLASH:"/",K_ASTERISK:"*",K_PLUS:"+",K_RETURN:"\n",K_SPACE:" "}
    # corresponding keys when shift is pressed
    shiftKeys = {"a":"A","b":"B","c":"C","d":"D","e":"E","f":"F","g":"G","h":"H",
                 "i":"I","j":"J","k":"K","h":"H","i":"I","j":"J","k":"K","l":"L",
                 "m":"M","n":"N","o":"O","p":"P","q":"Q","r":"R","s":"S","t":"T",
                 "u":"U","v":"V","w":"W","x":"X","y":"Y","z":"Z","1":"!","2":"@",
                 "3":"#","4":"(money)","5":"%","6":"^","7":"&","8":"*","9":"(",
                 "0":")","-":"_","=":"+","[":"{","]":"}","\\":"|",";":":","'":'"',
                 ",":"<",".":">","/":"?"," ":" "}
    for i in keys:
        # if key is pressed
        if eventSystem.key == i: return shiftKeys[keys[i]] if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT] or isCapsLock else keys[i]     
    return ""

def checkDelete(instanceList,object):
    # check if object is selected and delete is pressed
    if object.getSelected() and key.get_pressed()[K_DELETE]: instanceList.remove(object)

# check if a key is pressed / something is selected
def checkSelectionAndKey(instanceList,evnt,cpos):
    global initCoords, isCapsLock

    for instance in instanceList:
        # generate clickable coords from ori
        objectResizeIndicators = generatePropertyFromORI(lambda x: x.clickableCoords(cpos),instance,map)
        # check if mouse is there in the object's clickable coords
        print(instance.id)
        if instance.clickableCoords(cpos) or objectResizeIndicators.any():
            print("true")
            # check if clicked
            if evnt.type == MOUSEBUTTONDOWN: 
                # select and move it
                instance.setSelected(True)
                instance.setMoving(True)
                # check if it is plain click
                initCoords = array(cpos)
        # if not
        else:
            print("false")
            # deselect object when pressed
            if evnt.type == MOUSEBUTTONDOWN and not instance.properties.clickableCoords(cpos): instance.setSelected(False)
        # for dropping in the objects list
        if evnt.type == MOUSEBUTTONUP: 
            instance.setMoving(False) # room for optimisation
            if type(instance) == Circle and instance.pos[1]+instance.radius > 570: instanceList.remove(instance)
            elif (type(instance) in (Rectangle,Subroutine)) and instance.pos[1]+instance.dimy > 570: instanceList.remove(instance)
            elif type(instance) == Parallelogram and instance.pos[1]+instance.height > 570: instanceList.remove(instance)
            elif type(instance) == Diamond and instance.pos[1]+instance.width > 570: instanceList.remove(instance)
    
    # check if a key is pressed
    if evnt.type == KEYDOWN:
        # find out the object which is selected
        theOnlySelected = list(filter(lambda x: x.getSelected(), instanceList))
        # if there is an object which is selected
        if len(theOnlySelected):
            # unpack the list
            theOnlySelected = theOnlySelected[0]
            # initialise keys
            kGetPressed = key.get_pressed()
            # do this only when any property isn't selected
            if not (theOnlySelected.properties.chkSelected() and (kGetPressed[K_1] or kGetPressed[K_2] or kGetPressed[K_3] or kGetPressed[K_4] or kGetPressed[K_5] or kGetPressed[K_6] or kGetPressed[K_7] or kGetPressed[K_8] or kGetPressed[K_9] or kGetPressed[K_0])):
                # check if backspace is pressed
                if evnt.key == K_BACKSPACE: theOnlySelected.text = theOnlySelected.text[:-1]
                # if any other key is pressed
                else: theOnlySelected.text += returnKey(evnt)
        # if caps lock is pressed
        if evnt.key == K_CAPSLOCK: isCapsLock = True if isCapsLock is False else False

def changeCursor(instanceList):
    # create new list objectIndicators
    objectIndicators = []
    # map the instanceList into object indicators
    oldObjectIndicators = list(map(lambda x: x.objectIndicator, instanceList))
    # reshape it into 1d array
    for i in oldObjectIndicators:
        for j in i: objectIndicators.append(j)
    # filter so that the oris with hover status true is returned
    objectIndicators = filter(lambda x: x.hoverStatus == True,objectIndicators)
    # for loop so that the direction of the first instance is returned
    for i in objectIndicators: 
        # if direction is 1 or 2 (horizontal)
        if i.direction in (1,2): return 7
        # if direction is 3 or 4 (vertical)
        else: return 8
    # return main cursor if none of the oris are hovered
    return 0

# main function

def main():
    global isCapsLock

    s = display.set_mode((1280,720))
    c = time.Clock()
    
    # defining colours
    GREEN = (0,255,0)
    RED = (255,0,0)

    # creating displayOnly shapes

    doCircle = Circle((128,670),GREEN,40)
    doCircle.setDisplayOnly(True)

    doRect = Rectangle((266,630),GREEN,236,80)
    doRect.setDisplayOnly(True)

    doDiamond = Diamond((640,670),GREEN,40)
    doDiamond.setDisplayOnly(True)
    
    doParallelogram = Parallelogram((798,630),GREEN,216,80)
    doParallelogram.setDisplayOnly(True)
    
    doSubroutine = Subroutine((1034,630),GREEN,236,80)
    doSubroutine.setDisplayOnly(True)

    doLine = Line((590,595),(255,255,255),"edit me pls",100)
    doLine.setDisplayOnly(True)

    # instance list!

    instanceList = []

    while 1:
        c.tick(60)
        # creating cursorpos for following for loop
        cpos = mouse.get_pos()
        for i in event.get():
            if i.type == QUIT:
                quit() 
                exit()
            if i.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
                # checking for creating new instance
                if        doCircle.clickableCoords(cpos): instanceList.append(Circle(doCircle.pos,RED,80))
                if          doRect.clickableCoords(cpos): instanceList.append(Rectangle(doRect.pos,RED,doRect.dimx,doRect.dimy))
                if       doDiamond.clickableCoords(cpos): instanceList.append(Diamond(doDiamond.pos,RED,80))
                if doParallelogram.clickableCoords(cpos): instanceList.append(Parallelogram(doParallelogram.pos,RED,doParallelogram.base,doParallelogram.height))
                if    doSubroutine.clickableCoords(cpos): instanceList.append(Subroutine(doSubroutine.pos,RED,doSubroutine.dimx,doSubroutine.dimy))
                if          doLine.clickableCoords(cpos): instanceList.append(Line(doLine.pos,RED,"edit me pls",100))
            # check if a key is pressed / selection
            checkSelectionAndKey(instanceList,i,cpos)
        
        # reset the colours 
        s.fill((0,0,0))
        
        if scene == WORKSPACE:
            # display the guide button
            guideButton.display(s)

            # draw white lines to surround display only shapes
            drawLines(s)

            # display displayOnly shapes
            doCircle.display(s)
            doRect.display(s)
            doDiamond.display(s)
            doParallelogram.display(s)
            doSubroutine.display(s)
            doLine.display(s)

            # display instanceList shapes 
            for i in instanceList: 
                i.display(s)
                # check if delete is pressed
                checkDelete(instanceList,i)

                if i.getMoving():
                    i.notMovingTime = 0
                    if mouse.get_pressed()[0]: 
                        # checking if it is only click
                        finalCoords = array(cpos)
                        difference = finalCoords-initCoords

                        objectResizeIndicators = generatePropertyFromORI(lambda x: x.getSelected(),i,map)
                        if difference.all() and not objectResizeIndicators.any(): i.pos = cpos
                else: i.notMovingTime += 1 # to check the least value of notMoving time 
                
                # check for multiple selection
                checkMultipleSelection(instanceList)

            # check if ori is hovered
            mouse.set_cursor(changeCursor(instanceList))
        
        if scene == GUIDE: guide(s)

        display.update()

main()