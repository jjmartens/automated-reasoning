pieces = range(12)
power = range(2)
regular = range(2,12)
MAX_WIDTH = 30
MAX_HEIGHT = 30
widths = [4,4,4,4,5,6,6,6,7,7,10,10]
heights = [3,3,5,6,20,9,10,11,8,12,10,20]

def declareVar(i):
    clause = "(X{i} Int) (Y{i} Int) (O{i} Bool) (H{i} Int) (W{i} Int)"
    return clause.format(i=i)

def declareVars():
    clause = "(benchmark chip.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in pieces]))
    return clause

def declareOrientation(i):
    clause = "(or (and (not O{i}) (= H{i} {iheight}) (= W{i} {iwidth})) (and (O{i}) (= H{i} {iwidth}) (= W{i} {iheight})))".format(i=i, iheight=heights[i], iwidth=widths[i])
    return clause

def declareOrientations():
    return "\n".join([declareOrientation(i) for i in pieces])

def onLeft(i,j):
    clause = "(<= (+ X{i} W{i}) X{j})"
    return clause.format(i=i, j=j)

def onTop(i,j):
    clause = "(<= (+ Y{i} H{i}) Y{j})"
    return clause.format(i=i, j=j)

# Piece i connects on left edge 
def connectLeftEdge(i,j):
    clause = "(and (= X{i} (+ X{j} W{j})) (<= Y{j} (+ Y{i} H{i})) (<= Y{i} (+ Y{j} H{j})))"
    return clause.format(i=i, j=j)

def connectTopEdge(i,j):
    clause = "(and (= Y{i} (+ Y{j} H{j})) (<= X{j} (+ X{i} W{i})) (<= X{i} (+ X{j} W{j})))"
    return clause.format(i=i, j=j)

def connectAnyEdge(i,j):
    clause = "(or {})".format(" ".join([connectLeftEdge(i,j), connectLeftEdge(j,i), connectTopEdge(i,j), connectTopEdge(j,i)]))
    return clause

def notOverlayingAny():
    clause = "{}".format("\n".join([notOverlaying(i,j) for i in pieces for j in pieces if j<i])) 
    return clause

def notOverlaying(i,j):
    return "(or {})".format(" ".join([onLeft(i,j), onLeft(j,i), onTop(i,j), onTop(j,i)]))

def onBoard(i): 
    return "(<= X{i} {mw}) (>= X{i} 0) (>= Y{i} 0) (<= Y{i} {mh})".format(i=i, mw=MAX_WIDTH, mh=MAX_HEIGHT)

def allOnBoard():
    return "\n".join([onBoard(i) for i in pieces])

def connectToPower(i):
    return connectAnyEdge(i,0)

def allRegularConnectingToPower():
    clause = "(and {})".format(" ".join([connectToPower(i) for i in regular]))
    return clause

def distanceOver18(i,j):
    clause = "(or (<= (+ X{i} X{i} W{i}) (+ X{j} X{j} W{j} 36) (<= (+ Y{i} Y{i} Y{i}) (+ Y{j} Y{j} Y{j} 36)))"
    return "(or {} {})".format(clause.format(i=i,j=j), clause.format(i=j,j=i))

def formula(): 
    return ":formula (and \n{}\n))".format("".join([declareOrientations(), notOverlayingAny(), allRegularConnectingToPower() , allOnBoard()]))


print(declareVars())
print(formula())