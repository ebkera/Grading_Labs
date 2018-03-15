import PyPDF2
import subprocess
import os
import re #importing regualr expressions

from manipulateString import *
#open doc and read 

#[expNum][questionNum][Option0,Option1,...]  
#remember to have the second entry be the generic one 

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



ExplanationOptions=[["From Text Field","The first line for index purposes","Q1"], #JUst the first line
						 ["From Text Field","Attracted to rod is correct. No multiple answers","Q1"], #Q1
						 ["From Text Field","Answer is B","Q2"], #Q2
						 ["From Text Field","'Moves away from vertical","Q3"], #Q3
						 ["From Text Field","'False', 'False', 'True', 'True'","Q2"], #Q4
						 ["From Text Field","Answers: E, G, H, I","Q3"], #Q5
						 ["From Text Field","Answers: 0, 0, +, +","Q2"], #Q6
						 ["From Text Field","Small field corresponds to a dim arrow","Q3"], #Q7
						 ["From Text Field","E-field arrows reversed direction","Q2"], #Q8
						 ["From Text Field","Answer: '$E = (9\\times{10^{-9}})(1\\times{10^{-9}})/(1.5)^{2} = 4.0 N/C$","Units are wrong"], #Q9
						 ["From Text Field","Graph should have $1/r^2$ dependance","You need to measure the E-field using the E-field sensor","Bad data points therefore you have a bad fit", "question not answered","No fit done"], #Q10
						 ["From Text Field","'A' should be $\\cong$ 9.0","Question has not been answered"], #Q11
						 ["From Text Field","A = kq, or $9.0 N m^2/C$","Q2"], #Q12
						 ["From Text Field","A to left, B is 0 and C to right","A is wrong", "B is wrong","C is wrong"], #Q13
						 ["From Text Field","A to left, B to right and C to left","A is wrong", "B is wrong","C is wrong"], #Q14
						 ["From Text Field","Complete Calculations are needed for full marks","No units", "The x direction is wrong", "The y direction is wrong"], #Q15
						 ["From Text Field","Complete Calculations are needed for full marks","No units", "The x direction is wrong", "The y direction is wrong"], #Q16
						 ["From Text Field","Answers are: $37.9 N/C, 18^{\\circ}$", "The Magnitude is wrong", "The angle is wrong","The magnitude and the angle is wrong"], #Q17
						 ["From Text Field","The fit is not reasonable","You need to measure the E-field using the E-field sensor","Bad data points therefore you have a bad fit"], #Q18
						 ["From Text Field","n = 3","Q2"], #Q19
						 ["From Text Field","As you get further away, charges seem to be from the same location","Q2"], #Q20
						 ["From Text Field","The fit is not reasonable","Question has not been answered. n=?","n should be an integer","n=1","Question has not been answered. Fit?", "Question has not been answered"], #Q21
						 ["From Text Field","When you are closer the line looks infinite, and like a point from further away","Q2"], #Q22
						 ["From Text Field"," $\\lambda$ = (\\# Charges in 4 meters)*(1e$^{-9}$ C)/(4 m)","Q2"], #Q23
						 ["From Text Field","$\\lambda$ = 6.7 x $10^-9$ C/m","Q2"], #Q24
						 ["From Text Field","Percentage difference is a bit too high","Q2"], #Q25
						 ["From Text Field","Gauss Law assumes an infinite line of charge. Ours is not","Q2"], #Q26
						 ["From Text Field","The station was not very clean. Remember that you get a lot of points for keeping you station just the way you found it","Q3"]], #Q27


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
	pagetext=retainString.afterBackEnd(pagetext,"from vertical")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"(3)")
	studentsAnswer=studentsAnswer.strip().split("\n")

	if len(studentsAnswer)>1:
		if checkString.isStringFalse(studentsAnswer[0]) and checkString.isStringTrue(studentsAnswer[1]):
			marks+=1
			studentsAnswer=studentsAnswer[0]+", "+studentsAnswer[1]
		else: pass
	else: 
		if checkString.isStringTrue(studentsAnswer[0]):
			marks+=1
			studentsAnswer=studentsAnswer[0]
		else: pass

