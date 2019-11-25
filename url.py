	
import random
import time
import string
import sqlite3 as lite
import sys
import texttable as tt
import os
import subprocess

#Testing GIT - branch only

#Connect to DB
con = lite.connect('link.db')
cursor = con.cursor()


#Create random 4char string
def randomString(stringLength=4):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range (stringLength))


def createNginx():
	saveFile = open('/etc/nginx/ownfiles/location-url.conf', 'a')
	saveFile.write('\n\nlocation /'+ str(row[3]) +' {')
	saveFile.write('\n\t')
	saveFile.write('return 301 ' + row[1] + ';')
	saveFile.write('\n}')
	saveFile.close()



a = 1

while a == 1:

	userInput = int(input("Press 1 to add URL. Press 2 to show the table. Press 3 to quit\n"))

	if userInput == 1:

		#User Input
		longurl = input("Add your URL: ")
#		try:
#			cuturl = (longurl.split("/",1)[1])
#		except:
#			cuturl = 'non'
#			print ("No CUT url could be given")

		shorturl = randomString()

		cursor.execute('INSERT INTO url3 VALUES(?, ?, ?, ?)', (None, longurl, None, shorturl))

		print ("\nThis is your new URL: miraa.se/" + shorturl + "\n")

		cursor.execute('SELECT * from url3 WHERE SHORTURL = ?', (shorturl,) )
		for row in cursor.fetchall():
			createNginx()


		con.commit()

		subprocess.call(["sudo", "service", "nginx", "reload"])

	elif userInput == 2:
		tab = tt.Texttable()
		col_name = ['ID', 'ORIGURL', 'SHORTURL']
		tab.header(col_name)
		
		cursor.execute('SELECT ID, ORIGURL, SHORTURL FROM url3')
		for row in cursor.fetchall():
			tab.add_row(row)

		s = tab.draw()
		print (s)

	elif userInput == 3:
		#os.system('clear')
		break
	
	else:
		print("wtf")
