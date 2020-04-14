from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as Soup
import random
import time

links = set({})
counter = 0
url_mistake_count = 0 

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

		elif unformat[0:11] == "javascript:" or unformat[0:4] == "None" :
			continue
		
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
		
		print("Want to see the list? (y/n)")
		c = YN()
		if c == 1:
			print("Links:")
			for link in links:
				print(link)
		else:
			pass

		print("Proceed? (y/n)")
		c = YN()
		if c == 1:
			url_extractor(my_url, automode)
			return
		else:
			print ("Switch to manual? (y/n)")
			a = YN()
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
		#odabiranje linka
		lista = list(links)
		i = 0
		print("Links:")
		for link in links:
			i += 1
			print(i,": ", link)
		print("Proceed? (y/n)")
		c = YN()
		if c == 1:
			print("Enter the number of a link you want a crawler to go to next")
			my_url = lista[int(input())-1]
			url_extractor (my_url, automode)
			return
		else:
			print ("Switch to auto? (y/n)")
			a = YN()
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


#Unos linka stranice u program
def url_inserter (automode):
	tekst = str(input())
	tekst = tekst.strip()
	#volio bi tu ubaciti kod koji bi provjerio ako stranica postoji bez da izbaci 500 grešaka ali (zasada) nemam pojma kako
	url_extractor(tekst, automode)
	return


#Yes/No pitanja
def YN ():
	odg = str(input())
	odg = odg.strip()
	odg = odg.lower()
	
	if odg == 'y' or odg[0] == 'y':
		return 1
	elif odg == "n" or odg[0] == "n":
		return 0
	else:
		print("Please say 'yes' or 'no'")
		YN()
		return


#program starter
print("Do you want automode? (y/n)")
auto = YN()
print("Insert URL:")
url_inserter(auto)
