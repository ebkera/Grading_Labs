#--------------Biot Savart

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
questions.append([5,"(3)","Answer: C",2])#qnum:1
questions.append([6,"($\\bullet$)","Slope of graph is ~1.71 x 10-3, and mu_0 = 1.26 x 10–6 Tm/A is correct to within ~5%",4])#qnum:2
questions.append([7,"($\\bullet$)","Largest magnitude at 0.17 m, trailing off on either side (~ 1/r)",2])#qnum:3
questions.append([8,"(6)","Magnetic field is opposite to the arrows on the sensor.",2])#qnum:4
questions.append([8,"($\\bullet$)","Agreement between calculated value and measured value for magnetic field",2]) #qnum:5
questions.append([8,"(8)","Answer: 3",2])#qnum:6
questions.append([8,"(9)","Check agreement",2])#qnum:7
questions.append([9,"(10)","Answer: B -Check for reasonable explanation, which should include: “The weakening of the field away from center is represented by the field lines spreading apart,” or something similar.",1])#qnum:8
questions.append([9,"($\\bullet$)","Radial field should be small compared to axial (“True”)",1])#qnum:9
questions.append([10,"(1)","Answer: B",1])#qnum:10
questions.append([10,"(2)","Answer: 1",1])#qnum:11
questions.append([11,"($\\bullet$)","3 curves on graph, one for each coil, and then the superposition",2])#qnum:12
questions.append([12,"($\\bullet$)","T/F Questions: T T T T F T T",2])#qnum:13
questions.append([12,"(1)","Answer: A",1])#qnum:14
questions.append([12,"(2)","Answer: 2",1]) #qnum:15
questions.append([13,"($\\bullet$)","3 graphs – 2 individual, one superposition",2]) #qnum:16
questions.append([15,"($\\bullet$)","2 curves, one for parallel components and one for perpendicular",2]) #qnum:17
questions.append([15,"($\\bullet$)"," T/F Questions: F T F T F T T T (be generous with partial credit)",2]) #qnum:18
questions.append([16,"(4)","Extra Credit: Coil was improperly alligned (2Pts)",0])#qnum:19
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:20

ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","Answer: C"], #Q1
					 ["From Text Field","Slope of right hand graph is $\\approx$1.71 x 10$^{-6}$","$\\mu_{0}$ is off","$\\approx$5\\% ($\\mu_{0}$ = 1.26 x 10$^{-6}$ Tm/A)"], #Q2
					 ["From Text Field","Graph should have largest magnitude at 0.17 m, trailing off on either side ($\\approx$ 1/r)"], #Q3
					 ["From Text Field","The magnetic field is in the opposite direction to the arrows on the sensor"], #Q4
					 ["From Text Field","There should be agreement between calculated and measured values for B field"], #Q5
					 ["From Text Field","Answer: 3"], #Q6
					 ["From Text Field","Should have agreement between values"], #Q7
					 ["From Text Field","The weakening of the field away from center is represented by the field lines spreading apart"], #Q8
					 ["From Text Field",'Radial field should be small compared to axial (``True")'], #Q9
					 ["From Text Field","Answer: B"], #Q10
					 ["From Text Field","Answer: 1"], #Q11
					 ["From Text Field","Superposition is off"], #Q12
					 ["From Text Field","Answers: T T T T F T T"], #Q13
					 ["From Text Field","Answer: A"], #Q14
					 ["From Text Field","Answer: 2"], #Q15
					 ["From Text Field","Superposition is off"], #Q16
					 ["From Text Field","Prallel component curve is off","Perpendicular component is off"], #Q17
					 ["From Text Field","Answers: F T F T F T T T"], #Q18
					 ["From Text Field","Extra Credit Points","Extra Credit: Coil was improperly alligned"], #Q19
					 ["From Text Field","The station was not clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q20

def nameCheck(pagetext,students):
	"""  Reads the names, the plan for all experiments is that you strip everything of all the names and then make a list of six for the 3 names of the students   """
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
	"""  	Extra Credit   """
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

def q20(pagetext):
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
