time = range(18)
villages = range(1,5)

def declareVar(i):
    clause = "(V{j}{i} Int)"
    returnclause = " ".join(clause.format(j=j,i=i) for j in villages) + "(L{i} Int)(T{i} Int)".format(i=i)
    return returnclause

def declareVars():
    clause = "(benchmark villages.smt\n:logic QF_UFLIA\n:extrafuns ({})".format(" ".join([declareVar(i) for i in time]))
    return clause


def allCorrect(): 
    clause = "(and (>= L{i} 0) (<= L{i} 4) (>= T{i} 0) (<= T{i} 262) (>= V1{i} 0) (>= V2{i} 0) (>= V3{i} 0) (>= V4{i} 0) (<= V1{i} 110) (<= V3{i} 110) (<= V2{i} 160) (<= V4{i} 160))"
    return "\n".join([clause.format(i=i) for i in time])

def transitionFromS(i):
    clause = "(and (= L{i} 0) (= L{inext} 1) {costs}) (and (= L{i} 0) (= L{inext} 3) {costs})"
    return clause.format(i=i, inext=i+1, costs=travelCosts(i,15,0))

def transitionFromV1(i):
    toS = "(and (= L{i} 1) (= L{inext} 0) (= (+ (- V1{i} 15) T{i}) (+ V1{inext} T{inext})) (<= V1{inext} 95) {costs15})"
    toV3 = "(and (= L{i} 1) (= L{inext} 3) (= (+ (- V1{i} 11) T{i}) (+ V1{inext} T{inext})) (<= V1{inext} 99) {costs11})"
    toV2 = "(and (= L{i} 1) (= L{inext} 2) (= (+ (- V1{i} 17) T{i}) (+ V1{inext} T{inext})) (<= V1{inext} 93) {costs17})"
    clause = toS + toV3 + toV2
    return clause.format(i=i,inext=i+1, costs15=travelCosts(i,15,1), costs11=travelCosts(i,11,1), costs17=travelCosts(i,17,1))

def transitionFromV2(i):
    toV1 = "(and (= L{i} 2) (= L{inext} 1) (= (+ (- V2{i} 17) T{i}) (+ V2{inext} T{inext})) (<= V2{inext} 143) {costs17})"
    toV3 = "(and (= L{i} 2) (= L{inext} 3) (= (+ (- V2{i} 11) T{i}) (+ V2{inext} T{inext})) (<= V2{inext} 149) {costs11})"
    toV4 = "(and (= L{i} 2) (= L{inext} 4) (= (+ (- V2{i} 20) T{i}) (+ V2{inext} T{inext})) (<= V2{inext} 140) {costs20})"
    clause = toV1 + toV3 + toV4
    return clause.format(i=i,inext=i+1, costs17=travelCosts(i,17,2), costs11=travelCosts(i,11,2), costs20=travelCosts(i,20,2))

def transitionFromV3(i):
    toV1 = "(and (= L{i} 3) (= L{inext} 1) (= (+ (- V3{i} 11) T{i}) (+ V3{inext} T{inext})) (<= V3{inext} 99) {costs11})"
    toV2 = "(and (= L{i} 3) (= L{inext} 2) (= (+ (- V3{i} 11) T{i}) (+ V3{inext} T{inext})) (<= V3{inext} 99) {costs11})"
    toV4 = "(and (= L{i} 3) (= L{inext} 4) (= (+ (- V3{i} 20) T{i}) (+ V3{inext} T{inext})) (<= V3{inext} 90) {costs20})"
    toS = "(and (= L{i} 3) (= L{inext} 0) (= (+ (- V3{i} 15) T{i}) (+ V3{inext} T{inext})) (<= V3{inext} 95) {costs15})"
    clause = toS + toV1 + toV2 + toV4
    return clause.format(i=i,inext=i+1, costs15=travelCosts(i,15,3), costs11=travelCosts(i,11,3), costs20=travelCosts(i,20,3))

def transitionFromV4(i):
    toV2 = "(and (= L{i} 4) (= L{inext} 2) (= (+ (- V4{i} 20) T{i}) (+ V4{inext} T{inext})) (<= V4{inext} 140) {costs20})"
    toV3 = "(and (= L{i} 4) (= L{inext} 3) (= (+ (- V4{i} 20) T{i}) (+ V4{inext} T{inext})) (<= V4{inext} 140) {costs20})"
    clause = toV2 + toV3
    return clause.format(i=i,inext=i+1, costs20=travelCosts(i,20,4))



def singleTransition(i):
    clause = "(or {})"
    return clause.format(" ".join([transitionFromS(i),transitionFromV1(i), transitionFromV2(i), transitionFromV3(i), transitionFromV4(i)]))


def travelCosts(i, costs, frompoint=0):
    clause = "(= V1{inext} (- V1{i}  {costs})) (= V2{inext} (- V2{i}  {costs})) (= V3{inext} (- V3{i}  {costs})) (= V4{inext} (- V4{i}  {costs}))"
    if frompoint == 1:
        clause = "(= V2{inext} (- V2{i}  {costs})) (= V3{inext} (- V3{i}  {costs})) (= V4{inext} (- V4{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 2:
        clause = "(= V1{inext} (- V1{i}  {costs})) (= V3{inext} (- V3{i}  {costs})) (= V4{inext} (- V4{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 3:
        clause = "(= V1{inext} (- V1{i}  {costs})) (= V2{inext} (- V2{i}  {costs})) (= V4{inext} (- V4{i}  {costs})) (>= T{i} T{inext})"
    if frompoint == 4:
        clause = "(= V1{inext} (- V1{i}  {costs})) (= V2{inext} (- V2{i}  {costs})) (= V3{inext} (- V3{i}  {costs})) (>= T{i} T{inext})"
    return clause.format(i=i,inext=i+1, costs=costs)

def allTransitions():
    return " ".join([singleTransition(i) for i in time[:-1]])

def equal(i,j):
    clause = "(and (= V1{i} V1{j}) (= V2{i} V2{j})  (= V3{i} V3{j}) (= V4{i} V4{j})  (= L{i} L{j})  (= T{i} T{j}))"
    return clause.format(i=i,j=j)

def loop():
    clause = "(or {})".format("\n".join([equal(i,j) for i in time for j in time if j < i]))
    return clause

def initialState(): 
    return "(and (= L0 0) (= T0 262) (= V10 50) (= V40 50) (= V20 160) (= V30 110))"


def formula(): 
    return ":formula (and \n{}\n))".format("".join([allCorrect(), initialState(), allTransitions(), loop()]))


print(declareVars())
print(formula())
