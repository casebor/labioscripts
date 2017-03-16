#!/usr/bin/env python
import sys, os, string, math

QCS_PATH = "/home/carlos/Programs/QCS_update/"
PYTHON = "/usr/bin/python"

PALSSE_PATH = QCS_PATH + "palsse_pack/"
helpinfo = ""
helpinfo += "USAGE\n"
helpinfo += "  python getQCS.py -r [real_pdb_file] -m [model_pdb_file] [options]\n"      
helpinfo += "OPTIONS\n"
helpinfo += "  -new\tRequired for new targets; Specify if the [real_pdb_file] has not been processed in the current directory before.\n"
helpinfo += "  -r\tRequired; Input PDB file of real structure [real_pdb_file].\n"
helpinfo += "  -m\tRequired; Input PDB file for predicted model [model_pdb_file].\n"
helpinfo += "  -opt [weight1] [weight2] [weight3] [weight4] [weight5]\tOptional; Specify if other sets of weight (as integer or float number) is prefered.\n"
helpinfo += "  \t\tFrom the left to the right please input the weight of length score, position score, angle score, interaction score, handedness score and contact score score.\n"
helpinfo += "  -h\tOptional; Print a help message, and overwrite all other options.\n"

if os.path.exists(PALSSE_PATH + "palsse/etc/palsse.conf"):
	palsse_confp = os.popen("grep \"secoutdir\" " + PALSSE_PATH + "palsse/etc/palsse.conf")
	palsse_conf_info1 = palsse_confp.readline()
	palsse_conf_info2 = palsse_conf_info1.split("=")
	palsse_conf_info3 = palsse_conf_info2[1].split()
	if palsse_conf_info3[0][-1] == "/":
		PALSSEOUT_DIR = palsse_conf_info3[0]
	else:
		PALSSEOUT_DIR = palsse_conf_info3[0] + "/"
else:
	sys.exit("ERROR! Cannot find the confire file of PALSSE at " + PALSSE_PATH + "palsse/etc/palsse.conf\n") 

mode = ""
realpdb = ""
modelpdb = ""
newtarget = 0
userweights = []

if len(sys.argv) <= 1:
	print helpinfo
else:
	operations = sys.argv[1:]
	if "-h" in operations:
		print helpinfo
		sys.exit(0)
	else:
		if "-new" in operations:
			newtarget = 1
		for count, op in enumerate(operations):
			if op == "-r":
				realpdb = operations[count + 1]
				if not os.path.exists(realpdb):
					sys.exit("Error! Cannot find the PDB file for real structure.\n")
			if op == "-m":
				modelpdb = operations[count + 1]
				if not os.path.exists(modelpdb):
                                        sys.exit("Error! Cannot find the PDB file for predicted model.\n")
			if op == "-opt":
				for i in range(6):
					userweights.append(float(operations[count + 1 + i]))
if not realpdb or not modelpdb:
	sys.exit("Error! Cannot parse your options correctly. Please try again.\n")
realpdb_info = realpdb.split("/")
if realpdb[0] == "/" and len(realpdb_info) >= 2:
        workdir = "/" + string.join(realpdb_info[:-1], "/")
elif realpdb[0] != "/" and len(realpdb_info) >= 2:
        workdir = string.join(realpdb_info[:-1], "/")
else:
	workdir = "."
realpdbfile = realpdb_info[-1]
palssepdb = workdir + "/" + realpdb_info[-1][:4] + ".pdb"
ssdname = PALSSEOUT_DIR + realpdb_info[-1][:4] + ".ssd"
modelpdb_info = modelpdb.split("/")
modelpdbfile = modelpdb_info[-1]

if not newtarget:
	if not os.path.exists(realpdb + "_ca"):
		sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + ".randomscore"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + "_ca.ang"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + "_ca.dis"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + "_ca.int"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + "_ca.len"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")
	if not os.path.exists(realpdb + "_ca.res"):
                sys.exit("ERROR! The information for target pdb is not enough to obmit the target processing step. Please add \"-new\" option to the command line and start the job again!\n")

if newtarget:
	os.system(PYTHON + " " + QCS_PATH + "parsepdb.py " + realpdb)
os.system(PYTHON + " " + QCS_PATH + "parsepdb.py " + modelpdb)
if not os.path.exists(realpdb + "_ca") or not os.path.exists(modelpdb + "_ca"):
	sys.exit()

fp1 = open(realpdb + "_ca", "r")
info1 = fp1.readlines()
fp1.close()
fp2 = open(modelpdb + "_ca", "r")
info2 = fp2.readlines()
fp2.close()

coor1 = []
aatype1 = {}
for line1 in info1:
        word1 = line1[:-1].split("\t")
        aatype1[word1[0]] = word1[1]
        try:
                x = float(word1[2])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + realpdb)
        try:
                y = float(word1[3])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + realpdb)
        try:
                z = float(word1[4])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + realpdb)
        if [x,y,z] in coor1:
                print "Warning! Some CAs share the same coordinates in the Input PDB " + realpdb
        else:
                coor1.append([x,y,z])

coor2 = []
aatype2 = {}
for line2 in info2:
        word2 = line2[:-1].split("\t")
        aatype2[word2[0]] = word2[1]
        try:
                x = float(word2[2])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + modelpdb)
        try:
                y = float(word2[3])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + modelpdb)
        try:
                z = float(word2[4])
        except ValueError:
                sys.exit("Error! Cannot get correct coordinates from your Input PDB " + modelpdb)
        if [x,y,z] in coor2:
                print "Warning! Some CA share the same coordinates in the Input PDB " + modelpdb
        else:
                coor2.append([x,y,z])

for aa in aatype1.keys():
	if aatype2.has_key(aa):
	        if aatype1[aa] == aatype2[aa]:
        	        pass
        	else:
                	sys.exit("Error! The residues type at position " + aa + " do not match between the target and the model!")

rp1 = open(modelpdb + "_ca_modified", "w")
real_residue = []
real_coordinate = []
for count1, line1 in enumerate(info1):
	word1 = line1.split()
	real_residue.append([word1[0], word1[1], "no"])
	real_coordinate.append([float(word1[2]), float(word1[3]), float(word1[4])])
	if count1 >= 1:
		ca_dist=(real_coordinate[count1][0]-real_coordinate[count1-1][0])*(real_coordinate[count1][0]-real_coordinate[count1-1][0])
                ca_dist+=(real_coordinate[count1][1]-real_coordinate[count1-1][1])*(real_coordinate[count1][1]-real_coordinate[count1-1][1])
                ca_dist+=(real_coordinate[count1][2]-real_coordinate[count1-1][2])*(real_coordinate[count1][2]-real_coordinate[count1-1][2])
		ca_dist = math.sqrt(ca_dist)
		if ca_dist > 5.0:
			message = "It looks that the chain is broken in the real structure between residue " + real_residue[count1-1][0] + " and " + real_residue[count1][0]
			print message

model_residue = []
for line2 in info2:
        word2 = line2.split()
        newresi = [word2[0], word2[1], "no"]
	model_residue.append(newresi)

