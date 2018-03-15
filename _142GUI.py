#import matplotlib
#matplotlib.use("TkAgg") #back end of matplot lib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
#import matplotlib.animation as animation
#from matplotlib import style

#for email to work
import pickle # for saving obejects ans also loading them
import smtplib
import PyPDF2
import os #used to write to the system shell
import tkinter as tk
import subprocess

import exp1check
import exp2check
import exp3check
import exp4check
import exp5check
import exp6check
import exp7check
import exp8check


from manipulateString import *
from multipart import MIMEMultipart
from text import MIMEText
from base import MIMEBase
from encoders import *
from tkinter import ttk #To make the windows look better
from tkinter.messagebox import showerror#takes care of error messages
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror


#initializations
global students
global wednesdayStudents
global thursdayStudents
global experimentNames
#global expName
global explanationOptions

global questions

questions=[]

#[name,email,attendance(don't change-automatic)] The First line is for filling out empty lines
wednesdayStudents=[["","keep this line here",False], #do not delete this line
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Could not get name automatically","studentaddress@university.edu",False]]#do not delete this line


#[name,email,attendance(don't change-automatic)] The First line is for filling out empty lines
wednesdayStudents=[["","keep this line here",False], #do not delete this line
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Student Name","studentaddress@university.edu",False], 
					["Could not get name automatically","studentaddress@university.edu",False]]#do not delete this line

experimentNames=["Electrostatics",
				 "Equipotentials",
				 "DC Circuits",
				 "RC Circuits",
				 "Biot-Savart Law",
				 "Ampere's Law",
				 "Induction",
				 "AC Circuits",
				 "Interference and Diffraction"]

#[expNum][questionNum][Option0,Option1,...]  
#remember to have the second entry be the generic one 



LARGE_FONT_BOLD=("Times New Roman",15,"bold","red")
LARGE_FONT=("Times New Roman",12)
NORM_FONT=("Times New Roman",10)
SMALL_FONT=("Times New Roman",8)

def functionChecker():
	os.system('taskkill /IM FoxitReader.exe')

class experimentObject():  #make class for measurement
	global stDic
	def __init__(self):
		self.expSavedOnce=False
		self.file="Empty"
		self.st1=stDic[1]
		self.st2=stDic[2]
		self.st3=stDic[3]
		self.st4=stDic[4]
		self.st5=stDic[5]
		self.st6=stDic[6]
		self.st7=stDic[7]
		self.st8=stDic[8]
		self.st9=stDic[9]
		self.st10=stDic[10]
		self.st11=stDic[11]
		self.st12=stDic[12]

def saveExperimentPopup():
	global expObj
	expObj=experimentObject()
##		popupexp=tk.Tk() does not need to be defined because asksaveasfilename is a Tkinter prebuilt dialog window to access files	
	savefile = asksaveasfilename(filetypes=(("Student Marks", "*.era"),("All files", "*.*")))
	with open(savefile+'.era', 'wb') as output:
		pickle.dump(expObj, output, pickle.HIGHEST_PROTOCOL)
		expObj.file=savefile
		expObj.expSavedOnce= True

def quickSaveExperimentPopup():
	global stDic
	global expObj
	expObj.content=stDic
	if expObj.expSavedOnce:
		with open(expObj.file, 'wb') as output:
			pickle.dump(expObj, output, pickle.HIGHEST_PROTOCOL)
			expObj.expSavedOnce= True
	else:
		saveExperimentPopup()

def openExperimentPopup():
	global stDic
	global expObj
	name = askopenfilename(filetypes=(("Student Marks", "*.era"),("All files", "*.*")),title = "Choose a file.")
#Using try in case user types in unknown file or closes without choosing a file.
	try:
		with open(name, 'rb') as input:
			expObj = pickle.load(input)	
			expObj.expSavedOnce=True
			stDic=expObj.content
			mainWindow.refresh()
	except:
		showerror("Save File", "File is not supported or dialog was closed without opening a file" ) #(dilaog name, message)

def preamble():
	""" % ---
\\documentclass{article}

% Packages
% ---
\\usepackage{amsmath} % Advanced math typesetting
\\usepackage[utf8]{inputenc} % Unicode support (Umlauts etc.)
\\usepackage[UKenglish]{babel} % Change hyphenation rules
\\usepackage{hyperref} % Add a link to your document
\\usepackage{graphicx} % Add pictures to your document
\\usepackage{listings} % Source code formatting and highlighting
\\usepackage[letterpaper, portrait , margin=1in]{geometry}
\\usepackage{braket}
\\usepackage{parskip}
\\usepackage{epstopdf}
%\\usepackage[UKenglish]{babel}
\\usepackage[UKenglish]{isodate}
\\usepackage{multirow}


% Main document
% ---
\\begin{document}
\\pagenumbering{gobble}% Remove page numbers (and reset to 1)\n
"""

	textToWrite=preamble.__doc__
	return textToWrite

def heading():
	"""\\begin{table}[h]
	\\centering
	\\begin{tabular}{c}
	PHYS 142 - Computer Based Lab Feedback Form\\\\
	"""
	global exp
	text2="Lab Title: "+exp.expName+"\\\\Date: "

	date=int(exp.date)
	if date==1 or date==21:
		g="st"
	elif date==2 or date==22:
		g="nd"
	elif date==3 or date==23:
		g="rd"
	else:
		g="th"
	text=heading.__doc__+text2+exp.day+" "+exp.month+" "+str(exp.date)+"$^{"+g+"}$ "+exp.semester+" "+exp.year+" \\\\\\hline\n"
	text+="\\end{tabular}\n"
	text+="\\end{table}\n"	
	return text 

def end():
	"""\\end{document}
"""

	return end.__doc__

def compile():
	F = open("Scores.csv","w")
	F.close()	
	nP="\\clearpage" #newPage in Latex
	f = open('The_File.tex', 'w')
	final=preamble()
	final+=body("station1")+nP
	final+=body("station2")+nP
	final+=body("station3")+nP
	final+=body("station4")+nP
	final+=body("station5")+nP
	final+=body("station6")+nP
	final+=body("station7")+nP
	final+=body("station8")+nP
	final+=body("station9")+nP
	final+=body("station10")+nP
	final+=body("station11")+nP
	final+=body("station12")+nP
	final+=end()
	f.write(final)
	f.close()
	os.system('taskkill /IM FoxitReader.exe')  #killing the process so that it does not lag
	os.system('pdflatex The_File.tex')
	os.system('The_File.pdf')
	os.system('exit')
	emailAsk()

def emailAsk():
	global students
	global emailpopup
	count=0
	temp=""
	for x in range(1,len(students)-1): #starting at 1 and ending at len(students)-1 to ignore empty and not detected options
		if students[x][2]==False: 
			count+=1
			temp+="    "+str(count)+". "+students[x][0]+"    ::::: email at: "+students[x][1]+"\n"
	texToDisplay="\nLooks like "+str(count)+" student(s) didn't make it to the Lab (make sure names were read automatically). Do you want to email them?\n\n   Student(s) who didn't make it,\n\n"+temp
	if not count==0:
		emailpopup=tk.Tk()
		emailpopup.wm_title("Email Students")
		label=ttk.Label(emailpopup,text=texToDisplay,font=LARGE_FONT)
		label.pack(side="top", fill="x", padx=10, pady=10)
		B1= ttk.Button(emailpopup, text="Okay", command=lambda: email())
		B2= ttk.Button(emailpopup, text="No", command=emailpopup.destroy)
		B1.pack()
		B2.pack()
		emailpopup.mainloop()

def email():
	global students
	global exp
	global emailpopup
	date=int(exp.date)
	emailpopup.destroy()
	if date==1 or date==21:
		g="st"
	elif date==2 or date==22:
		g="nd"
	elif date==3 or date==23:
		g="rd"
	else:
		g="th"

	Stud={}
	for v in range(1,len(students)):
		if students[v][2]==False: Stud.update({students[v][0]:students[v][1]})
	listToMail={"Stud":Stud}
	fromaddr = ""
	server = smtplib.SMTP('smtp.live.com', 587)
	server.starttls()
	server.login(fromaddr, "")
	bodyForMe=""

	print("Sending email to students..")

	for ke in listToMail:
		allNames=""
		dic=listToMail[ke]
		y=len(dic)
		x=0
		for key in dic:
			toaddr = dic[key]	
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = toaddr
			if ke=="Stud":
				msg['Subject'] = "Missed Lab: '"+exp.expName+"' on "+exp.day+" the "+exp.date+g+" of "+exp.month+" "+exp.year
				body = "Dear "+key+",\n\nIt seems that you have missed the '"+exp.expName+"' Lab that was conducted on "+exp.day+" the "+exp.date+g+" of "+exp.month+" "+exp.year+". You can still make up the missed lab if you have a valid excuse. The make-up schedule is usually available under 142 course material. Please e-mail me with the date that you would like to reschedule it. It is best to take the make-up as soon as you can, as there are only a limited number of make-up sessions. \n\nThank You\n\nEranjan Kandegedara"
			msg.attach(MIMEText(body, 'plain'))
			text = msg.as_string()
			server.sendmail(fromaddr, toaddr, text)
			print(key)
			allNames+="\r\n "+str(x+1)+". "+key
			x+=1
		bodyForMe+="An automated email with subject, '"+msg['Subject']+"' was sent to the following recipients: "+allNames+"\r\nIf the code worked in its entirety there should be a total of "+str(y)+" entries.\r\n\r\n"
		print("Done sending to :"+ke)

	bodyForMe+="\r\n"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = fromaddr
	msg['Subject'] = "Batch emails sent"

	#bodyForMe = "\r\n\r\n An automated email with subject 'මොකෝ වෙන්නේ?' was sent to the following recipients: "+allNames+"\r\n If the code worked in its entirety there should be a total of "+str(y)+" entries."
	msg.attach(MIMEText(bodyForMe, 'plain'))
	text = msg.as_string()
	server.sendmail(fromaddr, fromaddr, text)
	server.quit()
	print("Done...")

def popupmsg(msg):
	popup=tk.Tk()
	popup.wm_title("Message!")
	label=ttk.Label(popup,text=msg,font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1= ttk.Button(popup, text="Okay", command=popup.destroy)
	B1.pack()
	popup.mainloop()

def animate(i): 
	pullData = open("sampleData.txt","r").read() 
	dataList = pullData.split('\n') 
	xList = [] 
	yList = [] 
	for eachLine in dataList: 
		if len(eachLine)>1: 
			x,y = eachLine.split(',') 
			xList.append(int(x)) 
			yList.append(int(y)) 
	a.clear() 
	a.plot(xList,yList)	

class Exp():
	def __init__(self, expNum):
		global explanationOptions
		global questions
		questionLoader={1:exp1check,2:exp2check,3:exp3check,4:exp4check,5:exp5check,6:exp6check,7:exp7check,8:exp8check}
		for key, val in questionLoader.items():
			if key == expNum: 
				questions=val.questions
				explanationOptions=val.ExplanationOptions
		self.Student1=""
		self.Student2=""
		self.Student3=""
		self.answers=[]
		for x in range(0,len(questions)):
			self.answers.append([questions[x][0],questions[x][1],questions[x][2],questions[x][3],"Answer not read from file",0,0,explanationOptions[x][1]]) #0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]

def readFromFile():
	global pdfsObjsDic
	pdfsObjsDic={}
	for stNum in range(1,13): #for all the stations put this under neath the for loop
		Obj = open(str(stNum)+'.pdf', 'rb')
		pdfReader = PyPDF2.PdfFileReader(Obj)
		dic={stNum:pdfReader}
		pdfsObjsDic.update(dic)

class student():
	"""Temporary student class for each station"""
	def __init__(self, *args):
		self.Name=""

class experiment():
	global stDic
	global explanationOptions
	def __init__(self, *args):
		global stDic
		global experimentNames
		global pdfsObjsDic
		global students
		global wednesdayStudents
		global thursdayStudents
		global questions
		self.day=args[0]
		self.month=args[1]
		self.date=args[2]
		self.semester=args[3]
		self.year=args[4]
		self.expName=args[5]
		stDic={}

		if self.day=="Wednesday":students=wednesdayStudents
		elif self.day=="Thursday":students=thursdayStudents

		readFromFile()


		print("Scanning PDF documents to extract student data on each station. Please wait...")

		if self.expName==experimentNames[0]:
			self.expNum=1
			expCheckSave=exp1check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27}#,expCheckSave.q28:28,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[1]:
			self.expNum=2
			expCheckSave=exp2check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21}#,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[2]:
			self.expNum=3
			expCheckSave=exp3check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21}#,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[3]:
			self.expNum=4
			expCheckSave=exp4check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28}#,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[4]:
			self.expNum=5
			expCheckSave=exp5check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20}#,expCheckSave.q21:21}#,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28}#,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[5]:
			self.expNum=6
			expCheckSave=exp6check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17}#,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20}#,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28}#,expCheckSave.q29:29,expCheckSave.q30:30}
		elif self.expName==experimentNames[6]:
			self.expNum=7
			expCheckSave=exp7check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28,expCheckSave.q29:29,expCheckSave.q30:30,expCheckSave.q31:31,expCheckSave.q32:32,expCheckSave.q33:33,expCheckSave.q34:34,expCheckSave.q35:35,expCheckSave.q36:36,expCheckSave.q37:37,expCheckSave.q38:38,expCheckSave.q39:39}
		elif self.expName==experimentNames[7]:
			self.expNum=8
			expCheckSave=exp8check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17}
		elif self.expName==experimentNames[8]:
			self.expNum=9
			expCheckSave=exp9check
			functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28}#,expCheckSave.q29:29,expCheckSave.q30:30}

		#qs={q1:1,q2:2,q3:3,q4:4,q5:5,q6:6,q7:7,q8:8,q9:9,q10:10,q11:11,q12:12,q13:13,q14:14,q15:15,q16:16,q17:17,q18:18,q19:19,q20:20,q21:21,q22:22,q23:23,q24:24,q25:25,q26:26,q27:27,q28:28,q29:29,q30:30}
		#functionsToCall={expCheckSave.q1:1,expCheckSave.q2:2,expCheckSave.q3:3,expCheckSave.q4:4,expCheckSave.q5:5,expCheckSave.q6:6,expCheckSave.q7:7,expCheckSave.q8:8,expCheckSave.q9:9,expCheckSave.q10:10,expCheckSave.q11:11,expCheckSave.q12:12,expCheckSave.q13:13,expCheckSave.q14:14,expCheckSave.q15:15,expCheckSave.q16:16,expCheckSave.q17:17,expCheckSave.q18:18,expCheckSave.q19:19,expCheckSave.q20:20,expCheckSave.q21:21,expCheckSave.q22:22,expCheckSave.q23:23,expCheckSave.q24:24,expCheckSave.q25:25,expCheckSave.q26:26,expCheckSave.q27:27,expCheckSave.q28:28,expCheckSave.q29:29,expCheckSave.q30:30}
		#xmax=len(questions)
		#for key, val in functionsToCall.items()
		#	if val<=xmax:dict_you_want = {key:val for key, val in functionsToCall.items() }

		for st in range(1,13):
			st1=Exp(self.expNum)
			stDic.update({st:st1})


