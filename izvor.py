'''
Program: Izvor.py
Programer: Petar Dušević
Korisnik: Vi
Hotel: Trivago
Mentor: Goran Boneta

7.5.2020. u Rijeci
Gimnazija Andrije Mohorovičića Rijeka

https://github.com/GAM-2-5/WebCrawler
'''

from urllib.request import urlopen as uReq    #pip
from colorama import init, Fore, Style        #pip
from bs4 import BeautifulSoup as Soup         #pip
from os import system, name 
from time import sleep
from PIL import Image                         #pip
import numpy as np                            #pip
import random
import sys

version = "v1.4"

#-----------------------------------------Url--------------------------------------------

#funkcija koja će biti korištena za ekstrakciju linka
def url_extractor (my_url):
	global links
	global visited_links_set
	global visited_links_list
	global key_blacklist
	global key

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
	if my_url in visited_links_set:
		return
	
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

	#ista stvar sa tekstom
	i = 0
	if key != "":
		output = ""
		text = page_soup.find_all(text=True)
		for t in text:
			if t.parent.name not in key_blacklist:
				output += '{} '.format(t)
				
				if key in t.lower():
					i += 1

	visited_links_set.add(my_url)
	visited_links_list.append(str(i) + my_url)


#Odabir sljedećega linka
def url_picker ():
	global automode
	global repeat
	global links
	global visited_links_list

	#Za automode
	if automode == 1:
		my_url = url_manager()
	
		if repeat > 0:
			repeat -= 1
			return my_url
			
		else:
			printer("\nAutomode has finished\n")

			printer(str(len(links)) + " scraped link(s)")
			printer(str(len(visited_links_list)) + " visited link(s)")
			
			matches = 0
			for x in visited_links_list :
				(num, link) = Separate(x)
				matches += int(num)

			printer(str(matches) + " key(s) found")
			printer("\n(-h for the help tab)")

			odg = Console(2)
			
			if odg == "-s":
				my_url = "-start url_picker"
				return my_url

			elif odg == "-lr":
				my_url = url_inserter()
				return my_url

			else:
				repeat = int(odg)
				return my_url

	#Bez automodea
	else:
		ShowList(1)

		printer("\n" + str(len(links)) + " scraped link(s)")
		printer(str(len(visited_links_list)) + " visited link(s)")
		
		matches = 0
		for x in visited_links_list :
			(num, link) = Separate(x)
			matches += int(num)

		printer(str(matches) + " key(s) found")
		printer("\n(-h for the help tab)")

		my_url = url_manager()

		return my_url

#Odabir linka
def url_manager ():
	global links
	global automode
	global visited_links_set
	
	if automode == 1:
		#Odabiranje nasumičnog linka
		tekst = random.choice(tuple(links))
		my_url = str(tekst)
	
	else:
		odg = Console(1)
		
		if odg == "-s":
			return "-start url_picker"
		
		elif odg == "-lr":
			my_url = url_inserter()

		else:
			goto = int(odg)
			lista = list(links)
			my_url = lista[goto - 1]

	#provjera postojanja
	postoji = url_checker(my_url)
	if postoji == 1:
		if my_url in visited_links_set == True:
			if automode == 0:
				print(Fore.RED, end = '')
				printer(" Link already visited")
				print(Fore.GREEN, end = '')
			
			my_url = url_manager()
	
	else:
		if automode == 0:
			print(Fore.RED, end = '')
			printer(" Link unavailable")
			print(Fore.GREEN, end = '')
		
		my_url = url_manager()
	
	return my_url

#Provjera linka
def url_checker (link):
	try:
		uReq(link)
		return 1

	except:
		return 0
	

#Funkcija za kratice
def url_shortcut (tekst):
	tekst.lower()
	
	if tekst.lower() == "help":
		print(Fore.GREEN, end = '')
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
	printer("Insert URL:\n")
	print(Fore.RED, end = ' ')

	tekst = str(input())
	tekst = tekst.strip()
	tekst = url_shortcut(tekst)

	postoji = url_checker(tekst)

	if postoji == 0:
		print(" Page does not exist")
		tekst = "0"
	
	elif postoji == 2:
		print(" Page unavailable")
		tekst = "0"
	
	print(Fore.GREEN, end = '')

	if tekst == "0":
		tekst = url_inserter()

	return tekst