count_match = 0
count_exact = 0
percent_match = 0.0
percent_exact = 0.0
towrite = []
for rresi in real_residue:
	for countm, mresi in enumerate(model_residue):
		if rresi[0] == mresi[0]:
			towrite.append(info2[countm])
			mresi[2] = "yes"
			count_match = count_match + 1
			if rresi[1] == mresi[1]:
				count_exact = count_exact + 1
			else:
				print ("The identity of residue does not match at position " + rresi[0])
			break
	else:
		towrite.append(rresi[0] + "\t" + rresi[1] + "\tmissing\n")

		print ("Residue at position " + rresi[0] + " is missing in the model")

for resi in model_residue:
	if resi[2] == "no":
		print ("Residue at position " + resi[0] + " in model is missing in real structure, so it is obmitted")
		
percent_match = float(count_match)/len(real_residue)
percent_exact = float(count_exact)/len(real_residue)
print (str(percent_match*100) + "% of the residues in the real structure is covered in the model")
print (str(percent_exact*100) + "% of the residues in the real structure is matched exactly by the residues in the model")

ex_buffer = []
po_buffer = []
last = []
newlines = []
missing_buffer = []
for count, line in enumerate(towrite):
	word = line.split()
	if not newlines: 
		if word[2] == "missing":
			last = word
		else:
			rp1.write(line)
			newlines.append(line)
			last = word
			ex_buffer = word
	else:
		if word[2] == "missing" and last[2] != "missing":
			last = word
			missing_buffer = [word]
			count_miss = 1
		elif word[2] == "missing" and last[2] == "missing":
			last = word
			missing_buffer.append(word)
			count_miss = count_miss + 1
                elif word[2] != "missing" and last[2] != "missing":
			last = word
                        ex_buffer = word
			rp1.write(line)
			newlines.append(line)	
                elif word[2] != "missing" and last[2] == "missing":
			last = word
			po_buffer = word
			exx = float(ex_buffer[2])
                        exy = float(ex_buffer[3])
                        exz = float(ex_buffer[4])
                        pox = float(po_buffer[2])
                        poy = float(po_buffer[3])
                        poz = float(po_buffer[4])
			for countin in range(1, count_miss + 1):
				x = exx + (pox - exx)*countin/(count_miss+1)
                        	y = exy + (poy - exy)*countin/(count_miss+1)
                        	z = exz + (poz - exz)*countin/(count_miss+1)
				newline = missing_buffer[countin-1][0]+"\t"+missing_buffer[countin-1][1]+"\t"+str(x)+"\t"+str(y) + "\t" + str(z) + "\n"
				rp1.write(newline)
				newlines.append(line)
			rp1.write(line)
			newlines.append(line)
			ex_buffer = word			
rp1.close()
resultp = open(workdir + "/" + realpdbfile + "_vs_" + modelpdbfile, "w")

if newtarget:
	if realpdb != palssepdb:
		os.system("cp " + realpdb + " " + palssepdb)
	os.system(PYTHON + " " + QCS_PATH + "check_palsse_input.py " + palssepdb)
	os.system(PALSSE_PATH + "local/bin/python " + PALSSE_PATH + "palsse/src/PALSSE.py " + palssepdb)
referp = open(realpdb + "_ca", "r")
modelp = open(modelpdb + "_ca", "r")

refinfo = referp.readlines()
referp.close()
refpoints = []
for refline in refinfo:
	refword = refline.split()
	refpoints.append([refword[0], float(refword[2]), float(refword[3]), float(refword[4])])

dismtx = []
for count1, point1 in enumerate(refpoints):
	for count2, point2 in enumerate(refpoints):
		if count2 > count1 + 1:
			dist = math.sqrt((point1[1]-point2[1])*(point1[1]-point2[1])+(point1[2]-point2[2])*(point1[2]-point2[2])+(point1[3]-point2[3])*(point1[3]-point2[3]))
			if dist <= 8.44:
				dismtx.append([point1[0], point2[0], dist])
 		elif count2 > count1 and int(point2[0]) > int(point1[0]) + 1:
                        dist = math.sqrt((point1[1]-point2[1])*(point1[1]-point2[1])+(point1[2]-point2[2])*(point1[2]-point2[2])+(point1[3]-point2[3])*(point1[3]-point2[3]))
                        if dist <= 8.44:
                                dismtx.append([point1[0], point2[0], dist])
mdinfo = modelp.readlines()
modelp.close()
mdpoints = []
for mdline in mdinfo:
	mdword = mdline.split()
	mdpoints.append([mdword[0], float(mdword[2]), float(mdword[3]), float(mdword[4])])

totalscore = 0.0
totalcount = 0
for pair in dismtx:
	totalcount = totalcount + 1
	resi1 = pair[0]
	resi2 = pair[1]
	rdist = pair[2]
	point1 = []
	point2 = []
	for point in mdpoints:
		if point[0] == resi1:
			point1 = point
		if point[0] == resi2:
			point2 = point
	if point1 and point2:
		mdist = math.sqrt((point1[1]-point2[1])*(point1[1]-point2[1])+(point1[2]-point2[2])*(point1[2]-point2[2])+(point1[3]-point2[3])*(point1[3]-point2[3]))
		diff = (mdist-rdist)/rdist
		if diff <= 1:
			score = math.exp(-(diff*diff)/(0.2*0.2)*math.log(2))
		else:
			score = 0
	else:
		score = 0	
	totalscore = totalscore + score
finalscore = totalscore/totalcount	
resultp.write("contact_score:\n")
resultp.write(str(finalscore)+"\n")
if newtarget:		
	os.system(PYTHON + " " + QCS_PATH + "target_analysis.py " + ssdname + " " + realpdb + "_ca")
	os.system(PYTHON + " " + QCS_PATH + "generate_random.py " + realpdb + "_ca")
	os.system("ls -1 " + realpdb + "_ca_*_random > " + realpdb + "_ca_randomlist")
	randomp = open(realpdb + "_ca_randomlist", "r")
	randomlist = randomp.readlines()
	randomp.close()
	randomtotal = 0
	randomcount = 0
	for line in randomlist:
		randomcount += 1
		randomname = line[:-1]
		if userweights:
			os.system(PYTHON + " " + QCS_PATH + "getQCS_random.py -r " + realpdb + "_ca -m " + randomname + " -opt " + str(userweights[0]) + " " + str(userweights[1]) + " " + str(userweights[2]) + " " + str(userweights[3]) + " " + str(userweights[4]) + " " + str(userweights[5]))
		else:
			os.system(PYTHON + " " + QCS_PATH + "getQCS_random.py -r " + realpdb + "_ca -m " + randomname)
		rscorep = open(randomname + ".score", "r")
		rscore_info = rscorep.readlines()
		rscore_final = rscore_info[2].split()
		rscore = float(rscore_final[-1])
		randomtotal += rscore
	randomave = randomtotal/randomcount
	randomfinalp = open(realpdb + ".randomscore", "w")
	randomfinalp.write(str(randomave))
	randomfinalp.close()