#----------Returning the values----------------
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q4(pagetext):
	pagetext=retainString.afterBackEnd(pagetext,"possesses charge with the same")
	pagetext=retainString.beforeFrontEnd(pagetext,"(5)")
	answers=pagetext.strip().split("\n") #stripping is very important to get the right positions
	ans=""
	if checkString.isStringFalse(answers[0]):ans+="C"
	else:ans+="W"
	if checkString.isStringFalse(answers[1]):ans+="C"
	else:ans+="W"	
	if checkString.isStringTrue(answers[2]):ans+="C"
	else:ans+="W"	
	if checkString.isStringTrue(answers[3]):ans+="C"
	else:ans+="W"

	return[float(ans.count("C"))*0.25, answers[0]+", "+answers[1]+", "+answers[2]+", "+answers[3]+" ("+ans+")"]

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

def q7and8(pagetext):
	pagetext=retainString.afterBackEnd(pagetext,"changing the sign of the charge:")
	pagetext=retainString.beforeFrontEnd(pagetext,"(5)")
	pagetext=pagetext.replace('\n', ' ') #so that we dont get a lot of lines
	checkforq7=["bold","light","transparen","dim","dark","fade","fading","colour","color","bright","opacity","opaque"]
	checkforq8=["reverse","opposite","point","direction","towards","away","face"]
	return [pagetext,checkString.containsString(pagetext,checkforq7),checkString.containsString(pagetext,checkforq8)]

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
	"""  	1 point for the entire quenstion """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

	pagetext=retainString.afterBackEnd(pagetext,"and don't forget the u\nnits:")
	pagetext=retainString.beforeFrontEnd(pagetext,"(6)")
	studentsAnswer=pagetext.replace('\n', ' ')

	if checkString.containsString(studentsAnswer,"4") and (checkString.containsString(studentsAnswer,["N/C","V/m"])):marks+=2

	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q10(pagetext):
	"""  	1 point for the entire quenstion """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	
	pagetext=retainString.afterBackEnd(pagetext,"Root MSE")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Data")

	studentsAnswer=studentsAnswer.strip()

	if len(studentsAnswer)>7:comment=5
	elif studentsAnswer=="": comment=4
	elif abs(float(studentsAnswer))==0.0:  comment=2 
	elif abs(float(studentsAnswer))>=0.500: comment=3
	else: marks+=1

	studentsAnswer="RMS: "+studentsAnswer

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q11(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------

	pagetext=retainString.afterBackEnd(pagetext,"A =")
	pagetext=retainString.beforeFrontEnd(pagetext,"(4)")
	studentsAnswer=pagetext.strip()

	if studentsAnswer=="": comment=2
	elif float(studentsAnswer)-9.0>=0.5: pass #the answer should be less than 0.5 in difference aatleast
	else: marks+=2


#----------Returning the values----------------
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q12(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext



#-----Checking for answers-------------

	pagetext=retainString.afterBackEnd(pagetext,"you know?")
	studentsAnswer=pagetext

	checkfor=["9","9.0"] # possible values that the student might give.. should be 9

	if (checkString.containsString(studentsAnswer,"k") and checkString.containsString(studentsAnswer,"q")) or checkString.containsString(studentsAnswer,checkfor): marks+=2

#----------Returning the values----------------
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]

def q13(pagetext):
	pagetext=retainString.afterBackEnd(pagetext,", as shown here:")
	pagetext=retainString.beforeFrontEnd(pagetext,"Prediction")
	answers=pagetext.strip().split("\n")
	#print(answers)
	wrong=["up","down"]
	ans1=["left","l"]
	ans2=["zero","0","o"]
	ans3=["right","r"]

	ans=""

	if len(answers)==0:pagetext="Question was not answered"
	elif len(answers)==1: pagetext="Answer not read from file"
	elif len(answers)<=2:
		if (checkString.containsString(answers[0],ans1)): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans2) and not checkString.containsString(answers[1],wrong) ): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans3)): ans+="C"
		else: ans+="W"
	else: 
		if (checkString.containsString(answers[0],ans1)): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans2) and not checkString.containsString(answers[1],wrong) ): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[2],ans3)): ans+="C"
		else: ans+="W"

