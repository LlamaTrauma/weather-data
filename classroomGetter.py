import requests
import pandas
from bs4 import BeautifulSoup
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
print(frame)