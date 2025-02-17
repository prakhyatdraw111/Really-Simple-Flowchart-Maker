from pygame import font,init
init()

font = font.Font("font.ttf",16)

def splitByNletters(word,n): return [word[i:i+n] for i in range(0,len(word),n)]

def convert(testcase,fnt,colour,n):
    oldTc = testcase.split(" ")
    oldTc = map(lambda x: splitByNletters(x,n),oldTc)
    tc = []

    for i in oldTc:
        for j in i: tc.append(j)
    
    output = ""

    for i in tc:
        line = output.split("\n")[-1]
        if len(line + i) > n: output += "\n"
        output += i + " "

    output = output.split("\n")
    output = list(map(lambda x: fnt.render(x,True,colour),output))

    return output