#If the student does not have full marks then gets 0.7 each
	if ans.count("C")==3: marks=float(2)
	else:marks=float(ans.count("C"))*0.7
	pagetext=pagetext.replace('\n', ' ')
	return[pagetext+" ("+ans+")", marks, 1]


def q14(pagetext):
	pagetext=retainString.afterBackEnd(pagetext,"Again,")
	pagetext=retainString.beforeFrontEnd(pagetext,"Prediction")
	answers=pagetext.strip().split("\n")
	wrong=["up","down"]
	ans1=["left","l"]
	ans2=["right","r"]
	ans3=["left","l"]

	answers=[answers[len(answers)-3],answers[len(answers)-2],answers[len(answers)-1]] # The three answers

	ans=""

	if len(answers)==0:pagetext="Question was not answered"
	elif len(answers)==1: pagetext="Answer not read from file"
	elif (len(answers[0])>7 or len(answers[1])>7 or len(answers[2])>7):pagetext="Answer not read from file"

	elif len(answers)<=2:
		if (checkString.containsString(answers[0],ans1)): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans2) and not checkString.containsString(answers[1],wrong) ): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans3)): ans+="C"
		else: ans+="W"
		pagetext=answers[0]+" "+answers[1]+" "+answers[2]

	else: 
		if (checkString.containsString(answers[0],ans1)): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[1],ans2) and not checkString.containsString(answers[1],wrong) ): ans+="C"
		else: ans+="W"
		if (checkString.containsString(answers[2],ans3)): ans+="C"
		else: ans+="W"
		pagetext=answers[0]+" "+answers[1]+" "+answers[2]
	

#If the student does not have full marks then gets 0.7 each
	if ans.count("C")==3: marks=float(2)
	else:marks=float(ans.count("C"))*0.7
	pagetext=pagetext.replace('\n', ' ')
	return[pagetext+" ("+ans+")", marks, 1]


def q15(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"(3)")
	studentsAnswer1=studentsAnswer

	xMagnitude=["36"]
	yMagnitude=["0"]
	units=["N/C","V/m"]


#0------for teh positive charge------------------------------------------------
#CHECKING FOR UNITS
	if (checkString.containsString(studentsAnswer,units)): marks+=0.5
	else: comment=2

#CHECKING X COMPONENT
	if (checkString.containsString(studentsAnswer,xMagnitude)): marks+=0.25
	else: comment=1

#CHECKING Y COMPONENT
	pagetext=retainString.afterBackEnd(pagetext,"36")
	if (checkString.containsString(studentsAnswer,yMagnitude)): marks+=0.25
	else: comment=1	

	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

#0------for teh negative charge------------------------------------------------
	pagetext=pagetextOriginal


#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"(2)")
	studentsAnswer2=studentsAnswer

	xMagnitude=["0"]
	yMagnitude=["12"]

	pagetextList=studentsAnswer.strip().split("\n")

#CHECKING FOR UNITS
	if (checkString.containsString(studentsAnswer,units)): marks+=0.5
	else: comment=2

#CHECKING X COMPONENT
	if (checkString.containsString(pagetextList[0],xMagnitude)): marks+=0.25
	else: comment=1

