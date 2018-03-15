import PyPDF2
import subprocess
import os
import re #importing regualr expressions

from manipulateString import *
#open doc and read 

questions=[] #pagenumber, step number, description of marks, marks to be given in full
questions.append([100,"(100)","Deafult",100]) #This is inthere so that we can revert to this during debugging and also so that the list is 
questions.append([4,"(5)","Attracted to rod is correct. No multiple answers",2])#qnum:1
questions.append([4,"(9)","Answer is B",1])#qnum:2
questions.append([5,"(4)","'Moves away from vertical' should be 'True'",1])#qnum:3
questions.append([5,"(5)","'False', 'False', 'True', 'True'",1])#qnum:4
questions.append([7,"(9)","Answers: E, G, H, I",1])#qnum:5
questions.append([7,"(10)","Answers: 0, 0, +, +",1]) #qnum:6
questions.append([9,"(1)","Small field corresponds to a dim arrow",2])#qnum:7
questions.append([9,"(3)","E-field arrows reversed direction.",1])#qnum:8
questions.append([9,"(5)","Answer: 'E = (9x10^{-9})(1x10^{-9})/(1.5)^2 = 4.0 N/C'",2])#qnum:9
questions.append([10,"($\\bullet$)","Graph should have 1/r^2 dependance",1])#qnum:10
questions.append([10,"(3)","Check that A = 9.0 (to within a few %)",2])#qnum:11
questions.append([10,"(4)","A = kq, or 9.0 N m2/C (don't worry about units)",2])#qnum:12
questions.append([11,"(2)","A to left, B is 0 and C to right. Check for reasonable justifications.",2])#qnum:13
questions.append([11,"(3)","A to left, B to right and C to left. Check for reasonable justifications.",2])#qnum:14
questions.append([12,"(1)","Check for complete calculations. Full credit only if work is completely shown and results",1])
questions.append([12,"(2)","Check for complete calculations. Full credit only if work is completely shown and results",1])
questions.append([12,"(3)","yield 37.9 N/C, 18° One point for each",2]) #qnum:17
questions.append([13,"($\\bullet$)","Check for a reasonable fit (Root MSE < 0.2 or so)",1])#qnum:18
questions.append([13,"(4)","check that n = 3.",1])#qnum:19
questions.append([14,"(1)","We want to see evidence that the students are thinking, so be generous with partial credit.\nIdeally, an answer would say something like 'As you get farther away from this charge distribution, the charges seem more and more as if they are at the same location.\nSince the net charge is zero, the field will be smaller than that of a single charge at large distances (r >>d).",2])#qnum:20
questions.append([15,"(3)","Check for a reasonable fit with n = 1",1])
questions.append([15,"(4)","A reasonable answer: 'When you are close to the line, the ends are far away, and so the line looks infinite.\nWhen you are far away, the charge configuration looks less like a line, and more like a point,\nso you would expect the field to drop more rapidly when you are far away, which agrees with the graph above.'",1])
questions.append([16,"(1)","Check their calculation: λ = (# Charges in 4 meters)*(1e-9 C)/(4 m)",1]) #qnum:23
questions.append([16,"(2)","Check their work. Sample response for A = 120: 'A = 2k \lambda 120 = 2 (9x10^9) \lambda\nlambda = 6.7 x 10^-9 C/m",2]) #qnum:24
questions.append([16,"(3)","Check their calculation, and that their % difference is less than 10%.",1])
questions.append([16,"(4)","Sample response: 'Again, the likeliest reason for the discrepancy, apart from measurement uncertainty in properly positioning the sensor,\nis the fact that Gauss's law assumes an infinite line of charge, whereas our line is most certainly finite'",1])
questions.append([0,"($\\bullet$)","Did the students check out properly",4]) #qnum:27


#[expNum][questionNum][Option0,Option1,...]  
#remember to have the second entry be the generic one 
ExplanationOptions=[["From Text Field","Change to General"], 
					 ["From Text Field","Change to General"]]


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

