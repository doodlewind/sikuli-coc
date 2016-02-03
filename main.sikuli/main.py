# Clash of Clans Auto Farm Script
# Start script on OS X in CLI:
# $ /Applications/SikuliX.app/run -r /path/to/sikuli-coc/main
# Stop script by press command + shift + C

import time
import math
import random


class Finder:        
        
    def findTownHall(self):
        
        townHallLv8 = r.find("1453952397524.png")
        if townHallLv8 is not None:
            return (townHallLv8.getX(), townHallLv8.getY())
        townHallLv7 = r.find("1453952443462.png")
        if townHallLv7 is not None:
            return [townHallLv7.getX(), townHallLv7.getY()] 
        return None

    def locationOf(self, *args):
        results = []
        for building in args:
            if building is not None:
                for b in building:
                    results.append((b.x, b.y))
        return results

    def findAllGold(self):
        goldsLv10Lv11 = r.findAll("1453953362202.png")
        if goldsLv10Lv11 is not None:
            return f.locationOf(goldsLv10Lv11)
        
        goldsLv9 = r.findAll("1453953124704.png")
        # goldsLv12 = r.findAll("1453953394802.png")
        return f.locationOf(goldsLv9)
    
    def findAllElixir(self):
        elixirsLv11Lv12 = r.findAll("1453953285030.png")
        if elixirsLv11Lv12 is not None:
            return f.locationOf(elixirsLv11Lv12)

        elixirsLv8Lv9 = r.findAll("1453953091853.png")
        # elixirsLv10 = r.findAll("1453953333748.png")
        # darkElixirs = r.findAll("1453996663798.png")
        return f.locationOf(elixirsLv8Lv9)
    

    def findAllArcherTower(self):
        towersLv7Lv8Lv9 = r.findAll("1453455834637.png")
        towersLv10 = r.findAll("1453566337555.png")
        return f.findBuilding(towersLv7Lv8Lv9, towersLv10)

    def findAllWizardTower(self):
        towersLv1Lv2Lv3Lv4Lv5 = r.findAll("1453567230793.png")
        towersLv6 = r.findAll("1453567557482.png")
        return f.findBuilding(towersLv1Lv2Lv3Lv4Lv5)


def steal(direction):
    
    def distance(p1, p2):
        return math.sqrt( math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2) )

    def minDistancePoint(point, threats):
        if len(threats) == 0:
            return None
        return min( threats, key=lambda x : distance(x, point) )

    def analyse(point, threats, threshold):
        minThreat = minDistancePoint(point, threats)
        if minThreat is None:
            return Location(r.getX() - 20, r.getY() - 20)
            
        if distance(point, minThreat) > threshold:
            dx = minThreat[0] - point[0]
            dy = minThreat[1] - point[1]
            # use length dz to unify the direction
            dz = math.sqrt(dx*dx + dy*dy)
            px = max(r.getX(), point[0] - 120 * dx/dz)
            py = max(r.getY(), point[1] - 120 * dy/dz)
            return Location(px, py)
        else:
            return False


    def getSafeClickLocation(x, y, direction):
        xMin = r.getX() + 20
        yMin = r.getY() + 20
        xMax = xMin + r.getW() - 20
        yMax = yMin + r.getH() - 20
        
        if direction == 'UP':
            y = max(y - 180, yMin)
        elif direction == 'RIGHT':
            x = min(x + 180, xMax)
        elif direction == 'DOWN':
            y = min(y + 180, yMax)
        else:
            x = max(x - 180, xMin)
        return Location(x, y)
    
    def clickTarget(target, direction):
        for i in range(3):
            randOff = int(random.random() * 100) - 100
            l = getSafeClickLocation(target[0] + randOff, target[1] + randOff, direction)
            r.click(l)
            
    clickFlag = False
    start = time.time()
    elixirPoints = f.findAllElixir()
    Debug.log("Time for elixir: " + str(time.time() - start))

    start = time.time()
    goldPoints = f.findAllGold()
    Debug.log("Time for gold: " + str(time.time() - start))

    # start = time.time()
    # thPoint = f.findTownHall()
    # Debug.log("Time for townhall: " + str(time.time() - start))
    targetPoints = elixirPoints + goldPoints

    if r.exists("1454337258874.png"):
        r.click("1454337258874.png")
    for t in targetPoints:
        clickFlag = True
        clickTarget(t, direction)
        
    return clickFlag


def myDragDrop(start, end):
    Settings.MoveMouseDelay = 0.1
    r.dragDrop(start, end)


def wander(act):
    startTime = time.time()
    start = r.getCenter()
    # go top
    end = start.below(300)
    r.dragDrop(start, end)
    act('UP') 

    # go right
    end = start.above(300).left(300)
    r.dragDrop(start, end)
    act('RIGHT')

    # go down
    end = start.above(300).right(300)
    r.dragDrop(start, end)
    act('DOWN')
    
    # go left
    end = start.below(300).right(300)
    r.dragDrop(start, end)
    act('LEFT')

    if r.exists("1454343020253.png"):
        r.click("1454343020253.png")
    
    if time.time() - startTime < 60:
        r.wait(40)

        Debug.log('WANDER done')


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


def quickSteal(): 
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
    r.wait(40)
    

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
    if r.wait("1453998706906.png"):
        r.click("1453998706906.png")
    # differt button
    elif r.wait("1454378179649.png"):
        r.click("1454378179649.png")
    r.setAutoWaitTimeout(12)
    r.wait("1453998721964.png")
    r.click("1453998721964.png")
    if r.wait("1453998840504.png"):
        wander(steal)
    elif r.exists("1453716128302.png"):
        r.click("1454174342067.png")


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
    r.setAutoWaitTimeout(0.3)
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


def donate():
    r.click("1454383023512.png")
    if r.wait("1454380331111.png"):
        r.click("1454380331111.png")
        for i in range(6):
            if r.wait("1454380350047.png"):
                r.click("1454380350047.png")
            else:
                break
    if r.exists("1454380371569.png"):
        r.click("1454380371569.png")
    r.click("1454380396647.png")


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
    if r.exists(Pattern("1454380729337.png").exact()):
        r.click("1454380744610.png")
        
    if r.wait("1453952146233.png"):
        Debug.log("COC Started")

        return True 
    else:
        return False

         
def start():
    switchApp("BlueStacks")
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
        trainTroops(30)
        #donate()
        farm()
        returnHome()
        