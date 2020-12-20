import sys 

def convert_profilefile(profile_file):
	profile = []
	for line in profile_file:
		line = line.split()
		if line[0] != 'A':
			profile.append(line[2:])
	return profile
#print(convert_profilefile(profile_file))
def convert_dsspfile(dssp_file):
	dssp_class = []
	for line in dssp_file:
		if not line.startswith('>'):
			line = line.rstrip()
			#print(line)
			for e in line:
				if (e == 'C') or (e == '-'):
					e = 3
				elif e == 'E':
					e = 2 
				else:
					e = 1
				dssp_class.append(e)
	#print(dssp_class)
	return dssp_class

def extract_input_SVM(window,profile,output_file,dssp_class):
	c = 0 
	while c != len(profile):
		m = [[str(0.0) for i in range(20)]for i in range(17)]
		d = int(window/2) 
		for i in range(-d,d+1):
			line_number = c + i
			if line_number >= 0 and line_number <= len(profile)-1:
				for j in range(20):
					if profile[line_number][j] != str(0.0):
						row = line_number + 8 - c
						m[row][j] = profile[line_number][j]
		d = 0

		file_line = "" 
		file_line = file_line + str(dssp_class[c])
		for line in m: 
			for e in line: 
				d = d +1 
				if e != str(0.0): 
					file_line = file_line + ' '+ str(d) + ":" + e 
		
		file_line = file_line + "\n"
		output_file.write(file_line)
		c += 1 
	return output_file

if __name__ == '__main__':
	input_file = sys.argv[1] ### File with all the .txt profiles (set0.txt)
	input_file = open(input_file,'r') 
	folder_dssp = sys.argv[2] ### Folder with all dssp files
	folder_output = sys.argv[3] ### Folder where all output files go (input_SVM)
	for line in input_file:
		line = line.rstrip()
		profile_file = open(line + '.txt','r')
		dssp_file = open(folder_dssp + line + '.dssp','r')
		output_file = open(folder_output + line + '_output.dat','w')
		profile = convert_profilefile(profile_file)
		dssp_class = convert_dsspfile(dssp_file)
		window = 17
		extract_input_SVM(window,profile,output_file,dssp_class)

