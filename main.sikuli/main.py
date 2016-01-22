# COC Auto Farm Script
import time
import math
import struct


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

    def findAllElixir(self):
        elixirs = r.findAll("1453455688110.png")
        results = []
        for e in elixirs:
            results.append((e.x, e.y))
        return results

    def findAllArcherTower(self):
        towers = r.findAll("1453455834637.png")
        results = []
        for t in towers:
            results.append((t.x, t.y))  
        return results


def stealElixir():
    start = time.time()
    
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

    elixirPoints = f.findAllElixir()
    archerTowerPoints = f.findAllArcherTower()
    
    for e in elixirPoints:
        # if it's safe to steal
        # analyse() will return the location to put archer
        stealPoint = analyse(e, archerTowerPoints, 159)
        if stealPoint:
            click(stealPoint)
            print "elixir available"
        else:
            print "elixir not available"

    print "\ntime cost:", time.time() - start

        
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
    r.click(trainBar.targetOffset(140, 225))
    for i in range(10):
        r.click(archer)
        
    r.click(trainBar.targetOffset(200, 225))
    for i in range(10):
        r.click(archer)

    r.click(trainBar.targetOffset(260, 225))
    for i in range(10):
        r.click(archer)

    r.click(trainBar.targetOffset(320, 225))
    for i in range(10):
        r.click(archer)

    r.click("1453366780412.png")
    return 


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
        Debug.log("COCO Started")

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

    stealElixir()
    # if start():
        # trainTroops()
        # farm()  
        # wander(collect)