#----------------------------------------Misc--------------------------------------------

def Separate (url):
	a = 0
	letter = "0"
	i = 0
	if letter.isdigit() == True:
		for letter in url :
			if letter.isdigit() == True:
				i += 1
				a *= 10
				a += int(letter)
			
			else:
				break

	link = ""
	b = 0
	for x in url:
		if b >= i:
			link += x
		b += 1
	
	return (a,link)

def KeyWord ():
	global key
	global key_blacklist

	line_breaker(40)

	printer("Insert a key word:\n")
	print(Fore.RED, end = ' ')
	
	key = str(input()) 
	key = key.lower()
	key = key.strip()

	if key in key_blacklist:
		print("Key blacklisted")
		print(Fore.GREEN, end = '')
		key = KeyWord()
	
	print(Fore.GREEN, end = '')
	return key

def ShowList (mode):
	global links
	global automode
	global visited_links_list
	global key

	# 1 - links list
	# 2 - visited list

	if mode == 1:
		i = 0
		printer("\nList of links:")
		sleep(1)

		if automode == 0:
			i = 0
			for x in links:
				i += 1
				print (i, " ", x)

		if automode == 1:
			for x in links:
				print (" ", x)

	elif mode == 2:
		i = 0
		printer("\nList of visited links:")
		sleep(1)
		i = 0
		for x in visited_links_list :
			i += 1
			(num, link) = Separate(x)
			if key != "":
				print (i, ": (", num, " keywords found ) ", link)

			else:
				print (i, ": ", link)

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
	print("\n")
	
	linija = '-' * duljina
	
	printer(linija)
	print("")

#Ispisivanje teksta u stilu
def printer (tekst):
	global animation

	for slovo in tekst:
		print(slovo, end = '', flush = True)
		sleep (0.01 * animation)

	print ("")

#---------------------------------------Konzola------------------------------------------

def Console (mode):
	global links
	global started
	global running
	global automode
	global visited_links_set
	global visited_links_list

	#Mode:
	#0 - Nothing
	#1 - Manual mode proceed
	#2 - Automode proceed
	#3 - Literally nothing

	if mode == 0:
		printer("\nWhat next? (type '-h' for options)")

	if mode == 1:
		printer("\nWhat link next? (number)")

	if mode == 2:
		printer("\nHow many links do I go to next?")

	print(Fore.YELLOW, end = ' ')

	odg = str(input())
	odg = odg.strip()
	odg = odg.lower()

	print(Fore.GREEN, end = '')

	if odg == "" or odg == "-":
		print(Style.DIM, end = '')
		
		printer (" Insert something lmao")
		
		print(Style.RESET_ALL, end = '')
		print(Fore.GREEN, end = '')
	
		odg = Console(mode)

	elif odg[0] == "-":
		if odg == "-help" or odg == "-h":
			Help()
		
		elif odg == "-stop" or odg == "-exit" or odg == "-halt" or odg == "-x":
			running = 0
			Quit()
	
		elif started != 0:	
			if odg == "-clear" or odg == "-cls":
				clear()
			
			elif odg[0:2] == "-l":
				if odg == "-list reset" or odg =="-lr":
					printer(" Are you sure you want to clear the list?")
					
					a = Question(0)
					if a == 1:
						links.clear()
						printer(" List cleared!")
						odg == "-lr"
						
						if mode == 1 or mode == 2:
							return odg

				elif odg == "-list save" or odg == "-ls":
					FileSave("scraped", "save")

				elif odg == "-list print" or odg == "-lp":
					FileSave("scraped", "print")

				elif odg == "-list load" or odg == "-ll":
					FileLoad("scraped")

				elif odg == "-list" or odg == "-l":			
					ShowList(1)
				else:
					print(Fore.RED, end = '')
					printer(" " + odg + " is not a recognizable command")
					print(Fore.GREEN, end = '')
			
			elif odg[0:2] == "-v": 
				if odg == "-visited" or odg == "-v":
					ShowList(2)
				
				elif odg == "-visited save" or odg == "-vs":
					FileSave("visited", "save")

				elif odg == "-visited print" or odg == "-vp":
					FileSave("visited", "print")

				elif odg == "-visited load" or odg == "-vl":
					FileLoad("visited")

				elif odg == "-visited reset" or odg == "-vr":
					printer(" Are you sure you want to clear the visited links?")
					
					a = Question(0)
					if a == 1:
						visited_links_set.clear()
						visited_links_list.clear()
						printer(" List cleared!")
				
				else:
					print(Fore.RED, end = '')
					printer(" " + odg + " is not a recognizable command")
					print(Fore.GREEN, end = '')

			elif odg == "-mode" or odg == "-m":
				if automode == 1:
					printer(" Automode running")
				
				else:
					printer(" Manual mode running")

			elif odg == "-switch" or odg == "-s":
				if automode == 0:
					Repeater()
				automode = 1 - automode
				printer("Modes switched")
				
				if mode == 1 or mode == 2:
					return "-s"
			
			else:
				print(Fore.RED, end = '')
				printer(" " + odg + " is not a recognizable command")
				print(Fore.GREEN, end = '')

		else:
			print(Fore.RED, end = '')
			printer(" " + odg + " cannot be run yet")
			print(Fore.GREEN, end = '')

		odg = Console(mode)

	elif mode == 1:
		goto = int(0)
		
		try:
			goto = [int(s) for s in odg.split() if s.isdigit()]
			if int(goto[0]) > len(links):
				a = int("a")
			return goto[0]
		
		except:
			print(Fore.RED, end =' ')
			printer(odg + " is not a valid number/reference")
			print(Fore.GREEN, end = '')
			
			odg = Console(mode)
			return odg
	
	elif mode == 2:
		goto = int(0)
		
		try:
			goto = int(odg[len(odg)-1])
			return goto
		
		except:
			print(Fore.RED, end =' ')
			printer(odg + " is not a number")
			print(Fore.GREEN, end = '')
			
			odg = Console(mode)
			return odg

	return odg

