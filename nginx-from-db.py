import os
import subprocess
import sqlite3 as lite
import texttable as tt

#Connect to the DB
con = lite.connect('link.db')
cursor = con.cursor()

def createNginx():
	saveFile = open('testnginx.conf', 'a')
	saveFile.write('\nlocation /'+ str(row[3]) +' {return 301 ' + row[1] + ';}')
	saveFile.close()


def showSQL():
	tab = tt.Texttable()
	col_name = ['ID', 'ORIGURL', 'SHORTURL']
	tab.header(col_name)
	cursor.execute('SELECT ID, ORIGURL, SHORTURL FROM url3')
	for row in cursor.fetchall():
		tab.add_row(row)
	s = tab.draw()
	print (s)



showSQL()
saveFile = open('testnginx.conf', 'w').close()

cursor.execute('SELECT * from url3')
for row in cursor.fetchall():
	createNginx()



con.close()
