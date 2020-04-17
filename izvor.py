from urllib.request import urlopen as uReq #pip
from bs4 import BeautifulSoup as Soup #pip
from os import system, name 
import requests #pip
import random
import time



################################################################################
#Url kod

links = set({})

#funkcija koja će biti korištena za ekstrakciju linka
def url_extractor (my_url, automode):

	secure = ""    #dio linka sa http ili https
	source = ""    #source link (tipa www.google.com)
	pagedown = ""  #link jednu stranicu ispod trenutnog linka

	#Određivanje je li link http ili https
	if my_url[0:5] == "https":
		secure = my_url[0:6]

	elif my_url[0:5] == "http:":
		secure = my_url[0:5]

	#Izdvajanje source linka i stranice ispod
	cnt = 0;
	slash_num = my_url.count("/")
	for letter in my_url:
		
		if letter == "/" :
			cnt += 1
		
		if cnt == slash_num and slash_num != 2:
			break
		
		elif cnt == 2 and letter != "/":
			source += letter
		
		elif cnt > 2:
			pagedown += letter

	links.add(secure + "//" + source)

	#Skidanje informacija sa stranice
	uClient = uReq(my_url)
	page = uClient.read()
	uClient.close()

	#izdvajanje linkova iz stranice
	page_soup = Soup(page, "html.parser")

	unformat = ""

	for link in page_soup.findAll('a'):
		unformat = str(link.get('href'))

		#formatiranje linkova
		if unformat[0:4] == "http":
			pass
		
		elif unformat[0:11] == "javascript:" or unformat[0:4] == "None" or len(unformat) < 3:
			continue

		elif unformat[0] == "/" :
			if unformat[1] == "/" :
				unformat = secure + unformat
			else:
				unformat = secure + "//" + source + unformat
		
		elif unformat[0:1] == "./":
			unformat = unformat.replace(".", "", 1)
			unformat = secure + "//" + source + pagedown + unformat
		
		elif unformat[0] == "#":
			unformat = unformat.replace("#", "", 1)
			unformat = secure + "//" + source + pagedown + "/" + unformat
		
		elif unformat[0:3] == "../" :
			unformat = secure + "//" + source + "/" + unformat

		else:
			unformat = secure + "//" + source + "/" + unformat
		
		links.add(unformat)

	url_picker(automode)
	return


#Odabir sljedećega linka
def url_picker (automode):
	if automode == 1:
		tekst = random.choice(tuple(links))
		my_url = str(tekst)
		
		postoji = url_checker(my_url)
		
		if postoji == 1:
			global repeat

			if repeat > 0:
				url_extractor(my_url, automode)
				repeat -= 1
			
			else:
				print("Want to see the list? (y/n)")
				c = Question(0)
			
				if c == 1:
					print("Links:")
					for link in links:
						print(link)
			
				else:
					pass
			
				print("Proceed? (y/n)")
				c = Question(0)
			
				if c == 1:
					return	
					url_extractor(my_url, automode)
			
				else:
					print ("Switch to manual? (y/n)")
					a = Question(0)
					
					if a == 1:
						print("\n Converting the list...")
						time.sleep(0.2)
						print("Switching to manual... \n")
						time.sleep(0.2)
						
						automode = 0
						url_picker(automode)
						return
					
					else:
						pass
					return
		else:
			url_picker(automode)
			return

	else:
		#odabiranje linka
		lista = list(links)
		i = 0
		print("Links:")
		for link in links:
			i += 1
			print(i,": ", link)
		
		print("Proceed? (y/n)")
		
		c = Question(0)
		if c == 1:
			print("Enter the number of a link you want me to go to next")
			my_url = lista[int(input())-1]
			url_extractor (my_url, automode)
			return
		
		else:
			print ("Switch to auto? (y/n)")
			a = Question(0)
			if a == 1:
				print("\n")
				print("Converting the list...")
				time.sleep(0.7)
				print("Switching to auto...")
				print("\n")
				time.sleep(0.7)
				print("\n")
				
				automode = 0
				url_picker(automode)
				return
			
			else:
				pass
			return


#Provjera linka
def url_checker (link):
	request = requests.get(link)
	if request.status_code < 400:
	  return 1  
	else:
		return 0



