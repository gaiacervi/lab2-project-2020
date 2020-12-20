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
		m[int(test[i])-1,int(prediction[i])-1] = m[int(test[i])-1,int(prediction[i])-1] + 1 
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
	test_input = sys.argv[1] ### file .input_performance_SVM.txt
	predicted_folder = sys.argv[2] ### ./pred_C2_g05
	test_folder = sys.argv[3] ### ./set_SVM/
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
	#print(test_input)
	test_input = open(test_input,'r')
	for line in test_input:
		m = np.zeros((3,3),dtype = int)
		line = line.rstrip()
		test_file = open(test_folder + 'test'+ line + '.dat','r')
		#print(test_file)
		pred_file = open(predicted_folder + 'pred' + line + '.txt','r')
		test = []
		pred = []
		for line in test_file:
			test.append(line[0])
		for line in pred_file:
			pred.append(line[0])
		#print(test,'test',line)
		#print(pred,'pred',line)
		m = matrix_score(m,test,pred)
		#print(m)
		Q3 = (m[0,0] + m[1,1] + m[2,2]) / len(test)
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
	mean_MCC_H = statistics.mean(MCCH_l)
	#error = np.std(MCCH_l) / math.sqrt(5)
	error_MCCH = statistics.stdev(MCCH_l) / math.sqrt(5)
	print('MCC_H ',mean_MCC_H, '+/-', error_MCCH)

	mean_MCC_C= statistics.mean(MCCC_l)
	error_MCCC = statistics.stdev(MCCC_l) / math.sqrt(5)
	print('MCC_C ',mean_MCC_C, '+/-', error_MCCC) 

	mean_MCC_E = statistics.mean(MCCE_l)
	error_MCCE = statistics.stdev(MCCE_l) / math.sqrt(5)
	print('MCC_E ',mean_MCC_E, '+/-',error_MCCE)

	mean_sen_H = statistics.mean(senH_l)
	error_senH = statistics.stdev(senH_l) / math.sqrt(5)
	print('sen_H ',mean_sen_H,'+/-',error_senH)

	mean_sen_C = statistics.mean(senC_l)
	error_senC = statistics.stdev(senC_l) / math.sqrt(5)
	print('sen_C ',mean_sen_C,'+/-',error_senC)

	mean_sen_E = statistics.mean(senE_l)
	error_senE = statistics.stdev(senE_l) / math.sqrt(5)
	print('sen_E ',mean_sen_E,'+/-', error_senE)

	mean_PPVH = statistics.mean(PPVH_l)
	error_PPVH = statistics.stdev(PPVH_l) / math.sqrt(5)
	print('PPV_H ',mean_PPVH,'+/-',error_PPVH)

	mean_PPVC = statistics.mean(PPVC_l)
	error_PPVC = statistics.stdev(PPVC_l) / math.sqrt(5)
	print('PPV_C ',mean_PPVC, '+/-' ,error_PPVC)

	mean_PPVE = statistics.mean(PPVE_l)
	error_PPVE = statistics.stdev(PPVE_l) / math.sqrt(5)
	print('PPV_E ',mean_PPVE,'+/-',error_PPVE)

	#print(Q3_l)
	mean_Q3 = statistics.mean(Q3_l)
	error_Q3= statistics.stdev(Q3_l) / math.sqrt(5)
	print('Q3 ',mean_Q3,'+/-',error_Q3)