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

def matrix_score(m,test,prediction):
	#print(len(prediction_line),'len')
	for i in range(len(prediction)):
		m[test[i]-1,prediction[i]-1] += 1 
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
	matrix[0,0] = m[index,index]
	matrix[0,1] = m[index,d[index][0]] + m[index,d[index][1]]
	matrix[1,0] = m[d[index][0],index] + m[d[index][1],index]
	a,b,c,d = all_couples(d[index][0],d[index][1])
	matrix[1,1] = m[a]+ m[b] + m[c] + m[d]
	#print(matrix)
	sen = matrix[0,0] / (matrix[0,0] + matrix[0,1])
	PPV = matrix[0,0] / (matrix[0,0] + matrix[1,0])
	n = (matrix[0,0]*matrix[1,1]) - (matrix[1,0]*matrix[0,1])
	d = (matrix[0,0] + matrix[1,0]) * (matrix[0,0] + matrix[0,1]) * (matrix[1,1] + matrix[1,0]) * (matrix[1,1] + matrix[0,1])
	MCC = n / math.sqrt(d)
	return sen, PPV, MCC 


if __name__ == '__main__':
	test_file = sys.argv[1] 
	pred_file = sys.argv[2]
	d = {0:[1,2],1:[0,2],2:[0,1]}
	m = np.zeros((3,3),dtype = int)
	test_file = open(test_file,'r')
	pred_file = open(pred_file,'r')
	test = []
	pred = []
	for line in test_file:
		test.append(int(line[0]))
	#print(test)
	for line in pred_file:
		pred.append(int(line[0]))
	#print(pred)
	m = matrix_score(m,test,pred)
	print(m)
	Q3 = (m[0,0] + m[1,1] + m[2,2]) / len(test)
	matrix = np.zeros((2,2),dtype = int)
	sen_H,PPV_H,MCC_H = performance(m,'H',d,matrix)
	sen_E,PPV_E,MCC_E = performance(m,'E',d,matrix)
	sen_C,PPV_C,MCC_C = performance(m,'C',d,matrix)

	print('H')
	print('MCC: ',round(MCC_H,4))
	print('sen: ',round(sen_H,4))
	print('PPV: ', round(PPV_H,4))

	print('E')
	print('MCC: ',round(MCC_E,4))
	print('sen: ',round(sen_E,4))
	print('PPV: ', round(PPV_E,4))

	print('C')
	print('MCC: ',round(MCC_C,4))
	print('sen: ',round(sen_C,4))
	print('PPV: ', round(PPV_C,4))

	print('Q3: ',round(Q3,4))