#--------------AC circuits-------

import PyPDF2
import subprocess
import os
import re #importing regualr expressions

from manipulateString import *
#open doc and read 

#[expNum][questionNum][Option0,Option1,...]  
#remember to have the second entry be the generic one 

questions=[] #pagenumber, step number, description of marks, marks to be given in full
questions.append([2,"(100)","Names Page",100]) #This is inthere so that we can revert to this during debugging and also so that the list is 
questions.append([4,"(2)","Vmax:3V, Period:0.001s, Freq:1000Hz",1])#qnum:1
questions.append([5,"(1)","1)160 2)0.0188 3)3 4)S:-90 C:-90",4])#qnum:2
questions.append([6,"(3)","Measured V_max:3 I_max:0.0188",0.5])#qnum:3
questions.append([6,"(5)","Measured \\Delta\\phi:-86.4",0.5])#qnum:4
questions.append([7,"(1)","1)188 2)1.6 3)2.54 4)2.54 5)S:-57.8 Res:0 Cap:-90",4])#qnum:5
questions.append([8,"(4)","Measured  I_max:0.0157  V_max(resistor):1.54  V_max(capacitor):2.52 ",1])#qnum:6
questions.append([8,"(5)","Measured \\Delta\\phi Source:-55.4   R:-3.96  C:-91.4",1])#qnum:7
questions.append([9,"(1)","1)50.3  2)0.0579  3)3  4)S:90  I:90",4])#qnum:8
questions.append([10,"(5)","Measured \\Delta\\phi Measured:-79.6",1])#qnum:9
questions.append([11,"(1)","1)112  2)0.0268  3)2.68  4)1.32  5)S:26.7  R:0  I:90",4])#qnum:10
questions.append([12,"(5)","Measured \\Delta\\phi S:26.6(-333)  R:-3.6  C:79.2",1])#qnum:11
questions.append([13,"(1)","1)148 2)0.0203  3)2.03  4)1.02  5)3.23  6)S:-57.8  R:0  I:90  C:-90",4])#qnum:12
questions.append([14,"(4)","Measured I_max:0.0157  V_max(r):1.89  V_max(I):0.975  V_max(c):3.09",1])#qnum:13
questions.append([14,"(5)","Measured \\Delta\\phi S:-44.3  R:-3.96  I:78.5  C:-90",1])#qnum:14
questions.append([15,"(1)","1780",2])#qnum:15
questions.append([15,"(2)","1700",2])#qnum:16
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:17

ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","V$_{max}$: 3V","Period: 0.001s","Freq: 1000Hz"], #Q1
					 ["From Text Field","1)160 $\\Omega$","2)0.0188 A","3)3 V","4)S:-90$^{\\circ}$","C:-90$^{\\circ}$"], #Q2
					 ["From Text Field","Measured V$_{max}$:3 V","Measured I$_{max}$:0.0188 A"], #Q3
					 ["From Text Field","Measured $\\Delta\\phi$:-86.4"], #Q4
					 ["From Text Field","1)188$\\Omega$","2)1.6 A","3)2.54 V","4)2.54 V","5)S:-57.8$^{\\circ}$","5)Res:0$^{\\circ}$","5)Cap:-90$^{\\circ}$"], #Q5
					 ["From Text Field","Measured I$_{max}$:0.0157 A","Measured V$_{max}$(resistor):1.54 V","Measured V$_{max}$(capacitor):2.52 V"], #Q6
					 ["From Text Field","Measured $\\Delta\\phi$ Source:-55.4$^{\\circ}$","Measured $\\Delta\\phi$ Resistor:-3.96$^{\\circ}$","Measured $\\Delta\\phi$ Capacitor:-91.4$^{\\circ}$"], #Q7
					 ["From Text Field","1)50.3 $\\Omega$","2)0.0579 A","3)3 V","4)S:90$^o$","I:90$^o$"], #Q8
					 ["From Text Field","Measured $\\Delta\\phi$ Measured:79.6$^{\\circ}$"], #Q9
					 ["From Text Field","1)112 $\\Omega$","2)0.0268 A","3)2.68 V","4)1.35 V","5)S:26.7$^{\\circ}$","5)R:0$^{\\circ}$","5)I:0$^{\\circ}$"], #Q10
					 ["From Text Field","Measured $\\Delta\\phi$ Source:26.6(-333)$^{\\circ}$","Measured $\\Delta\\phi$ Resistor:-3.6$^{\\circ}$","Measured $\\Delta\\phi$ Capacitor:79.2$^{\\circ}$"], #Q11
					 ["From Text Field","1)148 $\\Omega$","2)0.0203 A","3)2.03 V","4)1.02 V","5)3.23 V","6)Source:-57.8$^{\\circ}$","Resistor:0$^{\\circ}$","Inductor:90$^{\\circ}$","Capacitor:-90$^{\\circ}$",""], #Q12
					 ["From Text Field","Measured I$_{max}$:0.0157 A","Measured V$_{max}$(Resistor):1.89 V","Measured V$_{max}$(Inductor):0.975 V","Measured V$_{max}$(Capacitor):3.09 V"], #Q13
					 ["From Text Field","Measured $\\Delta\\phi$ Source:44.3$^{\\circ}$","Measured $\\Delta\\phi$ Resistor:-3.96","Measured $\\Delta\\phi$ Inductor:78.5","Measured $\\Delta\\phi$ Capacitor:-90"], #Q14
					 ["From Text Field","Calculated resonant frequency 1780 Hz"], #Q15
					 ["From Text Field","Measured resonant frequency 1700 Hz"], #Q16
					 ["From Text Field","The station was not very clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q17


def nameCheck(pagetext,students):
	"""  Reads the names, the plan for all experimetns is that you strip everything of all the names and then make a list of six for the 3 names of the students   """
#-----defaults-------------
	pagetextOriginal=pagetext
	student1="Couldnt get names automatically"
	student2="Couldnt get names automatically"
	student3="Couldnt get names automatically"
#-----Checking for answers-------------
	nostudent="your name"
	rem=0
	studentsInThisSt=[0,0,0]
	for	x in range(1,len(students)-1):
		studentToCheck=students[x][0]
		toCheck=studentToCheck.strip().split(" ")
		#checking for absentees by looking for the number of "no names" present
		p = re.compile(nostudent)
		absentNo=len(p.findall(pagetext))//2

		if checkString.regExSearch(pagetext,toCheck[0]) and checkString.regExSearch(pagetext,toCheck[1]):
			try:
				studentsInThisSt[rem]=x
				rem+=1
			except:pass

	if studentsInThisSt[0] != 0: student1=students[studentsInThisSt[0]][0]
	if studentsInThisSt[1] != 0: student2=students[studentsInThisSt[1]][0]
	if studentsInThisSt[2] != 0: student3=students[studentsInThisSt[2]][0]
	if absentNo>2:student1=""
	if absentNo>1:student2=""
	if absentNo>0:student3=""

#----------Returning the values----------------
	return[student1,student2,student3]	#ans is [students answer, marks, for default comment use 1]


def q1(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q2(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q3(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q4(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q5(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q6(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q7(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q8(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q9(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q10(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"back toward you.").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"a/b/c/d").split('\n')
	studentsAnswer=studentsAnswer[0]
	if checkString.regExSearch(studentsAnswer,"pos"): marks+=0.5

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q11(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"back toward you.").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"a/b/c/d").split('\n')
	if len(studentsAnswer)>1:
		studentsAnswer=studentsAnswer[1]
		if checkString.regExSearch(studentsAnswer,"a"): marks+=0.5

	elif len(studentsAnswer)>0:
		studentsAnswer=studentsAnswer[0]
		if checkString.regExSearch(studentsAnswer,"a"): marks+=0.5

	elif len(studentsAnswer)==0:
		studentsAnswer="Not Answered"

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q12(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"a/b/c/d").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"increasing/decreasing")
	#print("******************************************************************")
	#print(studentsAnswer)
	if checkString.regExSearch(studentsAnswer,"dec"): marks+=0.5
#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q13(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q14(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q15(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q16(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q17(pagetext):
	"""  	cleaning the station 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
#-----defaults-------------
	marks+=8
	return["Station is orderly",marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]






#below is a template to use for a question
def qNumber(pagetext):
	"""  	A description of the points goes here if there is a need   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


#def nameCheck(pagetext):
#	"""  Reads the names, the plan for all experimetns is that you strip everything of all the names and then make a list of six for the 3 names of the students   """
##-----defaults-------------
#	pagetextOriginal=pagetext
#	student1="Couldnt get names automatically"
#	student2="Couldnt get names automatically"
#	student3="Couldnt get names automatically"

##-----Checking for answers-------------


#	pagetext=retainString.afterBackEnd(pagetext,'the ').strip()
#	#pagetext=retainString.beforeFrontEnd(pagetext,"(2)").strip()	
#	pagetext=pagetext.strip().split("\n")

#	studentNames=pagetext
#	student1=studentNames[0].strip()+" "+studentNames[16].strip() #student 1 
#	student2=studentNames[14].strip()+" "+studentNames[17].strip() #student 1
#	student3=studentNames[15].strip()+" "+studentNames[18].strip() #student 1

#	nostudent="your name your name"
#	if student1.upper().strip()==nostudent.upper().strip(): student1=""
#	if student2.upper().strip()==nostudent.upper().strip(): student2=""
#	if student3.upper().strip()==nostudent.upper().strip():	student3=""


##----------Returning the values----------------
#	return[student1,student2,student3]	#ans is [students answer, marks, for default comment use 1]



