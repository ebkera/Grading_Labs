import re #importing regualr expressions

"""good if everyting is returned in all the classes in this file"""
#[x:y] this means take characters starting form before x(therefore includes x) and ending before y(therefore does not include y)
class retainString(object):
	def afterBackEnd(retain,s):
		chopHere=retain.find(s)+(len(s)-1)
		var=True
		while var:
			if retain[chopHere+1]==" ":chopHere+=1
			else: var=False
		return retain[chopHere+1:len(retain)]

	def afterFrontEnd(retain,s):return retain[retain.find(s):len(retain)]
	def beforeBackEnd(retain,s):return retain[0:retain.find(s)+len(s)]
	def beforeFrontEnd(retain,s):return retain[0:retain.find(s)]

class checkString(object):
	global trueCheck
	global falseCheck
	global negativeCheck
	global positiveCheck
	#update here
	trueCheck=["correct","t","true"]
	falseCheck=["wrong","incorrect","f","false"]
	negativeCheck=["neg","n","negative"]
	positiveCheck=["pos","p","positive"]

	def isStringTrue(self):
		global trueCheck
		if self.lower().strip() in trueCheck: return True
		else:return False

	def isStringFalse(self):
		global falseCheck
		if self.lower().strip() in falseCheck: return True
		else:return False

	def isStringPositive(self):
		global positiveCheck
		if self.lower().strip() in positiveCheck: return True
		else:return False

	def isStringNegative(self):
		global negativeCheck
		if self.lower().strip() in negativeCheck: return True
		else:return False

	def containsString(checkIfThis,containsThis):

		"""checkIfThis=a string, containsThis= a list of strings  
		**** will only work for a list of strings and not for a single string. if the single string contains only one char then that is also fine"""

		for x in containsThis:
			if x.lower() in checkIfThis.lower():
				return True
		return False

	def findInThisOrder(checkIfThis,containsThis):

		"""checkIfThis=a string, containsThis= a list of a list of strings where we check if the checkifThis has it in that particular order
		**** will only work for a list of strings and not for a single string. if the single string contains only one char then that is also fine"""
		checkIfThis.find(containsThis)
		for x in containsThis:
			if x.lower() in checkIfThis.lower():
				return True
		return False

	def regExSearch(checkIfThis,containsThis):
		"""checkIfThis=a string, containsThis= a list of strings """
		checkIfThis=checkIfThis.lower()
		containsThis=containsThis.lower()
		p = re.compile(containsThis)
		m = p.search(checkIfThis)
		return m