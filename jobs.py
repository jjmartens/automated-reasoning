jobs = range(1,13)
runningtimes = [ i + 5 for i in jobs]
max = 59
print("(benchmark test.smt\n:logic QF_UFLIA\n:extrafuns (")

for j in jobs:
	print("(J" + str(j) + " Int)")

print (")")

print(":formula (and ")

for j in jobs:
	print("(>= J" + str(j) + " 0)")
	
def afterfinish(j, i):
	return ("(>= J" + str(j) + " (+ J" + str(i) + " " + str(runningtimes[i-1]) + "))")

def notatsametime(j,i):
	return ("(or " + afterfinish(j,i) + " " + afterfinish(i,j) + ")")

print(afterfinish(3,1))
print(afterfinish(3,2))
print(afterfinish(5,3))
print(afterfinish(5,4))
print(afterfinish(7,3))
print(afterfinish(7,4))
print(afterfinish(7,6))

print("(>= J8 J5)")
print(afterfinish(9,5))
print(afterfinish(9,8))
print( afterfinish(11,10))
print( afterfinish(12,9))
print( afterfinish(12,11))

print(notatsametime(5,7))
print(notatsametime(5,10))
print(notatsametime(7,10))

for j in jobs:
	print("(<= (+ J" + str(j) + " " + str(runningtimes[j-1]) + ") " + str(max) +")")


print("))")