#CHECKING Y COMPONENT
	if (checkString.containsString(studentsAnswer,yMagnitude)): marks+=0.25
	else: comment=1	

	studentsAnswer=studentsAnswer1+"; "+studentsAnswer2

	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q16(pagetext):
	"""  	0.5 for the Units in both the x and y components(1 is enough) and 0.25 for the x component and 0.25 for the y component 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")
	xMagnitude=["32"]
	yMagnitude=["12"]
	wrongif=["-"]

	pagetextList=studentsAnswer.strip().split("\n")

#CHECKING X COMPONENT
	if len(pagetextList[0])>10 or len(pagetextList[0])<2 : return["Answer not read from file",marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1] #(to see if teh student has written something else)
	elif (checkString.containsString(pagetextList[0],"-")): comment=3
	elif (checkString.containsString(pagetextList[0],"32")): marks+=0.5

#CHECKING Y COMPONENT
	if len(pagetextList[1])>10 or len(pagetextList[1])<2 : return["Answer not read from file",marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1] #(to see if teh student has written something else)
	elif (checkString.containsString(pagetextList[1],"-")): comment=4
	elif (checkString.containsString(pagetextList[1],"12")): marks+=0.5

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]


def q17(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------

#__magnitude
	pagetext=retainString.afterBackEnd(pagetextOriginal,"Magnitude of E-")
	pagetext=retainString.beforeFrontEnd(pagetext,"Direction of E-")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"N/C")

	studentsMag=float(re.sub('[^0-9]','',studentsAnswer)) #retaining only the numeric characters
	if studentsMag>1000: studentsMag=studentsMag/100.0
	elif studentsMag>100: studentsMag=studentsMag/10.0
	magError=studentsMag-37.90
	if abs(magError)>0.5: 
		comment=2
	else: marks+=1

	studentsAnswer1=studentsAnswer

#__angle
	pagetext=retainString.afterBackEnd(pagetextOriginal,"+x direction")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"o1 nC")
	studentsAngle=float(studentsAnswer.strip())

	angleError=studentsAngle-18.0
	if abs(angleError)>0.5: 
		if comment==2: comment=4
		else: comment=3
	else: marks+=1

	studentsAnswer2=studentsAnswer

	studentsAnswer=studentsAnswer1+"; "+studentsAnswer2

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]





def q18(pagetext):
	"""  	1 point for the entire quenstion """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	
	pagetext=retainString.afterBackEnd(pagetext,"Root MSE")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Data")

	studentsAnswer=studentsAnswer.strip()
	
	if abs(float(studentsAnswer))==0.0:  comment=2
	elif abs(float(studentsAnswer))>=0.200: comment=3
	else: marks+=1

	studentsAnswer="RMS: "+studentsAnswer

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q19(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component  	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	
	pagetext=retainString.afterBackEnd(pagetext,"n =")
	studentsAnswer=pagetext.strip()

	if float(studentsAnswer)==3:marks+=1

	studentsAnswer="n= "+studentsAnswer

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q20(pagetext):
	"""  	0.5 for the Units in both the x and y omponents(1 is enough) and 0.25 for the x component and 0.25 for the y component  	"""
#-----defaults-------------
	marks=1
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
	
	pagetext=retainString.afterBackEnd(pagetext,"think!)")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Activity")

	lookFor=["far","same point","large distance", "away from the","cancel","neutral","netural","opposite charge","further","zero","concentrated near the dipole","postive to negative","decreased more rapidly with increasing distance"]
	if checkString.containsString(studentsAnswer,lookFor): marks+=1
	else: studentsAnswer="Answer not read from file"


#----------Returning the values----------------
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q21(pagetext):
	"""  	0.5 for n=1 , 0.5 for n=2,"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext

#-----Checking for answers-------------
#---------checking n---------
	pagetext=retainString.afterBackEnd(pagetext,"fit this data.")
	pagetext=retainString.beforeFrontEnd(pagetext,"n =")

	studentsAnswer=pagetext.strip()

	if studentsAnswer=="": comment=2
	elif float(studentsAnswer)%1 != 0.0: comment=3
	elif float(studentsAnswer)>1: comment=4
	else: marks+=0.5

	studentsAnswer1="n= "+studentsAnswer

#---------checking fit---------
	pagetext=retainString.afterBackEnd(pagetextOriginal,"Root MSE")
	pagetext=retainString.beforeFrontEnd(pagetext,"Data")

	studentsAnswer=pagetext.strip()

	if len(studentsAnswer)>10: 
		if comment==2:comment=6
		else:comment=5
	else: marks+=0.5

	studentsAnswer2="RMS: "+studentsAnswer

	studentsAnswer=studentsAnswer1+"; "+studentsAnswer2
	
#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [studnts answer(or "Could not read from file" ), marks, for default comment use 1]

def q22(pagetext):
	"""  	1 point for the explanation   """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------

	pagetext=retainString.afterBackEnd(pagetextOriginal,"..)")
	pagetext=retainString.beforeFrontEnd(pagetext,"Record the value")

	studentsAnswer=pagetext.strip()

	lookFor=["far","close","finite","Gauss"]
	if checkString.containsString(studentsAnswer,lookFor): marks+=1
	else: studentsAnswer="Answer not read from file"
	
	
	#----------Returning the values----------------
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


