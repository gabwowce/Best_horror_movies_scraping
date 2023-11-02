from bs4 import BeautifulSoup
import lxml
import requests
import reverse
response = requests.get("https://www.empireonline.com/movies/features/best-horror-movies/")
movie_page = response.text

soup = BeautifulSoup(movie_page, "lxml")

movie_list_x = []
movies = soup.select("h2")
for i in movies:
    movie_list_x.append(i.string)
movie_list = movie_list_x[::-1]

with open("movies.txt", "w") as file:
    for i in movie_list:
        file.write(i+"\n")

