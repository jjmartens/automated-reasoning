time = range(25)

def declareVar(i):
    clause = "(L{i} Int)(A{i} Int)(B{i} Int)(C{i} Int)(D{i} Int)(T{i} Int)"
    return clause.format(i=i)

def declareVars():
    clause = "(benchmark villages.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in time]))
    return clause

def allCorrect(): 
    clause = "(and (>= L{i} 0) (<= L{i} 5) (>= T{i} 0) (<= T{i} 250) (>= A{i} 0) (>= B{i} 0) (>= C{i} 0) (>= D{i} 0) (<= A{i} 110) (<= C{i} 110) (<= B{i} 160) (<= D{i} 160))"
    return "\n".join([clause.format(i=i) for i in time])

def transitionFromS(i):
    clause = "(and (= L{i} 0) (= L{inext} 1) {costs}) (and (= L{i} 0) (= L{inext} 3) {costs})"
    return clause.format(i=i, inext=i+1, costs=travelCosts(i,15,0))

def transitionFromA(i):
    toS = "(and (= L{i} 1) (= L{inext} 0) (= (+ (- A{i} 15) T{i}) (+ A{inext} T{inext})) (<= A{inext} 95) {costs15})"
    toC = "(and (= L{i} 1) (= L{inext} 3) (= (+ (- A{i} 11) T{i}) (+ A{inext} T{inext})) (<= A{inext} 99) {costs11})"
    toB = "(and (= L{i} 1) (= L{inext} 2) (= (+ (- A{i} 17) T{i}) (+ A{inext} T{inext})) (<= A{inext} 93) {costs17})"
    clause = toS + toC + toB
    return clause.format(i=i,inext=i+1, costs15=travelCosts(i,15,1), costs11=travelCosts(i,11,1), costs17=travelCosts(i,17,1))

def transitionFromB(i):
    toA = "(and (= L{i} 2) (= L{inext} 1) (= (+ (- B{i} 17) T{i}) (+ B{inext} T{inext})) (<= B{inext} 143) {costs17})"
    toC = "(and (= L{i} 2) (= L{inext} 3) (= (+ (- B{i} 11) T{i}) (+ B{inext} T{inext})) (<= B{inext} 149) {costs11})"
    toD = "(and (= L{i} 2) (= L{inext} 4) (= (+ (- B{i} 20) T{i}) (+ B{inext} T{inext})) (<= B{inext} 140) {costs20})"
    clause = toA + toC + toD
    return clause.format(i=i,inext=i+1, costs17=travelCosts(i,17,2), costs11=travelCosts(i,11,2), costs20=travelCosts(i,20,2))

def transitionFromC(i):
    toA = "(and (= L{i} 3) (= L{inext} 1) (= (+ (- C{i} 11) T{i}) (+ C{inext} T{inext})) (<= C{inext} 99) {costs11})"
    toB = "(and (= L{i} 3) (= L{inext} 2) (= (+ (- C{i} 11) T{i}) (+ C{inext} T{inext})) (<= C{inext} 99) {costs11})"
    toD = "(and (= L{i} 3) (= L{inext} 4) (= (+ (- C{i} 20) T{i}) (+ C{inext} T{inext})) (<= C{inext} 90) {costs20})"
    toS = "(and (= L{i} 3) (= L{inext} 0) (= (+ (- C{i} 15) T{i}) (+ C{inext} T{inext})) (<= C{inext} 95) {costs15})"
    clause = toS + toA + toB + toD
    return clause.format(i=i,inext=i+1, costs15=travelCosts(i,15,3), costs11=travelCosts(i,11,3), costs20=travelCosts(i,20,3))

def transitionFromD(i):
    toB = "(and (= L{i} 4) (= L{inext} 2) (= (+ (- D{i} 20) T{i}) (+ D{inext} T{inext})) (<= D{inext} 140) {costs20})"
    toC = "(and (= L{i} 4) (= L{inext} 3) (= (+ (- D{i} 20) T{i}) (+ D{inext} T{inext})) (<= D{inext} 140) {costs20})"
    clause = toB + toC
    return clause.format(i=i,inext=i+1, costs20=travelCosts(i,20,4))



def singleTransition(i):
    clause = "(or {})"
    return clause.format(" ".join([transitionFromS(i),transitionFromA(i), transitionFromB(i), transitionFromC(i), transitionFromD(i)]))


def travelCosts(i, costs, frompoint=0):
    clause = "(= A{inext} (- A{i}  {costs})) (= B{inext} (- B{i}  {costs})) (= C{inext} (- C{i}  {costs})) (= D{inext} (- D{i}  {costs}))"
    if frompoint == 1:
        clause = "(= B{inext} (- B{i}  {costs})) (= C{inext} (- C{i}  {costs})) (= D{inext} (- D{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 2:
        clause = "(= A{inext} (- A{i}  {costs})) (= C{inext} (- C{i}  {costs})) (= D{inext} (- D{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 3:
        clause = "(= A{inext} (- A{i}  {costs})) (= B{inext} (- B{i}  {costs})) (= D{inext} (- D{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 4:
        clause = "(= A{inext} (- A{i}  {costs})) (= B{inext} (- B{i}  {costs})) (= C{inext} (- C{i}  {costs})) (>= T{i} T{inext})"
    return clause.format(i=i,inext=i+1, costs=costs)

def allTransitions():
    return " ".join([singleTransition(i) for i in time[:-1]])

def equal(i,j):
    clause = "(and (= A{i} A{j}) (= B{i} B{j})  (= C{i} C{j}) (= D{i} D{j})  (= L{i} L{j})  (= T{i} T{j}))"
    return clause.format(i=i,j=j)

def loop():
    clause = "(or {})".format("\n".join([equal(i,j) for i in time for j in time if j < i]))
    return clause

def initialState(): 
    return "(and (= L0 0) (= T0 250) (= A0 50) (= D0 50) (= B0 160) (= C0 110))"


def formula(): 
    return ":formula (and \n{}\n))".format("".join([allCorrect(), initialState(), allTransitions(), loop()]))


print(declareVars())
print(formula())