def q23(pagetext):
	"""  	not implementeed due to complicated nature  """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	marks+=1

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


def q24(pagetext):
	"""  	not implementeed due to complicated nature  """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	marks+=2

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


def q25(pagetext):
	"""  	not implementeed due to complicated nature  """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	marks+=1

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


def q26(pagetext):
	"""  	not implementeed due to complicated nature  """
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
	pagetextOriginal=pagetext


#-----Checking for answers-------------
	marks+=1

#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


def q27(pagetext):
	"""  	cleaning the station 	"""
#-----defaults-------------
	marks=0
	comment=1
	studentsAnswer="Answer not read from file"
#-----defaults-------------
	marks+=4
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
	pagetext=retainString.afterBackEnd(pagetext,"y - component")
	studentsAnswer=retainString.beforeFrontEnd(pagetext,"Do the same thing")


#----------Returning the values----------------
	studentsAnswer=studentsAnswer.replace('\n', ' ')
	return[studentsAnswer,marks,comment]	#ans is [students answer, marks, for default comment use 1]


#####__________Important- contains all the effort into programming auto recongnition__________##############


##------------------------------------reading Names---------------------------------------------
#			print("Reading names...")
#			for stNum in range(1,13): #for all the stations\
#				student1obj=student()
#				student2obj=student()
#				student3obj=student()
#				stDic[stNum].stationStudent={1:student1obj,2:student2obj,3:student3obj}

#				pageObj = pdfsObjsDic[stNum].getPage(1) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#				namesPageText=pageObj.extractText()
#				namesPageTextOriginal=namesPageText

#				namesPageText=retainString.afterBackEnd(namesPageText,"names in the")
#				namesPageText=retainString.beforeFrontEnd(namesPageText,"(2)")
#				student1=namesPageText
				
#				namesPageText=retainString.afterBackEnd(namesPageTextOriginal,'-".').strip()
#				namesPageText=namesPageText.split("\n")


#				student1="your name your name"
#				student2="your name your name"
#				student3="your name your name"

#				if len(namesPageText)==5:
#					student1=student1.strip()+" "+namesPageText[2].strip()
#					student2=namesPageText[0].strip()+" "+namesPageText[3].strip()
#					student3=namesPageText[1].strip()+" "+namesPageText[4].strip()
#				elif len(namesPageText)==3: #sometimes the students erase the your name part in the empty boxes
#					student1=student1.strip()+" "+namesPageText[1].strip()
#					student2=namesPageText[0].strip()+" "+namesPageText[2].strip()
#					student3="your name your name"

#				if student1=="your name your name": student1=""   #getting rid of un entered names
#				if student2=="your name your name": student2=""
#				if student3=="your name your name": student3=""

#				temp1=len(students)-1 #DEFAULTING TO:-COULD NOT GET NAMES AUTOMATICALLY
#				temp2=len(students)-1
#				temp3=len(students)-1

#				for x in range (0,len(students)): # which three students are in this station
#					if student1.upper().strip()==students[x][0].upper().strip(): temp1=x
#					if student2.upper().strip()==students[x][0].upper().strip(): temp2=x
#					if student3.upper().strip()==students[x][0].upper().strip(): temp3=x
#				for y in range (1,4):
#					if y==1: temp=temp1
#					if y==2: temp=temp2
#					if y==3: temp=temp3
#					stDic[stNum].stationStudent[y].Name=students[temp][0]
#					stDic[stNum].stationStudent[y].index=temp


####------------------------------------Page 4-------------------------------------------
#			print("Reading page 4 of 17...")
#			for stNum in range(1,13): #for all the stations\
#					pageObj = pdfsObjsDic[stNum].getPage(3) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#					pdfsObjsDic[stNum].namesPageText=pageObj.extractText().split('\n')

