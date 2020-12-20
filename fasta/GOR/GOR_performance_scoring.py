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
	matrix[0,0] = m[index,index]
	matrix[0,1] = m[index,d[index][0]] + m[index,d[index][1]]
	matrix[1,0] = m[d[index][0],index] + m[d[index][1],index]
	a,b,c,d = all_couples(d[index][0],d[index][1])
	matrix[1,1] = m[a]+ m[b] + m[c] + m[d]
	#print(matrix)
	sen = matrix[0,0] / (matrix[0,0] + matrix[0,1])
	PPV = matrix[0,0] / (matrix[0,0] + matrix[1,0])
	n = matrix[0,0]*matrix[1,1] - matrix[1,0]*matrix[0,1]
	d = (matrix[0,0] + matrix[1,0]) * (matrix[0,0] + matrix[0,1]) * (matrix[1,1] + matrix[1,0]) * (matrix[1,1] + matrix[0,1])
	MCC = n / math.sqrt(d)
	return sen, PPV, MCC 


if __name__ == '__main__':
	input_test = sys.argv[1] ### Input file with ID testing for CV 
	data_dssp = sys.argv[2] ### Folder with all dssps
	input_test = open(input_test,'r')
	d = {0:[1,2],1:[0,2],2:[0,1]}
	MCCH_l = []
	senH_l = []
	PPVH_l = []

	MCCE_l = []
	senE_l = []
	PPVE_l = []

	MCCC_l = []
	senC_l = []
	PPVC_l = []
	Q3_l = []
	for test in input_test:
		test = test.rstrip()
		input_ID = open('./' + test +'/' + test + '.txt','r')
		m = np.zeros((3,3),dtype = int)
		tot_length_seq = 0 
		for line in input_ID:
			line = line.rstrip()
			prediction_file = open('./'+ test + '/' + 'GOR_' + line + '.txt','r') 
			dssp_file = open(data_dssp + line + '.dssp','r') 
			#print(dssp_file)
			dssp_line = dssp_file.readlines()[1]
			dssp_line = dssp_line.rstrip()
			prediction_line = prediction_file.readline()
			#print(prediction_line)
			prediction_line = prediction_line.rstrip()
			tot_length_seq = tot_length_seq + len(prediction_line)
			m = matrix_score(m,prediction_line,dssp_line)
		#print(m,test)
		#print(tot_dssp,tot_length_seq)
		Q3 = (m[0,0] + m[1,1] + m[2,2]) / tot_length_seq
		matrix = np.zeros((2,2),dtype = int)
		sen_H,PPV_H,MCC_H = performance(m,'H',d,matrix)
		sen_E,PPV_E,MCC_E = performance(m,'E',d,matrix)
		sen_C,PPV_C,MCC_C = performance(m,'C',d,matrix)
		senH_l.append(sen_H)
		MCCH_l.append(MCC_H)
		PPVH_l.append(PPV_H)

		senE_l.append(sen_E)
		MCCE_l.append(MCC_E)
		PPVE_l.append(PPV_E)

		senC_l.append(sen_C)
		MCCC_l.append(MCC_C)
		PPVC_l.append(PPV_C)

		Q3_l.append(Q3)

	print('H')
	mean_MCC_H = statistics.mean(MCCH_l)
	error_MCCH = statistics.stdev(MCCH_l) / math.sqrt(5)
	print('MCC: ', round(mean_MCC_H,4), '+/-', round(error_MCCH,4))

	mean_sen_H = statistics.mean(senH_l)
	error_senH = statistics.stdev(senH_l) / math.sqrt(5)
	print('sen: ',round(mean_sen_H,4),'+/-',round(error_senH,4))

	mean_PPVH = statistics.mean(PPVH_l)
	error_PPVH = statistics.stdev(PPVH_l) / math.sqrt(5)
	print('PPV: ',round(mean_PPVH,4),'+/-',round(error_PPVH,4))

	print('C')
	mean_MCC_C= statistics.mean(MCCC_l)
	error_MCCC = statistics.stdev(MCCC_l) / math.sqrt(5)
	print('MCC: ',round(mean_MCC_C,4), '+/-', round(error_MCCC,4)) 

	mean_sen_C = statistics.mean(senC_l)
	error_senC = statistics.stdev(senC_l) / math.sqrt(5)
	print('sen: ',round(mean_sen_C,4),'+/-',round(error_senC,4))

	mean_PPVC = statistics.mean(PPVC_l)
	error_PPVC = statistics.stdev(PPVC_l) / math.sqrt(5)
	print('PPV: ',round(mean_PPVC,4), '+/-' ,round(error_PPVC,4))

	print('E')
	mean_MCC_E = statistics.mean(MCCE_l)
	error_MCCE = statistics.stdev(MCCE_l) / math.sqrt(5)
	print('MCC: ',round(mean_MCC_E,4), '+/-',round(error_MCCE,4))

	mean_sen_E = statistics.mean(senE_l)
	error_senE = statistics.stdev(senE_l) / math.sqrt(5)
	print('sen: ',round(mean_sen_E,4),'+/-', round(error_senE,4))

	mean_PPVE = statistics.mean(PPVE_l)
	error_PPVE = statistics.stdev(PPVE_l) / math.sqrt(5)
	print('PPV: ',round(mean_PPVE,4),'+/-',round(error_PPVE,4))

	mean_Q3 = statistics.mean(Q3_l)
	error_Q3= statistics.stdev(Q3_l) / math.sqrt(5)
	print('Q3 ',round(mean_Q3,4),'+/-',round(error_Q3,4))
















