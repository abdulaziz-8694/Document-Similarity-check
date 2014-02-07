##################################################
#Filename: similarity.py
#Author: Abdul Aziz 
#How to run: On terminal type python similarity.py
##################################################
import Tkinter, tkFileDialog
import os, mimetypes, sys
from munkres import Munkres

S = []
alpha = 0.4
beta = 0.1

#dirname = "C:/Users/AbdulAziz/Desktop/rs agarwal"
def init_matrix(n):
	A = []
	for i in range(n):
		temp = []
		for j in range(n):
			temp.append(0)
		A.append(temp)
	#print A
	return A
	
	
def senSim(senA,senB,alpha):
	senA = senA.split(" ")
	senB = senB.split(" ")
	A_union_B = len(set(senA).union(set(senB)))
	A_intersection_B = len(set(senA).intersection(set(senB)))
	result = float(A_intersection_B)/A_union_B
	if result < alpha:
		result = 0
	return result

def getFileSim(fileA,fileB,alpha,beta):
	File1=open(fileA, "r")
	File2=open(fileB, "r")
	content1=File1.readlines()
	#print content1
	content2=File2.readlines()
	#print content2
	if len(content1) > len(content2):
		#print "big"
		content1,content2 = content2,content1
	#print content1
	#print content2
	sim=[]
	for sen_A in content1:
		temp = []
		sen_A = sen_A.lower()
		for sen_B in content2:
			sen_B = sen_B.lower()
			temp.append(senSim(sen_A,sen_B,alpha))
		sim.append(temp)
		
	for i in range(len(sim)): #to make it a maximum cost problem
		for j in range(len(sim[i])):
			sim[i][j] = 1-sim[i][j]
	m=Munkres()
	result_matrix=m.compute(sim)
	#print sim
	#print result_matrix
	maxSimMatrix = []
	for row,column in result_matrix:
		if	sim[row][column]!=1.0:
			maxSimMatrix.append(1-sim[row][column])
	FileSim=float(len(maxSimMatrix))/(len(content1))
	
	if FileSim<beta:
		FileSim = 0;
	
	return FileSim
		
	


def getFilepaths(dirname):
	filepaths=[]
	#i=0
	for file in os.listdir(dirname):
		#print file
		filepath = dirname+'/'+file
		if mimetypes.guess_type(filepath) == ('text/plain',None ):
			filepaths.append(dirname+'/'+file)
			#print "text"
		#else:
			#print "not text"
		#print filepath
	return filepaths
	

root = Tkinter.Tk()
root.withdraw()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

#if len(dirname ) > 0:
   	#print "You chose %s" % dirname
	
files=getFilepaths(dirname)
#print files
S = init_matrix(len(files))

for a in range(len(files)):
	for b in range(len(files)):
		#print files[a]
		if a==b:
			S[a][b] = 1
		else:
			#print files[b]
			S[a][b] = getFileSim(files[a],files[b],alpha,beta)
print S






	