###0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
#					qnum=1#question 1 in doc (page 4 of pdf)
#					if pdfsObjsDic[stNum].namesPageText[53].lower().strip() in trueCheck or (pdfsObjsDic[stNum].namesPageText[54].lower() in falseCheck and pdfsObjsDic[stNum].namesPageText[55].lower() in falseCheck):
#						stDic[stNum].answers[qnum][5]=stDic[stNum].answers[qnum][3]   #The student obtained full marks
#						stDic[stNum].answers[qnum][4]="True False Type"
#						stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically

#					else:
#						stDic[stNum].answers[qnum][5]=0 
#						stDic[stNum].answers[qnum][4]="True False Type"
#						stDic[stNum].answers[qnum][6]=1 #wrong and taken care of automatically

#					qnum=2#question 2 in doc (page 3 of pdf)
#					if (pdfsObjsDic[stNum].namesPageText[len(pdfsObjsDic[stNum].namesPageText)-1].lower().strip() in ("b")):
#						stDic[stNum].answers[qnum][5]=stDic[stNum].answers[qnum][3] 
#						stDic[stNum].answers[qnum][4]=pdfsObjsDic[stNum].namesPageText[len(pdfsObjsDic[stNum].namesPageText)-1].strip()
#						stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#					else:
#						stDic[stNum].answers[qnum][5]=0 
#						stDic[stNum].answers[qnum][4]=pdfsObjsDic[stNum].namesPageText[len(pdfsObjsDic[stNum].namesPageText)-1].strip()
#						stDic[stNum].answers[qnum][6]=1 #wrong and taken care of automatically


####------------------------------------Page 5-------------------------------------------
#			print("Reading page 5 of 17...")
#			for stNum in range(1,13): #for all the stations\
#				pageObj = pdfsObjsDic[stNum].getPage(4) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#				pageText=pageObj.extractText()
#				pdfsObjsDic[stNum].namesPageText=pageObj.extractText().split('\n')
#				qnum=3
#				ans=exp1check.q3(pageText)
#				####0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
#				stDic[stNum].answers[qnum][4]=ans[0] #since you have to display the answer if the student gets it right or wrong
#				stDic[stNum].answers[qnum][5]=ans[1]   #The students marks
#				if ans[1]==stDic[stNum].answers[qnum][3]:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				elif "Answer not read from file" in ans[0]:stDic[stNum].answers[qnum][6]=0
#				else:stDic[stNum].answers[qnum][6]=1
#				stDic[stNum].answers[qnum][7]=explanationOptions[self.expNum-1][qnum][ans[2]]   #explanationOptions[expNum-1][x][ans[2]] 


###0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]				
#				qnum=4		#question 4 in doc (page 5 of pdf)
#				namesPageText=pageObj.extractText()
#				ans=exp1check.q4(namesPageText)
#				stDic[stNum].answers[qnum][4]=ans[1] #since you have to display the answer if the student gets it right or wrong
#				stDic[stNum].answers[qnum][5]=ans[0]   #The students marks
#				if ans[0]==1:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				else:stDic[stNum].answers[qnum][6]=1
####------------------------------------Page 7-------------------------------------------
#			print("Reading page 7 of 17...")
#			for stNum in range(1,13): #for all the stations\
#				pageObj = pdfsObjsDic[stNum].getPage(6) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#				pdfsObjsDic[stNum].namesPageText=pageObj.extractText().split('\n')

###0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]				
#				qnum=5		#question 4 in doc (page 7 of pdf)
#				answerstring1=""
#				if pdfsObjsDic[stNum].namesPageText[25].lower().strip().find("e")==0:answerstring1+="c"
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[25].lower().strip().find("g")==1:answerstring1+="c"
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[25].lower().strip().find("h")==2:answerstring1+="c"
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[54].lower().strip().find("i")==0:answerstring1+="c"
#				else:answerstring1+="w"
#				score=[float(answerstring1.count("c"))*0.25,answerstring1]

#				stDic[stNum].answers[qnum][5]=score[0]   #The students marks
#				stDic[stNum].answers[qnum][4]="True False Type, Ans: "+score[1]
#				if score[0]==1:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				else: stDic[stNum].answers[qnum][6]=1

