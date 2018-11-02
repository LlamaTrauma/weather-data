import requests
import pandas
import sqlalchemy
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import sqlite3
page = requests.get('https://weather.com/weather/tenday/l/USOR0190:1:US')
soup = BeautifulSoup(page.content, 'html.parser')
feed = soup.select('main.region.region-main')
days = [i.get_text() for i in soup.select('span.day-detail.clearfix')]
descs = [i['title'] for i in soup.select('td.description')]
descs2 = [i.get_text() for i in soup.select('td.description span')]
temp = [i.get_text() for i in soup.select('td.temp div')]
temps = ["High: " + i[:3] + " / Low: " + i[3:] for i in temp]
frame = pandas.DataFrame({
    "Date": days,
    "Desc": descs2,
    "Temp": temps,
    "More": descs
})

conn = sqlite3.connect('weather-sql.db')

c = conn.cursor()

conn.execute('DROP TABLE IF EXISTS forecast')

conn.execute('''CREATE TABLE forecast(
        DATE        text,
        DESC        text,
        TEMP        text,
        MORE        text
        )''')

for i in range(0, len(days) - 1, 1):
    conn.execute('INSERT INTO forecast VALUES(?, ?, ?, ?)', (str(days[i]), str(descs[i]), str(temps[i]), str(descs2[i])))

for i in c.execute('SELECT * FROM forecast ORDER BY DATE'):
    print(i)

conn.commit()

conn.close()
