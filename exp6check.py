#--------------Amperes Law

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
questions.append([5,"(1)","$\\mu_0$I = 3.77 x 10$^{-4}$ Tm",2])#qnum:1
questions.append([5,"(9)","Answer: B, Reason should mention direction and density of field lines",2])#qnum:2
questions.append([6,"($\\bullet$)","Check for agreement and qualitatively correct graph",2])#qnum:3
questions.append([7,"($\\bullet$)","Look for reasonable correct explanation",2])#qnum:4
questions.append([8,"(4)","Ans:No- exp evidence:(area != 0) and parallel component’s role in B . dl integral",2])#qnum:5
questions.append([9,"(3)","Ans:0- the two currents are equal and in opp directions within the enclosed area.",2]) #qnum:6
questions.append([9,"(7)","Answer Yes: area < estimated error",1])#qnum:7
questions.append([9,"(8)","Answer Yes: area < estimated error",1])#qnum:8
questions.append([9,"($\\bullet$)","Look for qualitatively correct graph",2])#qnum:9
questions.append([10,"(4)","Answer should be around 2 times the single coil result",2])#qnum:10
questions.append([11,"(6)","Similar to single coil, explanation: Ienclosed is the same as the single coil",2])#qnum:11
questions.append([11,"($\\bullet$)","Check for 2 graphs, similar areas",2])#qnum:12
questions.append([12,"($\\bullet$)","Direction of enclosed current and the idea of net enclosed current",4])#qnum:13
questions.append([13,"($\\bullet$)","Reasonable graph (proves that they actually did the measurement!)",2])#qnum:14
questions.append([13,"(15)","Answer should be same as single coil, small track.",2])#qnum:15
questions.append([13,"(18)","Answer: No! Path independance!",2]) #qnum:16
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:17

ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","$\\mu_0$I = 3.77 x 10$^{-4}$ Tm"], #Q1
					 ["From Text Field","Answer: B","Direction and density of field lines are wrong"], #Q2
					 ["From Text Field","Values don't agree","Graph is not qualitatively correct"], #Q3
					 ["From Text Field","Explanation is not correct"], #Q4
					 ["From Text Field","Answer: No, $\\vec{B}$ should be parallel to $\\vec{dl}$. If perpendicular we will have zero since $\\vec{B} \\cdot \\vec{dl}=0$"], #Q5
					 ["From Text Field","Answer: Zero"], #Q6
					 ["From Text Field","Answer: Yes"], #Q7
					 ["From Text Field","Answer: Yes"], #Q8
					 ["From Text Field","Graph is not qualitatively correct"], #Q9
					 ["From Text Field","Answer should be around 2 times the single coil result"], #Q10
					 ["From Text Field","Answer should be similar to single coil","I$_{enclosed}$ is the same as the single coil result"], #Q11
					 ["From Text Field","The two graphs should have similar areas"], #Q12
					 ["From Text Field","Should mention of direction of enclosed current and the idea of net enclosed current"], #Q13
					 ["From Text Field","Graphs are not reasonable"], #Q14
					 ["From Text Field","Answer should be same as single coil, small track."], #Q15
					 ["From Text Field","Answer: No. Path independance!"], #Q16
					 ["From Text Field","The station was not clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q17

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

