# C Auto Farm Script
import time
import math


class Finder:        
        
    def findTownHall(self):
        if r.exists(Pattern("1453393835539.png").similar(0.85)):
            return 8
        elif r.exists(Pattern("1453394040213.png").similar(0.85)):
            return 7
        elif r.exists(Pattern("1453394091038.png").similar(0.85)):
            return 6
        else:
            return 0

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
    
    def distance(p1, p2):
        return math.sqrt( math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2) )

    def minDistancePoint(point, threats):
        return min( threats, key=lambda x : distance(x, point) )

    def analyse(point, threats, threshold):
        minThreat = minDistancePoint(point, threats)
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

    start = time.time()
    elixirPoints = f.findAllElixir()
    Debug.log("Time for elixir: " + str(time.time() - start))

    start = time.time()
    goldPoints = f.findAllGold()
    Debug.log("Time for gold: " + str(time.time() - start))
    
    targetPoints = elixirPoints + goldPoints

    start = time.time()
    archerTowerPoints = f.findAllArcherTower()
    Debug.log("Time for archer tower: " + str(time.time() - start))
    
    start = time.time()
    wizardTowerPoints = f.findAllWizardTower()
    Debug.log("Time for wizard tower: " + str(time.time() - start))
    
    threatPoints = archerTowerPoints + wizardTowerPoints 
    for t in targetPoints:
        # if it's safe to steal
        # analyse() will return the location to put archer
        stealPoint = analyse(t, threatPoints, 159)
        if stealPoint:
            r.click(stealPoint)


def wander(callback):
    
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
    callback()

    # go right
    end = start.above(280).left(500)
    myDragDrop(start, end)
    callback()

    # go down
    end = start.above(280).right(500)
    myDragDrop(start, end)
    callback()

    # go left
    end = start.below(280).right(500)
    myDragDrop(start, end)
    callback()


def nothing():
    pass


def farm():
    r.click("1453368735143.png")
    r.click("1453369288279.png")
    r.setAutoWaitTimeout(5)
    if r.wait("1453369323452.png"):
        if r.exists():
            pass
    r.click("1453369509967.png")


def trainTroops():
    r.click("1453452912845.png")
    trainBar = Pattern("1453364606200.png") 
    archer = Pattern("1453459008655.png")
    Settings.MoveMouseDelay = 0.01
    
    offsets = [(140, 225), (200, 225), (260, 225), (320, 225)]
    for i in range(4):
        o = offsets[i]
        r.click(trainBar.targetOffset(o[0], o[1]))
        for i in range(10):
            r.click(archer)
    r.click("1453366780412.png")


def collect():
    r.setAutoWaitTimeout(0.1)
    golds = r.findAll("1453371882963.png")
    if golds:
        for g in golds:
            r.click(g)
        
    elixirs = r.findAll("1453371892290.png")
    if elixirs: 
        for e in elixirs:
            r.click(e)
        
    darkElixirs = r.findAll("1453371962628.png")
    if darkElixirs:
        for d in darkElixirs:
            r.click(d)


def startCOC():
    r.setAutoWaitTimeout(1)
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

    # if start():
        # trainTroops()
        # farm()
        # wander(steal)
        # wander(collect)
