import PyPDF2
import subprocess
import os
import re #importing regualr expressions

from manipulateString import *
#open doc and read 

#[expNum][questionNum][Option0,Option1,...]  
#remember to have the second entry be the generic one 

questions=[] #pagenumber, step number, description of marks, marks to be given in full
questions.append([3,"(100)","Names Page",100]) #This is inthere so that we can revert to this during debugging and also so that the list is 
questions.append([4,"(9)","Check that their measured resistances are close to 3 Ω, 5.6 Ω and 10 Ω (to within a few %).",2])#qnum:1
questions.append([5,"($\\bullet$)","Check that their value is not far off.",1])#qnum:2
questions.append([5,"(6)","Answer is “Yes”",1])#qnum:3
questions.append([6,"(3)","Check for completeness",0.5])#qnum:4
questions.append([6,"(4)","Check for completeness",0.5])#qnum:5
questions.append([6,"($\\bullet$)","battery’s internal resistance < 1 Ω",1]) #qnum:6
questions.append([7,"(1)","Req aprx 18.6Ω within a few %",2])#qnum:7
questions.append([7,"(6)","Check agreement between (8) and (9)",2])#qnum:8
questions.append([8,"(10)","Check agreement between (8) and (9)",2])#qnum:9
questions.append([8,"(1)","on right: Check that Req is the sum of the reciprocals of the 3 parallel resistances (~1.63 Ω)",2])#qnum:10
questions.append([9,"($\\bullet$)","Check agreement between (7) and (8)",2])#qnum:11
questions.append([10,"(2)","on right: Answer “Resistance.”",2])#qnum:12
questions.append([10,"(4)"," Value should be about 5.6 Ω",1])#qnum:13
questions.append([10,"(5)","Answer “Yes”",1])#qnum:14
questions.append([11,"(6)","No, since the graph is non-linear",2])#qnum:15
questions.append([11,"(7)","Be lenient on the grading here. A dynamite, but unlikely answer: “As the temperature increases, the collision time between electrons and ions decreases, which increases the resistance.",2]) #qnum:16
questions.append([12,"(8)","Check that the potentials for the 3 Ω is positive, while the potentials for the 10 Ω and V2 are negative",3]) #qnum:17
questions.append([12,"($\\bullet$)","Also check that the Total is < 0.02 V",1]) #qnum:18
questions.append([13,"(12)","Check that the potentials for the 3 Ω and 5.6 Ω are negative, while the potential for V1 is positive. Also check that the Total is < 0.02 V or so",3])#qnum:19
questions.append([13,"(3)","on right: Check that I1 - I2 - I3 < 0.02 A or so",1])#qnum:20
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:21


ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","3 $\\Omega$, 5.6 $\\Omega$ and 10 $\\Omega$"], #Q1
					 ["From Text Field","Values are off"], #Q2
					 ["From Text Field","Answer is `Yes'"], #Q3
					 ["From Text Field","Answers not complete"], #Q4
					 ["From Text Field","Answers not complete"], #Q5
					 ["From Text Field","Battery's internal resistance $<$ 1 $\\Omega$"], #Q6
					 ["From Text Field","Answers not complete","Req aprox 18.6 $\\Omega$"], #Q7
					 ["From Text Field","Computed current and calculated current should be similar"], #Q8
					 ["From Text Field","(8) and (9) should agree"], #Q9
					 ["From Text Field","Req is the sum of the reciprocals of the 3 parallel resistances ($\\cong$1.63 $\\Omega$)"], #Q10
					 ["From Text Field","(8) and (7) should agree"], #Q11
					 ["From Text Field","Answer: `Resistance'"], #Q12
					 ["From Text Field","Value should be about 5.6 $\\Omega$"], #Q13
					 ["From Text Field","Answer: `Yes'"], #Q14
					 ["From Text Field","No, since the graph is non-linear"], #Q15
					 ["From Text Field","As the temperature increases, the collision time between electrons and ions decreases, which increases the resistance"], #Q16
					 ["From Text Field","3 $\\Omega$ is positive, while the potentials for the 10 $\\Omega$ and V2 are negative"], #Q17
					 ["From Text Field","Total is $<$ 0.02 V"], #Q18
					 ["From Text Field","Potentials for the 3 $\\Omega$ and 5.6 $\\Omega$ are negative, while the potential for V1 is positive. Total is $<$ 0.02 V or so"], #Q19
 					 ["From Text Field","I1 - I2 - I3 $<$ 0.02 A"], #Q20
					 ["From Text Field","The station was not very clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q27

def nameCheck(pagetext):
	"""  Reads the names, the plan for all experimetns is that you strip everything of all the names and then make a list of six for the 3 names of the students   """
#-----defaults-------------
	pagetextOriginal=pagetext
	

#-----Checking for answers-------------

	pagetext=retainString.afterBackEnd(pagetext,"page.").strip()
	pagetext=retainString.beforeFrontEnd(pagetext,"(2)").strip()	
	pagetext=pagetext.strip().split("\n")
	studentNames=pagetext

	#all 3 students present
	if len(studentNames)==12:
		try:student1=studentNames[0].strip()+" "+studentNames[10].strip() #student 1 
		except:student1=""	
		try:student2=studentNames[1].strip()+" "+studentNames[11].strip() #student 1 
		except:student2=""	
		try:student3=studentNames[2].strip()+" "+studentNames[9].strip() #student 1 
		except:student3=""

	#2 students present
	elif len(studentNames)==10:
		try:student1=studentNames[0].strip()+" "+studentNames[9].strip() #student 1 
		except:student1=""	
		try:student2=studentNames[1].strip()+" "+studentNames[8].strip() #student 1 
		except:student2=""	
		try:student3=studentNames[100].strip()+" "+studentNames[100].strip() #student 1 
		except:student3=""

	else:
		student1="Couldnt get names automatically"
		student2="Couldnt get names automatically"
		student3="Couldnt get names automatically"

	#pagetext=retainString.afterBackEnd(pagetextOriginal,'#3').strip()
	#pagetext=retainString.beforeFrontEnd(pagetext,"Please").strip()
	#pagetext=pagetext.strip().split("\n")

	## we dont have enough data to make up the 3rd person so might have to edit in future itereations
	#if len(studentNames)==2:
	#	student1=studentNames[1]+" "+pagetext[0]
	#	student2=studentNames[0]+" "+pagetext[1]
	#elif len(studentNames)==1:
	#	student1=studentNames[0]+" "+pagetext[0]
	#	student2=""

	#student3=""

# not really needed till now but good to keep around since it might be needed when surguei implements something else and suddenly the your name thing comes into play
	#if len(namesPageText)==5:
	#	student1=student1.strip()+" "+namesPageText[2].strip()
	#	student2=namesPageText[0].strip()+" "+namesPageText[3].strip()
	#	student3=namesPageText[1].strip()+" "+namesPageText[4].strip()
	#elif len(namesPageText)==3: #sometimes the students erase the "your name" part in the empty boxes
	#	student1=student1.strip()+" "+namesPageText[1].strip()
	#	student2=namesPageText[0].strip()+" "+namesPageText[2].strip()
	#	student3="your name your name"

	#if student1=="your name your name": student1=""   #getting rid of unentered names
	#if student2=="your name your name": student2=""
	#if student3=="your name your name": student3=""


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

