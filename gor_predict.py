import numpy as np 
import sys 

def I_parameter(profile_matrix,i,e,SSE_matrix,count,R_matrix):
	t = count * R_matrix[i,e]
	j = SSE_matrix[i,e] / t
	p = profile_matrix * np.log(j) 
	return p

def return_SSE(I_H,I_C,I_E):
	b = max(I_H,I_C,I_E)
	#print(b,'b')
	if b == I_C:
		return 'C'
	elif b == I_E:
		return 'E' 
	elif b == I_H:
		return 'H' 

def prediction_SSE(profile_matrix,n_row,window,output_file):
	output_file = open(output_file,'w')
	c = 0 
	SSE = ""
	n = int(window)-1
	while c != (n_row-n):
		I_H = 0 
		I_E = 0 
		I_C = 0 
		for i in range(int(window)): 
			for e in range(20):
				if profile_matrix[c+i,e] != float(0):		
					I_H +=  I_parameter(profile_matrix[c+i,e],i,e,H,count_H,R) 
					I_E +=  I_parameter(profile_matrix[c+i,e],i,e,E,count_E,R) 
					I_C +=  I_parameter(profile_matrix[c+i,e],i,e,C,count_C,R)
		SSE_predicted = return_SSE(I_H,I_C,I_E)
		SSE = SSE + SSE_predicted
		c = c +1
	output_file.write(SSE)

 
if __name__ == '__main__':
	model = sys.argv[1]  ### ./GOR/test0/model0.npz
	input_ID = sys.argv[2] ### ./GOR/test0/test0.txt
	window = sys.argv[3] #17
	output_data = sys.argv[4] ### ./GOR/test0/ 
	model = np.load(model)
	C = (model['C_matrix'])
	H = (model['H_matrix'])
	E = (model['E_matrix'])
	R = (model['R_matrix'])
	count_C = (model['count_C'])
	count_H = (model['count_H'])
	count_E = (model['count_E'])
	input_ID = open(input_ID,'r')
	zeros = np.zeros((8,20))
	for line in input_ID:
		line = line.rstrip()
		profile_file = open(line + '.txt','r') 
		output_file = output_data + 'GOR_'+ line + '.txt'
		L = np.loadtxt(profile_file,skiprows = 1, usecols=range(2,22))
		profile_matrix = np.concatenate((zeros,L,zeros),axis = 0)
		n_row = profile_matrix.shape[0]
		prediction_SSE(profile_matrix,n_row,window,output_file)


		