#------------------------------------reading Names---------------------------------------------
		print("Reading names...")
		for stNum in range(1,13): #for all the stations\
			student1obj=student()
			student2obj=student()
			student3obj=student()
			stDic[stNum].stationStudent={1:student1obj,2:student2obj,3:student3obj}
			pageObj = pdfsObjsDic[stNum].getPage(questions[0][0]-1) #use pages x-1 if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
			namesPageText=pageObj.extractText()
			getNames=expCheckSave.nameCheck(namesPageText,students)
			student1=getNames[0]
			student2=getNames[1]
			student3=getNames[2]

			temp1=len(students)-1 #DEFAULTING TO:-COULD NOT GET NAMES AUTOMATICALLY
			temp2=len(students)-1
			temp3=len(students)-1

			for x in range (0,len(students)): # which three students are in this station
				if student1.upper().strip()==students[x][0].upper().strip(): temp1=x
				if student2.upper().strip()==students[x][0].upper().strip(): temp2=x
				if student3.upper().strip()==students[x][0].upper().strip(): temp3=x
			for y in range (1,4):
				if y==1: temp=temp1
				if y==2: temp=temp2
				if y==3: temp=temp3
				stDic[stNum].stationStudent[y].Name=students[temp][0]
				stDic[stNum].stationStudent[y].index=temp


