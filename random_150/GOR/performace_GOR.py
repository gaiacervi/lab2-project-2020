import sys 
import numpy as np 
import math 
import statistics 

def index_matrix(element):
	if element == 'H':
		return 0
	elif element == 'E':
		return 1
	else:
		return 2

def matrix_score(m,prediction_line,dssp_line):
	for i in range(len(prediction_line)):
		observed_i = index_matrix(str(dssp_line[i]))
		#print(dssp_line[i])
		predict_i = index_matrix(str(prediction_line[i]))
		m[observed_i,predict_i] += 1 
	return m 

def all_couples(a,b):
	c = (a,a)
	d = (a,b)
	e = (b,a)
	f = (b,b)
	return c,d,e,f
	

### Function that returns the 2,2 matrix!
def performance(m,element,d,matrix): 
	index = index_matrix(element)
	#print(index)
	matrix[0,0] = m[index,index]
	matrix[0,1] = m[index,d[index][0]] + m[index,d[index][1]]
	matrix[1,0] = m[d[index][0],index] + m[d[index][1],index]
	a,b,c,d = all_couples(d[index][0],d[index][1])
	matrix[1,1] = m[a]+ m[b] + m[c] + m[d]
	#print(matrix)
	sen = matrix[0,0] / (matrix[0,0] + matrix[0,1])
	#print(sen,element)
	PPV = matrix[0,0] / (matrix[0,0] + matrix[1,0])
	n = matrix[0,0]*matrix[1,1] - matrix[1,0]*matrix[0,1]
	d = (matrix[0,0] + matrix[1,0]) * (matrix[0,0] + matrix[0,1]) * (matrix[1,1] + matrix[1,0]) * (matrix[1,1] + matrix[0,1])
	MCC = n / math.sqrt(d)
	return sen, PPV, MCC 


if __name__ == '__main__':
	input_ID = sys.argv[1] ### Input file with ID testing 
	data_dssp = sys.argv[2] ### Folder with all dssps
	d = {0:[1,2],1:[0,2],2:[0,1]}
	m = np.zeros((3,3),dtype = int)
	tot_length_seq = 0 
	input_ID = open(input_ID,'r')
	for line in input_ID:
		line = line.rstrip()
		#print(line)
		prediction_file = open('GOR_' + line + '.txt','r') 
		dssp_file = open(data_dssp + line + '.dssp','r') 
		dssp_line = dssp_file.readlines()[1]
		dssp_line = dssp_line.rstrip()
		prediction_line = prediction_file.readline()
		prediction_line = prediction_line.rstrip()
		tot_length_seq = tot_length_seq + len(prediction_line)
		m = matrix_score(m,prediction_line,dssp_line)
	#print(m)
	Q3 = (m[0,0] + m[1,1] + m[2,2]) / tot_length_seq
	matrix = np.zeros((2,2),dtype = int)
	sen_H,PPV_H,MCC_H = performance(m,'H',d,matrix)
	sen_E,PPV_E,MCC_E = performance(m,'E',d,matrix)
	sen_C,PPV_C,MCC_C = performance(m,'C',d,matrix)
	

	print('H')
	print('MCC: ', round(MCC_H,4)) 
	print('sen: ',round(sen_H,4))
	print('PPV: ',round(PPV_H,4))

	print('C')
	print('MCC: ',round(MCC_C,4)) 
	print('sen: ',round(sen_C,4))
	print('PPV: ',round(PPV_C,4))

	print('E')
	print('MCC: ',round(MCC_E,4))
	print('sen: ',round(sen_E,4))
	print('PPV: ',round(PPV_E,4))

	print('Q3 ',round(Q3,4))