######################################################################################
######################################################################################
#Animation related stvari

#3 dots console animation
def console_dots (duration, lb_duljina):
	duration = duration - 0.5
	time.sleep(0.5)
	
	#definiranje animacije
	length = int(duration / 1.5)
	
	#1,5 sekunde za jedan krug
	for y in range(length):
		for x in range(3):
			print('.', end = '', flush = True)
			time.sleep (1/3)
		for x in range(3):
			clear()
			print('.' * (3 - x))
	clear ()
	print ("\n")
	line_breaker (lb_duljina)

#Clear screen funkcija
def clear(): 
  #windows 
  if name == 'nt': 
    _ = system('cls') 

  #Mac & Linux (posix) 
  else: 
    _ = system('clear') 

#Crta
def line_breaker (duljina):
	
	sleeptime = 0.000625 * duljina

	for x in range(duljina):
		print('-', end = '', flush = True)
		time.sleep(sleeptime)
	print("\n")



######################################################################################
#Text stvari

#Help function
def Help ():
	console_dots(3.5, 40)
	print("\r\nHelp tab:")
	print("\nChoose an option")
	print("0: Automode and Manual mode explained")
	print("1: URL inserting help")
	print("\nChoose an option:")

	mode = int(input())

	print("\nLoading...")
	time.sleep(1.5)

	if mode == 0:
		print("\nManual mode allows you to choose which links I will go to while scraping")
		time.sleep(3)
		print("Auto mode makes me run autonomously, and choose randomly which links i want to go to")
		time.sleep(3)
		print("You can change between modes whenever you want, by telling me to stop")
		time.sleep(3)
		print("If i am in auto, you can type 'stop' or 'halt' and i will stop")
		time.sleep(3)
		print("After you do that it will ask you if you want to switch to the other mode")

	if mode == 1:
		print("\nYou have to insert a link that I will start scraping from")
		time.sleep(3)
		print("When you write the link you must write it whole")
		time.sleep(3)
		print("By that i mean that you should write https://www.google.com instead of something shortened")
		time.sleep(3)
		print("For example www.google.com is wrong, and so is https://google.com")
		time.sleep(3)
		print("If you write it wrong I will run into errors and halt")

	print("\r\nEnd of the help line, thanks for listening\n")
	return


#Automode alert
def AutoAlert ():
	print("\nYou are about to atart automode, during that preiod, the program could wander anywhere over the internet")
	print ("if you say yes, you are taking all the responsibility on what happenes during that time, do you agree to that?\n")
	c = Question(0)
	if c == 1:
		return 1
	else:
		return 0

#Automode repeater
def Repeater ():
	print ("\nHow many links do you want the automode to visit?\n")
	c = input()
	c = c.strip()
	c = c.lower()
	if c == 'help':
		Help()
		f = Repeater()
		return f
	else:
		rpt = int(c)
		return rpt

#Yes/No pitanja
def Question (mode):
	odg = str(input())
	odg = odg.strip()
	odg = odg.lower()
	
	#tip pitanja
	#mode 0 = yes/no
	#mode 1 = manual/auto

	if mode == 0:
		slovo1 = "y"
		option1 = "yes"
		slovo2 = "n"
		option2 = "no"
	
	elif mode == 1:
		slovo1 = "a"
		option1 = "auto"
		slovo2 = "m"
		option2 = "manual"
	
	if odg == slovo1 or odg[0] == slovo1:
		return 1
	
	elif odg == slovo2 or odg[0] == slovo2:
		return 0
	
	else:
		print("\n")
		if odg == "help":
			Help()
			print("Now please choose ", option1, " or ", option2)
		else:
			print("Please choose ", option1, " or ", option2)

		f = Question(mode)
		return f



######################################################################################
#program starter
console_dots(6.5, 80)
print("Do you want the program to run the program manually, or in automode? (m/a)\n")
auto = Question(1)

if auto == 1:
	auto = AutoAlert()

if auto == 1:
	repeat = Repeater()

console_dots(3.5, 40)
print("Insert URL:\n")

tekst = str(input())
tekst = tekst.strip()

url_extractor(tekst, auto)

######################################################################################