randomfinalp = open(realpdb + ".randomscore", "r")
randomfinal = randomfinalp.readlines()
randomscore = float(randomfinal[0][:-1])
os.system(PYTHON + " " + QCS_PATH + "model_analysis.py " + modelpdb + "_ca" + " " + realpdb + "_ca.res")
lp = open(realpdb + "_ca.len", "r")
len_info = lp.readlines()
lp.close()
ap = open(realpdb + "_ca.ang", "r")
ang_info = ap.readlines()
ap.close()
ip = open(realpdb + "_ca.int", "r")	
int_info = ip.readlines()
ip.close()
resp = open(realpdb + "_ca.res", "r")
res_info = resp.readlines()
resp.close()
mip = open(modelpdb + "_ca.int", "r")
mint_info = mip.readlines()
mip.close()
disp = open(realpdb + "_ca.dis", "r")
dis_info = disp.readlines()
disp.close()
mdisp = open(modelpdb + "_ca.dis", "r")   
mdis_info = mdisp.readlines()
mdisp.close()


len_ends = []
weight1 = []
for count, line in enumerate(len_info):
	words = line.split()
	if count%3 == 2:
		weight1.append(int(words[0]))
	else:
		if words:
			residues = []
			for word in words:
				residues.append(word)
			len_ends.append(residues)

ang_ends = []
weight2raw = []
ang_centers = []
for count, line in enumerate(ang_info):
        words = line.split()
	if count%4 == 3:
                weight2raw.append(int(words[0]))
        elif count%4 == 2:
	        if words:
                	residues = []
                	for word in words:
	                       	residues.append(word)
               		ang_centers.append(residues)
	else:
                if words:
                        residues = []
                        for word in words:
                                residues.append(word)
                        ang_ends.append(residues)


int_ends = []
weight3 = []
for c1, line in enumerate(int_info):
	dis = []
       	words = line.split()
	if words:
		for c2, word in enumerate(words):
			char = word.split(",")
			dis.append(float(char[0]))
			if float(char[0]) < 8.5 and c2 > c1:
       		       		int_ends.append([char[1]])
				int_ends.append([char[2]])
				weight3.append(int(char[3])*int(char[4]))
for c1, line in enumerate(mint_info):
        words = line.split()
        if words:
                for c2, word in enumerate(words):
                        char = word.split(",")
                        if float(char[0]) < 8.5 and c2 > c1:
                                int_ends.append([char[1]])
                                int_ends.append([char[2]])
                                weight3.append(-int(char[3])*int(char[4]))

real_distances = []
model_distances = []
distances = []  
weight6 = []
ruleout = []
for c1, line in enumerate(dis_info):
        dis = []
        words = line.split()
        if words:
                for c2, word in enumerate(words):
                        char = word.split(",")
			if c1 != c2:
				if float(char[0]) != 0:
                        		dis.append(float(char[0]))
					real_distances.append(float(char[0]))
					weight6.append(int(char[3])*int(char[4]))
				else:
					dis.append(4.5)
					ruleout.append([c1,c2])
			else:
				dis.append(0)
		distances.append(dis)
for c1, line in enumerate(mdis_info):
	words = line.split()
        if words:
                for c2, word in enumerate(words):
                        char = word.split(",")
			if c1 != c2:
				if [c1,c2] in ruleout:
					pass
				else:
		        		model_distances.append(float(char[0]))


sse_res = []
all_sse_res = []
all_res_weight = []
weight4raw = []
for count, line in enumerate(res_info):
	words = line.split()
	if count%2 == 0:
		one_sse = []
		for word in words:
			one_sse.append(word)
			all_sse_res.append(word)
		sse_res.append(one_sse)
	else:
		weight4raw.append(int(words[0]))
		if words[1] == "H":
			for i in range(len(one_sse)):
				all_res_weight.append(1)
		elif words[1] == "E":
			for i in range(len(one_sse)):
				all_res_weight.append(2)
			
missing_penalty = 1
total_resi = sum(all_res_weight)
missing_resi = 0
for line in towrite:
	word = line[:-1].split("\t")
	if word[0] in all_sse_res:
		res_index = all_sse_res.index(word[0])
		if word[2] == "missing":
			missing_resi += all_res_weight[res_index]
