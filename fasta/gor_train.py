import sys
import numpy as np 

def create_empty_dictionary(d_H,d_E,d_C,d_R):
	AA = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T', 'W', 'Y', 'V']
	for aa in AA: 
		d_H[aa] = [0 for i in range(17)]
		d_E[aa] = [0 for i in range(17)]
		d_C[aa] = [0 for i in range(17)]
		d_R[aa] = [0 for i in range(17)]
	return(d_H,d_E,d_C,d_R)

### Function that retrieves the dictionary correspondent to the SSE element. 
def get_dictionary(SSE,d_H,d_E,d_C,d_R,i,frequency,residue):
	d_R[residue][i+8] = round(d_R[residue][i+8] + frequency,2)
	if SSE in( '-' or 'C'):
		d_C[residue][i+8] = round(d_C[residue][i+8] + frequency,2)
	elif SSE == 'H':
		d_H[residue][i+8] = round(d_H[residue][i+8] + frequency,2)
	elif SSE == 'E':
		d_E[residue][i+8] = round(d_E[residue][i+8] + frequency,2)
	return(d_H,d_E,d_C,d_R)

def get_count_residue(d_R,i):
	count = 0 
	for key in d_R.keys():
		count = round(count + d_R[key][i],2)
	return count

def get_count_SSE(SSE,count_H,count_E,count_C):
	if SSE == 'H':
		count_H += 1 
	elif SSE == 'E':
		count_E += 1 
	else:
		count_C += 1 
	return count_H,count_E,count_C

def GOR(profile_file, dssp_file, window,d_H,d_C,d_E,d_R,count_H,count_E,count_C):
	profile_file = open(profile_file,'r')
	dssp_file = open(dssp_file,'r')
	dssp_line = dssp_file.readlines()[1]
	dssp_line = dssp_line.rstrip()
	m = len(dssp_line) ### length dssp 
	L = []
	for line in profile_file:
		line = line.split()
		if line[0] == 'A':
			AA = line
		else:
			line = line[2:]
			L.append(line)
	#print(L,'L')	
	c = 0
	while c != m:
		SSE = dssp_line[c]
		count_H,count_E,count_C = get_count_SSE(SSE,count_H,count_E,count_C)
		d = int(int(window)/2) ### put window as parameter in function! 
		for i in range(-d,d+1):
			line_number = c + i 
			#print(line_number,'line_number')
			if line_number >= 0 and line_number <= m -1:
				profile_line = L[line_number]
				#print(profile_line,line_number)
				for j in range(len(profile_line)):
					if float(profile_line[j]) != 0.0:
						frequency = float(profile_line[j])
						residue = AA[j]
						#print(frequency,residue)
						d_H,d_E,d_C,d_R = get_dictionary(SSE,d_H,d_E,d_C,d_R,i,frequency,residue)
		c += 1 
	return (d_H,d_E,d_C,d_R,count_H,count_E,count_C)

### Function that normalizes the complete dictionary 
def normalization(d_R,d_H,d_E,d_C,window):
	for i in range(int(window)):
		count = get_count_residue(d_R,i)
		#print(count,'count',i,'i')
		for key in d_R.keys():
			d_H[key][i] = d_H[key][i] / count
			d_E[key][i] = d_E[key][i] / count 
			d_C[key][i] = d_C[key][i] / count
			d_R[key][i] = d_R[key][i] / count
	return d_H,d_E,d_C,d_R

if __name__ == '__main__':
	input_file = sys.argv[1] ### File txt with all IDs
	data = sys.argv[2]		### Folder with all profiles 
	window = sys.argv[3] ### Window you would like to have 
	output_file = sys.argv[4]
	d_H = {}
	d_E = {}
	d_C = {}
	d_R = {}
	count_H = 0 
	count_E = 0 
	count_C = 0 
	d_H,d_E,d_C,d_R = create_empty_dictionary(d_H,d_E,d_C,d_R)
	input_file = open(input_file,'r')
	for line in input_file:
		line = line.rstrip()
		profile_file = line + '.txt'
		profile_dssp = data + line + '.dssp'
		d_H,d_E,d_C,d_R,count_H,count_E,count_C = GOR(profile_file, profile_dssp, window,d_H,d_C,d_E,d_R,count_H,count_E,count_C)
	d_H,d_E,d_C,d_R = normalization(d_R,d_H,d_E,d_C,window)
	total = count_H + count_C + count_E 
	#print(total,'total_counts_SSE')
	count_H = count_H / total 
	count_E = count_E / total 
	count_C = count_C / total 
	E = []
	for i in range(17):
		e = []
		for keys in d_E.keys():
			e.append(d_E[keys][i])
		E.append(e)
	E = np.array(E) 
	H = []
	for i in range(17):
		h = []
		for keys in d_H.keys():
			h.append(d_H[keys][i])
		H.append(h)
	H = np.array(H)
	#print('C')
	C = []
	for i in range(17):
		e = []
		for keys in d_C.keys():
			e.append(d_C[keys][i])
		C.append(e)
	C = np.array(C)
	#print('R')
	R = []
	for i in range(17):
		e = []
		for keys in d_R.keys():
			e.append(d_R[keys][i])
		R.append(e)
	R = np.array(R)
	np.savez(output_file,C_matrix=C,H_matrix=H,E_matrix=E,
		R_matrix=R,count_C= count_C,count_H= count_H,count_E=count_E)


