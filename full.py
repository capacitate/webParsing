# -*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

#1. search movie 
#2. draw movie information
#3. search the actors information 

def directors(director_id):
	print("")

def searchPage(max_pages):
	page = 1

	while page <= max_pages:
		print("************" + str(page) + "************")
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
				ids_dir = ids_dir + id_d['onclick'].split('\'')[3] + ','	#id_director

			ids_dir = ids_dir[:-1]	#remove last character of string
			directors_id = ids_dir.split(",")

			for d_id in directors_id:
				directors(d_id)	# should return information of directors, name of director

			#information of actors @@from here actors information
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
					# print("%s\n" % actor_str)
					actor_dic = eval(actor_str)
					if(int(actor_dic["actorGb"]) == 1):
						# print(str(actor_dic["peopleNm"]))
						main_actors = main_actors + actor_dic["peopleNm"] + ","
						main_actors_id = main_actors_id + actor_dic["peopleCd"] + ","	
					elif(int(actor_dic["actorGb"]) == 2):
						sub_actors += actor_dic["peopleNm"] + ","
						sub_actors_id += actor_dic["peopleCd"] + ","	


			cols = [ele.text.strip() for ele in cols]
			productYear = cols[2].strip()	#productYear

			print("=================")
			print("film_id :\t" + film_id)
			print("prodcuctYear :\t" + productYear)
			print("directors :\t" + ids_dir)

			movie_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			movie_source = requests.post(movie_url, {'code' : film_id})
			movie_soup = BeautifulSoup(movie_source.content, "lxml")

			try:
				openDT = movie_soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")[0]
				openDT = openDT.replace("-", "")
			except:
				openDT = movie_soup.find("dt", text=str(u'개봉(예정)일')).findNext("dd").text.strip().split("\r\n")[0]
				openDT = openDT.replace("-", "")

			if("해당정보" in openDT):
				openDT = "    "

			print("openDT :\t" + openDT[:4])


			# cols = row.findAll('td')
			# all_nation = cols[3]['title']	#nation_all
			
			# all_genre = cols[5]['title']	#genre_all

			# id_directors_list = cols[7].findAll('a')
			# ids_dir = ''
			# for id_d in id_directors_list:
			# 	ids_dir = ids_dir + id_d['onclick'].split('\'')[3] + ','	#id_director

			# movie_id = cols[0].find('a')['onclick'].split('\'')[3]

			# cols = [ele.text.strip() for ele in cols]

			# movieNM_kor = cols[0].strip()	#kor_movieNM
			# movieNM_en = cols[1].strip()	#en_movieNM
			# yearProduct = cols[2].strip()	#productYear

		page += 1


searchPage(1)