missing_penalty = 1 - float(missing_resi)/total_resi
todolist = [realpdb, modelpdb]
weight2 = []
weight4 = []
weight5 = []
all_ca = 0
count_ca = 0
for pdb in todolist:
	a = []
	for i in range(len(len_ends)):
		b = []
		a.append(b)
	c = []
	for i in range(len(ang_ends)):
		d = []
		c.append(d)
	e = []
	for i in range(len(int_ends)):
		f = []
		e.append(f)
	p = []
	for i in range(len(ang_centers)):
		q = []
		p.append(q)
	k = []
	for i in range(len(sse_res)):
		l = []
		k.append(l)
	
	if pdb == realpdb:
		pdbp = open(realpdb + "_ca", "r")
		pdbinfo = pdbp.readlines()
		pdbp.close()
	elif pdb == modelpdb:
		pdbp = open(modelpdb + "_ca_modified", "r")
		pdbinfo = pdbp.readlines()
		pdbp.close()
	for line1 in pdbinfo:
		all_ca += 1
		word = line1.split()
		for count, end in enumerate(len_ends):
			if word[0] in end:
				a[count].append([float(word[2]), float(word[3]), float(word[4])])
		for count, end in enumerate(ang_ends):
			if word[0] in end:
                	        c[count].append([float(word[2]), float(word[3]), float(word[4])])
        	for count, end in enumerate(int_ends):
               		if word[0] in end:
                       		e[count].append([float(word[2]), float(word[3]), float(word[4])])
		for count, res in enumerate(sse_res):
			if word[0] in res:
				count_ca += 1
				k[count].append([float(word[2]), float(word[3]), float(word[4])])
                for count, end in enumerate(ang_centers):
                        if word[0] in end:
                                p[count].append([float(word[2]), float(word[3]), float(word[4])])

 

	ax = []
	ay = []
	az = []
	length = []
	for i in range(len(a)):
		ax.append(0)
		ay.append(0)
		az.append(0)
		if i%2 == 0:
			length.append(0) 	
	
	for j in range(len(length)):
		m = 2 * j
		n = 2 * j + 1
		if a[m] and a[n]:
			for i in range(len(a[m])):
				ax[m] = ax[m] + a[m][i][0]
	                      	ay[m] = ay[m] + a[m][i][1]
        	               	az[m] = az[m] + a[m][i][2]
			ax[m] = ax[m]/(len(a[m]))
	       	        ay[m] = ay[m]/(len(a[m]))
        	      	az[m] = az[m]/(len(a[m]))

	        	for i in range(len(a[n])):
                       		ax[n] = ax[n] + a[n][i][0]
                		ay[n] = ay[n] + a[n][i][1]
	               		az[n] = az[n] + a[n][i][2]
	                ax[n] = ax[n]/(len(a[n]))
        	   	ay[n] = ay[n]/(len(a[n]))
               		az[n] = az[n]/(len(a[n])) 
                        length[j] = math.sqrt(math.pow((ax[m]-ax[n]),2) + math.pow((ay[m]-ay[n]),2) + math.pow((az[m]-az[n]),2))
                elif a[m] and not a[n]:
			if len(a[m]) <= 1:
				length[j] = -1
			else:
                        	for i in range(len(a[m])/2):
                                	ax[m] = ax[m] + a[m][i][0]
                                	ay[m] = ay[m] + a[m][i][1]
                                	az[m] = az[m] + a[m][i][2]
                        	ax[m] = ax[m]/(len(a[m])/2)
                        	ay[m] = ay[m]/(len(a[m])/2)
                        	az[m] = az[m]/(len(a[m])/2) 
	                        for i in range(len(a[m])/2, len(a[m])):
                                	ax[n] = ax[n] + a[m][i][0]
                                	ay[n] = ay[n] + a[m][i][1]
                                	az[n] = az[n] + a[m][i][2]
                        	ax[n] = ax[n]/(len(a[m]) - len(a[m])/2)
                        	ay[n] = ay[n]/(len(a[m]) - len(a[m])/2)
                        	az[n] = az[n]/(len(a[m]) - len(a[m])/2) 
                        	length[j] = math.sqrt(math.pow((ax[m]-ax[n]),2) + math.pow((ay[m]-ay[n]),2) + math.pow((az[m]-az[n]),2))
                elif not a[m] and a[n]:
                        if len(a[n]) <= 1:
                                length[j] = -1
                        else:
                                for i in range(len(a[n])/2):
                                        ax[m] = ax[m] + a[n][i][0]
                                        ay[m] = ay[m] + a[n][i][1]
                                        az[m] = az[m] + a[n][i][2]
                                ax[m] = ax[m]/(len(a[n])/2)
                                ay[m] = ay[m]/(len(a[n])/2)
                                az[m] = az[m]/(len(a[n])/2)
                                for i in range(len(a[n])/2, len(a[n])):
                                        ax[n] = ax[n] + a[n][i][0]
                                        ay[n] = ay[n] + a[n][i][1]
                                        az[n] = az[n] + a[n][i][2]
                                ax[n] = ax[n]/(len(a[n]) - len(a[n])/2)
                                ay[n] = ay[n]/(len(a[n]) - len(a[n])/2)
                                az[n] = az[n]/(len(a[n]) - len(a[n])/2)
                                length[j] = math.sqrt(math.pow((ax[m]-ax[n]),2) + math.pow((ay[m]-ay[n]),2) + math.pow((az[m]-az[n]),2))


		else:
			length[j] = -1

	ex = []
	ey = []
	ez = []
	inter = []
	for i in range(len(e)):
		ex.append(0)
		ey.append(0)	
		ez.append(0)
		if i%2 == 0:
			inter.append(-1) 
	for j in range(len(inter)):
        	m = 2 * j
        	n = 2 * j + 1
        	if e[m] and e[n]:   
                	for i in range(len(e[m])):
                        	ex[m] = ex[m] + e[m][i][0]
                        	ey[m] = ey[m] + e[m][i][1]
                        	ez[m] = ez[m] + e[m][i][2]
	                ex[m] = ex[m]/(len(e[m]))
        	        ey[m] = ey[m]/(len(e[m]))
                	ez[m] = ez[m]/(len(e[m]))
                
	                for i in range(len(e[n])):
        	                ex[n] = ex[n] + e[n][i][0]
                	        ey[n] = ey[n] + e[n][i][1]
                        	ez[n] = ez[n] + e[n][i][2]
	                ex[n] = ex[n]/(len(e[n]))
        	        ey[n] = ey[n]/(len(e[n]))
                	ez[n] = ez[n]/(len(e[n]))
	                inter[j] = math.sqrt(math.pow((ex[m]-ex[n]),2) + math.pow((ey[m]-ey[n]),2) + math.pow((ez[m]-ez[n]),2))
		else:
			inter[j] = -1

        cx = []
        cy = []
        cz = []
	px = []
	py = []
	pz = []
        dist = []
        for i in range(len(c)):
                cx.append(0)
                cy.append(0)
                cz.append(0)
	for i in range(len(p)):
		px.append(0)
		py.append(0)
		pz.append(0)
                dist.append(0)
        vector = []
	middle = []
	heads = []
	tails = []
        for j in range(len(dist)):
                newvec = [0,0,0]
		newmid = [0,0,0]
		dist[j] = -1
                m = 2 * j
                n = 2 * j + 1
                if c[m] and c[n] and p[j]:
                        for i in range(len(c[m])):
                                cx[m] = cx[m] + c[m][i][0]
                                cy[m] = cy[m] + c[m][i][1]
                                cz[m] = cz[m] + c[m][i][2]
                        cx[m] = cx[m]/(len(c[m])) 
                        cy[m] = cy[m]/(len(c[m]))
                        cz[m] = cz[m]/(len(c[m]))
                        for i in range(len(c[n])):
                                cx[n] = cx[n] + c[n][i][0]
                                cy[n] = cy[n] + c[n][i][1]
                                cz[n] = cz[n] + c[n][i][2]
                        cx[n] = cx[n]/(len(c[n]))
                        cy[n] = cy[n]/(len(c[n]))
                        cz[n] = cz[n]/(len(c[n]))
                        for i in range(len(p[j])):
                                px[j] = px[j] + p[j][i][0]
                                py[j] = py[j] + p[j][i][1]
                                pz[j] = pz[j] + p[j][i][2]
                        px[j] = px[j]/(len(p[j]))
                        py[j] = py[j]/(len(p[j]))
                        pz[j] = pz[j]/(len(p[j]))
                        newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                        newmid = [px[j], py[j], pz[j]]
			head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
			tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
			dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))
                elif c[m] and not c[n] and not p[j]:
                        if len(c[m]) > 1:
                                for i in range(len(c[m])/2):
                                        cx[m] = cx[m] + c[m][i][0]
                                        cy[m] = cy[m] + c[m][i][1]
                                        cz[m] = cz[m] + c[m][i][2]
                                cx[m] = cx[m]/(len(c[m])/2)
                                cy[m] = cy[m]/(len(c[m])/2)
                                cz[m] = cz[m]/(len(c[m])/2)
                                for i in range(len(c[m])/2, len(c[m])):
                                        cx[n] = cx[n] + c[m][i][0]
                                        cy[n] = cy[n] + c[m][i][1]
                                        cz[n] = cz[n] + c[m][i][2]
                                cx[n] = cx[n]/(len(c[m]) - len(c[m])/2)
                                cy[n] = cy[n]/(len(c[m]) - len(c[m])/2)
                                cz[n] = cz[n]/(len(c[m]) - len(c[m])/2)
				for i in range(len(c[m])/4, len(c[m]) - len(c[m])/4):
                                        px[j] = px[j] + c[m][i][0]
                                        py[j] = py[j] + c[m][i][1]
                                        pz[j] = pz[j] + c[m][i][2]
                                px[j] = px[j]/(len(c[m]) - len(c[m])/4 - len(c[m])/4) 
                                py[j] = py[j]/(len(c[m]) - len(c[m])/4 - len(c[m])/4)
                                pz[j] = pz[j]/(len(c[m]) - len(c[m])/4 - len(c[m])/4)
			        newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                        	newmid = [px[j], py[j], pz[j]]
	                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
        	                tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                        	dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))
                elif not c[m] and c[n] and not p[j]:
                        if len(c[n]) > 1:
                                for i in range(len(c[n])/2):
                                        cx[m] = cx[m] + c[n][i][0]
                                        cy[m] = cy[m] + c[n][i][1]
                                        cz[m] = cz[m] + c[n][i][2]
                                cx[m] = cx[m]/(len(c[n])/2)
                                cy[m] = cy[m]/(len(c[n])/2)
                                cz[m] = cz[m]/(len(c[n])/2)
                                for i in range(len(c[n])/2, len(c[n])):
                                        cx[n] = cx[n] + c[n][i][0]
                                        cy[n] = cy[n] + c[n][i][1]
                                        cz[n] = cz[n] + c[n][i][2]
                                cx[n] = cx[n]/(len(c[n]) - len(c[n])/2)
                                cy[n] = cy[n]/(len(c[n]) - len(c[n])/2)
                                cz[n] = cz[n]/(len(c[n]) - len(c[n])/2)
                                for i in range(len(c[n])/4, len(c[n]) - len(c[n])/4):
                                        px[j] = px[j] + c[n][i][0]   
                                        py[j] = py[j] + c[n][i][1]
                                        pz[j] = pz[j] + c[n][i][2]
                                px[j] = px[j]/(len(c[n]) - len(c[n])/4 - len(c[n])/4)
                                py[j] = py[j]/(len(c[n]) - len(c[n])/4 - len(c[n])/4)
                                pz[j] = pz[j]/(len(c[n]) - len(c[n])/4 - len(c[n])/4)
                                newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                                newmid = [px[j], py[j], pz[j]]
	                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
        	                tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                                dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))

                elif not c[m] and not c[n] and p[j]:
                        if len(p[j]) > 1:
                                for i in range(len(p[j])/2):
                                        cx[m] = cx[m] + p[j][i][0]
                                        cy[m] = cy[m] + p[j][i][1]
                                        cz[m] = cz[m] + p[j][i][2]
                                cx[m] = cx[m]/(len(p[j])/2)
                                cy[m] = cy[m]/(len(p[j])/2)
                                cz[m] = cz[m]/(len(p[j])/2)
                                for i in range(len(p[j])/2, len(p[j])):
                                        cx[n] = cx[n] + p[j][i][0]
                                        cy[n] = cy[n] + p[j][i][1]
                                        cz[n] = cz[n] + p[j][i][2]
                                cx[n] = cx[n]/(len(p[j]) - len(p[j])/2)
                                cy[n] = cy[n]/(len(p[j]) - len(p[j])/2)
                                cz[n] = cz[n]/(len(p[j]) - len(p[j])/2)
                                for i in range(len(p[j])/4, len(p[j]) - len(p[j])/4):
                                        px[j] = px[j] + p[j][i][0]   
                                        py[j] = py[j] + p[j][i][1]
                                        pz[j] = pz[j] + p[j][i][2]
                                px[j] = px[j]/(len(p[j]) - len(p[j])/4 - len(p[j])/4)
                                py[j] = py[j]/(len(p[j]) - len(p[j])/4 - len(p[j])/4)
                                pz[j] = pz[j]/(len(p[j]) - len(p[j])/4 - len(p[j])/4)
                                newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                                newmid = [px[j], py[j], pz[j]]
	                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
        	                tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                                dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))

                elif c[m] and c[n] and not p[j]:
                        for i in range(len(c[m])):
                                cx[m] = cx[m] + c[m][i][0]
                                cy[m] = cy[m] + c[m][i][1]
                                cz[m] = cz[m] + c[m][i][2]
                        cx[m] = cx[m]/len(c[m])
                        cy[m] = cy[m]/len(c[m])
                        cz[m] = cz[m]/len(c[m])
                        for i in range(len(c[n])):
                                cx[n] = cx[n] + c[n][i][0]
                                cy[n] = cy[n] + c[n][i][1]
                                cz[n] = cz[n] + c[n][i][2]
                        cx[n] = cx[n]/len(c[n])
                        cy[n] = cy[n]/len(c[n])
                        cz[n] = cz[n]/len(c[n])
                        for i in range(len(c[m])/2, len(c[m])):
                                px[j] = px[j] + c[m][i][0]
                                py[j] = py[j] + c[m][i][1]
                                pz[j] = pz[j] + c[m][i][2]
			for i in range(len(c[n])/2 + 1):
                                px[j] = px[j] + c[n][i][0]
                                py[j] = py[j] + c[n][i][1]
                                pz[j] = pz[j] + c[n][i][2]
                        px[j] = px[j]/(len(c[n])/2 + 1 + len(c[m]) - len(c[m])/2)
                        py[j] = py[j]/(len(c[n])/2 + 1 + len(c[m]) - len(c[m])/2)
                        pz[j] = pz[j]/(len(c[n])/2 + 1 + len(c[m]) - len(c[m])/2)
                        newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                        newmid = [px[j], py[j], pz[j]]
                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
                        tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                        dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))

                elif c[m] and not c[n] and p[j]:
                        for i in range(len(c[m])):
                                cx[m] = cx[m] + c[m][i][0]
                                cy[m] = cy[m] + c[m][i][1]
                                cz[m] = cz[m] + c[m][i][2]
                        cx[m] = cx[m]/len(c[m])
                        cy[m] = cy[m]/len(c[m])
                        cz[m] = cz[m]/len(c[m])
                        for i in range(len(p[j])):
                                cx[n] = cx[n] + p[j][i][0]
                                cy[n] = cy[n] + p[j][i][1]
                                cz[n] = cz[n] + p[j][i][2]
                        cx[n] = cx[n]/len(p[j])
                        cy[n] = cy[n]/len(p[j])
                        cz[n] = cz[n]/len(p[j])
                        for i in range(len(c[m])/2, len(c[m])):
                                px[j] = px[j] + c[m][i][0]
                                py[j] = py[j] + c[m][i][1]
                                pz[j] = pz[j] + c[m][i][2]
                        for i in range(len(p[j])/2 + 1):
                                px[j] = px[j] + p[j][i][0]
                                py[j] = py[j] + p[j][i][1]
                                pz[j] = pz[j] + p[j][i][2]
                        px[j] = px[j]/(len(p[j])/2 + 1 + len(c[m]) - len(c[m])/2)
                        py[j] = py[j]/(len(p[j])/2 + 1 + len(c[m]) - len(c[m])/2)
                        pz[j] = pz[j]/(len(p[j])/2 + 1 + len(c[m]) - len(c[m])/2)
                        newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                        newmid = [px[j], py[j], pz[j]]
                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
                        tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                        dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))

                elif not c[m] and c[n] and p[j]:
                        for i in range(len(p[j])):
                                cx[m] = cx[m] + p[j][i][0]
                                cy[m] = cy[m] + p[j][i][1]
                                cz[m] = cz[m] + p[j][i][2]
                        cx[m] = cx[m]/len(p[j])
                        cy[m] = cy[m]/len(p[j])
                        cz[m] = cz[m]/len(p[j])
                        for i in range(len(c[n])):
                                cx[n] = cx[n] + c[n][i][0]
                                cy[n] = cy[n] + c[n][i][1]
                                cz[n] = cz[n] + c[n][i][2]
                        cx[n] = cx[n]/len(c[n])
                        cy[n] = cy[n]/len(c[n])
                        cz[n] = cz[n]/len(c[n])
                        for i in range(len(p[j])/2, len(p[j])):
                                px[j] = px[j] + p[j][i][0]
                                py[j] = py[j] + p[j][i][1]
                                pz[j] = pz[j] + p[j][i][2]
                        for i in range(len(c[n])/2 + 1):
                                px[j] = px[j] + c[n][i][0]
                                py[j] = py[j] + c[n][i][1]
                                pz[j] = pz[j] + c[n][i][2]
                        px[j] = px[j]/(len(c[n])/2 + 1 + len(p[j]) - len(p[j])/2)
                        py[j] = py[j]/(len(c[n])/2 + 1 + len(p[j]) - len(p[j])/2)
                        pz[j] = pz[j]/(len(c[n])/2 + 1 + len(p[j]) - len(p[j])/2)
                        newvec = [(cx[n]-cx[m]),(cy[n]-cy[m]), (cz[n]-cz[m])]
                        newmid = [px[j], py[j], pz[j]]
                        head = [cx[m]-px[j],cy[m]-py[j],cz[m]-pz[j]]
                        tail = [cx[n]-px[j],cy[n]-py[j],cz[n]-pz[j]]
                        dist[j] = math.sqrt(math.pow((cx[m]-cx[n]),2) + math.pow((cy[m]-cy[n]),2) + math.pow((cz[m]-cz[n]),2))
                vector.append(newvec)
		middle.append(newmid)
		heads.append(head)
		tails.append(tail)

        ang = []
        for c1, v1 in enumerate(vector):
                for c2, v2 in enumerate(vector):
                        if c1 < c2:
                                if dist[c1] > 0 and dist[c2] > 0:
                                        p1 = middle[c1]
					p2 = [middle[c1][0]+v1[0]/dist[c1], middle[c1][1]+v1[1]/dist[c1], middle[c1][2]+v1[2]/dist[c1]]
					p3 = middle[c2]  
                                        p4 = [middle[c2][0]+v2[0]/dist[c2], middle[c2][1]+v2[1]/dist[c2], middle[c2][2]+v2[2]/dist[c2]]
					v13 = [p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]]
					v12 = [p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
                                        v14 = [p4[0]-p1[0],p4[1]-p1[1],p4[2]-p1[2]]
					c1213 = [v12[1]*v13[2]-v12[2]*v13[1],v12[2]*v13[0]-v12[0]*v13[2],v12[0]*v13[1]-v12[1]*v13[0]]
					lc1213 = math.sqrt(math.pow(c1213[0],2)+math.pow(c1213[1],2)+math.pow(c1213[2],2))
					d1213 = v12[0]*v13[0] + v12[1]*v13[1] + v12[2]*v13[2]
                                        c1214 = [v12[1]*v14[2]-v12[2]*v14[1],v12[2]*v14[0]-v12[0]*v14[2],v12[0]*v14[1]-v12[1]*v14[0]]
                                        lc1214 = math.sqrt(math.pow(c1214[0],2)+math.pow(c1214[1],2)+math.pow(c1214[2],2))
                                        d1214 = v12[0]*v14[0] + v12[1]*v14[1] + v12[2]*v14[2]
					c1213_1214 = [c1213[1]*c1214[2]-c1213[2]*c1214[1],c1213[2]*c1214[0]-c1213[0]*c1214[2],c1213[0]*c1214[1]-c1213[1]*c1214[0]]
					lc1213_1214 = math.sqrt(math.pow(c1213_1214[0],2)+math.pow(c1213_1214[1],2)+math.pow(c1213_1214[2],2))
					d1213_1214 = c1213[0]*c1214[0] + c1213[1]*c1214[1] + c1213[2]*c1214[2]
					cross_check = c1213_1214[0]*v12[0]+c1213_1214[1]*v12[1]+c1213_1214[2]*v12[2]
					newp3 = [lc1213,0,d1213]

					if cross_check > 0:
						newp4 = [lc1214*d1213_1214/(lc1213*lc1214),lc1214*lc1213_1214/(lc1213*lc1214),d1214]
					else:
						newp4 = [lc1214*d1213_1214/(lc1213*lc1214),-lc1214*lc1213_1214/(lc1213*lc1214),d1214]
					newv34 = [newp4[0]-newp3[0],newp4[1]-newp3[1],newp4[2]-newp3[2]]
					lnewv34 = math.sqrt(math.pow(newv34[0],2)+math.pow(newv34[1],2)+math.pow(newv34[2],2)) 
                                        ang.append([newv34[0]/lnewv34,newv34[1]/lnewv34,newv34[2]/lnewv34]) 
                                else:
                                        ang.append("N/A")
                                if pdb == realpdb:
                                        w = float(weight2raw[c1]*weight2raw[c2])
                                        weight2.append(w/distances[c1][c2])
	hand = []
        for c1, v1 in enumerate(vector):
                for c2, v2 in enumerate(vector):
			for c3, v3 in enumerate(vector):
                        	if c1 != c2 and c1 != c3 and c2 != c3:
                                	if dist[c1] > 0 and dist[c2] > 0 and dist[c3] > 0:
						if v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] > 0:
							vn = [v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]]
						else:
							vn = [v1[0]-v2[0],v1[1]-v2[1],v1[2]-v2[2]]
						lvn = math.sqrt(math.pow(vn[0],2)+math.pow(vn[1],2)+math.pow(vn[2],2))
						uvn = [vn[0]/lvn, vn[1]/lvn, vn[2]/lvn]
	                                        p1 = middle[c1]
						d1a = uvn[0]*heads[c1][0]*1.8 + uvn[1]*heads[c1][1]*1.8 + uvn[2]*heads[c1][2]*1.8
						d1b = uvn[0]*tails[c1][0]*1.8 + uvn[1]*tails[c1][1]*1.8 + uvn[2]*tails[c1][2]*1.8
        	                                p2 = [middle[c1][0]+vn[0]/lvn, middle[c1][1]+vn[1]/lvn, middle[c1][2]+vn[2]/lvn]
                                        	p3 = middle[c2]
                                                d3c = uvn[0]*heads[c2][0]*1.8 + uvn[1]*heads[c2][1]*1.8 + uvn[2]*heads[c2][2]*1.8
                                                d3d = uvn[0]*tails[c2][0]*1.8 + uvn[1]*tails[c2][1]*1.8 + uvn[2]*tails[c2][2]*1.8
                                        	p4 = middle[c3]
                                        	v13 = [p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]]
                                        	v12 = [p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
                                        	v14 = [p4[0]-p1[0],p4[1]-p1[1],p4[2]-p1[2]]
						lv13 = math.sqrt(math.pow(v13[0],2)+math.pow(v13[1],2)+math.pow(v13[2],2))
						lv13n = (v13[0]*vn[0] + v13[1]*vn[1] + v13[2]*vn[2])/lvn
						if math.fabs(lv13) <= math.fabs(lv13n) + 0.00001:
							hand.append("N/A")
						else:
							lv13p = math.sqrt(math.pow(lv13,2) - math.pow(lv13n,2))
	                                        	c1213 = [v12[1]*v13[2]-v12[2]*v13[1],v12[2]*v13[0]-v12[0]*v13[2],v12[0]*v13[1]-v12[1]*v13[0]]
        	                                	lc1213 = math.sqrt(math.pow(c1213[0],2)+math.pow(c1213[1],2)+math.pow(c1213[2],2))
                	                        	d1213 = v12[0]*v13[0] + v12[1]*v13[1] + v12[2]*v13[2]
                        	                	c1214 = [v12[1]*v14[2]-v12[2]*v14[1],v12[2]*v14[0]-v12[0]*v14[2],v12[0]*v14[1]-v12[1]*v14[0]]
	                                        	lc1214 = math.sqrt(math.pow(c1214[0],2)+math.pow(c1214[1],2)+math.pow(c1214[2],2))
        	                                	d1214 = v12[0]*v14[0] + v12[1]*v14[1] + v12[2]*v14[2]
	        	                                c1213_1214 = [c1213[1]*c1214[2]-c1213[2]*c1214[1],c1213[2]*c1214[0]-c1213[0]*c1214[2],c1213[0]*c1214[1]-c1213[1]*c1214[0]]
        	        	                        lc1213_1214 = math.sqrt(math.pow(c1213_1214[0],2)+math.pow(c1213_1214[1],2)+math.pow(c1213_1214[2],2))
                	        	                d1213_1214 = c1213[0]*c1214[0] + c1213[1]*c1214[1] + c1213[2]*c1214[2]
                        	        	        cross_check = c1213_1214[0]*v12[0]+c1213_1214[1]*v12[1]+c1213_1214[2]*v12[2]
							newp1 = [0,0,0]
							newp2 = [0,0,1]
							newp3 = [lc1213,0,d1213]
							newpa = [0,0,d1a]
							newpb = [0,0,d1b]
							newpc = [lc1213,0,d1213+d3c]
							newpd = [lc1213,0,d1213+d3d]
                                        		if cross_check > 0:
                                                		newp4 = [lc1214*d1213_1214/(lc1213*lc1214),lc1214*lc1213_1214/(lc1213*lc1214),d1214]
	                                        	else:
        	                                        	newp4 = [lc1214*d1213_1214/(lc1213*lc1214),-lc1214*lc1213_1214/(lc1213*lc1214),d1214]
							newpe = [newp4[0],0,newp4[2]]
							if pdb == modelpdb:
								hand.append([newp4[1],lv13p])
							elif pdb == realpdb:
								check1 = 0
								check2 = 0
								check3 = 0
								check4 = 0
								if newp1[0]-newpe[0] <=  math.fabs(newp4[1]):
									check1 = 1
								if newpe[0] - newp3[0] <=  math.fabs(newp4[1]):
									check2 = 1
	                                                        vab = [0,0,d1b-d1a]	
        	                                      		vcd = [0,0,d3d-d3c]
								vba = [0,0,d1a-d1b]

                	                               		if vab[2]*vcd[2] >= 0:
									vae = [newpe[0],0,newpe[2]-newpa[2]]
									vac = [newpc[0],0,newpc[2]-newpa[2]]
									lvac = math.sqrt(math.pow(vac[0],2)+math.pow(vac[1],2)+math.pow(vac[2],2))
									caeac = [vae[1]*vac[2]-vae[2]*vac[1],vae[2]*vac[0]-vae[0]*vac[2],vae[0]*vac[1]-vae[1]*vac[0]]
									lcaeac = math.sqrt(math.pow(caeac[0],2)+math.pow(caeac[1],2)+math.pow(caeac[2],2))
									cabac = [vab[1]*vac[2]-vab[2]*vac[1],vab[2]*vac[0]-vab[0]*vac[2],vab[0]*vac[1]-vab[1]*vac[0]]
									daeac_abac = caeac[0]*cabac[0] + caeac[1]*cabac[1] + caeac[2]*cabac[2]
									if daeac_abac >= 0:
										check3 = 1
									elif math.fabs(lcaeac/lvac) <=  math.fabs(newp4[1]):
										check3 = 1
                                                                        vbe = [newpe[0],0,newpe[2]-newpb[2]]
                                                                        vbd = [newpd[0],0,newpd[2]-newpb[2]]
                                                                        lvbd = math.sqrt(math.pow(vbd[0],2)+math.pow(vbd[1],2)+math.pow(vbd[2],2))
                                                                        cbebd = [vbe[1]*vbd[2]-vbe[2]*vbd[1],vbe[2]*vbd[0]-vbe[0]*vbd[2],vbe[0]*vbd[1]-vbe[1]*vbd[0]]
                                                                        lcbebd = math.sqrt(math.pow(cbebd[0],2)+math.pow(cbebd[1],2)+math.pow(cbebd[2],2))
                                                                        cbabd = [vba[1]*vbd[2]-vba[2]*vbd[1],vba[2]*vbd[0]-vba[0]*vbd[2],vba[0]*vbd[1]-vba[1]*vbd[0]]
                                                                        dbebd_babd = cbebd[0]*cbabd[0] + cbebd[1]*cbabd[1] + cbebd[2]*cbabd[2]
                                                                        if dbebd_babd >= 0:
                                                                                check4 = 1
                                                                        elif math.fabs(lcbebd/lvbd) <=  math.fabs(newp4[1]):
                                                                                check4 = 1
                                                                else:
                                                                        vae = [newpe[0],0,newpe[2]-newpa[2]]
                                                                        vad = [newpd[0],0,newpd[2]-newpa[2]]
                                                                        lvad = math.sqrt(math.pow(vad[0],2)+math.pow(vad[1],2)+math.pow(vad[2],2))
                                                                        caead = [vae[1]*vad[2]-vae[2]*vad[1],vae[2]*vad[0]-vae[0]*vad[2],vae[0]*vad[1]-vae[1]*vad[0]]
                                                                        lcaead = math.sqrt(math.pow(caead[0],2)+math.pow(caead[1],2)+math.pow(caead[2],2))
                                                                        cabad = [vab[1]*vad[2]-vab[2]*vad[1],vab[2]*vad[0]-vab[0]*vad[2],vab[0]*vad[1]-vab[1]*vad[0]]
                                                                        daead_abad = caead[0]*cabad[0] + caead[1]*cabad[1] + caead[2]*cabad[2]
                                                                        if daead_abad >= 0:
                                                                                check3 = 1
                                                                        elif math.fabs(lcaead/lvad) <= math.fabs(newp4[1]):
                                                                                check3 = 1
                                                                        vbe = [newpe[0],0,newpe[2]-newpb[2]]
                                                                        vbc = [newpc[0],0,newpc[2]-newpb[2]]
                                                                        lvbc = math.sqrt(math.pow(vbc[0],2)+math.pow(vbc[1],2)+math.pow(vbc[2],2))
                                                                        cbebc = [vbe[1]*vbc[2]-vbe[2]*vbc[1],vbe[2]*vbc[0]-vbe[0]*vbc[2],vbe[0]*vbc[1]-vbe[1]*vbc[0]]
                                                                        lcbebc = math.sqrt(math.pow(cbebc[0],2)+math.pow(cbebc[1],2)+math.pow(cbebc[2],2))
                                                                        cbabc = [vba[1]*vbc[2]-vba[2]*vbc[1],vba[2]*vbc[0]-vba[0]*vbc[2],vba[0]*vbc[1]-vba[1]*vbc[0]]
                                                                        dbebc_babc = cbebc[0]*cbabc[0] + cbebc[1]*cbabc[1] + cbebc[2]*cbabc[2]   
                                                                        if dbebc_babc >= 0:
                                                                                check4 = 1
                                                                        elif math.fabs(lcbebc/lvbc) <=  math.fabs(newp4[1]):
                                                                                check4 = 1
								if check1 and check2 and check3 and check4:
									hand.append([newp4[1],lv13p, c1, c2, c3])
								else:
									hand.append("N/A")	

	                                else:
        	                                hand.append("N/A")
                	                if pdb == realpdb:
                        	                w = float(weight2raw[c1]*weight2raw[c2]*weight2raw[c3])
                                	        weight5.append(w)

        position = []
        centers = []
	starts = []
	ends = [] 
        for ks in k:
                if len(ks) >= 1:
			one_third = len(ks)/3 + 1
                        ssec = [0,0,0]
			sses = [0,0,0]
			ssee = [0,0,0]
                        for kr in ks[:one_third]:
                                sses[0] = sses[0] + kr[0]
                                sses[1] = sses[1] + kr[1]
                                sses[2] = sses[2] + kr[2]
                        sses[0] = sses[0]/one_third
                        sses[1] = sses[1]/one_third
                        sses[2] = sses[2]/one_third
                        starts.append(sses)
			for kr in ks[(one_third-1):(len(ks)-one_third+1)]:
                                ssec[0] = ssec[0] + kr[0]      
                                ssec[1] = ssec[1] + kr[1]      
                                ssec[2] = ssec[2] + kr[2]      
                        ssec[0] = ssec[0]/(len(ks)-2*one_third+2)   
                        ssec[1] = ssec[1]/(len(ks)-2*one_third+2)      
                        ssec[2] = ssec[2]/(len(ks)-2*one_third+2)
                        centers.append(ssec)      
                        for kr in ks[(len(ks)-one_third):len(ks)]:
                                ssee[0] = ssee[0] + kr[0]
                                ssee[1] = ssee[1] + kr[1]
                                ssee[2] = ssee[2] + kr[2]
                        ssee[0] = ssee[0]/one_third  
                        ssee[1] = ssee[1]/one_third
                        ssee[2] = ssee[2]/one_third
                        ends.append(ssee)

                else:
                        centers.append([])
			starts.append([])
			ends.append([])

        for count1, sse1 in enumerate(centers):
		for count2, sse2 in enumerate(centers):
			if count1 > count2:
				if sse1 and sse2:
		                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))
                		else:
                        		ssedis = -1
                		position.append(ssedis)

				if pdb == realpdb:
					weight4.append(weight4raw[count1]*weight4raw[count2])
        for count1, sse1 in enumerate(starts): 
                for count2, sse2 in enumerate(starts):    
                        if count1 > count2:      
                                if sse1 and sse2:  
                                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))    
                                else:
                                        ssedis = -1    
                                position.append(ssedis)    
                        
                                if pdb == realpdb:
                                        weight4.append(weight4raw[count1]*weight4raw[count2])      
        for count1, sse1 in enumerate(ends): 
                for count2, sse2 in enumerate(ends):    
                        if count1 > count2:      
                                if sse1 and sse2:  
                                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))    
                                else:
                                        ssedis = -1    
                                position.append(ssedis)    
                        
                                if pdb == realpdb:
                                        weight4.append(weight4raw[count1]*weight4raw[count2])      
        for count1, sse1 in enumerate(centers): 
                for count2, sse2 in enumerate(starts):    
                        if count1 != count2 and sse1 != sse2:      
                                if sse1 and sse2:  
                                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))    
                                else:
                                        ssedis = -1    
                                position.append(ssedis)    
                        
                                if pdb == realpdb:
                                        weight4.append(weight4raw[count1]*weight4raw[count2])      
        for count1, sse1 in enumerate(centers): 
                for count2, sse2 in enumerate(ends):    
                        if count1 != count2 and sse1 != sse2:  
                                if sse1 and sse2:  
                                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))    
                                else:
                                        ssedis = -1    
                                position.append(ssedis)    
                        
                                if pdb == realpdb:
                                        weight4.append(weight4raw[count1]*weight4raw[count2])      
        for count1, sse1 in enumerate(starts):
                for count2, sse2 in enumerate(ends):   
                        if count1 != count2 and sse1 != sse2:
                                if sse1 and sse2:
                                        ssedis = math.sqrt(math.pow((sse1[0]-sse2[0]),2)+math.pow((sse1[1]-sse2[1]),2)+math.pow((sse1[2]-sse2[2]),2))
                                else:
                                        ssedis = -1
                                position.append(ssedis)
                        
                                if pdb == realpdb:
                                        weight4.append(weight4raw[count1]*weight4raw[count2])



	if pdb == realpdb:
		resultp.write("length_weights:\n")
        	for w in weight1:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")
                resultp.write("angle_weights:\n")
                for w in weight2:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")
                resultp.write("interaction_weights:\n")
                for w in weight3:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")      
                resultp.write("packing_weights:\n")
                for w in weight4:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")
                resultp.write("handedness_weights:\n")
                for w in weight5:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")
                resultp.write("distance_weights:\n") 
                for w in weight6:
                        resultp.write(str(w) + "\t")
                resultp.write("\n")      
		resultp.write("real_length:\n")	
		for dis in length:
			resultp.write(str(dis) + "\t")
		resultp.write("\n")
                resultp.write("real_angle:\n")        
                for an in ang:
                        resultp.write(str(an) + "\t")
                resultp.write("\n")       
                resultp.write("real_interaction:\n")        
                for it in inter:
                        resultp.write(str(it) + "\t")
                resultp.write("\n")       
                resultp.write("real_packing:\n")        
                for po in position:
                        resultp.write(str(po) + "\t")
                resultp.write("\n")
		resultp.write("real_handedness:\n")
		for ha in hand:
			resultp.write(str(ha) + "\t")
		resultp.write("\n")
                resultp.write("real_distance:\n")   
                for dis in real_distances:  
                        resultp.write(str(dis) + "\t")
                resultp.write("\n")
	elif pdb == modelpdb:
                resultp.write("model_length:\n")
                for dis in length:    
                        resultp.write(str(dis) + "\t")
                resultp.write("\n")
                resultp.write("model_angle:\n")
                for an in ang:
                        resultp.write(str(an) + "\t")
                resultp.write("\n")
                resultp.write("model_interaction:\n")
                for it in inter:   
                        resultp.write(str(it) + "\t")  
                resultp.write("\n")
                resultp.write("model_packing:\n")
                for po in position:
                        resultp.write(str(po) + "\t")
                resultp.write("\n")
		resultp.write("model_handedness:\n")
		for ha in hand:
			resultp.write(str(ha) + "\t")
		resultp.write("\n")
                resultp.write("model_distance:\n")
                for dis in model_distances:
                        resultp.write(str(dis) + "\t")
                resultp.write("\n")
       
resultp.close()
percent = float(count_ca)/all_ca
if percent < 0.1:
	os.system(PYTHON + " " + QCS_PATH + "integrate.py " + workdir + "/" + realpdbfile + "_vs_" + modelpdbfile + " " + str(missing_penalty) + " " + str(randomscore) + " 0")
	print "drop_sses!"
else:
	if userweights:
        	os.system(PYTHON + " " + QCS_PATH + "integrate.py " + workdir + "/" + realpdbfile + "_vs_" + modelpdbfile + " " + str(userweights[0]) + " " + str(userweights[1]) + " " + str(userweights[2]) + " " + str(userweights[3]) + " " + str(userweights[4]) + " " + str(userweights[5]) + " " + str(missing_penalty) + " " + str(randomscore))
	else:
        	os.system(PYTHON + " " + QCS_PATH + "integrate.py " + workdir + "/" + realpdbfile + "_vs_" + modelpdbfile + " " + str(missing_penalty) + " " + str(randomscore))

