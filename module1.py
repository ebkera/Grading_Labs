#RC Circuits

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
questions.append([4,"(1)","$\\Tau$ = 0.47 s",0.5])#qnum:1
questions.append([4,"(2)","c, a, b",0.5])#qnum:2
questions.append([4,"(3)","a",0.5])#qnum:3
questions.append([4,"(4)","c",0.5])#qnum:4
questions.append([4,"(5)","Imax = 0.015 A, Qmax = 0.007 C",0.5])#qnum:5
questions.append([4,"(6)","Q(t = 1s) = 0.006 C",0.5]) #qnum:6
questions.append([4,"(7)","I (t = 1s) = 0.0018 A",0.5])#qnum:7
questions.append([4,"(8)","Area under I(t) graph = Q(t), answer is 0.006 C",0.5])#qnum:8
questions.append([6,"($\\bullet$)","Check agreement between (5) and (6)",2])#qnum:9
questions.append([6,"(8)","Check that '$\\Tau$ measured' value is equal to 1/C, where C is their fit parameter found in (7). (If not, they probably faked the calculation.)",2])#qnum:10
questions.append([7,"($\\bullet$)","Check agreement (4) to (6)",2])#qnum:11
questions.append([7,"(8)","Check that '$\\Tau$ measured' value is equal to 1/C, where C is their fit parameter found in (7). (If not, they probably faked the calculation.)",2])#qnum:12
questions.append([8,"($\\bullet$)","Check that the VR+ VC graph is a flat horizontal line",1])#qnum:13
questions.append([8,"(5)","Answers: T T F (0.5 each)",1.5])#qnum:14
questions.append([9,"(2)","Answers: a & a",0.5])#qnum:15
questions.append([9,"(3)","Answer: a",0.5]) #qnum:16
questions.append([9,"(4)","Answer: a",0.5]) #qnum:17
questions.append([10,"($\\bullet$)","This measurement requires some thought to execute properly, so check that their graph is indeed an exponential decay, and that their fit parameter A is close to the battery voltage (~1.5 V).",2]) #qnum:18
questions.append([10,"(4)","Check that '$\\Tau$ measured' value is equal to 1/C, where C is their fit parameter found in (7). (If not, they probably faked the calculation)",1])#qnum:19
questions.append([11,"(3)","Answer: 66.7 $\\Omega$",1])#qnum:20
questions.append([11,"(2)","Check that new time constant $\\Tau$ = 0.313 s",1]) #qnum:21
questions.append([11,"(3)","Answer: b",1])#qnum:22
questions.append([12,"(7)","Check for reasonable agreement",2]) #qnum:23
questions.append([13,"($\\bullet$)","Check for completeness",2])#qnum:24
questions.append([14,"(4)","Check for reasonable agreement and qualitatively correct graphs",2]) #qnum:25
questions.append([15,"(5)","Check for reasonable agreement, qualitatively correct graphs, and reasonable fits. Students should lose points if they failed to highlight only the section of the graph corresponding to AFTER the switch was closed!",2])#qnum:26
questions.append([17,"($\\bullet$)","Check for reasonable agreement and qualitatively correct graphs",2]) #qnum:27
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:28

ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","$\\tau$ = 0.47 s"], #Q1
					 ["From Text Field","c, a, b"], #Q2
					 ["From Text Field","a"], #Q3
					 ["From Text Field","c"], #Q4
					 ["From Text Field","I$_{max}$ = 0.015 A, Q$_{max}$ = 0.007 C"], #Q5
					 ["From Text Field","Q (t = 1s) = 0.006 C"], #Q6
					 ["From Text Field","I (t = 1s) = 0.0018 A"], #Q7
					 ["From Text Field","Area under I(t) graph = Q(t) = 0.006 C"], #Q8
					 ["From Text Field","(5) and (6) should agree"], #Q9
					 ["From Text Field","V$_{max}$ should be close to 1.5V. Has not taken the offset into consideration.","$\\tau$=1/C"], #Q10
					 ["From Text Field","There should agreement on (4)-(6)"], #Q11
					 ["From Text Field","$\\tau$=1/C"], #Q12
					 ["From Text Field","the V$_{R}$+ V$_{C}$ graph is a flat horizontal line"], #Q13
					 ["From Text Field","Answers: T T F"], #Q14
					 ["From Text Field","Answers: a \\& a"], #Q15
					 ["From Text Field","Answer: a"], #Q16
					 ["From Text Field","Answer: a"], #Q17
					 ["From Text Field","The graph should be an exponential decay","A$\\approx$1.5"], #Q18
					 ["From Text Field","$\\tau$=1/C","Values don't agree"], #Q19
 					 ["From Text Field","Answer: 66.7 $\\Omega$"], #Q20
 					 ["From Text Field","New time constant $\\tau$=0.313"], #Q21
 					 ["From Text Field","Answer: b"], #Q22
 					 ["From Text Field","Values don't agree"], #Q23
 					 ["From Text Field","Values don't agree"], #Q24
 					 ["From Text Field","The graphs don't seem to be qualitatively correct"], #Q25
 					 ["From Text Field","The graphs don't seem to be qualitatively correct","The fit should only take into account the section of the graph corresponding to AFTER the switch was closed"], #Q26
 					 ["From Text Field","The graphs don't seem to be qualitatively correct"], #Q27
					 ["From Text Field","The station was not very clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q28

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
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


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
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


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
#	pagetext=retainString.afterBackEnd(pagetext,"y - component")
#	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


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

def q18(pagetext):
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

def q19(pagetext):
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

def q20(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q21(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q22(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q23(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q24(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q25(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q26(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q27(pagetext):
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
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1

def q28(pagetext):
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
