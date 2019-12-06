
import random
import time
import string
import sqlite3 as lite
import sys
import texttable as tt
import os
import subprocess
import re

#Connect to the DB
con = lite.connect('link.db')
cursor = con.cursor()

# GLOBAL VARIABLES

pattern = re.compile(
 r'(http|ftp|https)://([\w-]+(?:(?:.[\w-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', re.IGNORECASE)



# FUNCTIONS

# Create random 4char string
def randomString(stringLength=4):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range (stringLength))

# Creating the nginx config. Make sure you refer to the new file in your default.conf in nginx
def createNginx():
	saveFile = open('/etc/nginx/ownfiles/location-url.conf', 'a')
	saveFile.write('\nlocation /'+ str(row[3]) +' {return 301 ' + row[1] + ';}')
	saveFile.close()

# Deleting row from SQLite3 database
def delSql(chooseID):
	cursor.execute('DELETE FROM url3 WHERE ID = ?', (chooseID,))
	con.commit()

# Deleting the line of text on the nginx configuration file and reloading nginx
def delNginx(chooseID):
	cursor.execute('SELECT * FROM url3 WHERE ID = ?', (chooseID,))
	for row in cursor.fetchall():
		textprint = ('location /'+ str(row[3]) +' {return 301 ' + row[1] + ';}') #the exact row that is going to be deleted
		with open('/etc/nginx/ownfiles/location-url.conf', 'r') as f:
			lines = f.readlines()
		with open('/etc/nginx/ownfiles/location-url.conf', 'w') as f:
			for line in lines:
				if line.strip("\n") != textprint:
					f.write(line)

	subprocess.call(["sudo", "service", "nginx", "reload"])




a = 1
while a == 1:

	try:
		userInput = int(input("\nMENU: Press 1 to add URL. Press 2 to show the table. Press 3 to delete an entry. Press 4 to show nginx conf. Press 9 to quit\nMake your choice: "))

		if userInput == 1: #Generating the URL. Adding the Original URL and New URL to SQLite3 database

			longurl = input("Add your URL: ")
			random_or_own = input("Press 1 for choosing your own url or 2 for generating a random url: ")
			if random_or_own == "1":
				own_url = input("Insert your own url. Max 10 letters lowercase. miraa.se/")
				if len(own_url) < 11 and own_url.islower() and own_url.isalpha():
					shorturl = own_url
				else:
					print ("*** Only 10 letters and lowercase is allowed!! ***\n")
					continue

			elif random_or_own == "2":
				shorturl = randomString()
			else:
				print ("wrong input")
				continue


			result = re.search(pattern, longurl) #Matching the url against the REGEX
			if result:
				cursor.execute('INSERT INTO url3 VALUES(?, ?, ?, ?)', (None, longurl, None, shorturl))
				print ("\nThis is your new URL: miraa.se/" + shorturl + "\n")
				cursor.execute('SELECT * from url3 WHERE SHORTURL = ?', (shorturl,) )
				for row in cursor.fetchall():
					createNginx()
				con.commit()
				subprocess.call(["sudo", "service", "nginx", "reload"])

			else:
				print ("\n*** Insert a valid URL. For example: https://www.google.com/search?q=python ***\n")
				continue


		elif userInput == 2: #Shows the table
			tab = tt.Texttable()
			col_name = ['ID', 'ORIGURL', 'SHORTURL']
			tab.header(col_name)

			cursor.execute('SELECT ID, ORIGURL, SHORTURL FROM url3')
			for row in cursor.fetchall():
				tab.add_row(row)

			s = tab.draw()
			print (s)

		elif userInput == 9:
			con.commit()
			con.close()
			break

		elif userInput == 3:
			chooseID = input("What's your ID? ")
			delNginx(chooseID)
			delSql(chooseID)

		elif userInput == 4:
			subprocess.call(["sudo", "cat", "/etc/nginx/ownfiles/location-url.conf"])
			print("\n")
		else:
			print("That is not a valid option")
	except:
		print("Please choose from the menu numbers")