#----------------the Universal function to call all the questions ------------------------------------------------------------------
		maxQNumber=len(questions) #remember that the Questions list has the first entry to be a user defined entry
		for qnum in range(1,7):  #	range(9,len(questions)): 			
			print("Reading question "+str(qnum)+" of "+str(maxQNumber-1)+"...")
			for stNum in range(1,13): #for all the stations
				pageObj = pdfsObjsDic[stNum].getPage(questions[qnum][0]-1) #use pages x-1 ex:if you want page 3 call page 2  #pdfObjsDic has the 12 stations stored
				pageText=pageObj.extractText()
				for key, val in functionsToCall.items():
					if val == qnum: ans=key(pageText)	##ans is [students answer(or "Could not read from file" ), marks]
				###0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
				stDic[stNum].answers[qnum][4]=ans[0] #since you have to display the answer if the student gets it right or wrong
				stDic[stNum].answers[qnum][5]=ans[1]   #The students marks
				if ans[1]==stDic[stNum].answers[qnum][3]:stDic[stNum].answers[qnum][6]=2 #correct and taken care of automatically
				elif "Answer not read from file" in ans[0]:stDic[stNum].answers[qnum][6]=0
				else:stDic[stNum].answers[qnum][6]=1
				stDic[stNum].answers[qnum][7]=explanationOptions[qnum][ans[2]]   #explanationOptions[expNum-1][x][ans[2]]

def refresh2():mainWindow.refresh()


class mainWindow(tk.Tk):  #make class and inherit from tk.TK
	global exp
	def __init__(self,*args,**kwargs): 
		global z
		global container
		global quaziselfmainwindow
		quaziselfmainwindow=self
		tk.Tk.__init__(self,*args,*kwargs)
