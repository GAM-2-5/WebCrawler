#Program za konveretiranje .petar fileova
#Odabir modea
print("Choose:")
print("1- .txt to .petar")
print("2- .petar to .txt")

mode = int(input()) 


if mode == 1:
	#unos imena
	print ("Txt filename:")
	txt_name = str(input())
	
	#file type provjera
	ext = txt_name[-4:-1] + txt_name[len(txt_name)-1]
	if ext != ".txt":
		txt_name += ".txt"
	
	#unos imena
	print ("Petar file name:")
	name = str(input())
	
	#file type provjera
	ext = name[-6:-1] + name[len(name)-1]
	if ext != ".petar":
		name += ".petar"

	#priprema fileova
	r = open(txt_name, "r")
	f = open(name, "w")

	new_row = ""

	#enkripcija
	for row in r:
	    new_row = ""
	    for letter in row:
	        new_row += chr(ord(letter) + 5)
	    f.write(new_row)


elif mode == 2:
	#unos imema
	print ("Petar filename:")
	name = str(input())
	
	#file type provjera	
	ext = name[-6:-1] + name[len(name)-1]
	if ext != ".petar":
		name += ".petar"
	
	#unos imena
	print ("Txt file name:")
	txt_name = str(input())
	
	#file type provjera
	ext = txt_name[-4:-1] + txt_name[len(txt_name)-1]
	if ext != ".txt":
		txt_name += ".txt"

	#priprema fileova
	r = open(name, "r")
	f = open(txt_name, "w")

	new_row = ""

	#dekripcija
	for row in r:
	    new_row = ""
	    for letter in row:
	        new_row += chr(ord(letter) - 5)
	    f.write(new_row)

print ("Done")


