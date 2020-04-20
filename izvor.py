from urllib.request import urlopen as uReq    #pip
from colorama import init, Fore, Style        #pip
from bs4 import BeautifulSoup as Soup         #pip
from os import system, name 
from time import sleep
import requests                               #pip
import random


#----------------------------------------Url--------------------------------------------

#funkcija koja će biti korištena za ekstrakciju linka
def url_extractor (my_url):
	global links
	
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

	url_picker()
	return


#Odabir sljedećega linka
def url_picker ():
	global automode
	global repeat

	#Za automode
	if automode == 1:
		#Odabiranje nasumičnog linka
		tekst = random.choice(tuple(links))
		my_url = str(tekst)
		
		#provjera postojanja
		postoji = url_checker(my_url)
		
		if postoji == 1:
			if repeat > 0:
				repeat -= 1
				url_extractor(my_url)
				
			else:
				line_breaker(40)
				print("\nWant to see the list? (y/n)")
				c = Question(0)
			
				if c == 1:
					print("\nLinks:\n")
					for link in links:
						print("   ", link)
			
				else:
					pass
			
				print("\nProceed? (y/n)")
				c = Question(0)
			
				if c == 1:
					url_extractor(my_url)
					return
			
				else:
					print ("\nSwitch to manual? (y/n)")
					a = Question(0)
					
					if a == 1:
						print("\nConverting the list...")
						sleep(0.2)
						print("Switching to manual... \n")
						sleep(0.2)
						
						automode = 0
						url_picker()
						return
					
					else:
						pass
					return
		else:
			url_picker()
			return

	#Bez automodea
	else:
		#Odabiranje linka
		line_breaker(40)

		lista = list(links)
		i = 0
		print("Links:")
		for link in links:
			i += 1
			print(i,": ", link)
		
		print("\nProceed? (y/n)")
		
		c = Question(0)
		if c == 1:
			print("\nEnter the number of a link you want me to go to next")
			print(Fore.YELLOW, end = ' ')
			my_url = lista[int(input())-1]
			print(Fore.GREEN, end = '')
			url_extractor (my_url)
			return
		
		else:
			print ("\nSwitch to automode? (y/n)")
			a = Question(0)
			if a == 1:
				print("\nConverting the list...")
				sleep(0.7)
				print("Switching to automode...\n")

				line_breaker(40)
				Repeater()

				automode = 1
				url_picker()
				return
			
			else:
				pass
			return


#----------------------------------------Misc--------------------------------------------

#Provjera linka
def url_checker (link):
	request = requests.get(link)
	if request.status_code < 400:
		return 1  
	else:
		return 0

#Funkcija za kratice (dodavat ću ih kasnije, ovo su sada samo da nemoram ja svaki put pisat cijeli link dok testiram)
def url_shortcut (tekst):
	tekst.lower()
	
	if tekst.lower() == "help":
		Help()
		tekst = "0"

	elif tekst == "":
		tekst = "0"
	
	elif tekst.lower() == "google":
		tekst = "https://www.google.com"
	
	elif tekst.lower() == "youtube":
		tekst = "https://www.youtube.com"

	return tekst

#Funkcija za unos linka
def url_inserter ():
	line_breaker(40)

	#Unos i obrada linka
	print("Insert URL:\n")
	print(Fore.RED, end = ' ')

	tekst = str(input())
	tekst = tekst.strip()
	tekst = url_shortcut(tekst)

	print(Fore.GREEN, end = '')

	if tekst == "0":
		tekst = url_inserter()
	
	return tekst


#--------------------------------------Animation-----------------------------------------

#3 dots console animation
def console_dots (duration):
	global animation
	
	if animation == 1:
		duration = duration - 0.5
		sleep(0.5)
		
		#definiranje animacije
		length = int(duration / 1.5)
		
		#2 sekunde za jedan krug
		for y in range(length):
			clear()
			sleep(0.5)
			for x in range(3):
				print('.', end = '', flush = True)
				sleep (1/3)
			'''
			Dio animacije koji mi se prije sviđao ali sad smatram da je nepotrebno loš

			for x in range(3):
				clear()
				print('.' * (2 - x), end = '', flush = True)
				sleep(1/3)
			'''


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
	global animation

	print(Style.RESET_ALL)
	print(Fore.GREEN)

	sleeptime = 0.000625 * duljina * animation

	for x in range(duljina):
		print('-', end = '', flush = True)
		sleep(sleeptime)
	
	print(Style.DIM, "\n")


#---------------------------------------Tekst------------------------------------------

#Help function
def Help ():
	console_dots(3.5)
	line_breaker(40)
	
	print("\r\nHelp tab:")
	print("\nChoose an option")
	
	print("0: Automode and Manual mode explained")
	print("1: URL inserting help")
	
	print("\nChoose an option:")

	print(Fore.YELLOW, end = ' ')
	mode = int(input())
	print(Fore.GREEN, end = '')

	print("\nLoading...")
	sleep(1.5)

	if mode == 0:
		print("\n Manual mode allows you to choose which links I will go to while scraping")
		sleep(2)
		print(" Auto mode makes me run autonomously, and choose randomly which links i want to go to")
		sleep(2.5)
		print(" You can change between modes whenever you want, by telling me to stop")
		sleep(2)
		print(" After you do that it will ask you if you want to switch to the other mode")
		sleep(2.5)

	if mode == 1:
		print("\n You have to insert a link that I will start scraping from")
		sleep(3)
		print(" When you write the link you must write it whole")
		sleep(3)
		print(" By that i mean that you should write https://www.google.com instead of something shortened")
		sleep(3)
		print(" For example www.google.com is wrong, and so is https://google.com")
		sleep(3)
		print(" If you write it wrong I will run into errors and halt")

	print("\r\nEnd of the help line\n")
	return


#Automode alert
def AutoAlert ():
	print(Fore.RED, end = '')
	
	print("\nWARNING:")
	
	print(Fore.GREEN, end = '')
	
	print(" You are about to atart automode, during that preiod, the program could wander anywhere over the internet, if")
	print (" you say yes, you are taking all the responsibility on what happenes during that time, do you agree to that? (y/n)")
	
	print(Fore.GREEN, end = ' ')
	
	c = Question(0)
	
	if c == 1:
		return 1
	else:
		print("\nSwitching to manual...\n")
		sleep(0.5)
		return 0

#Automode repeater
def Repeater ():
	global repeat

	print ("\nHow many links do you want the automode to visit?")
	
	print(Fore.YELLOW, end = ' ')

	c = input()
	c = c.strip()
	c = c.lower()
	
	print(Fore.GREEN, end = '')

	if c == 'help':
		Help()
		Repeater()
	
	else:
		repeat = int(c)
		

#Yes/No pitanja
def Question (mode):
	print(Fore.YELLOW, end = ' ')

	odg = str(input())
	odg = odg.strip()
	odg = odg.lower()
	
	print(Fore.GREEN, end = '')


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


#--------------------------------------Program-------------------------------------------

#pokretanje colorame
init()

#globalne varijable
repeat = int(0)
links = set({})

#Brze ili fancy animacije
print(Fore.GREEN, '\nToggle animations? (y/n)')
print(Style.DIM, end = '')
animation = Question(0)

#Animacija učitavanja konzole
console_dots(6.5)
clear()
line_breaker(80)

#Odabir načina rada
print("Do you want the program to run the program manually, or in automode? (m/a)")

automode = Question(1)

if automode == 1:
	automode = AutoAlert()

if automode == 1:
	Repeater()

tekst = url_inserter()
url_extractor(tekst)

#-------------------------------------------------------------------------------------
