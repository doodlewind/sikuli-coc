# Clash of Clans Auto Farm Script
# Stop script by press command + shift + C

import time
import math


class Finder:        
        
    def findTownHall(self):
        
        townHallLv8 = r.find("1453952397524.png")
        if townHallLv8 is not None:
            return (townHallLv8.getX(), townHallLv8.getY())
        townHallLv7 = r.find("1453952443462.png")
        if townHallLv7 is not None:
            return (townHallLv7.getX(), townHallLv7.getY()) 
        return None

    def findBuilding(self, *args):
        results = []
        for building in args:
            if building is not None:
                for b in building:
                    results.append((b.x, b.y))
        return results

    def findAllGold(self):
        # goldsLv9 = r.findAll("1453953124704.png")
        goldsLv10Lv11 = r.findAll("1453953362202.png")
        # goldsLv12 = r.findAll("1453953394802.png")
        return f.findBuilding(goldsLv10Lv11)

    def findAllElixir(self):
        # elixirsLv8Lv9 = r.findAll("1453953091853.png")
        # elixirsLv10 = r.findAll("1453953333748.png")
        elixirsLv11Lv12 = r.findAll("1453953285030.png")
        # darkElixirs = r.findAll("1453996663798.png")
        return f.findBuilding(elixirsLv11Lv12)
    

    def findAllArcherTower(self):
        towersLv7Lv8Lv9 = r.findAll("1453455834637.png")
        towersLv10 = r.findAll("1453566337555.png")
        return f.findBuilding(towersLv7Lv8Lv9, towersLv10)

    def findAllWizardTower(self):
        towersLv1Lv2Lv3Lv4Lv5 = r.findAll("1453567230793.png")
        towersLv6 = r.findAll("1453567557482.png")
        return f.findBuilding(towersLv1Lv2Lv3Lv4Lv5)


def myDragDrop(start, end):
    Settings.MoveMouseDelay = 0.1
    r.dragDrop(start, end)


def wanderCollect(): 
    start = r.getCenter()
    # go top
    end = start.below(300)
    r.dragDrop(start, end)
    collect()

    # go right
    end = start.above(300).left(300)
    r.dragDrop(start, end)
    collect()

    # go down
    end = start.above(300).right(300)
    r.dragDrop(start, end)
    collect()
    
    # go left
    end = start.below(300).right(300)
    r.dragDrop(start, end)
    collect()

    if r.exists("1454343020253.png"):
        r.click("1454343020253.png")
    Debug.log('collect done')


def wanderSteal(): 
    start = r.getCenter()
    
    # go top
    end = start.below(280)
    r.dragDrop(start, end)
    if r.exists("1454337258874.png"):
        r.click("1454337258874.png")
        toClick = r.getCenter().above(280)
        for i in range(4):
            r.click(toClick.right(80 * i))
        
    # go right
    end = start.above(280).left(280)
    r.dragDrop(start, end)
    if r.exists("1454337258874.png"):
        r.click("1454337258874.png")
        toClick = r.getCenter().right(400)
        for i in range(5):
            r.click(toClick.below(60 * i))

    # go down
    end = start.above(280).right(280)
    r.dragDrop(start, end)
    if r.exists("1454337258874.png"):
        r.click("1454337258874.png")
        toClick = r.getCenter().below(220)
        for i in range(5):
            r.click(toClick.left(60 * i))
    
    # go left
    end = start.below(280).right(280)
    r.dragDrop(start, end)
    if r.exists("1454337258874.png"):
        r.click("1454337258874.png")
        toClick = r.getCenter().left(320)
        for i in range(5):
            r.click(toClick.above(60 * i))  
    
    r.wait(70)
    

def nothing(x):
    pass


def returnHome():    
    if r.exists("1454333202149.png"):
        r.click("1454333202149.png")
        r.wait("1454333227365.png")
        r.click("1454333227365.png")
        r.wait("1454333248854.png")
        r.click("1454333248854.png")
    elif r.exists("1454333305866.png"):
        r.click("1454333305866.png")
    Debug.log("RETURN Done")    
             

def farm():
    r.wait("1453998706906.png")
    r.click("1453998706906.png")
    r.setAutoWaitTimeout(12)
    r.wait("1453998721964.png")
    r.click("1453998721964.png")
    if r.wait("1453998840504.png"):
        wanderSteal()
        returnHome()
        return True
        
    elif r.exists("1453716128302.png"):
        r.click("1454174342067.png")
        return False


def trainTroops(total):
    r.click("1453952569173.png")
    trainBar = Pattern("1453952593719.png")
    r.wait(trainBar)
    archer = Pattern("1453952623673.png")
    Settings.MoveMouseDelay = 0.01
    perBarack = total / 4
    
    offsets = [(140, 225), (200, 225), (260, 225), (320, 225)]
    for i in range(4):
        o = offsets[i]
        r.click(trainBar.targetOffset(o[0], o[1]))
        for i in range(perBarack):
            r.click(archer)
    r.click("1453952643385.png")


def collect():
    clickFlag = False
    r.setAutoWaitTimeout(0.1)
    golds = r.findAll("1453952674225.png")
    if golds:
       clickFlag = True
       for g in golds:
           r.click(g)
        
    elixirs = r.findAll("1453952690966.png")
    if elixirs: 
        clickFlag = True
        for e in elixirs:
            r.click(e)
        
    darkElixirs = r.findAll("1453952714596.png")
    if darkElixirs:
        clickFlag = True
        for d in darkElixirs:
            r.click(d)
    return clickFlag


def donote():
    r.click("1453707563632.png")
    r.setAutoWaitTimeout(0.5)
    if r.exists("1453707610212.png"):
        r.click("1453707610212.png")
        for i in range(6):
            if r.exists("1453707470685.png"):
                r.click("1453707470685.png")
            else:
                break
    r.click("1453707883529.png")
    r.click("1453707800568.png")


def startCOC():
    r.setAutoWaitTimeout(2)
    if r.exists("1453348472944.png"):
        r.click("1453348472944.png")

    if r.exists("1454345155589.png"):
        r.click("1454345145879.png")
    if r.exists("1453355759177.png"):
        r.click("1453355776940.png")
    if r.exists("1453367221323.png"):
        r.click("1453367234552.png")
    if r.wait("1453952146233.png"):
        Debug.log("COC Started")

        return True 
    else:
        return False

         
def start():
    startFlag = False
    startCount = 0
    while not startFlag:
        startFlag = startCOC()
        startCount += 1
        if startCount == 20:
            break
    return startFlag


if __name__ == '__main__':
    popup("Please start BlueStacks first.")
    switchApp("BlueStacks")
    r = Region(App.focusedWindow())
    r.setFindFailedResponse(SKIP)
    f = Finder()

    while True:
        start()
        wanderCollect()
        #trainTroops(30)
        #farm()   
        