#				qnum=6		#question 6 in doc (page 7 of pdf)
#				answerstring1=""
#				if pdfsObjsDic[stNum].namesPageText[54].strip().find("0")==1 or pdfsObjsDic[stNum].namesPageText[54].lower().strip().find("o")==1:answerstring1+="c"					
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[54].strip()[2:4].find("0")==0 or pdfsObjsDic[stNum].namesPageText[54].strip()[2:4].find("o")==0:answerstring1+="c"
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[54].lower().strip().find("+")==3:answerstring1+="c"
#				else:answerstring1+="w"
#				if pdfsObjsDic[stNum].namesPageText[62].lower().strip().find("+")==0:answerstring1+="c"
#				else:answerstring1+="w"
#				score=[float(answerstring1.count("c"))*0.25,answerstring1]

#				stDic[stNum].answers[qnum][5]=score[0]   #The students marks
#				stDic[stNum].answers[qnum][4]="True False Type, Ans: "+score[1]
#				if score[0]==1:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				else: stDic[stNum].answers[qnum][6]=1


####------------------------------------Page 9-------------------------------------------
#			print("Reading page 9 of 17...")
#			for stNum in range(1,13): #for all the stations\
#				pageObj = pdfsObjsDic[stNum].getPage(8) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#				namesPageText=pageObj.extractText()

####0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
# ##questions 7 and 8 are done together...
#				ans=exp1check.q7and8(namesPageText)

#				qnum=7		#question 9 in doc (page 7 of pdf)
#				stDic[stNum].answers[qnum][4]="Here the Students answer to both this question and the next question are displayed, the second answer relates to this question:\n\n"+ans[0] #since you have to display the answer if the student gets it right or wrong
#				if ans[1]==True:
#					stDic[stNum].answers[qnum][5]=stDic[stNum].answers[qnum][3]   #The student obtained full marks
#					stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				else: stDic[stNum].answers[qnum][6]=1 #kokatath check karanna kiyala e thiyenne

#				qnum=8		#question 9 in doc (page 7 of pdf)
#				stDic[stNum].answers[qnum][4]="Here the Students answer to both this question and the previous questions are displayed, the first answer relates to this question:\n\n"+ans[0] #since you have to display the answer if the student gets it right or wrong
#				if ans[2]==True:
#					stDic[stNum].answers[qnum][5]=stDic[stNum].answers[qnum][3]   #The student obtained full marks
#					stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#				else: stDic[stNum].answers[qnum][6]=1 #kokatath check karanna kiyala e thiyenne

##----------------the Universal function to call all the questions for exp 1------------------------------------------------------------------

#			functionsToCall={exp1check.q9:9,exp1check.q10:10,exp1check.q11:11,exp1check.q12:12,exp1check.q13:13,exp1check.q14:14,exp1check.q15:15,exp1check.q16:16,exp1check.q17:17,exp1check.q18:18,exp1check.q19:19,exp1check.q20:20,exp1check.q21:21,exp1check.q22:22,exp1check.q23:23,exp1check.q24:24,exp1check.q25:25,exp1check.q26:26,exp1check.q27:27}
#			for qnum in range(9,len(questions)):  #	range(9,len(questions)): 
#				maxQNumber=len(questions) #remember that the Questions list has the first entry to be a user defined entry
#				print("Reading question "+str(qnum)+" of "+str(maxQNumber-1)+"...")

#				for stNum in range(1,13): #for all the stations
#					pageObj = pdfsObjsDic[stNum].getPage(questions[qnum][0]-1) #use pages x-1 ex:if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
#					pageText=pageObj.extractText()

#					for key, val in functionsToCall.items():
#						if val == qnum: ans=key(pageText)	##ans is [students answer(or "Could not read from file" ), marks]


#					####0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
#					stDic[stNum].answers[qnum][4]=ans[0] #since you have to display the answer if the student gets it right or wrong
#					stDic[stNum].answers[qnum][5]=ans[1]   #The students marks
#					if ans[1]==stDic[stNum].answers[qnum][3]:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
#					elif "Answer not read from file" in ans[0]:stDic[stNum].answers[qnum][6]=0
#					else:stDic[stNum].answers[qnum][6]=1
#					stDic[stNum].answers[qnum][7]=explanationOptions[self.expNum-1][qnum][ans[2]]   #explanationOptions[expNum-1][x][ans[2]] 

