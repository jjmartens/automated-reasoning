trucks = range(8)
packages = range(5)
weights = [800, 1100, 1000, 2500, 200]
packageconstraints = [4, 19,8, 10, 20]
print("(benchmark trucksb.smt\n:logic QF_UFLIA\n:extrafuns (")
for t in trucks:
	for p in packages:
		print("(B" + str(t) + str(p) +" Int)")
		
print(")\n:formula (and")

#You can't carry negative packages
for t in trucks:
	for p in packages:
		print("(>= B" + str(t) + str(p) + " 0)")

#weightlimit
for t in trucks:
	weightlimit = "(<= (+"
	for p in packages:
		weightlimit += " (* B" + str(t) + str(p) + " " + str(weights[p])+ ")"
	weightlimit += ") 8000)"	
	print (weightlimit)

#capacitylimit
for t in  trucks:
	capacitylimit = "(<= (+"
	for p in packages:
		capacitylimit += " B" + str(t) + str(p)
	capacitylimit += ") 8)"
	print (capacitylimit)

#All packages should be delivered	
for p in packages:
	packageconstraint = "(= (+"
	for t in  trucks:
		packageconstraint += " B" + str(t) + str(p)
	packageconstraint += ") " + str(packageconstraints[p]) + ")"
	print (packageconstraint)

#explosions
for t in trucks:
	print("(or (= B{t}1 0) (= B{t}3 0))".format(t=t))
	
#coolcontstraint
coolconstraint = "(= (+"
for t in  trucks:
	if t >= 3:
		coolconstraint += " B" + str(t) + str(2)
coolconstraint += ") 0)"
print (coolconstraint)

#Valuables
for t in  trucks:
	print("(<= B" + str(t) + str(0) + " 1)")

print ("))")