#		tk.Tk.iconbitmap(self, default="logo.ico")
		tk.Tk.wm_title(self, "142 Grading")
		
		container=tk.Frame(self) 
		container.pack(side="top", fill="both", expand= True)	#"fill" will fill in the space that you have alloted to pack, expand tells it to what ever the pack is just expand that to the entire window
		container.grid_rowconfigure(0,weight=1) #0 is the minimum size, weight is for the priority
		container.grid_columnconfigure(0,weight=1) #
		
		menubar=tk.Menu(container) #adding the menu bar
		
		#The "File" menu Option
		filemenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
		filemenu.add_command(label="Save Experiment As", command=lambda:saveExperimentPopup())		#labmda si a throwaway function and it makes the function not run immediately
		filemenu.add_command(label="Save Experiment", command=lambda:quickSaveExperimentPopup())		
		filemenu.add_command(label="Load Experiment", command=lambda: openExperimentPopup())
		filemenu.add_command(label="Read pdfs", command=lambda: readFromFile())	
		filemenu.add_command(label="Refresh", command=lambda: refresh2())
		filemenu.add_command(label="Fution checker", command=lambda: functionChecker())	
		filemenu.add_separator()
		filemenu.add_command(label="Exit",underline=0, command=quit, accelerator="Ctrl+Q")
		menubar.add_cascade(label="File", menu=filemenu)

		#The "Station" menu Option
		stationMenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
		stationMenu.add_command(label="Start Page", command=lambda: self.show_frame(StartPage))
		stationMenu.add_command(label="Station 1", command=lambda: self.show_frame(station1))
		stationMenu.add_command(label="Station 2", command=lambda: self.show_frame(station2))
		stationMenu.add_command(label="Station 3", command=lambda: self.show_frame(station3))
		stationMenu.add_command(label="Station 4", command=lambda: self.show_frame(station4))
		stationMenu.add_command(label="Station 5", command=lambda: self.show_frame(station5))
		stationMenu.add_command(label="Station 6", command=lambda: self.show_frame(station6))
		stationMenu.add_command(label="Station 7", command=lambda: self.show_frame(station7))
		stationMenu.add_command(label="Station 8", command=lambda: self.show_frame(station8))
		stationMenu.add_command(label="Station 9", command=lambda: self.show_frame(station9))
		stationMenu.add_command(label="Station 10", command=lambda: self.show_frame(station10))
		stationMenu.add_command(label="Station 11", command=lambda: self.show_frame(station11))
		stationMenu.add_command(label="Station 12", command=lambda: self.show_frame(station12))	
		menubar.add_cascade(label="Window", menu=stationMenu)


		#The "Compile" menu Option
		compileMenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
		compileMenu.add_command(label="Compile", command=lambda: compile())
		menubar.add_cascade(label="Compile", menu=compileMenu)
		
		
		#The "Help" menu Option		
		helpMenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
		helpMenu.add_command(label="Documentation", command=lambda: popupmsg("Not Supported just yet!"))
		menubar.add_cascade(label="Help", menu=helpMenu)		
		
		# tk.Tk.bind("<Key>", key)
		container.bind("<Control-q>", quit)
#		container.bind("F5", compile())
		tk.Tk.config(self, menu=menubar)
	
		self.frames={} 	#
		
		z=[StartPage]
		for F in z:		
			frame=F(container, self)	
			self.frames[F]=frame		
			frame.grid(row=0,column=0,sticky="nsew")	
		self.show_frame(StartPage)

	def refresh():
		global container
		global quaziselfmainwindow
		global loadGradingLabel
		global z

		if 'exp' in globals():
			startpage=StartPage(container, quaziselfmainwindow)	
			station1=station(container, quaziselfmainwindow,"station1")
			station2=station(container, quaziselfmainwindow,"station2")
			station3=station(container, quaziselfmainwindow,"station3")
			station4=station(container, quaziselfmainwindow,"station4")
			station5=station(container, quaziselfmainwindow,"station5")
			station6=station(container, quaziselfmainwindow,"station6")
			station7=station(container, quaziselfmainwindow,"station7")
			station8=station(container, quaziselfmainwindow,"station8")
			station9=station(container, quaziselfmainwindow,"station9")
			station10=station(container, quaziselfmainwindow,"station10")
			station11=station(container, quaziselfmainwindow,"station11")
			station12=station(container, quaziselfmainwindow,"station12")

			z=[startpage, station1, station2, station3, station4, station5, station6, station7, station8, station9, station10, station11, station12]
			for frame in z:		
				#frame=F(container, quaziselfmainwindow)	
				quaziselfmainwindow.frames[frame]=frame		
				frame.grid(row=0,column=0,sticky="nsew")	

			quaziselfmainwindow.show_frame(startpage)
			loadGradingLabel.config(background="green2")
			loadGradingLabel.config(text="Experiment: "+expName.get())
		else: showerror("No experiment", "Please set all parameters and press 'Load Experiment' \n Error code: refresh" ) #(dilaog name, message)


	def show_frame(self,cont):
		try:
			frame=self.frames[cont] #looking for the value of self.frame witht the key "cont"
			frame.tkraise() #raising frames to the front
		except: showerror("No experiment", "Please set all parameters and press 'Load Experiment' \n Error code: show frame" ) #(dilaog name, message)
		
		
class StartPage(tk.Frame):
	global exp
	global stDic
	def __init__(self,parent, controller):
		global day
		global month
		global date
		global semester
		global experimentNames
		global yearEntry
		global expName
		global loadGradingLabel
		def loadGrading():
			global exp
			global day
			global month
			global date
			global semester
			global experimentNames
			global yearEntry
			global expName
			exp=experiment(day.get(),month.get(),date.get(),semester.get(),yearEntry.get(),expName.get())
			loadGradingLabel.config(background="green2")
			loadGradingLabel.config(text="Experiment: "+expName.get())
			mainWindow.refresh()
			print("Ready...")

		tk.Frame.__init__(self,parent)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		rownumbers=15
		for x in range(0, rownumbers):
			self.grid_rowconfigure(x, weight=1)
		x=0 #resetting x to be reused

		expNameLabel=tk.Label(self,text="Experiment Details",font=LARGE_FONT)
		expNameLabel.grid(row=x, column=0, columnspan=2, pady=0 , padx=10, sticky="nsew")
		x+=1 # increment row to use with grid

		previousPage=tk.Button(self,text="<Prev\n  St.", background="royal blue", command=lambda: previousStation(0))
		previousPage.grid(row=x, column=0, rowspan=2, pady=10 , padx=10, sticky="nsew")
		nextPage=tk.Button(self,text="Next\n  St. >", background="royal blue", command=lambda: nextStation(0))
		nextPage.grid(row=x, column=1, rowspan=2, pady=10 , padx=10, sticky="nsew")
		x+=2 # increment row to use with grid

		loadGradingLabel=tk.Label(self,text="Experiment not Loaded",background="orange")
		loadGradingLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		loadGradingButton=ttk.Button(self,text="Load Experiment", command=lambda: loadGrading())
		loadGradingButton.grid(row=x, column=1, pady=0 , padx=10, sticky="nsew")	
		x+=1 # increment row to use with grid

		expNameLabel=tk.Label(self,text="Experiment Name:")
		expNameLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		expName = tk.StringVar(self)
		option = ttk.OptionMenu(self, expName, experimentNames[7], *experimentNames)
		option.grid(row=x, column=1, sticky="nsew")
		x+=1 # increment row to use with grid

		expDayLabel=tk.Label(self,text="The day the lab was done:")
		expDayLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		day = tk.StringVar(self)
		choices = ['Wednesday', 'Thursday']
		option = ttk.OptionMenu(self, day, choices[0], *choices)
		option.grid(row=x, column=1, sticky="nsew")
		x+=1 # increment row to use with grid

		expMonthLabel=tk.Label(self,text="The Month the lab was done:")
		expMonthLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		month = tk.StringVar(self)
		choices = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
		option = ttk.OptionMenu(self, month, choices[10], *choices)
		option.grid(row=x, column=1, sticky="nsew")
		x+=1 # increment row to use with grid

		expDateLabel=tk.Label(self,text="The Date the lab was done:")
		expDateLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		date = tk.StringVar(self)
		choices = ['1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21', '22','23','24','25','26','27','28','29','30','31']
		option = ttk.OptionMenu(self, date, choices[1], *choices)
		option.grid(row=x, column=1, sticky="nsew")
		x+=1 # increment row to use with grid

		expSemesterLabel=tk.Label(self,text="The Semester the lab was done:")
		expSemesterLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		semester = tk.StringVar(self)
		choices = ['Fall','Spring','Summer']
		option = ttk.OptionMenu(self, semester, choices[0], *choices)
		option.grid(row=x, column=1, sticky="nsew")
		x+=1 # increment row to use with grid
		
		expYearLabel=tk.Label(self,text="The Year the lab was done:")
		expYearLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
		yearEntry=ttk.Entry(self) #creates user input field in the popup "popupexp"
		yearEntry.insert(0,"2017") #at the zeroth place the default value which is expName
		yearEntry.grid(row=x, column=1, pady=0 , padx=10, sticky="nsew")
		x+=1 # increment row to use with grid

		previousPage=tk.Button(self,text="Tab delimit Wednesday students", background="royal blue", command=lambda: tabDlimitWed())
		previousPage.grid(row=x, column=0, rowspan=2, pady=10 , padx=10, sticky="nsew")
		nextPage=tk.Button(self,text="Tab delimit Thursday students", background="royal blue", command=lambda: tabDlimitThu())
		nextPage.grid(row=x, column=1, rowspan=2, pady=10 , padx=10, sticky="nsew")
		x+=2 # increment row to use with grid


