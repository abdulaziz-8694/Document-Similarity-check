########################################################################################################
#Filename: similarity.py                                                                       #
#Author: Abdul Aziz CS12B1001                                                                			#
#How to run:  import the required library then run the console and type  python similarity.py  #
#Description :this file takes input  and generates data.json and files									#
#########################################################################################################
import Tkinter, tkFileDialog, tkSimpleDialog #for gui
import os, mimetypes, sys						#for 
from munkres import Munkres
import json, shutil, re

S = []

dirname = "C:/Users/AbdulAziz/Desktop/rs agarwal"
def init_matrix(n):
	A = []
	for i in range(n):
		temp = []
		for j in range(n):
			temp.append(0)
		A.append(temp)
	return (A)
def senSim(senA,senB,alpha):
	senA = re.sub('[\W]', ' ', senA)
	senA = senA.split(" ")
	senB = re.sub('[\W]', ' ', senB)
	senB = senB.split(" ")
	A_union_B = len(set(senA).union(set(senB)))
	A_intersection_B = len(set(senA).intersection(set(senB)))
	result = float(A_intersection_B)/A_union_B
	if result < alpha:
		result = 0
	return result

def getFileSim(fileA,fileB,alpha,beta):
	File1=open(dirname+'/'+fileA, "r")
	File2=open(dirname+'/'+fileB, "r")
	content1=File1.readlines()
	flag=0
	content2=File2.readlines()
	if len(content1) > len(content2):
		flag=1
		content1,content2 = content2,content1
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
			sim[i][j] = 1.0-sim[i][j]
	m=Munkres()
	result_matrix=m.compute(sim)
	maxSimMatrix = []
	for row,column in result_matrix:
		if	sim[row][column]!=1.0:
			if flag==1:
				row,column=column,row
			maxSimMatrix.append([row,column])
	FileSim=float(len(maxSimMatrix))/(len(content1))
	
	if FileSim<beta:
		FileSim = 0
	return (FileSim, maxSimMatrix)
		
	


def getFile(dirname):
	files=[]
	for file in os.listdir(dirname):
		filepath = dirname+'/'+file
		if mimetypes.guess_type(filepath) == ('text/plain',None ):
			files.append(file)
	return files

root = Tkinter.Tk()
root.withdraw()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
alpha = tkSimpleDialog.askfloat('Alpha', 'Enter the value of alpha', initialvalue=0.6, minvalue=0.0, maxvalue=1.0)
beta = tkSimpleDialog.askfloat('Beta', 'Enter the value of beta', initialvalue=0.1, minvalue=0.0, maxvalue=1.0)
if dirname=='':
	dirname='.'
if alpha==None:
	alpha=0.6
if beta==None:
	beta=0.1

	
files=getFile(dirname)
S = init_matrix(len(files))
sim=init_matrix(len(files))
result=[]
for a in range(len(files)):
	temp1=[]
	temp2=[]
	for b in range(len(files)):
		if a==b:
			S[a][b] = 1
		else:
			(x,y) = getFileSim(files[a],files[b],alpha,beta)
			#print "just after", y
			S[a][b]=x
			sim[a][b]=y
print sim
#for creating json file
def getData(dirname,files,S,sim,beta):
	data={}
	filelist = []
	#print len(files)
	for file in files:
		temp={}
		temp['name'] = file
		content=open(dirname+'/'+file).read()
		filelist.append(temp)
	data['nodes'] = filelist
	links = []
	for i in range(len(S)):
		for j in range(i+1,len(S)):
			#print i,j
			if	S[i][j]>=beta:
				temp={}
				temp['source'] = i
				temp['target'] = j
				temp['weight'] = S[i][j]
				temp2=[]
				temp['pairs'] = sim[i][j]
				links.append(temp)
	data['links'] = links
	return data

def getData2(dirname,files):
	data=""
	filesdata="["
	name="["
	for file in files:
		name+="'"+file+"',"
		f=open(dirname+'/'+file, "r")
		content=f.readlines()
		filesdata+="["
		for sen in content:
			l=str(sen)
			m=l.replace('"',r'\"')
			m=m.replace('<', r'&lt;')
			m=m.replace('>', r'&gt;')
			filesdata+="\""+m+"\","
		filesdata+="],"
	name+="];"
	filesdata+="]"
	filesdata=re.sub("\n","",filesdata)
	data = "filename="+name+'\n'+"filedata="+filesdata
	return data

def dumpData(data,dirname):
	with open('data.json', 'wb') as f:
		json.dump(data, f)
		
data=getData(dirname,files,S,sim,beta)
data2 = getData2(dirname,files)
filedata=open("data.js", "w")
filedata.write(data2)
dumpData(data,dirname)







	
