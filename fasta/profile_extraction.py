import os 

directory = r'/home/gaia/lab2/project/fasta'
#directory = r'/home/gaia/lab2/project/blindset/blindset_dssp/mapped_fasta/random_150'

for filename in os.listdir(directory):
	#print(filename)
	if filename.endswith(".pssm"):
		f = open(filename)
		PDBID = str(filename[:len(filename)-5])
		#print(PDBID)
		#f_output_fasta = open(directory + '/' + PDBID +'.txt','w')
		length = 0
		c = 0
		lista = []
		for line in f:  
			a = line.split()
			if len(a) == 40:
				header = a[20:]
		
	
			elif len(a) == 44:
				length += 1 
				begin = a[0:2]
				profile = a[22:42]
				l = []
				for i in profile:
					frequency = int(i)/100
					if frequency == 0.0 or frequency == 0:
						c += 1 
					l.append(str(frequency))
				begin.extend(l)
				lista.append(begin)

		if c != 20*length:												### check the presence of empty profiles. 
			f_output_fasta = open(directory + '/' + PDBID +'.txt','w')
			t = '             ' + '     '.join(header) + '\n'
			#print(t)
			f_output_fasta.write(t)
			for e in lista:
				s = ""
				for elem in e:
					if len(elem) == 1:
						s = s + elem + "     " 
					elif len(elem) == 2:
						s = s + elem + "    "
					elif len(elem) == 3:
						s = s + elem + "   "
					else:
						s = s + elem + "  "
				s = s + "\n"
				#print(s)
				f_output_fasta.write(s)