def throwAwayCalculation(name):
	global stDic

	if name=="station1":
		throwAwayStNum=1
		stDic[throwAwayStNum].Name="station 1"
	if name=="station2":
		throwAwayStNum=2
		stDic[throwAwayStNum].Name="station 2"
	if name=="station3":
		throwAwayStNum=3
		stDic[throwAwayStNum].Name="station 3"
	if name=="station4":
		throwAwayStNum=4
		stDic[throwAwayStNum].Name="station 4"
	if name=="station5":
		throwAwayStNum=5
		stDic[throwAwayStNum].Name="station 5"
	if name=="station6":
		throwAwayStNum=6
		stDic[throwAwayStNum].Name="station 6"
	if name=="station7":
		throwAwayStNum=7
		stDic[throwAwayStNum].Name="station 7"
	if name=="station8":
		throwAwayStNum=8
		stDic[throwAwayStNum].Name="station 8"
	if name=="station9":
		throwAwayStNum=9
		stDic[throwAwayStNum].Name="station 9"
	if name=="station10":
		throwAwayStNum=10
		stDic[throwAwayStNum].Name="station 10"
	if name=="station11":
		throwAwayStNum=11
		stDic[throwAwayStNum].Name="station 11"
	if name=="station12":
		throwAwayStNum=12
		stDic[throwAwayStNum].Name="station 12"

	return throwAwayStNum

def body(station):
	global exp
	global stDic
	global students
	global questions

#------------------------------------------figuring out students/partners in station and tabulating--------------------
	throwAwayStNum=throwAwayCalculation(station)
	stDic[throwAwayStNum].stationStudent[1].Name=stDic[throwAwayStNum].student1Name.get()
	stDic[throwAwayStNum].stationStudent[2].Name=stDic[throwAwayStNum].student2Name.get()
	stDic[throwAwayStNum].stationStudent[3].Name=stDic[throwAwayStNum].student3Name.get()
	stDic[throwAwayStNum].stationStudent[1].preLab=stDic[throwAwayStNum].preLab1Options.get()
	stDic[throwAwayStNum].stationStudent[2].preLab=stDic[throwAwayStNum].preLab2Options.get()
	stDic[throwAwayStNum].stationStudent[3].preLab=stDic[throwAwayStNum].preLab3Options.get()

	for x in range (1,len(students)): #making the change of variable to signify that these students were present
		if students[x][0]==stDic[throwAwayStNum].stationStudent[1].Name: students[x][2]=True
		if students[x][0]==stDic[throwAwayStNum].stationStudent[2].Name: students[x][2]=True
		if students[x][0]==stDic[throwAwayStNum].stationStudent[3].Name: students[x][2]=True
	text=""

#this piece of code writes out a single page for a student--------------------		
	for x in range(1,4): #going through all the three students in the station, everythin should be under this "for" loop
		if not stDic[throwAwayStNum].stationStudent[x].Name=="": #if the studnet is present
			text+=heading()
			text+="\\begin{table}[h]\\centering \\begin{tabular}{|c|c|p{9.9 cm}|c|}\\hline Station \\#  & Checkout Initials & \\multicolumn{1}{|c|}{Students Name} & Prelab \\\\\\hline\\multirow{3}{*}{"+str(throwAwayStNum)+"}& \\multirow{3}{*}{$EK$} & &\\\\& &\\multicolumn{1}{|c|}{"+stDic[throwAwayStNum].stationStudent[x].Name+"}&"+stDic[throwAwayStNum].stationStudent[x].preLab+"\\\\&   &  &\\\\\\hline\n\\end{tabular}\n\\end{table}\n"
#figuring out the partners			

			y=(x+1)%3
			z=(x+2)%3
			if y==0:y=3
			if z==0:z=3
			if not stDic[throwAwayStNum].stationStudent[y].Name=="": #these Lines work out the students partners
				temp=stDic[throwAwayStNum].stationStudent[y].Name 
				if not stDic[throwAwayStNum].stationStudent[z].Name=="": temp+=" and "+stDic[throwAwayStNum].stationStudent[z].Name
			elif not stDic[throwAwayStNum].stationStudent[z].Name=="": temp=stDic[throwAwayStNum].stationStudent[z].Name
			else:temp="No partners"

			text+="Partner(s): "+temp+"\\\\\n"

#____________________________________________________starting the table and the table heading_______________________________________________________________________________
			text+="\\\\Please find a breakdown of your grades below. The table shows your grades according to the slide number of the experiment. Only questions that you have made mistakes on, are shown in the table. You have scored full marks for all questions that are not listed below.\n\n"
			text+="\\begin{table}[h!] \\centering \\label{my-label} \\begin{tabular}{|c|p{11.75 cm}|c|c|}\\hline\n"
			text+="\\multirow{2}{1cm}{Page \\#}& \\multicolumn{1}{|c|}{\\multirow{2}{*}{Description}}  & \\multirow{2}{1.5 cm}{Points Awarded} & \\multirow{2}{1 cm}{Full Points} \\\\   &  &  &\\\\\\hline\n"  

