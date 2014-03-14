from bs4 import BeautifulSoup #for sch parsing
import copy #for Object list cloning
from circuithub.settings import BASE_DIR
import os

#main function is in this file is schParse. it returns a tuple

class Component:
	def __init__(self, value="", kind="", subtype="", name="", model=""):
		self.value = value
		self.type = kind #possible values: RLC, BJT, Diode, Misc
		self.subtype = subtype
		self.name = name
		self.model = model

	#prints all data excluding amount
	def printData(self): 
		print "name=" + self.name + " type=" + self.type + " subtype=" + \
		self.subtype + " value=" + self.value + " model=" + self.model

	#prints all data including amount
	def printDataAmount(self):
		print "name=" + self.name + " type=" + self.type + " subtype=" + \
		self.subtype + " value=" + self.value + " model=" + self.model + \
		" amount=" + str(self.amount)

def isNum(char):
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	count=0
	for i in numbers:
		if char!=i: count=count+1
	if count==10:
		return False
	return True


#case insensitive; searches for a model match and returns the price
#if no model match, returns -1
#usage: findPrice("1n4148", "pricelist.csv")
def findPrice(modelname, filename):
	prices = []
	with open(os.path.join(BASE_DIR,filename)) as data_file:
	   for line in data_file:
	      prices.append(line.strip().split(','))
	if (modelname.lower()=="resistor" or modelname.lower()=="inductor" or modelname.lower()=="capacitor"):
		for i in range(0, len(prices)):
			if prices[i][1].lower()==modelname.lower(): return float(prices[i][3])
	else:
		for i in range(0, len(prices)):
			if prices[i][2].lower()==modelname.lower(): return float(prices[i][3])
	return 0
#print findPrice("1N4148", "pricelist.csv")

#inputs to this can be of the form:
#	<float or integer><multiplier><optional: F or H>
#	<integer><multiplier><integer><optional: F or H>
#where multiplier is 'M', 'u', etc
#returns the integer value of that string
#ex.: realValue(4k4) and realValue(4.4k) both return 4400
def realValue(string):
	if string=="":
		return 0
	if string[len(string)-1]=='F': string=string[0:len(string)-1] #remove farad
	if string[len(string)-1]=='H': string=string[0:len(string)-1] #remove henry
	newstring=string

	#if string is found to be not a number (e.g. "NA"), returns the string
	count=0;
	for i in range(0, len(string)):
		if isNum(string[i])==False and string[i]!='.':
			count=count+1
	if (count>=2):
		return string

	for i in range(0, len(string) - 1):
		if (isNum(string[i]))==False and string[i]!='.':
			newstring=string[0:i] + '.' + string[i+1:len(string)] + string[i]
	#at this point, newstring is of the form <integer or float><multiplier>
	notNum=False
	multiplier = 1
	if isNum(newstring[len(newstring)-1])==False:
		if newstring[len(newstring)-1]=='p': multiplier=0.000000000001
		elif newstring[len(newstring)-1]=='n': multiplier=0.000000001
		elif newstring[len(newstring)-1]=='u': multiplier=0.000001
		elif newstring[len(newstring)-1]=='m': multiplier=0.001
		elif newstring[len(newstring)-1]=='k': multiplier=1000
		elif newstring[len(newstring)-1]=='K': multiplier=1000
		elif newstring[len(newstring)-1]=='M': multiplier=1000000
		else: multiplier = 1
		realValue = float(newstring[0:len(newstring)-1]) * multiplier
	else:
		realValue = float(newstring[0:len(newstring)])
	return realValue

#given a parts array and the indices of the parts you want to compare,
#returns true if the parts in those indices are equivalent
def partsEqualityCheck(parts, i, j):
	if (parts[i].type==parts[j].type) and (parts[i].subtype==parts[j].subtype) and \
	(parts[i].model==parts[j].model) and \
	realValue(parts[i].value) == realValue(parts[j].value):
		return True
	return False


def collapseParts(parts):
	for i in range(0, len(parts)):
		parts[i].amount = 1 #initialize amount to 1
	i=0
	j=1
	while (i < len(parts)):
		popped = False
		while (j < len(parts)):
			if partsEqualityCheck(parts,i,j)==True:
				parts[i].amount = parts[i].amount + parts[j].amount
				parts.pop(j)
				popped = True
			j=j+1
		if popped==False: i=i+1
		j=i+1
	return parts


#notes:
#	parser supports the rcl, transistor, and diode libraries, all other parts will be under Misc
#
def schParts(filename):
	soup = BeautifulSoup(filename).parts
	#soup = soup.parts
	plist = soup.find_all('part')
	parts = []
	for i in range(0, len(plist)):
		append = False
		#note, you won't append all the time because some "parts" aren't real (e.g. GND)
		if (plist[i]["library"] == "rcl" or plist[i]["library"] == "resistor"): #rcl parser
			name = plist[i]["name"]
			value = plist[i]["value"]
			kind = "RLC"
			subtype = plist[i]["deviceset"][0]
			model = ""
			if plist[i]["deviceset"][0].encode('ascii','ignore').lower()=='r': model="Resistor"
			elif plist[i]["deviceset"][0].encode('ascii','ignore').lower()=='c': model="Capacitor"
			elif plist[i]["deviceset"][0].encode('ascii','ignore').lower()=='l': model="Inductor"
			append = True
		elif (plist[i]["library"] == "transistor"): #transistor parser
			name = plist[i]["name"]
			value = ""
			kind = "BJT"
			subtype = ""
			model = plist[i]["deviceset"]
			append = True
		elif (plist[i]["library"] == "diode"): #diode parser
			name = plist[i]["name"]
			value = ""
			kind = "Diode"
			subtype = ""
			model = plist[i]["deviceset"]
			append = True
		elif (plist[i]["library"]!="frames" and plist[i]["library"]!="supply1" and plist[i]["library"]!="supply2"): #misc parser
			name = plist[i]["name"]
			value = ""
			kind = "Misc"
			subtype = plist[i]["library"]
			model = plist[i]["deviceset"]
			append = True
		if append==True:
			newPart = Component(value, kind, subtype , name, model) 
			parts.append(newPart)
	parts.sort(key=lambda x: x.name)
	parts.sort(key=lambda x: x.type)
	partslist = copy.deepcopy(parts) #clone the parts array
	partslist = collapseParts(partslist)
	return parts, partslist
	#parts is a list of objects of the class Component
	#partslist is a collapsed version of parts (i.e. it has an amount field)


#run this for debugging purposes
def debugger():
	(a,b)=schParts('testSCH.sch')
	for i in range(0, len(a)):
		a[i].printData()
	print ('\n \n \n')
	for i in range(0, len(b)):
		b[i].printDataAmount()

#debugger()







