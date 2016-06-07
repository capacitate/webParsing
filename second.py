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
			movie_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			try:
				source_code = requests.post(movie_url, {'code' : id_film})
			except:
				source_code = requests.post(movie_url, {'code' : id_film})
			
			soup = BeautifulSoup(source_code.content, "lxml")
			# openDT = movie_soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")[0]

			try:
				openDT = soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")[0]
				openDT = openDT.replace("-", "")

				temp_open = soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")
				temp_open = [t.strip() for t in temp_open if t.strip()]

			except:
				openDT = soup.find("dt", text=str(u'개봉(예정)일')).findNext("dd").text.strip().split("\r\n")[0]
				openDT = openDT.replace("-", "")

				temp_open = soup.find("dt", text=str(u'개봉(예정)일')).findNext("dd").text.strip().split("\r\n")
				temp_open = [t.strip() for t in temp_open if t.strip()]

			productYear = temp_open[2][:4]
			openDT = openDT[:4]


			movie_staff_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovStaffLists.do'
			staff_code = requests.post(movie_staff_url, {'movieCd':id_film}, headers={
			    'Accept': 'application/json'
			})

			directors = ""
			id_directors = ""

			for d in staff_code.content.decode().split('{'):
				if("[" not in d):
					d_str = "{" + d
					d_str = d_str.replace("null", "1")
					if("]" in d_str):
						d_str = d_str.replace("]", "")
					else:
						d_str = d_str[:-1]	#remove last character of string
					# print("%s\n" % actor_str)
					d_dic = eval(d_str)
					if(d_dic["roleNm"] == "감독"):
						print(d_dic["peopleNm"])
						print(d_dic["peopleCd"])

						directors += d_dic["peopleNm"] + ", "
						id_directors += d_dic["peopleCd"] + ", "


						
					# print(d_str)
					# if(int(actor_dic["actorGb"]) == 1):
					# 	# print(str(actor_dic["peopleNm"]))
					# 	main_actors = main_actors + actor_dic["peopleNm"] + ","
					# 	main_actors_id = main_actors_id + actor_dic["peopleCd"] + ","	
					# elif(int(actor_dic["actorGb"]) == 2):
					# 	sub_actors += actor_dic["peopleNm"] + ","
					# 	sub_actors_id += actor_dic["peopleCd"] + ","	
			# print(staff_code.text)
			
			# with open("film.txt", 'w') as outfile:
			# 	outfile.write(source_code.content.decode("utf-8").replace(u"\ufeff", " "))

			break

searchMovie()