#_________________________________________________________________individual table rows go here__________________________________________________________________
##0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?,7)Your comment(0=wrong not taken care of or couldn't read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[throwAwayStNum].answers[qnum][parameter]
			score=float(0) #calculating the score
			for qnum in range(1,len(questions)):
				score+=float(stDic[throwAwayStNum].answers[qnum][5])
				if stDic[throwAwayStNum].answers[qnum][6]==1 or stDic[throwAwayStNum].answers[qnum][6]==0 : #if diabled then for testing:::Essential piece of code remmeber to tab the below two lines when uncommented
					text+=str(stDic[throwAwayStNum].answers[qnum][0])+"&"+stDic[throwAwayStNum].answers[qnum][1]+" "+stDic[throwAwayStNum].answers[qnum][7]+"&"+str(float(stDic[throwAwayStNum].answers[qnum][5]))+"&"+str(stDic[throwAwayStNum].answers[qnum][3])+"\\\\\\hline\n"

#____________________________________________________ending the table__________________________________________________________________
			text+="\\multicolumn{2}{|c|}{\\multirow{1}{*}{Total for experimental part}} &"+str(score) +"& 40 \\\\\\hline"
			expScore=score
			score+=float(stDic[throwAwayStNum].stationStudent[x].preLab) 

			text+="\\multicolumn{2}{|c|}{\\multirow{2}{*}{\\textbf{Total for Lab}}} &\\multirow{2}{*}{\\textbf{"+str(score) +"}}& \\multirow{2}{*}{\\textbf{50}} \\\\ \\multicolumn{2}{|c|}{}&&\\\\ \\hline\\hline"
			text+="\\end{tabular}\n \\end{table}\n"
			text+="\\clearpage\n" #newPage in Latex

			text+="\\null\\vfill \\begin{center}Prepared by Eranjan Kandegedara\\end{center}  \\clearpage\n\n\n%------------next student-------------------------\n\n" 

			F = open("Scores.csv","a+")
			F.write(stDic[throwAwayStNum].stationStudent[x].Name+";"+stDic[throwAwayStNum].stationStudent[x].preLab+";"+str(expScore)+";"+str(score)+"\n") 
			F.close()		
	return text

def openFileinFoxit(stNum,pgNum):
	os.system('taskkill /IM FoxitReader.exe')  #killing the process so that it does not lag
	path_to_pdf = os.path.abspath(str(stNum)+".pdf")
	# I am testing this on my Windows Install machine
	path_to_foxit = os.path.abspath('C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe') 

	# this will open your document on page 12
	process=subprocess.Popen([path_to_foxit, '/A', 'page='+str(pgNum), path_to_pdf], shell=False, stdout=subprocess.PIPE)
	process.wait()

def openFileinAdobe(stNum,pgNum):
	path_to_pdf = os.path.abspath(str(stNum)+".pdf")
	# I am testing this on my Windows Install machine
	path_to_acrobat = os.path.abspath('C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32') 

	# this will open your document on page 12
	process=subprocess.Popen([path_to_acrobat, '/A', 'page='+str(pgNum), path_to_pdf], shell=False, stdout=subprocess.PIPE)
	process.wait()

def fullmarkButton(throwAwayStNum,qnum):
	global stDic
	global questions
	global explanationOptions
	global exp
	stDic[throwAwayStNum].table[qnum][5].config(background="DodgerBlue2")
	stDic[throwAwayStNum].table[qnum][6].config(text=str(stDic[throwAwayStNum].answers[qnum][3]))
	stDic[throwAwayStNum].answers[qnum][5]=float(str(stDic[throwAwayStNum].answers[qnum][3]))
	stDic[throwAwayStNum].answers[qnum][6]=2 #setting it as a correct answer

def fix(throwAwayStNum,qnum):
	global stDic
	global questions
	global explanationOptions
	global exp

	def subroutine():
		if not kawa.get()==explanationOptions[qnum][0]:
			stDic[throwAwayStNum].answers[qnum][7]=kawa.get() # if the drop down menu says anything other than "get from the text field" then this happens, therefore this is default to the question text
		else: stDic[throwAwayStNum].answers[qnum][7]=correctionText.get() # If it says "get from text field then this happens"
		stDic[throwAwayStNum].table[qnum][5].config(background="DodgerBlue2")
		stDic[throwAwayStNum].table[qnum][6].config(text=str(correctionScore.get()))
		stDic[throwAwayStNum].answers[qnum][5]=float(correctionScore.get())

		if stDic[throwAwayStNum].answers[qnum][5]==stDic[throwAwayStNum].answers[qnum][3]:stDic[throwAwayStNum].answers[qnum][6]=2
		else :stDic[throwAwayStNum].answers[qnum][6]=1
		fixPopup.destroy()

	def giveFullMarks():
		if not kawa.get()==explanationOptions[qnum][0]:
			stDic[throwAwayStNum].answers[qnum][7]=kawa.get() # if the drop down menu says anything other than "get from the text field" then this happens, therefore this is default to the question text
		else: stDic[throwAwayStNum].answers[qnum][7]=correctionText.get() # If it says "get from text field then this happens"
		stDic[throwAwayStNum].table[qnum][5].config(background="DodgerBlue2")
		stDic[throwAwayStNum].table[qnum][6].config(text=str(stDic[throwAwayStNum].answers[qnum][3]))
		stDic[throwAwayStNum].answers[qnum][5]=float(str(stDic[throwAwayStNum].answers[qnum][3]))

		if stDic[throwAwayStNum].answers[qnum][5]==stDic[throwAwayStNum].answers[qnum][3]:stDic[throwAwayStNum].answers[qnum][6]=2
		else :stDic[throwAwayStNum].answers[qnum][6]=1
		fixPopup.destroy()


	qnum=int(qnum) # we get str type from fixCall method
	
