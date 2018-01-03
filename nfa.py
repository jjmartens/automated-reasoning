states = range(2)


def declareTransitions():
    clause = "(A{i}{j} Boolean)(B{i}{j} Boolean)"
    return  " ".join([clause.format(i=i,j=j) for i in states for j in states])


def declareFinalStates(i):
    return "(F{i} Boolean)".format(i=i)

def declareVars():
    clause = "(benchmark villages.smt\n:logic QF_UFLIA\n:extrafuns ({} {})".format(" ".join([declareFinalStates(i) for i in states]), declareTransitions())
    return clause

def transitions(word):
    clause = "(or (and A01 B11 F1) (and A00 B00 F0) (and A00 B01 F1) (and A01 B10 F0))"
    
    return 

def formula(): 
    return ":formula (and \n{}\n))".format("".join([allCorrect(), initialState(), allTransitions()]))

print(declareVars())
print(formula())