#Funkcija za izlazak
def Quit ():
	print ("\nExiting...")
	print(Style.RESET_ALL)
	sleep (0.5)
	raise SystemExit

#----------------------------------------Files-------------------------------------------

#Čitač datoteka
def FileRead (filename):
	filename = "Speech/" + filename + ".petar"
	r = open(filename, "r")
	sentence = ""

	#dekripcija
	for row in r:
		for letter in row:
			if letter == '':
				printer(sentence)
				sentence = ""
			
			else:
				sentence += chr(ord(letter) - 5)
		
		printer(sentence)

#Učitavač datokeka
def FileLoad (data):
	global links
	global visited_links_set
	global visited_links_list

	printer(" File name?")
	print(Fore.YELLOW, end = ' ')

	filename = str(input())
	filename = filename.strip()

	print(Fore.GREEN, end = '')

	if filename.lower() == 'cancel' or filename.lower() == 'exit':
		printer( "Process cancelled")
		return

	if data == "scraped":
		filename = "Saves/Scraped/" + filename + ".petar"
	
	else:
		filename = "Saves/Visited/" + filename + ".petar"

	try:
		r = open(filename, "r")
		#dekripcija
		sentence = ""
		for row in r:
			for letter in row:
				if letter == '':
					if data == "scraped":
						links.add(sentence)	
					else:
						visited_links_set.add(sentence)
					
					sentence = ""
				
				else:
					sentence += chr(ord(letter) - 5)
			
		if data == "scraped":
			links.add(sentence)

		else:
			visited_links_set.add(sentence)	
		
		visited_links_list = list(visited_links_set)
		printer(" Loaded")

	except:
		print(Fore.RED, end = ' ')
		printer(filename + " does not exist")	
		print(Fore.GREEN, end = '')
		FileLoad(data)