#0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]	
	fixPopup=tk.Tk()
	fixPopup.wm_title("Corrections")
	label=ttk.Label(fixPopup,text="The Correct answer: "+questions[qnum][2],font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
	label=ttk.Label(fixPopup,text="My Comments (will appear in pdf unless changed): "+stDic[throwAwayStNum].answers[qnum][7],font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
	label=ttk.Label(fixPopup,text="The Student's answer: "+stDic[throwAwayStNum].answers[qnum][4],font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)	
	label=ttk.Label(fixPopup,text="Text to be displayed: ",font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
#______________________text stuff________________
	sep = ttk.Separator(fixPopup, orient="horizontal")
	sep.pack(side="top", fill="x", pady=10, padx=10)
	correctionText=ttk.Entry(fixPopup) #creates user input field in the popup "popupexp"
	correctionText.insert(0,explanationOptions[qnum][1]) #at the zeroth place the default value which is expName
	correctionText.pack(side="top", fill="x", pady=10, padx=10)
	kawa= tk.StringVar(fixPopup)
	option = ttk.OptionMenu(fixPopup, kawa, explanationOptions[qnum][0], *explanationOptions[qnum])
	option.pack(side="top", fill="x", pady=10, padx=10)
#______________________score stuff_____________________________
	sep = ttk.Separator(fixPopup, orient="horizontal")
	sep.pack(side="top", fill="x", pady=10, padx=10)
	label=ttk.Label(fixPopup,text="Enter score (full marks= "+str(stDic[throwAwayStNum].answers[qnum][3])+"): ",font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
	correctionScore=ttk.Entry(fixPopup) #creates user input field in the popup "popupexp"
	correctionScore.insert(0,"0") #at the zeroth place the default value which is expName
	correctionScore.pack(side="top", fill="x", pady=10, padx=10)

	B1= ttk.Button(fixPopup, text="වෙනස් කරන්න", command=lambda: subroutine())
	B1.pack(side="left", fill="x", pady=10, padx=10)
	B2= ttk.Button(fixPopup, text="වෙනස් කරන්න එපා", command=fixPopup.destroy)
	B2.pack(side="right", fill="x", pady=10, padx=10)
	B3= ttk.Button(fixPopup, text="ෆයිල් එක අරින්න හරි පිටුවට: Adobe", command=lambda: openFileinAdobe(throwAwayStNum,stDic[throwAwayStNum].answers[qnum][0]))
	B3.pack(side="bottom", fill="x", pady=10, padx=10)
	B4= ttk.Button(fixPopup, text="ෆයිල් එක අරින්න හරි පිටුවට: Foxit", command=lambda: openFileinFoxit(throwAwayStNum,stDic[throwAwayStNum].answers[qnum][0]))
	B4.pack(side="bottom", fill="x", pady=10, padx=10)
	B5= ttk.Button(fixPopup, text="Give Full Marks", command=lambda: giveFullMarks())
	B5.pack(side="bottom", fill="x", pady=10, padx=10)
	fixPopup.mainloop()

def nextStation(currSt):
	global z
	# number 0 is the start page
	mainWindow.show_frame(app,z[(currSt+1)%13])

def previousStation(currSt):
	# number 0 is the start page
	global z
	if currSt==0:currSt=13
	mainWindow.show_frame(app,z[currSt-1])

def tabDlimitWed():
	global wednesdayStudents
	F = open("wednesdayStudents.csv","w")
	for x in range(1,len(wednesdayStudents)-1):
		F.write(wednesdayStudents[x][0]+"\n") 
	F.close()
	print("Saved as wednesdayStudents.csv")

def tabDlimitThu():
	global thursdayStudents
	F = open("thursdayStudents.csv","w")
	for x in range(1,len(thursdayStudents)-1):
		F.write(thursdayStudents[x][0]+"\n") 
	F.close()
	print("Saved as thursdayStudents.csv")

class station(tk.Frame):
	global experimentNames
	global students
	global exp
	global stDic
	def __init__(self, parent, controller,stationName):
		global stDic
		global questions
		global exp
		myClassName=stationName
		throwAwayStNum=throwAwayCalculation(myClassName)
		try: # just in case station or ex are not yet instatiated
			tk.Frame.__init__(self,parent)
			#setting the grid
			self.grid_columnconfigure(0, weight=1)
			self.grid_columnconfigure(1, weight=1)
			self.grid_columnconfigure(2, weight=2)
			self.grid_columnconfigure(3, weight=0)
			self.grid_columnconfigure(4, weight=2)
			self.grid_columnconfigure(5, weight=1)
			rownumbers=10+len(questions)
			for x in range(0, rownumbers):
				self.grid_rowconfigure(x, weight=1)
			x=0 #resetting x to be reused

			stationLabel=tk.Label(self,text=stDic[throwAwayStNum].Name.capitalize(),font=LARGE_FONT) #,background="indian red"
			stationLabel.grid(row=x, column=0, columnspan=6, pady=10 , padx=10, sticky="nsew")
			x+=1 # increment row to use with grid


			temp1=[]
			temp2=[]
			temp3=[]
			for y in range(0,len(students)): #making lists for student names for the dropdownlists
				temp1.append(students[y][0])
				temp2.append(students[y][0])
				temp3.append(students[y][0])

			label=tk.Label(self,text="Student Name")
			label.grid(row=x, column=2, pady=0 , padx=10, sticky="nsew")
			label=tk.Label(self,text="Prelab")
			label.grid(row=x, column=3, pady=0 , padx=10, sticky="nsew")
			label=tk.Label(self,text="  Eranjan\nKandegedara",  background="royal blue", foreground="orange")
			label.grid(row=x, column=4, rowspan=4, pady=10 , padx=10, sticky="nsew")
	
#trying to go to next station
			previousPage=tk.Button(self,text="<Prev\n  St.", background="royal blue", command=lambda: previousStation(throwAwayStNum))
			previousPage.grid(row=x, column=0, rowspan=4, pady=10 , padx=10, sticky="nsew")
			nextPage=tk.Button(self,text="Next\n  St. >", background="royal blue", command=lambda: nextStation(throwAwayStNum))
			nextPage.grid(row=x, column=5, rowspan=4, pady=10 , padx=10, sticky="nsew")
			x+=1 # increment row to use with grid

			student1Label=tk.Label(self,text="Student 1:")
			student1Label.grid(row=x, column=1, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].student1Name = tk.StringVar(self)
			option1 = ttk.OptionMenu(self, stDic[throwAwayStNum].student1Name, stDic[throwAwayStNum].stationStudent[1].Name, *temp1) # since student names are teh items in the temp list use this for the default value
			option1.grid(row=x, column=2, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].preLab1Options = tk.StringVar(self)
			choices = ['','0','1', '2','3','4','5','6','7','8','9','10']
			option = ttk.OptionMenu(self, stDic[throwAwayStNum].preLab1Options, choices[11], *choices)
			option.grid(row=x, column=3, sticky="nsew")
			if stDic[throwAwayStNum].student1Name.get()=="Could not get name automatically":option1['menu'].config(background="red")
			x+=1 # increment row to use with grid

			student2Label=tk.Label(self,text="Student 2:")
			student2Label.grid(row=x, column=1, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].student2Name = tk.StringVar(self)
			option2 = ttk.OptionMenu(self, stDic[throwAwayStNum].student2Name, stDic[throwAwayStNum].stationStudent[2].Name, *temp2) # since student names are teh items in the temp list use this for the default value
			option2.grid(row=x, column=2, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].preLab2Options = tk.StringVar(self)
			option = ttk.OptionMenu(self, stDic[throwAwayStNum].preLab2Options, choices[11], *choices)
			option.grid(row=x, column=3, sticky="nsew")
			if stDic[throwAwayStNum].student2Name.get()=="Could not get name automatically":option2['menu'].config(background="red")
			x+=1 # increment row to use with grid

			student3Label=tk.Label(self,text="Student 3:")
			student3Label.grid(row=x, column=1, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].student3Name = tk.StringVar(self)
			option3 = ttk.OptionMenu(self, stDic[throwAwayStNum].student3Name, stDic[throwAwayStNum].stationStudent[3].Name, *temp3) # since student names are teh items in the temp list use this for the default value
			option3.grid(row=x, column=2, pady=0 , padx=0, sticky="nsew")
			stDic[throwAwayStNum].preLab3Options = tk.StringVar(self)
			option = ttk.OptionMenu(self, stDic[throwAwayStNum].preLab3Options, choices[11], *choices)
			option.grid(row=x, column=3, sticky="nsew")
			if stDic[throwAwayStNum].student3Name.get()=="Could not get name automatically":option3['menu'].config(background="red")
			x+=1 # increment row to use with grid

			sep = ttk.Separator(self, orient="horizontal")
			sep.grid(row=x, column=0, columnspan=6, sticky="nsew", pady=0 , padx=10)
			x+=1 # increment row to use with grid

			if stDic[throwAwayStNum].student1Name.get()==students[len(students)-1][0]:student1Label.config(background="red")
			if stDic[throwAwayStNum].student2Name.get()==students[len(students)-1][0]:student2Label.config(background="red")
			if stDic[throwAwayStNum].student3Name.get()==students[len(students)-1][0]:student3Label.config(background="red")

			tableLabel=tk.Label(self,text="Page", cursor="shuttle")
			tableLabel.grid(row=x, column=0, pady=0 , padx=10, sticky="nsew")
			tableLabel=tk.Label(self,text="Bullet")
			tableLabel.grid(row=x, column=1, pady=0 , padx=10, sticky="nsew")
			tableLabel=tk.Label(self,text="Question")
			tableLabel.grid(row=x, column=2, pady=0 , padx=10, sticky="nsew")
			tableLabel=tk.Label(self,text="Fullpoints")
			tableLabel.grid(row=x, column=3, pady=0 , padx=10, sticky="nsew")
			tableLabel=tk.Label(self,text="Students answer")
			tableLabel.grid(row=x, column=4, pady=0 , padx=10, sticky="nsew")
			tableLabel=tk.Label(self,text="Marks")
			tableLabel.grid(row=x, column=5, pady=0 , padx=10, sticky="nsew")
			x+=1 # increment row to use with grid
			sep.grid(row=x, column=0, columnspan=6, sticky="nsew", pady=0 , padx=10)
			x+=1 # increment row to use with grid


#---------------------------populting the configuration table for each station------------------------
			stDic[throwAwayStNum].table=[]
			stDic[throwAwayStNum].table.append([0,"Page","Bullet","Question","Full points","Studnet Answer","Marks Given"])
			qnumSave=[0]
			for qnum in range(1,len(questions)):
				#twice appending so that we can start with index1
				stDic[throwAwayStNum].table.append([0,"Page","Bullet","Question","Full ponts","Studnet Answer","Marks Given"]) 
				qnumSave.append(qnum)
#0)page number,1)bullet number,2)Question,3)full marks,4)answer,5)marks given,6)answer correct?, 7) Your comment [for 6:=0=wrong not taken care of or couldnt read properly,1=wrong taken care of,2=correct and taken care of) ex: stDic[stNum].answers[questionNum][parameter]
				if len(stDic[throwAwayStNum].answers[qnum][2])>120: textToDisplay="Too Large to Display"
				else:textToDisplay=stDic[throwAwayStNum].answers[qnum][2]
	
				stDic[throwAwayStNum].table[qnum][1]=tk.Label(self,text=str(stDic[throwAwayStNum].answers[qnum][0]))
				stDic[throwAwayStNum].table[qnum][2]=tk.Label(self,text=stDic[throwAwayStNum].answers[qnum][1])
				stDic[throwAwayStNum].table[qnum][3]=tk.Label(self,text=textToDisplay)

				#stDic[throwAwayStNum].table[qnum][4]=tk.Label(self,text=str(stDic[throwAwayStNum].answers[qnum][3]))
				stDic[throwAwayStNum].table[qnum][4]=tk.Button(self,text=str(stDic[throwAwayStNum].answers[qnum][3]), command=lambda j=qnum: fullmarkButton(throwAwayStNum,j))

				stDic[throwAwayStNum].table[qnum][6]=tk.Label(self,text=str(stDic[throwAwayStNum].answers[qnum][5]))

				if len(stDic[throwAwayStNum].answers[qnum][4])>35: textToDisplay="Too Large to Display"
				else:textToDisplay=stDic[throwAwayStNum].answers[qnum][4]
				
				if stDic[throwAwayStNum].answers[qnum][6]==2:stDic[throwAwayStNum].table[qnum][5]=tk.Button(self,text=textToDisplay, background="green2", command=lambda j=qnum: fix(throwAwayStNum,j))
				elif stDic[throwAwayStNum].answers[qnum][6]==1:stDic[throwAwayStNum].table[qnum][5]=tk.Button(self,text=textToDisplay, background="orange", command=lambda j=qnum: fix(throwAwayStNum,j))
				else:stDic[throwAwayStNum].table[qnum][5]=tk.Button(self,text=textToDisplay, background="red", command=lambda j=qnum: fix(throwAwayStNum,j))

				stDic[throwAwayStNum].table[qnum][1].grid(row=x, column=0, pady=0 , padx=0, sticky="nsew")
				stDic[throwAwayStNum].table[qnum][2].grid(row=x, column=1, pady=0 , padx=0, sticky="nsew")
				stDic[throwAwayStNum].table[qnum][3].grid(row=x, column=2, pady=0 , padx=0, sticky="nsew")
				stDic[throwAwayStNum].table[qnum][4].grid(row=x, column=3, pady=0 , padx=0, sticky="nsew")
				stDic[throwAwayStNum].table[qnum][5].grid(row=x, column=4, pady=0 , padx=0, sticky="nsew")
				stDic[throwAwayStNum].table[qnum][6].grid(row=x, column=5, pady=0 , padx=0, sticky="nsew")

				x+=1 # increment row to use with grid
		except:pass


app=mainWindow()
app.geometry("1000x900")
app.mainloop()