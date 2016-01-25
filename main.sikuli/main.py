# C Auto Farm Script
import time
import math


class Finder:        
        
    def findTownHall(self):
        
        townHallLv8 = r.find(Pattern("1453393835539.png").similar(0.85))
        if townHallLv8 is not None:
            return (townHallLv8.getX(), townHallLv8.getY())

        townHallLv7 = r.find(Pattern("1453708440856.png").similar(0.85))
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
        # goldsLv9 = r.findAll("1453565509397.png")
        goldsLv10Lv11 = r.findAll("1453566796795.png")
        # goldsLv12 = r.findAll("1453565859031.png")
        return f.findBuilding(goldsLv10Lv11)

    def findAllElixir(self):
        elixirsLv9 = r.findAll("1453566941841.png")
        # elixirsLv10 = r.findAll("1453565377030.png")
        elixirsLv11Lv12 = r.findAll("1453567004749.png")
        return f.findBuilding(elixirsLv9, elixirsLv11Lv12)
    

    def findAllArcherTower(self):
        towersLv7Lv8Lv9 = r.findAll("1453455834637.png")
        towersLv10 = r.findAll("1453566337555.png")
        return f.findBuilding(towersLv7Lv8Lv9, towersLv10)

    def findAllWizardTower(self):
        towersLv1Lv2Lv3Lv4Lv5 = r.findAll("1453567230793.png")
        # towersLv6 = r.findAll("1453567557482.png")
        return f.findBuilding(towersLv1Lv2Lv3Lv4Lv5)


def steal():
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
            return Location(r.getX() - 120, r.getY() - 120)
            
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

    def stealHownHall():
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
                r.click("1453706733808.png")
                r.click(stealPoint)
            return clickFlag

    start = time.time()
    elixirPoints = f.findAllElixir()
    Debug.log("Time for elixir: " + str(time.time() - start))

    start = time.time()
    goldPoints = f.findAllGold()
    Debug.log("Time for gold: " + str(time.time() - start))
    
    targetPoints = elixirPoints + goldPoints

    # start = time.time()
    # archerTowerPoints = f.findAllArcherTower()
    # Debug.log("Time for archer tower: " + str(time.time() - start))
    
    # start = time.time()
    # wizardTowerPoints = f.findAllWizardTower()
    # Debug.log("Time for wizard tower: " + str(time.time() - start))
    
    # threatPoints = archerTowerPoints + wizardTowerPoints
    threatPoints = []
    
    for t in targetPoints:
        Debug.log(str(time.time()))
        # if it's safe to steal
        # analyse() will return the location to put archer
        stealPoint = analyse(t, threatPoints, 165)
        if stealPoint:
            clickFlag = True
            r.click("1453706733808.png")
            r.click(stealPoint)

    # stealTownHall(threatPoints) 
    return clickFlag


def wander(callback):
    clickFlag = False
    
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
    clickFlag = clickFlag or callback()

    # go right
    end = start.above(280).left(500)
    myDragDrop(start, end)
    clickFlag = clickFlag or callback()

    # go down
    # end = start.above(280).right(500)
    # myDragDrop(start, end)
    # clickFlag = clickFlag or callback()

    # go left
    # end = start.below(280).right(500)
    # myDragDrop(start, end)
    # clickFlag = clickFlag or callback()
    
    return clickFlag


def nothing():
    pass


def farm():
    r.click("1453368735143.png")
    r.setAutoWaitTimeout(5)
    if r.wait("1453369288279.png"):
        r.click("1453369288279.png")
    farmFlag = True
    farmOnce()


def farmOnce():
    r.setAutoWaitTimeout(6)
    if r.wait("1453369323452.png"):
        wander(steal)
        if r.exists("1453709602497.png"):
            r.click("1453709618877.png")
        r.wait("1453709641549.png")
        r.click("1453709641549.png")


def trainTroops(total):
    r.click("1453452912845.png")
    trainBar = Pattern("1453364606200.png") 
    archer = Pattern("1453459008655.png")
    Settings.MoveMouseDelay = 0.01
    perBarack = total / 4
    
    offsets = [(140, 225), (200, 225), (260, 225), (320, 225)]
    for i in range(4):
        o = offsets[i]
        r.click(trainBar.targetOffset(o[0], o[1]))
        for i in range(perBarack):
            r.click(archer)
    r.click("1453366780412.png")


def collect():
    clickFlag = False
    r.setAutoWaitTimeout(0.1)
    golds = r.findAll("1453371882963.png")
    if golds:
       clickFlag = True
       for g in golds:
           r.click(g)
        
    elixirs = r.findAll("1453371892290.png")
    if elixirs: 
        clickFlag = True
        for e in elixirs:
            r.click(e)
        
    darkElixirs = r.findAll("1453371962628.png")
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
    if r.wait("1453356703238.png"):
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
        farm()
        # wander(collect)
        # trainTroops()
        # wander(steal)    
    else:
        popup("COC not started! Exit now.")
        