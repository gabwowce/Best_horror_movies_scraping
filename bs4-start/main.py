from bs4 import BeautifulSoup
import lxml
import requests

response = requests.get("https://news.ycombinator.com/show")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "lxml")

title_list = []
point_list = []
link_list = []

points = soup.select(".score")
for i in points:
    point_list.append(int(i.string.split()[0]))

titles = soup.select("span.titleline > a")
for i in titles:
     title_list.append(i.string)

a = soup.select("span.titleline > a")
for i in a:
    link_list.append(i["href"])

print(point_list)

biggest = 0
for i in point_list:
    if i > biggest:
        biggest = i

print(biggest)
for i in point_list:
    if biggest == i:
        index = point_list.index(i)

print(title_list[index])
print(link_list[index])