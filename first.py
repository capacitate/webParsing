# -*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

def loading(pages):
	page = 176

	filename = "first138.csv"
	with open(filename, 'w', newline='') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(["id_movie", "movie_kor","id_director", "id_actors"])

	while page <= pages:
		print("************" + str(page) + "page" + "************")
		url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do'
		source_code = requests.post(url, {'curPage' : page})
		
		encoding = source_code.encoding if 'charset' in source_code.headers.get('content-type', '').lower() else None
		soup = BeautifulSoup(source_code.content, "lxml", from_encoding=encoding)

		movie_table = soup.find('table', attrs={'class':'boardList03'})
		table_body = movie_table.find('tbody')
		rows = table_body.findAll('tr')

		for row in rows:
			cols = row.findAll('td')
			
			film_id = cols[0].find('a')['onclick'].split('\'')[3]

			#information of directors
			temp_dir = cols[7].findAll('a')
			ids_dir = ''
			for id_d in temp_dir:
				ids_dir = ids_dir + str(id_d['onclick'].split('\'')[3]) + ", "	#id_director

			

			ids_dir = ids_dir[:-1]	#remove last character of string

			cols = [ele.text.strip() for ele in cols]
			movieNM_kor = cols[0].strip()	#kor_movieNM

			# print("=========")
			# print("directors\t" + ids_dir)
			# print("name\t" + movieNM_kor)

			#information of actors
			movie_staff = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovActorLists.do', data={
			    'movieCd': film_id,
			}, headers={
			    'Accept': 'application/json'
			})	

			main_actors = "" 
			main_actors_id = ""

			sub_actors = ""
			sub_actors_id = ""

			for actor in movie_staff.content.decode().split('{'):
				if("[" not in actor):
					actor_str = "{" + actor
					actor_str = actor_str.replace("null", "1")
					if("]" in actor_str):
						actor_str = actor_str.replace("]", "")
					else:
						actor_str = actor_str[:-1]	#remove last character of string

					actor_dic = eval(actor_str)
					# print(actor_dic["peopleCd"])
					if(int(actor_dic["actorGb"]) == 1):
						try:
							main_actors_id = main_actors_id + actor_dic["peopleCd"] + ","	
						except:
							main_actors_id = main_actors_id
					elif(int(actor_dic["actorGb"]) == 2):
						try:
							sub_actors_id += actor_dic["peopleCd"] + ","	
						except:
							sub_actors_id = sub_actors_id

			id_actors = main_actors_id + sub_actors_id

			# print(film_id)
			# print(ids_dir)
			# print(id_actors)

			temp = []
			temp.append(str(film_id))
			temp.append(str(movieNM_kor))
			temp.append(str(ids_dir))
			temp.append(str(id_actors))
			
			with open(filename, 'a', newline='') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(temp)

		page += 1

loading(5559)