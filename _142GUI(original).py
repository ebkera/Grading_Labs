#importing tkinter stuff
import tkinter as tk
import os #used to write to the system shell
from tkinter import ttk ##To make the windows look better (for example the buttons look better. this is like css for tikinter)

class station():
	def  __init__(self, name1, name2, name3):
		self.name1=name1
		self.name2=name2
		self.name3=name3
		self.stationNumber=stationNumber

def popupmsg(msg):
	popup=tk.Tk()
	popup.wm_title("Message!")
	label=ttk.Label(popup,text=msg,font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
	B1= ttk.Button(popup, text="හරි", command=popup.destroy)
	B1.pack()
	popup.mainloop()
	

def stationCreate(x,b):
	if bin:
		popup=tk.Tk()
		popup.wm_title("Message!")
		label=ttk.Label(popup,text="This was teh test",font=NORM_FONT)
		label.pack(side="top", fill="x", pady=10, padx=10)
		B1= ttk.Button(popup, text="හරි", command=popup.destroy)
		B1.pack()
		popup.mainloop()
	else:
		pass

def compileInPython(filenumber):
	if filenumber==1:
		os.chdir('C:\\Users\\Eranjan\\OneDrive\\Research\\Keithley IV controller at Device Testing Lab\\The IV controller project')
		os.system('python GUItest.py')

	elif filenumber==2:
		os.chdir('C:\\Users\\Eranjan\\Desktop')
		os.system('python myMail.py')

def chooseExp(msg):
	popup=tk.Tk()
	popup.wm_title("Choose an Experiment")
	label=ttk.Label(popup,text=msg,font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10, padx=10)
	B1= ttk.Button(popup, text="හරි", command=popup.destroy)
	B1.pack()
	popup.mainloop()

def heading(day, month, date, sem, year):
	"""\\begin{table}[h]
\\centering
\\begin{tabular}{c}
PHYS 142 - Computer based lab feedback form\\\\
Lab Title: Diffraction\\\\
Date:"""

	if date==1:
		g="st"
	elif date==2:
		g="nd"
	elif date==3:
		g="rd"
	else:
		g="th"
	text=heading.__doc__+day+" "+month+" "+date+"$^{"+g+"}$ "+sem+" "+year+" \\\\\\hline\n"
	text+="\\end{tabular}\n"
	text+="\\end{table}"	
	return text 

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

"""

	textToWrite=preamble.__doc__
	return textToWrite

def body():
	"""
This is the body of the file
\\end{document}
"""
	textToWrite=body.__doc__
	return textToWrite

def compile():
	pass

def load():
	#pullData = open("code.txt","r").read()
	#print(pullData)
	te=preamble()
	te3=heading("Wednesday","May","16","Summer","2017")
	te2=body()
	f = open('The_File.tex', 'w')
	final=te+te3+te2
	f.write(final)
	f.close()
	os.system('pdflatex The_File.tex')
	os.system('The_File.pdf')
		
LARGE_FONT=("Times New Roman",12)
NORM_FONT=("Times New Roman",10)
SMALL_FONT=("Times New Roman",8)

app=tk.Tk()
app.title("එරන්ජන්ගේ 142 ලැබ් එකේ ලකුණු දැමීම පහසු කරගැනීමට හදපු මෘදුකාංගය")
app.geometry("800x500")  # the size of our application
#tk.Tk.iconbitmap(app, default="logo.ico")


menubar=tk.Menu(app) #adding the menu bar		
#The "File" menu Option
filemenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
filemenu.add_command(label="New Grading", command=lambda:  load()) #labmda si a throwaway function and it makes the function not run immediately	
#filemenu.add_separator()
filemenu.add_command(label="Exit",underline=0, command=quit, accelerator="Ctrl+Q")
menubar.add_cascade(label="File", menu=filemenu)

#The "Edit" menu Option		
runMenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
runMenu.add_command(label="Compile and run", command=lambda: popupmsg("තාම වැඩ ඉවර නෑ!!"))
runMenu.add_command(label="Open PDf", command=lambda: IVinitPopup())
menubar.add_cascade(label="Run", menu=runMenu)
		
#The "Help" menu Option		
helpMenu=tk.Menu(menubar, tearoff=0) #tearing off enables you to literally tear off this manu from the menu bar
helpMenu.add_command(label="Documentation", command=lambda: popupmsg("තාම වැඩ ඉවර නෑ!!"))
menubar.add_cascade(label="Help", menu=helpMenu)		

# tk.Tk.bind("<Key>", key)
app.bind("<Control-q>", quit)
tk.Tk.config(app, menu=menubar)

#app.pack(side="top", fill="both", expand= True)	#"fill" will fill in the space that you have alloted to pack, expand tells it to what ever the pack is just expand that to the entire window
app.grid_columnconfigure(0,weight=1) #
app.grid_columnconfigure(1,weight=0) #
app.grid_columnconfigure(2,weight=0) #

totalRows=12
totalCoumns=3

for x in range(0,totalRows+1):
	app.grid_rowconfigure(x,weight=1) #0 is the minimum size, weight is for the priority

label=tk.Label(app,text="ලේසි වෙන්න මේක පාවිච්චි කරන්න ")
label.grid(row=0, column=0, columnspan=2, sticky="nsew")

label=tk.Label(app,text="Station Number")
label.grid(row=0, column=0, columnspan=2, sticky="nsew")

for x in range (0,totalRows):
	label=tk.Label(app,text=x+1)
	label.grid(row=x+1, column=0, columnspan=2, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(1, True))
buttonGO1.grid(row=1, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(2, True))
buttonGO1.grid(row=2, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(3, True))
buttonGO1.grid(row=3, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(4, True))
buttonGO1.grid(row=4, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(5, True))
buttonGO1.grid(row=5, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(6, True))
buttonGO1.grid(row=6, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(7, True))
buttonGO1.grid(row=7, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(8, True))
buttonGO1.grid(row=8, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(9, True))
buttonGO1.grid(row=9, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(10, True))
buttonGO1.grid(row=10, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(11, True))
buttonGO1.grid(row=11, column=1, sticky="nsew")
buttonGO1= ttk.Button(app, text="හරි", command=lambda: stationCreate(12, True))
buttonGO1.grid(row=12, column=1, sticky="nsew")

buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(1,False))
buttonRE1.grid(row=1, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(2,False))
buttonRE1.grid(row=2, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(3,False))
buttonRE1.grid(row=3, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(4,False))
buttonRE1.grid(row=4, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(5,False))
buttonRE1.grid(row=5, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(6,False))
buttonRE1.grid(row=6, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(7,False))
buttonRE1.grid(row=7, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(8,False))
buttonRE1.grid(row=8, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(9,False))
buttonRE1.grid(row=9, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(10,False))
buttonRE1.grid(row=10, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(11,False))
buttonRE1.grid(row=11, column=2, sticky="nsew")
buttonRE1= ttk.Button(app, text="රි", command=lambda: stationCreate(12,False))
buttonRE1.grid(row=12, column=2, sticky="nsew")

app.after(1000)
app.mainloop()