#Spremač datoteka
def FileSave (data, mode):
	global links
	global visited_links_list

	if mode == "print":
		printer(" File name?")
	else:
		printer(" Save name?")
	
	print(Fore.YELLOW, end = ' ')

	filename = str(input())
	filename = filename.strip()

	print(Fore.GREEN, end = '')

	if filename.lower() == 'cancel' or filename.lower() == 'exit':
		printer(" Proces cancelled")
		return

	if mode == "save":
		if data == "scraped":
			filename = "Saves/Scraped/" + filename + ".petar"
		
		else:
			filename = "Saves/Visited/" + filename + ".petar"

	else:
		filename = filename + ".txt" 


	if mode == "save":
		a = open(filename, "a")
		new_row = ""
		
		if data == "scraped":
			#enkripcija
			for link in links:
			    new_row = ""
			    for letter in link:
			        new_row += chr(ord(letter) + 5)
			    
			    a.write(new_row)
			    a.write('')

		else:
			#enkripcija
			for link in visited_links_list:
			    new_row = ""
			    for letter in link:
			        new_row += chr(ord(letter) + 5)
			    
			    a.write(new_row)
			    a.write('')

	else:
		w = open(filename, "w")
		
		if data == "scraped":
			for link in links:
				w.write(link)
				w.write('\n')
		
		else:
			for link in visited_links_list:
				w.write(link)
				w.write('\n')

	printer("\n Done!")
#----------------------------------------Tekst-------------------------------------------

#Help function
def Help ():
	line_breaker(40)
	
	printer("\r\nHelp tab:")
	FileRead("He")
	printer("\nChoose an option:")

	print(Fore.YELLOW, end = ' ')
	
	mode = int(input())
	
	print(Fore.GREEN, end = '')

	printer("\nLoading...")
	sleep(1.5)

	file = ""
	if mode == 0:
		return

	if mode in [1,2,3,4,5]:
		file = "He" + str(mode)
		FileRead(file)
		printer("\r\nEnd of the help line\n")

	else:
		printer("\n" + str(mode) +" is not a valid option")

	Help()


#Automode alert
def AutoAlert ():
	print(Fore.RED, end = '')
	
	printer("\nWARNING:")
	
	print(Fore.GREEN, end = '')

	FileRead("Al0")

	print(Fore.GREEN, end = ' ')
	
	c = Question(0)
	
	if c == 1:
		return 1
	
	else:
		printer("\nSwitching to manual...\n")
		sleep(0.5)
		return 0

#Automode repeater
def Repeater ():
	global repeat

	printer("\nHow many links do you want the automode to visit?")
	
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
	odg = Console(3)

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
			printer("Now please choose " + option1 + " or " + option2)
		else:
			printer("Please choose " + option1 + " or " + option2)

		f = Question(mode)
		return f

#----------------------------------------Intro-------------------------------------------

#intro
def Intro ():
	global version
	
	console_dots(5)
	clear()
	printer("Starting up...\n")
	sleep(1)
	ImageDisplay()
	printer("Izvor " + version + "\n")
	printer("Made by: Petar Dušević")
	
	print("")
	line_breaker(80)

#intro slika
def ImageDisplay ():
	global animation
	#neopisivo:
	chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@')) 
	f = "izvor.jpg" 
	SC = 0.12
	GCF = 1.8
	
	if f == "izvor.jpg":
		WCF = 5/2
	else:
		WCF = 7/4
	
	img = Image.open(f)
	
	S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
	img = np.sum( np.asarray( img.resize(S) ), axis=2)
	img -= img.min()
	img = (1.0 - img/img.max())**GCF*(chars.size-1)
	
	storage = animation
	animation *= 0.001 
	printer( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
	animation = storage

#--------------------------------------Program-------------------------------------------

#pokretanje colorame
init()

#globalne varijable
links = set({})
visited_links_set = set({})

visited_links_list = list([])
key_blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head','input', 'body', 'script', '\n', '\r', '\r\n', 'style']

repeat = 0
animation = 0
started = 0
running = 0

#displaymode = "default"

key = ""

#Brze ili fancy animacije
print(Fore.GREEN, '\nToggle animations? (y/n)')
animation = Question(0)

#Animacija učitavanja konzole
Intro()

#Odabir načina rada
printer("Do you want the program to run the program manually, or in automode? (m/a)")

automode = Question(1)

if automode == 1:
	automode = AutoAlert()

if automode == 1:
	Repeater()

printer("Do you need a search keyword? (y/n)")

need = Question(0)

if need == 1:
	KeyWord()

tekst = url_inserter()

started = 1
running = 1

while running == 1:
	if tekst == "-start url_picker":
		tekst = url_picker()
	
	else:
		url_extractor(tekst)
		tekst = url_picker()

Quit()
#-------------------------------------------------------------------------------------



#i ovo je bilo vaših današnjih (skoro) 1000 linija koda
#ukoliko pronađete ikakve bugove prijavite ih na githubu, hvala!
