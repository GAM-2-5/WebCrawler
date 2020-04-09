from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as Soup

#Unos linka stranice i osnovnih parametara
my_url = "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card"

links = set({})

secure = ""    #dio linka sa http ili https
source = ""    #source link (tipa www.google.com)
pagedown = ""  #link jednu stranicu ispod trenutnog linka


#Određivanje je li link http ili https
if my_url[0:5] == "https":
	secure = my_url[0:6]

elif my_url[0:5] == "http:":
	secure = my_url[0:5]

else:
	print("Insert a valid link")


#Izdvajanje source linka i stranice ispod
cnt = 0;
slash_num = my_url.count("/")
for letter in my_url:
	if letter == "/" :
		cnt += 1
	if cnt == slash_num:
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

#printout
for link in links:
	print(link)