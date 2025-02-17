from pygame import *

init()

s = display.set_mode((1280,720))
c = time.Clock()

x = image.load("main cursor.png")
x = transform.rotate(x,90)

while 1:
    c.tick(60)
    for evnt in event.get():
        if evnt.type == QUIT: 
            quit()
            exit()

    s.blit(x,(100,100))
    display.update()
    