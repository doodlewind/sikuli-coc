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
        goldsLv12 = r.findAll("1453953394802.png")
        return f.findBuilding(goldsLv10Lv11, goldsLv12)

    def findAllElixir(self):
        # elixirsLv8Lv9 = r.findAll("1453953091853.png")
        # elixirsLv10 = r.findAll("1453953333748.png")
        elixirsLv11Lv12 = r.findAll("1453953285030.png")
        darkElixirs = r.findAll("1453996663798.png")
        return f.findBuilding(elixirsLv11Lv12, darkElixirs)
    

    def findAllArcherTower(self):
        towersLv7Lv8Lv9 = r.findAll("1453455834637.png")
        towersLv10 = r.findAll("1453566337555.png")
        return f.findBuilding(towersLv7Lv8Lv9, towersLv10)

    def findAllWizardTower(self):
        towersLv1Lv2Lv3Lv4Lv5 = r.findAll("1453567230793.png")
        towersLv6 = r.findAll("1453567557482.png")
        return f.findBuilding(towersLv1Lv2Lv3Lv4Lv5)


def steal(direction):
    clickFlag = False
    
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

    def clickTarget(target, direction):
        if direction == 'UP':
            l = Location(target[0], target[1] - 120)
        elif direction == 'RIGHT':
            l = Location(target[0] + 120, target[1])
        elif direction == 'DOWN':
            l = Location(target[0], target[1] + 120)
        else:
            l = Location(target[0] - 120, target[1])
        r.doubleClick(l)

    def stealTownHall():
        clickFlag = False
        thPoint = f.findTownHall()
        if thPoint is not None:
            minX = min(threatPoints, key = lambda x : x[0])
            maxX = max(threatPoints, key = lambda x : x[0])
            minY = max(threatPoints, key = lambda x : x[1])
            maxY = max(threatPoints, key = lambda x : x[1])
            if (thPoint[0] < minX or thPoint[0] > maxX) and (thPoint[1] < minY or thPoint[1] > maxY):
                if thPoint[0] < minX:
                    xOffset = -80
                else:
                    xOffset = 80
                if thPoint[1] < minY:
                    yOffset = -80
                else:
                    yOffset = 80
                stealPoint = Location(thPoint[0] + xOffset, thPoint[1] + yOffset)
                clickFlag = True
                r.click("1453952476599.png")
                r.click(stealPoint)
            return clickFlag

    start = time.time()
    elixirPoints = f.findAllElixir()
    Debug.log("Time for elixir: " + str(time.time() - start))

    start = time.time()
    goldPoints = f.findAllGold()
    Debug.log("Time for gold: " + str(time.time() - start))
    
    targetPoints = elixirPoints + goldPoints

    for t in targetPoints:
        clickFlag = True
        clickTarget(t, direction)
    # threatPoints = archerTowerPoints + wizardTowerPoints    
    # for t in targetPoints:
    #     stealPoint = analyse(t, threatPoints, 165)
    #     if stealPoint:
    #         clickFlag = True
    #         r.click("1453706733808.png")
    #         r.click(stealPoint)
    # stealTownHall(threatPoints) 
    return clickFlag


def wander(act):
    
    def myDragDrop(start, end):
        Settings.MoveMouseDelay = 0.1
        r.dragDrop(start, end)
    
    start = r.getCenter()
    # reset to top left
    end = start.below(250).right(300)
    Settings.MoveMouseDelay = 0.1
    Settings.DelayBeforeDrop = 0.05
    Settings.MoveMouseDelay = 0.05
    myDragDrop(start, end)

    # go top
    end = start.above(190).left(500)
    myDragDrop(start, end)
    act('UP')

    # go right
    end = start.above(280).left(500)
    myDragDrop(start, end)
    act('RIGHT')

    # go down
    end = start.above(280).right(500)
    myDragDrop(start, end)
    act('DOWN')

    # go left
    end = start.below(280).right(500)
    myDragDrop(start, end)
    act('LEFT')
    

def nothing(x):
    pass


def farm():
    r.wait("1453998706906.png")
    trainTroops(60)
    r.click("1453998706906.png")
    r.setAutoWaitTimeout(5)
    if r.wait("1453998721964.png"):
        r.click("1453998721964.png")
        if r.exists("1453716128302.png"):
            return False
        farmOnce()


def farmOnce():
    r.setAutoWaitTimeout(6)
    if r.exists("1453998840504.png"):
        wander(steal)
        Debug.log("FARM Done")
        r.setAutoWaitTimeout(10)
        r.wait(10)
        r.click("1453709602497.png")
        r.click("1453709618877.png")
        r.wait("1453709641549.png")
        r.click("1453709641549.png")
        Debug.log("RETURN Done")


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


def collect(direction):
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
    if r.wait("1453952146233.png"):
        Debug.log("COC Started")

        return True
    else: 
        if r.exists("1453355759177.png"):
            r.click("1453355776940.png")
        if r.exists("1453367221323.png"):
            r.click("1453367234552.png")
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

    if start():
        while True:
            wander(collect)
            farm()
    else:
        popup("COC not started! Exit now.")
        