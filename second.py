# -*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

#1. read the csv and get the movie code
#2. bring the source and parse

def searchMovie():
	with open('film_id.csv', "r") as f:
		reader = csv.reader(f)
		print(reader)
		for id_film in reader:
			print("=============\t" + id_film[0])
			url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			try:
				source_code = requests.post(url, {'code' : id_film})
			except:
				source_code = requests.post(url, {'code' : id_film})
			
			soup = BeautifulSoup(source_code.content, "lxml")
			# openDT = movie_soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")[0]
			print(soup.find("em", text=u'제작연도').parent.text.split("\r\n"))
			
			# with open("film.txt", 'w') as outfile:
			# 	outfile.write(source_code.content.decode("utf-8").replace(u"\ufeff", " "))

			break

searchMovie()
