pindex = range(40)

def declareVar(i):
    clause = "(I{i} Int) (J{i} Int) (C{i} Int)"
    return clause.format(i=i)

def declareVars():
    clause = "(benchmark chip.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in pindex]) + declareVar(40))
    return clause

def initialValues():
    return "(and (= I0 1) (= J0 1) (= C0 0))"

def bounds():
    clause = "(<= I{i} 21) (<= J{i} 21) (> I{i} 0) (> J{i} 0) (>= C{i} 0)"
    return "(and {})".format(" ".join([clause.format(i=i) for i in pindex]) + clause.format(i=40))

def stepI(i):
    clause = "(and (= I{inext} (+ I{i} 1)) (= J{i} J{inext}) (or (and (>= C{i} 20) (= C{inext} (+ C{i} I{i}))) (and (< C{i} 20) (= C{inext} (+ C{i} 1)))) )"
    return clause.format(i=i, inext=i+1)

def stepJ(i):
    clause = "(and (= J{inext} (+ J{i} 1))(= I{i} I{inext}) (or (and (>= C{i} 20) (= C{inext} (+ C{i} J{i}))) (and (< C{i} 20) (= C{inext} (+ C{i} 1)))))"
    return clause.format(i=i, inext=i+1)
    
def step(i):
    clause = "(or {} {})".format(stepI(i), stepJ(i))
    return clause 

def allSteps():
    return "\n".join(step(i) for i in pindex)

def endRequirements():
    return "(= C40 330)"

def formula(): 
    return ":formula (and \n{}\n))".format("\n".join([initialValues(), bounds(), allSteps(), endRequirements()]))


print(declareVars())
print(formula())