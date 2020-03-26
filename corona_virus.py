"""
This script will take the information about Corona Pandemic from this website :

worldometers.info/coronavirus


Author : Youssef Alaoui Belrhiti
Country : Morocco

"""

import requests
import lxml.html as lh
import unicodedata
import sqlite3
import datetime


# make dataBase

sql_db = """CREATE TABLE IF NOT EXISTS CORONA (Country TEXT, TotalCases TEXT, 
NewCases TEXT, TotalDeaths TEXT, NewDeaths text, TotalRecovered text, ActiveCases text, Critical text,
 TotCases_1M_pop text, TotDeaths_1M_pop text, Date DATE, PRIMARY KEY(Country, Date))"""

con = sqlite3.connect("Corona_db.db")
curs = con.cursor()

con.execute(sql_db)
con.commit()

tr_elements = [None]
try:

    url = "http://worldometers.info/coronavirus"
    page = requests.get(url)
    doc = lh.fromstring(page.content)

    header = []
    tr_elements = doc.xpath("//tr")
    toDay = datetime.datetime.now().date()
except:
    print("Connexion Error, please try Again")

"""  
for t in tr_elements[0]:
    header.append(unicodedata.normalize("NFKD", t.text_content()))
"""

try:
    for row in tr_elements[1:]:
        erow = []

        for cell in row:
            erow.append(cell.text_content())
        erow.append(toDay)
        sql_insert = "INSERT INTO CORONA(Country, TotalCases, NewCases, TotalDeaths, NewDeaths, TotalRecovered, " \
                     "ActiveCases, Critical,TotCases_1M_pop, TotDeaths_1M_pop, Date) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        curs.execute(sql_insert, erow)
        con.commit()
        if erow[0] == "Total:":
            break
        print(" data of %s is added successfully" % row[0].text_content())
    print("Process finished with success, congrats!")
except:
    print("The data of this day %s is already saved in the database, Thanks" % toDay)
finally:
    con.close()
