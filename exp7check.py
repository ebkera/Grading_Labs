#--------------EM Inducion

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
questions.append([5,"($\\bullet$)","Look for some evidence that they were doing some real testing",2])#qnum:1
questions.append([6,"(2)","negative",0.5])#qnum:2
questions.append([6,"(3)","a",0.5])#qnum:3
questions.append([6,"(4)","increasing",0.5])#qnum:4
questions.append([6,"(5)","c",0.5])#qnum:5
questions.append([6,"(6)","CCW",0.5])#qnum:6
questions.append([6,"(7)","negative",0.5])#qnum:7
questions.append([7,"(9)","Induced EMF should be positive",2])#qnum:8
questions.append([7,"(10)","Induced EMF=0 when magnet becomes stationary ( flux is no longer changing in time)",1])#qnum:9
questions.append([8,"(12)","positive",0.5])#qnum:10
questions.append([8,"(13)","a",0.5])#qnum:11
questions.append([8,"(14)","decreasing",0.5])#qnum:12
questions.append([8,"(15)","a",0.5])#qnum:13
questions.append([8,"(16)","CW",0.5])#qnum:14
questions.append([8,"(17)","positive",0.5])#qnum:15
questions.append([9,"($\\bullet$)","EMF goes negative and then positive",1])#qnum:16
questions.append([9,"($\\bullet$)","2-stage process(As the north pole approaches, the increasing positive (positive flux:field pointing away) flux induces CCW current:+ve EMF. As the south pole recedes, the decreasing positive magnetic flux induces a CW current:-ve EMF'",2]) #qnum:17
questions.append([10,"(1)","D",1])#qnum:18
questions.append([11,"(1)","Answer: Away",1])#qnum:19
questions.append([11,"(4)","Regardless of their prediction in #2, they should be able to explain why there is no induced EMF – there is nothing changing in time",1])#qnum:20
questions.append([12,"(3)","Away",0.5])#qnum:21
questions.append([12,"(4)","Away",0.5])#qnum:22
questions.append([12,"(5)","CCW",0.5])#qnum:23
questions.append([12,"(6)","CW",0.5])#qnum:24
questions.append([12,"(7)","Look for a well-justified prediction, even if it's not 100% correct.",1])#qnum:25
questions.append([13,"($\\bullet$)","Check that the value in (11) is approximately double the value in (9)",1])#qnum:26
questions.append([14,"($\\bullet$)","Look for a well-justified prediction, even if it's not 100% correct",0.5]) #qnum:27
questions.append([15,"($\\bullet$)","Look for a well-justified prediction, even if it's not 100% correct",0.5]) #qnum:28
questions.append([16,"(3)","They should notice that when the input voltage is at a maximum, the induced EMF is zero",1]) #qnum:29
questions.append([16,"(4)","When input voltage goes +ve  to -ve, induced EMF is at a +ve max, cuz flux is changing rapidly, Delta Phi < 0 (flux decreasing), the induced EMF will be +ve",2]) #qnum:30
questions.append([18,"(6)","This time, the magnetic field is constant, but we are changing the angle Theta. In either case, that will yield a change in ",2])#qnum:31
questions.append([19,"(3)","close to zero",0.5]) #qnum:32
questions.append([19,"(4)","extreme",0.5]) #qnum:33
questions.append([19,"(5)","Again, they need to justify their results here and compare with their prediction",1])#qnum:34
questions.append([22,"(6)","r is close to 0.024m",0.5]) #qnum:35
questions.append([22,"(11)","close to 20 Gauss",0.5])#qnum:36
questions.append([23,"($\\bullet$)","Check for agreement between values in (17) and (18) and check the calculation for the % difference",1]) #qnum:37
questions.append([23,"(19)","Check for reasonable answer",1])#qnum:38
questions.append([0,"($\\bullet$)","Did the students check out properly",8]) #qnum:39

ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
					 ["From Text Field","Explanations are wrong"], #Q1
					 ["From Text Field","Negative"], #Q2
					 ["From Text Field","Answer: a"], #Q3
					 ["From Text Field","Increasing"], #Q4
					 ["From Text Field","Answer: c"], #Q5
					 ["From Text Field","CCW"], #Q6
					 ["From Text Field","Negative"], #Q7
					 ["From Text Field","Induced EMF should be positive"], #Q8
					 ["From Text Field","Induced EMF=0 when magnet becomes stationary ( flux is no longer changing in time)"], #Q9
					 ["From Text Field","Positive"], #Q10
					 ["From Text Field","Answer: a"], #Q11
					 ["From Text Field","Decreasing"], #Q12
					 ["From Text Field","Answer: a"], #Q13
					 ["From Text Field","CW"], #Q14
					 ["From Text Field","Positive"], #Q15
					 ["From Text Field","EMF goes negative and then positive"], #Q16
					 ["From Text Field","Think and a 2-stage process, A north pole approaching the coil, and a south pole receding from the opposite side of the coil"], #Q17
					 ["From Text Field","Answer: d"], #Q18
					 ["From Text Field","Answer: Away"], #Q19
 					 ["From Text Field","No induced EMF - there is nothing changing in time"], #Q20
 					 ["From Text Field","Answer: Away"], #Q21
 					 ["From Text Field","Answer: Away"], #Q22
 					 ["From Text Field","CCW"], #Q23
 					 ["From Text Field","CW"], #Q24
 					 ["From Text Field","Predictions are wrong"], #Q25
 					 ["From Text Field","Value for (11) is approximately double the value for (9)"], #Q26
 					 ["From Text Field","Predictions are wrong"], #Q27
					 ["From Text Field","Predictions are wrong"], #Q28
					 ["From Text Field","When the input voltage is at a maximum, the induced EMF is zero"], #Q29
					 ["From Text Field","When the input voltage passes from positive to negative, the induced EMF is at a positive maximum, because the flux is changing rapidly here. Also, since  $\\Delta$ $\\phi<=0$ (flux decreasing), the induced EMF will be positive"], #Q30
					 ["From Text Field","This time, the magnetic field is constant, but we are changing the angle $\\theta$. In either case, that will yield a change in $\\phi$"], #Q31
					 ["From Text Field","Close to zero"], #Q32
					 ["From Text Field","Extreme"], #Q33
					 ["From Text Field","Predictions are wrong"], #Q34
					 ["From Text Field","Radius is close to 0.024m"], #Q35
					 ["From Text Field","close to 10 Gauss"], #Q36
					 ["From Text Field","There should be reasonable agreement between values in (17) and (18)"], #Q37
					 ["From Text Field","Explanations are not reasonable"], #Q38
					 ["From Text Field","The station was not very clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]] #Q39


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
	"""  	The first experiemnt where they have to do random things to come up with how magnetic fields create an EMF   """
#-----defaults-------------
	marks=2
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
	pagetext=retainString.afterBackEnd(pagetext,"less than one second!").strip().strip("\n").strip().split("\n")
	#studentsAnswer=retainString.beforeFrontEnd(pagetext,"(2)")
	studentsAnswer=pagetext[0]
	if checkString.isStringNegative(studentsAnswer): marks+=0.5

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
	pagetext=retainString.afterBackEnd(pagetext,"field through the coil?").strip().strip("\n").strip().split("\n")
	studentsAnswer=pagetext[0]#getting the first string
	if len(studentsAnswer)==8:
		studentsAnswer=studentsAnswer[0]   #getting the first char which is the answer
		if checkString.containsString(studentsAnswer,"a"): marks+=0.5
	elif len(studentsAnswer)==7: 
		studentsAnswer="Not answered"

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
	pagetext=retainString.afterBackEnd(pagetext,"a/b/c/d").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"increasing/decreasing")
	if checkString.containsString(studentsAnswer,"increasing"): marks+=0.5

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
	pagetext=retainString.afterBackEnd(pagetext,"point?").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"a/b/c/d")
	if checkString.containsString(studentsAnswer,"c"): marks+=0.5

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
	pagetext=retainString.afterBackEnd(pagetext,")?").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"CW/CCW")
	if checkString.regExSearch(studentsAnswer,"ccw"): marks+=0.5

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
	pagetext=retainString.afterBackEnd(pagetext,"terminal").strip().strip("\n").strip()
	pagetext=retainString.afterBackEnd(pagetext,")").strip().strip("\n").strip()
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"pos/neg")
	if checkString.regExSearch(studentsAnswer,"neg"): marks+=0.5

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

def q29(pagetext):
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

def q30(pagetext):
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

def q31(pagetext):
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

def q32(pagetext):
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

def q33(pagetext):
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

def q34(pagetext):
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

def q35(pagetext):
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

def q36(pagetext):
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

def q37(pagetext):
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

def q38(pagetext):
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

def q39(pagetext):
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


