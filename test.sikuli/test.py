# COC Auto Farm Script


def farm():
    r.click("1453366918127.png")
    r.click("1453366933167.png")


def trainTroops():
    r.click("1453363485336.png")  
    r.click("1453363502778.png")
    trainBar = Pattern("1453364606200.png") 
    goblin = Pattern("1453364936808.png")
    Settings.MoveMouseDelay = 0.01
    r.click(trainBar.targetOffset(140, 225))
    for i in range(10):
        r.click(goblin)
        
    r.click(trainBar.targetOffset(200, 225))
    for i in range(10):
        r.click(goblin)

    r.click(trainBar.targetOffset(260, 225))
    for i in range(10):
        r.click(goblin)

    r.click(trainBar.targetOffset(320, 225))
    for i in range(10):
        r.click(goblin)

    r.click("1453366780412.png")
    return


def farm():
    pass    


def collect():
    r.setAutoWaitTimeout(0.1)
    golds = r.findAll(Pattern("1453359139007.png").similar(0.55))
    if golds:
        for g in golds:
            r.click(g)
        
    elixirs = r.findAll("1453359162038.png")
    if elixirs: 
        for e in elixirs:
            r.click(e)
        
    darkElixirs = r.findAll(Pattern("1453359216407.png").similar(0.80))
    reDarkElixirs = r.findAll(Pattern("1453359216407.png").similar(0.80).targetOffset(10,-2))
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
        if startCount == 10:
            break
    return startFlag


if __name__ == '__main__':
    # popup("Please start COC in BlueStacks.\nZoom out as far as possible.")
    switchApp("BlueStacks")
    r = Region(App.focusedWindow())
    r.setFindFailedResponse(SKIP)
    
    if start():
        collect()
    # trainTroops()
    exit()

    
    
