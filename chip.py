pieces = range(10)
widths = [3 for i in range(10)]
heights = [3 for i in range(10)]


def declareVar(i):
    clause = "(X{i} Int) (Y{i} Int) (O{i} Bool)"
    return clause.format(i=i)

def declareVars():
    clause = "(benchmark chip.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in pieces]))
    return clause

def onLeft(i,j):
    clause = "(or (and (not O{i}) (<= (+ X{i} {iwidth}) X{j})) (and O{i} (<= (+ X{i} {iheight}) X{j})))"
    return clause.format(i=i, iwidth=2, j=j, iheight=3)

def onTop(i,j):
    clause = "(or (and (not O{i}) (<= (+ Y{i} {iheight}) X{j})) (and O{i} (<= (+ Y{i} {iwidth}) X{j})))"
    return clause.format(i=i, iwidth=2, j=j, iheight=3)


def notOverlayingAny():
    clause = "{}".format("\n".join([notOverlaying(i,j) for i in pieces for j in pieces if j != i])) 
    return clause

def notOverlaying(i,j):
    return "(and (or {}) (or {}))".format(" ".join([onLeft(i,j), onLeft(j,i)]), " ".join([onTop(i,j), onTop(j,i)]))

def onBoard(i): 
    return "(<= X{i} 20) (>= X{i} 0) (>= Y{i} 0) (<= Y{i} 3)".format(i=i)

def allOnBoard():
    return "\n".join([onBoard(i) for i in pieces])

def formula(): 
    return ":formula (and \n{}\n))".format("".join([notOverlayingAny(), allOnBoard()]))


print(declareVars())
print(formula())