time = 18

def declareVar(i):
    clause = "(X0{i} Int)(X1{i} Int)(X2{i} Int)(X3{i} Int)(X4{i} Int)(X5{i} Int)(X6{i} Int)(X7{i} Int)(X8{i} Int)"
    return clause.format(i=i)

def declareVars():
    clause = "(benchmark sliding.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in range(time)]))
    return clause

def allCorrect(): 
    clause = "(and (>= X1{i} 0) (<= X1{i} 8) (>= X2{i} 0) (<= X2{i} 8) (>= X3{i} 0) (<= X3{i} 8) (>= X4{i} 0) (<= X4{i} 8) (>= X5{i} 0) (<= X5{i} 8)(>= X6{i} 0) (<= X6{i} 8)(>= X7{i} 0) (<= X7{i} 8)(>= X8{i} 0) (<= X8{i} 8))"
    return "\n".join([clause.format(i=i) for i in range(time)])

def transition(a,b,i):
    return "(and (= X{b}{i} 0)(= X{a}{inext} 0)(= X{b}{inext} X{a}{i})) ".format(a=a,b=b,i=i,inext=i+1)

def singleTransition(i):
    clause = "(and "
    clause += "(or (= X0{i} 0) (and (not (= X0{i} 0)) (= X0{i} X0{inext})) (or " + transition(0,1,i) + transition(0,3,i) + "))" 
    clause += "(or (= X1{i} 0) (and (not (= X1{i} 0)) (= X1{i} X1{inext})) (or " + transition(1,0,i) + transition(1,2,i) + transition(1,4,i) + "))"
    clause += "(or (= X2{i} 0) (and (not (= X2{i} 0)) (= X2{i} X2{inext})) (or " + transition(2,1,i) + transition(2,5,i) + "))"
    clause += "(or (= X3{i} 0) (and (not (= X3{i} 0)) (= X3{i} X3{inext})) (or " + transition(3,4,i) + transition(3,6,i) + transition(3,0,i) + "))"
    clause += "(or (= X4{i} 0) (and (not (= X4{i} 0)) (= X4{i} X4{inext})) (or " + transition(4,3,i) + transition(4,1,i) + transition(4,7,i) + "))"
    clause += "(or (= X5{i} 0) (and (not (= X5{i} 0)) (= X5{i} X5{inext})) (or " + transition(5,4,i) + transition(5,2,i) + transition(5,8,i) + "))"
    clause += "(or (= X6{i} 0) (and (not (= X6{i} 0)) (= X6{i} X6{inext})) (or " + transition(6,7,i) + transition(6,3,i) + "))"
    clause += "(or (= X7{i} 0) (and (not (= X7{i} 0)) (= X7{i} X7{inext})) (or " + transition(7,6,i) + transition(7,8,i) + transition(7,4,i) + "))"
    clause += "(or (= X8{i} 0) (and (not (= X8{i} 0)) (= X8{i} X8{inext})) (or " + transition(8,7,i) + transition(8,5,i) + ")))"
    return clause.format(i=i, inext=i+1)

def allTransitions():
    return "\n".join([singleTransition(i) for i in range(time-1)])

def initial():
    return "(and (= X00 3)(= X10 7)(= X20 6)(= X30 5) (= X40 1)(= X50 2) (= X60 4) (=X70 0) (= X80 8))"
def goal():
    clause = "(or "
    clause += "\n".join(["(and (= X0{max} 1)(= X1{max} 2)(= X2{max} 3)(= X3{max} 4) (= X4{max} 5)(= X5{max} 6) (= X6{max} 7) (=X7{max} 8) (= X8{max} 0))".format(max=i) for i in range(time)])
    return clause + ")"
def formula(): 
    return ":formula (and \n{}\n)".format("".join([allTransitions(), allCorrect(), initial(), goal()]))


print(declareVars())
print(formula())
