import itertools
states = range(7)
letters = ["A","B"]

def declareTransitions():
    clause = "(A{i}{j} Bool)(B{i}{j} Bool)"
    return  " ".join([clause.format(i=i,j=j) for i in states for j in states])


def declareFinalStates(i):
    return "(F{i} Bool)".format(i=i)

def declareVars():
    clause = "(benchmark nfa.smt\n:logic QF_UFLIA\n:extrafuns ({} {})".format(" ".join([declareFinalStates(i) for i in states]), declareTransitions())
    return clause

def wordInLanguage(word):
    clause = "(or "
    paths = [p for p in itertools.product(states,repeat = len(word))]
    for p in paths:
        pathclause = "(and "
        state = 0 
        for i in range(len(word)):
            pathclause += "{l}{state}{i} ".format(l=word[i], state=state,i=p[i])
            state = p[i]
        pathclause += " F{state})".format(state=state)
        clause += pathclause
    clause += ")"
    return clause

def wordNotInLanguage(word):
    clause = "(not {})"
    return clause.format(wordInLanguage(word))

def allWordRequirements():
    allcombinations = []
    for i in range(1,5):
        allcombinations.extend([p for p in itertools.product("AB",repeat = i)])
    requirements = "(and "
    for word in allcombinations:
        if word == ('A', 'A') or word == ('A', 'B', 'A') or word == ('B', 'A', 'A') or word == ('A', 'B','A','B') or word == ('B', 'A','B','B'):
            requirements += wordInLanguage(word)
        else:
            requirements += wordNotInLanguage(word)
    requirements += wordInLanguage("AAABA")
    requirements += wordInLanguage("BAAAA")
    requirements += wordNotInLanguage("ABAAA")

    return requirements

def formula(): 
    return ":formula (and \n{}\n))".format("".join([allWordRequirements()]))

print(declareVars())
print(formula())