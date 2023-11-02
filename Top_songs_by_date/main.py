from bs4 import BeautifulSoup
import lxml
import requests
import urllib.request
import re

#Select a date to find the most popular songs from that time.
chosen_date = input("Choose the date (YYYY-MM-DD): ")

#Create a list of the most popular songs for a chosen date
URL = f"https://www.billboard.com/charts/hot-100/{chosen_date}"

response = requests.get(URL)
songs_page = response.text
soup = BeautifulSoup(songs_page, "lxml")

songs_list = []
singers_list = []
replaced_songs_list = []
songs = soup.select("li.o-chart-results-list__item > h3")

for i in songs:
    songs_list.append(i.string.strip())

singers = soup.select("li.o-chart-results-list__item > h3#title-of-a-story + span.c-label")

for i in singers:
    singers_list.append(i.string.strip())

for i in range(0, len(songs_list)):
        songs_list[i] += " by " +  singers_list[i]

#Replace every song's name with a Youtube searchable
for i in range(0, len(songs_list)):
    replaced_songs_list.append(songs_list[i].replace(" ", "+"))


#finds every song link on Youtube
video_links = []
for song in replaced_songs_list[0:20]: #slised list to first 20 song
    search_url = f"https://www.youtube.com/results?search_query={song}"
    html_content = urllib.request.urlopen(search_url).read().decode()
    video_id = re.findall(r"watch\?v=(\S{11})", html_content)
    if video_id:
        video_links.append(f"https://www.youtube.com/watch?v={video_id[0]}")

#Put every song's name and Youtube link into txt file
with open(f"Top {chosen_date} Songs", "w") as file:
    for link, song in zip(video_links, songs_list):
        line = f"SONG: {song}, YOUTUBE LINK: {link}\n\n"
        file.write(line)
