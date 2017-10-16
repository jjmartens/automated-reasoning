trucks = range(8)
packages = range(5)
weights = [800, 1100, 1000, 2500, 200]
packageconstraints = [4, 21,8, 10, 20]
print("(benchmark test.smt\n:logic QF_UFLIA\n:extrafuns (")
for t in trucks:
	for p in packages:
		print("(B" + str(t) + str(p) +" Int)")
		
print(")\n:formula (and")
for t in trucks:
	for p in packages:
		print("(>= B" + str(t) + str(p) + " 0)")

for t in trucks:
	weightlimit = "(<= (+"
	for p in packages:
		weightlimit += " (* B" + str(t) + str(p) + " " + str(weights[p])+ ")"
	weightlimit += ") 8000)"	
	print weightlimit

for t in  trucks:
	capacitylimit = "(<= (+"
	for p in packages:
		capacitylimit += " B" + str(t) + str(p)
	capacitylimit += ") 8)"
	print capacitylimit
	
for p in packages:
	packageconstraint = "(= (+"
	for t in  trucks:
		packageconstraint += " B" + str(t) + str(p)
	packageconstraint += ") " + str(packageconstraints[p]) + ")"
	print packageconstraint

coolconstraint = "(= (+"
for t in  trucks:
	if t >= 3:
		coolconstraint += " B" + str(t) + str(2)
coolconstraint += ") 0)"
print coolconstraint

for t in  trucks:
	print("(<= B" + str(t) + str(0) + " 1)")

print "))"