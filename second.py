# -*- coding:utf-8 -*-
import requests
import csv
import re
from bs4 import BeautifulSoup

#1. read the csv and get the movie code
#2. bring the source and parse


def director_search(id_actor, id_film, productYear):
	# id_actor = str(10058252)
	# id_film = str(20127192)
	# productYear = 2012
	result = {}

	di_sf = 0
	di_family = 0
	di_horror = 0
	di_docu = 0
	di_drama = 0
	di_romance = 0
	di_mystery = 0
	di_western = 0
	di_action = 0
	di_adventure = 0
	di_war = 0
	di_comedy = 0
	di_fantasy = 0
	di_criminal = 0
	di_musical = 0
	di_traditional = 0
	di_thriller = 0
	di_total_movie = 0

	try:
		actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
		    'code': id_actor,
		    'sType': "filmo",
		    'etcParam':1
		}, headers={
		    'Accept': 'application/json'
		})
	except:
		actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
		    'code': id_actor,
		    'sType': "filmo",
		    'etcParam':1
		}, headers={
		    'Accept': 'application/json'
		})

	# print("%s" % str(actor.content.decode("utf-8")))

	# with open("actor.txt", 'w') as outfile:
	# 	outfile.write(actor.content.decode("utf-8"))

	director_soup = BeautifulSoup(actor.content, "lxml")

	#get etcParam(page list)
	# movie_soup.find("li", text=str(u'배급사')).findNext("li").findAll("a")
	# print(actor_soup.find("p", attrs={'class':"pageList pmt2"}).text.split("\n"))
	page_list = director_soup.find("p", attrs={'class':"pageList pmt2"}).text.split("\n")
	pages = [p for p in page_list if p]	#remove empty string, etcParam
	
	# print(pages)	#etcParam
	# genre check
	for p in pages:
		try:
			actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
			    'code': id_actor,
			    'sType': "filmo",
			    'etcParam':p
			}, headers={
			    'Accept': 'application/json'
			})	
		except:
			actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
			    'code': id_actor,
			    'sType': "filmo",
			    'etcParam':p
			}, headers={
			    'Accept': 'application/json'
			})	

		director_soup = BeautifulSoup(actor.content, "lxml")		

		movie_list = director_soup.find('ul', attrs={'class':"fmList"})
		movie_list = movie_list.findAll('dd', attrs={'class':'minfo'})
		# print(movie_list)
		for i in movie_list:
			if("감독" not in i.parent.find("dd").text):
				continue
			# print(i.text)
			m_list = i.text.split("|")
			# print(m_list)	#m_list[0] - year, m_list[1] - nation, m_list[2] - genre
			# print("=============" + m_list[0])
			ac_debut = m_list[0]

			movieYear = 0
			try:
				movieYear = int(m_list[0])
			except:
				movieYear = int(productYear)

			if(int(productYear) > movieYear):
				di_total_movie += 1
				# print(m_list[1])
				# print("멜로" in m_list[2])
				for j in m_list:
					ac_genre = j.strip()
					# print(ac_genre)

					if("SF" in ac_genre):
						di_sf += 1
					if("가족" in ac_genre):
						di_family += 1
					if("호러" in ac_genre):
						di_horror += 1
					if("다큐멘터리" in ac_genre):
						di_docu += 1
					if("드라마" in ac_genre):
						di_drama += 1
					if("멜로" in ac_genre):
						di_romance += 1
					if("미스터리" in ac_genre):
						di_mystery += 1
					if("서부" in ac_genre):
						di_western += 1
					if("액션" in ac_genre):
						di_action += 1
					if("어드벤처" in ac_genre):
						di_adventure += 1
					if("전쟁" in ac_genre):
						di_war += 1
					if("코미디" in ac_genre):
						di_comedy += 1
					if("판타지" in ac_genre):
						di_fantasy += 1
					if("범죄" in ac_genre):
						di_criminal += 1
					if("뮤지컬" in ac_genre):
						di_musical += 1
					if("사극" in ac_genre):
						di_traditional += 1
					if("스릴러" in ac_genre):
						di_thriller += 1

		#1. parse movie list
		#2. get text from span tag
		
			# print(j.find('span'))

	result['di_sf_genre'] = di_sf
	result['di_family_genre'] = di_family
	result['di_horror_genre'] = di_horror
	result['di_docu_genre'] = di_docu
	result['di_drama_genre'] = di_drama
	result['di_romance_genre'] = di_romance
	result['di_mystery_genre'] = di_mystery
	result['di_western_genre'] = di_western
	result['di_action_genre'] = di_action
	result['di_adventure_genre'] = di_adventure
	result['di_war_genre'] = di_war
	result['di_comedy_genre'] = di_comedy
	result['di_fantasy_genre'] = di_fantasy
	result['di_criminal_genre'] = di_criminal
	result['di_musical_genre'] = di_musical
	result['di_traditional_genre'] = di_traditional
	result['di_thriller_genre'] = di_thriller
	result['di_total_movie'] = di_total_movie

	return result

def actor_search(id_actor, id_film, productYear):
	# id_actor = str(20217606)
	# id_film = 20127192
	# productYear = 2015
	result = {}

	ac_sf = 0
	ac_family = 0
	ac_horror = 0
	ac_docu = 0
	ac_drama = 0
	ac_romance = 0
	ac_mystery = 0
	ac_western = 0
	ac_action = 0
	ac_adventure = 0
	ac_war = 0
	ac_comedy = 0
	ac_fantasy = 0
	ac_criminal = 0
	ac_musical = 0
	ac_traditional = 0
	ac_thriller = 0
	ac_total_movie = 0

	ac_debut = 0
	ac_bir_y = 0
	ac_sex = 0

	try:
		actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
		    'code': id_actor,
		    'sType': "filmo",
		    'etcParam':1
		}, headers={
		    'Accept': 'application/json'
		})
	except:
		actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
		    'code': id_actor,
		    'sType': "filmo",
		    'etcParam':1
		}, headers={
		    'Accept': 'application/json'
		})

	# print("%s" % str(actor.content.decode("utf-8")))

	# with open("actor.txt", 'w') as outfile:
	# 	outfile.write(actor.content.decode("utf-8"))

	actor_soup = BeautifulSoup(actor.content, "lxml")

	#get etcParam(page list)
	# movie_soup.find("li", text=str(u'배급사')).findNext("li").findAll("a")
	# print(actor_soup.find("p", attrs={'class':"pageList pmt2"}).text.split("\n"))
	page_list = actor_soup.find("p", attrs={'class':"pageList pmt2"}).text.split("\n")
	pages = [p for p in page_list if p]	#remove empty string, etcParam
	
	# print(pages)	#etcParam
	# genre check
	for p in pages:
		try:
			actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
			    'code': id_actor,
			    'sType': "filmo",
			    'etcParam':p
			}, headers={
			    'Accept': 'application/json'
			})	
		except:
			actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
			    'code': id_actor,
			    'sType': "filmo",
			    'etcParam':p
			}, headers={
			    'Accept': 'application/json'
			})

		actor_soup2 = BeautifulSoup(actor.content, "lxml")		

		movie_list = actor_soup2.find('ul', attrs={'class':"fmList"})
		movie_list = movie_list.findAll('dd', attrs={'class':'minfo'})
		# print(movie_list)
		for i in movie_list:
			# print(i.text)
			if("주연" not in i.parent.find("dd").text):
				is_actor = 1

			if("조연" not in i.parent.find("dd").text):
				is_actor = 1

			if("단역" not in i.parent.find("dd").text):
				is_actor = 1

			if(is_actor != 1):
				continue

			m_list = i.text.split("|")
			# print(m_list)	#m_list[0] - year, m_list[1] - nation, m_list[2] - genre
			# print("=============" + m_list[0])
			if(m_list[0].strip() == ""):
				ac_debut = ac_debut
			else:
				ac_debut = m_list[0]

			movieYear = 0
			try:
				movieYear = int(m_list[0])
			except:
				movieYear = int(productYear)

			if(int(productYear) > movieYear):
				ac_total_movie += 1
				# print(m_list[1])
				# print("멜로" in m_list[2])
				for j in m_list:
					ac_genre = j.strip()
					# print(ac_genre)

					if("SF" in ac_genre):
						ac_sf += 1
					if("가족" in ac_genre):
						ac_family += 1
					if("호러" in ac_genre):
						ac_horror += 1
					if("다큐멘터리" in ac_genre):
						ac_docu += 1
					if("드라마" in ac_genre):
						ac_drama += 1
					if("멜로" in ac_genre):
						ac_romance += 1
					if("미스터리" in ac_genre):
						ac_mystery += 1
					if("서부" in ac_genre):
						ac_western += 1
					if("액션" in ac_genre):
						ac_action += 1
					if("어드벤처" in ac_genre):
						ac_adventure += 1
					if("전쟁" in ac_genre):
						ac_war += 1
					if("코미디" in ac_genre):
						ac_comedy += 1
					if("판타지" in ac_genre):
						ac_fantasy += 1
					if("범죄" in ac_genre):
						ac_criminal += 1
					if("뮤지컬" in ac_genre):
						ac_musical += 1
					if("사극" in ac_genre):
						ac_traditional += 1
					if("스릴러" in ac_genre):
						ac_thriller += 1

		#1. parse movie list
		#2. get text from span tag
		
			# print(j.find('span'))


	#basic information
	actor_url = 'http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do'
	try:
		actor_stat = requests.post(actor_url, data = {
				'code':str(id_actor),
				'titleYN':'Y',
				'isOuterReq':'false'
			})
	except:
		actor_stat = requests.post(actor_url, data = {
				'code':str(id_actor),
				'titleYN':'Y',
				'isOuterReq':'false'
			})

	# with open("actor2.txt", 'w') as outfile:
	# 	outfile.write(actor_stat.content.decode("utf-8"))
	
	actor_soup3 = BeautifulSoup(actor_stat.content, "lxml")
	# actor = actor_soup.find("strong").text
	# print("********************")
	# print(id_actor)
	# print(actor_soup3.text)
	if(actor_soup3.find("dt", text=str(u"성별")) is None):
		if("남자" in actor_soup3.text):
			ac_sex = 1
		elif("여자" in actor_soup3.text):
			ac_sex = 0
		else:
			ac_sex = ""
		# print(actor_soup3.find("dt", text=str(u"출생")))
		# print(actor_soup3.find("dt", text=str(u"출생")) is None)
		# print(actor_soup3.text)
		# print(actor_soup3)
	else:
		actor_stat_list = actor_soup3.find("dt", text=str(u"성별")).findNext("dd").text.strip().split("\r\n")
		actor_stat_list = [ac.strip() for ac in actor_stat_list if ac.strip()]

		if("남" in actor_stat_list[0]): 
			ac_sex = 1 
		else: 
			ac_sex = 0	#sex

		if("해당" in actor_stat_list[0]):
			ac_sex = ""

		ac_bir_y = actor_stat_list[2][:4]
		if("해당" in ac_bir_y):
			ac_bir_y = ""

	# print(actor_soup.find("table", attrs = {'class':'board02'}).findAll("a"))
	award_str = ""

	try:
		for ac in actor_soup3.find("table", attrs = {'class':'board02'}).findAll("a"):
			# print(ac)
			award_str += str(ac)
	except:
		award_str = ""

	# search the movie code, return how many times the specific string occur 
	# print(len(re.findall(id_film, award_str)))	#film_id should be the value
	ac_award = len(re.findall(id_film, award_str))

	result['ac_debut'] = ac_debut
	result['ac_bir_y'] = ac_bir_y
	result['ac_sex'] = ac_sex
	result['ac_award'] = ac_award

	result['ac_sf_genre'] = ac_sf
	result['ac_family_genre'] = ac_family
	result['ac_horror_genre'] = ac_horror
	result['ac_docu_genre'] = ac_docu
	result['ac_drama_genre'] = ac_drama
	result['ac_romance_genre'] = ac_romance
	result['ac_mystery_genre'] = ac_mystery
	result['ac_western_genre'] = ac_western
	result['ac_action_genre'] = ac_action
	result['ac_adventure_genre'] = ac_adventure
	result['ac_war_genre'] = ac_war
	result['ac_comedy_genre'] = ac_comedy
	result['ac_fantasy_genre'] = ac_fantasy
	result['ac_criminal_genre'] = ac_criminal
	result['ac_musical_genre'] = ac_musical
	result['ac_traditional_genre'] = ac_traditional
	result['ac_thriller_genre'] = ac_thriller
	result['ac_total_movie'] = ac_total_movie
	# result['actor'] = actor

	return result

def searchMovie():
	start = 3000
	end = 3805
	index_movie_main = 0	
	filename = "second_2_4_3000_3805.csv"
	with open(filename, 'w', newline='') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(["film_id", "title_kor", "productYear","openDT", "id_director", "director", "id_actor", "actor", "ac_debut", "ac_bir_y", "ac_sex", "ac_award", "ac_main",
					"sf_genre", "family_genre", "horror_genre", "docu_genre", "drama_genre", "romance_genre", "mystery_genre", "western_genre", "action_genre", "adventure_genre", 
					"war_genre", "comedy_genre", "fantasy_genre", "criminal_genre", "musical_genre", "traditional_genre", "thriller_genre",
					"ac_sf_genre", "ac_family_genre", "ac_horror_genre", "ac_docu_genre", "ac_drama_genre", "ac_romance_genre", 
					"ac_mystery_genre", "ac_western_genre", "ac_action_genre", "ac_adventure_genre", 
					"ac_war_genre", "ac_comedy_genre", "ac_fantasy_genre", "ac_criminal_genre", "ac_musical_genre", "ac_traditional_genre", "ac_thriller_genre", "ac_total_movie",
					"di_sf_genre", "di_family_genre", "di_horror_genre", "di_docu_genre", "di_drama_genre", "di_romance_genre", "di_mystery_genre", 
					"di_western_genre", "di_action_genre", "di_adventure_genre", 
					"di_war_genre", "di_comedy_genre", "di_fantasy_genre", "di_criminal_genre", "di_musical_genre", "di_traditional_genre", "di_thriller_genre", "di_total_movie",
					"major_distributor", "adult"
					])

	with open('film_id.csv', "r") as f:
		reader = csv.reader(f)

		for id_film in reader:
			print("=============\t" + id_film[0] + "\t" + id_film[1] + "\t" + id_film[2] + "\t" + str(index_movie_main))
			index_movie_main = index_movie_main + 1
		
			if(index_movie_main < start):
				continue
			if(index_movie_main > end):
				break

			# id_film = ['19970014', '사극', "제목"]	#@@for debug
			# print("=============\t" + id_film[0] + "\t")
			movie_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			try:
				source_code = requests.post(movie_url, {'code' : id_film[0]})
			except:
				source_code = requests.post(movie_url, {'code' : id_film[0]})
			
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

			is_adult = 0
			try:
				if("청소년관람불가" in soup.find("p", text=str(u'[관람등급]')).findNext("li").text):
					is_adult = 1
			except:
				is_adult = 0


			#distributor
			distributor = ""
			try:
				for ch in soup.find("li", text=str(u'배급사')).findNext("li").text:
					try:
						distributor += ch
					except:
						distributor = distributor
			except:
				distributor = ""

			major_distributor = 0

			if("CGV" in distributor.strip()):
				major_distributor = 1
			
			if("롯데" in distributor.strip()):
				major_distributor = 1

			if("쇼박스" in distributor.strip()):
				major_distributor = 1

			if("씨제이" in distributor.strip()):
				major_distributor = 1

			#genre of movie
			sf_genre = 0
			family_genre = 0
			horror_genre = 0
			docu_genre = 0
			drama_genre = 0
			romance_genre = 0
			mystery_genre = 0
			western_genre = 0
			action_genre = 0
			adventure_genre = 0
			war_genre = 0
			comedy_genre = 0
			fantasy_genre = 0
			criminal_genre = 0
			musical_genre = 0
			traditional_genre = 0
			thriller_genre = 0

			if("SF" in id_film[1]):
				sf_genre += 1
			if("가족" in id_film[1]):
				family_genre += 1
			if("호러" in id_film[1]):
				horror_genre += 1
			if("다큐멘터리" in id_film[1]):
				docu_genre += 1
			if("드라마" in id_film[1]):
				drama_genre += 1
			if("멜로" in id_film[1]):
				romance_genre += 1
			if("미스터리" in id_film[1]):
				mystery_genre += 1
			if("서부" in id_film[1]):
				western_genre += 1
			if("액션" in id_film[1]):
				action_genre += 1
			if("어드벤처" in id_film[1]):
				adventure_genre += 1
			if("전쟁" in id_film[1]):
				war_genre += 1
			if("코미디" in id_film[1]):
				comedy_genre += 1
			if("판타지" in id_film[1]):
				fantasy_genre += 1
			if("범죄" in id_film[1]):
				criminal_genre += 1
			if("뮤지컬" in id_film[1]):
				musical_genre += 1
			if("사극" in id_film[1]):
				traditional_genre += 1
			if("스릴러" in id_film[1]):
				thriller_genre += 1

			movie_staff_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovStaffLists.do'
			try:
				staff_code = requests.post(movie_staff_url, {'movieCd':id_film[0]}, headers={
				    'Accept': 'application/json'
				})
			except:
				staff_code = requests.post(movie_staff_url, {'movieCd':id_film[0]}, headers={
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
					# print(d_str)
					d_dic = eval(d_str)
					if(d_dic["roleNm"] == "감독"):
						directors += d_dic["peopleNm"] + ", "
						id_directors += d_dic["peopleCd"] + ", "

			try:
				movie_staff = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovActorLists.do', data={
				    'movieCd': id_film[0],
				}, headers={
				    'Accept': 'application/json'
				})	
			except:
				movie_staff = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovActorLists.do', data={
				    'movieCd': id_film[0],
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
						main_actors = main_actors + actor_dic["peopleNm"] + ", "
						main_actors_id = main_actors_id + actor_dic["peopleCd"] + ", "	
					elif(int(actor_dic["actorGb"]) == 2):
						sub_actors += actor_dic["peopleNm"] + ", "
						sub_actors_id += actor_dic["peopleCd"] + ", "	

			# print(main_actors_id[:-2].split(", "))
			# print(sub_actors_id[:-2].split(", "))

			id_directors_list = id_directors[:-2].split(", ")
			

			id_main_actors_list = main_actors_id[:-2].split(", ")
			id_sub_actors_list = sub_actors_id[:-2].split(", ")

			
			# actor_stat_list = [ac.strip() for ac in actor_stat_list if ac.strip()]

			id_main_actors_list = [idm.strip() for idm in id_main_actors_list if idm.strip()]
			id_sub_actors_list = [ids.strip() for ids in id_sub_actors_list if ids.strip()]

			# print(len(id_sub_actors_list))
			# print("=======film id : \t" + id_film[0])

			index_dir = 0
			index_movie = 0
			
			for id_director in id_directors_list:
				index_main = 0
				index_sub = 0
				# print(directors[:-2].split(", ")[index_dir])
				director_name = directors[:-2].split(", ")[index_dir]
				index_dir += 1
				# print(director_search(id_director, id_film[0], productYear))
				info_director = director_search(id_director, id_film[0], productYear)
				for id_main in id_main_actors_list:
					# print(actor_search(id_main, id_film[0], productYear))
					info_actor = actor_search(id_main, id_film[0], productYear)
					# print(info_actor)

					temp = []
					temp.append(id_film[0])
					temp.append(id_film[2])
					temp.append(productYear)
					temp.append(openDT)
					temp.append(id_director)
					temp.append(director_name)
					temp.append(id_main)
					temp.append(main_actors[:-2].split(", ")[index_main])
					temp.append(info_actor['ac_debut'])
					temp.append(info_actor['ac_bir_y'])
					temp.append(info_actor['ac_sex'])
					temp.append(info_actor['ac_award'])
					temp.append(str(1))	#ac_main 1 - main, 0 - sub
					temp.append(sf_genre)
					temp.append(family_genre)
					temp.append(horror_genre)
					temp.append(docu_genre)
					temp.append(drama_genre)
					temp.append(romance_genre)
					temp.append(mystery_genre)
					temp.append(western_genre)
					temp.append(action_genre)
					temp.append(adventure_genre)
					temp.append(war_genre)
					temp.append(comedy_genre)
					temp.append(fantasy_genre)
					temp.append(criminal_genre)
					temp.append(musical_genre)
					temp.append(traditional_genre)
					temp.append(thriller_genre)
					temp.append(info_actor['ac_sf_genre'])
					temp.append(info_actor['ac_family_genre'])
					temp.append(info_actor['ac_horror_genre'])
					temp.append(info_actor['ac_docu_genre'])
					temp.append(info_actor['ac_drama_genre'])
					temp.append(info_actor['ac_romance_genre'])
					temp.append(info_actor['ac_mystery_genre'])
					temp.append(info_actor['ac_western_genre'])
					temp.append(info_actor['ac_action_genre'])
					temp.append(info_actor['ac_adventure_genre'])
					temp.append(info_actor['ac_war_genre'])
					temp.append(info_actor['ac_comedy_genre'])
					temp.append(info_actor['ac_fantasy_genre'])
					temp.append(info_actor['ac_criminal_genre'])
					temp.append(info_actor['ac_musical_genre'])
					temp.append(info_actor['ac_traditional_genre'])
					temp.append(info_actor['ac_thriller_genre'])
					temp.append(info_actor['ac_total_movie'])
					temp.append(info_director['di_sf_genre'])
					temp.append(info_director['di_family_genre'])
					temp.append(info_director['di_horror_genre'])
					temp.append(info_director['di_docu_genre'])
					temp.append(info_director['di_drama_genre'])
					temp.append(info_director['di_romance_genre'])
					temp.append(info_director['di_mystery_genre'])
					temp.append(info_director['di_western_genre'])
					temp.append(info_director['di_action_genre'])
					temp.append(info_director['di_adventure_genre'])
					temp.append(info_director['di_war_genre'])
					temp.append(info_director['di_comedy_genre'])
					temp.append(info_director['di_fantasy_genre'])
					temp.append(info_director['di_criminal_genre'])
					temp.append(info_director['di_musical_genre'])
					temp.append(info_director['di_traditional_genre'])
					temp.append(info_director['di_thriller_genre'])
					temp.append(info_director['di_total_movie'])
					temp.append(major_distributor)
					temp.append(is_adult)

					index_main += 1
					with open(filename, "a", newline='') as outfile:
						writer = csv.writer(outfile)
						writer.writerow(temp)

				for id_sub in id_sub_actors_list:
					# print(actor_search(id_sub, id_film[0], productYear))
					info_actor = actor_search(id_sub, id_film[0], productYear)
					# print(info_actor['actor'])

					temp = []
					temp.append(id_film[0])
					temp.append(id_film[2])
					temp.append(productYear)
					temp.append(openDT)
					temp.append(id_director)
					temp.append(director_name)
					temp.append(id_sub)
					temp.append(sub_actors[:-2].split(", ")[index_sub])
					temp.append(info_actor['ac_debut'])
					temp.append(info_actor['ac_bir_y'])
					temp.append(info_actor['ac_sex'])
					temp.append(info_actor['ac_award'])
					temp.append(str(0))	#ac_main 1 - main, 0 - sub
					temp.append(sf_genre)
					temp.append(family_genre)
					temp.append(horror_genre)
					temp.append(docu_genre)
					temp.append(drama_genre)
					temp.append(romance_genre)
					temp.append(mystery_genre)
					temp.append(western_genre)
					temp.append(action_genre)
					temp.append(adventure_genre)
					temp.append(war_genre)
					temp.append(comedy_genre)
					temp.append(fantasy_genre)
					temp.append(criminal_genre)
					temp.append(musical_genre)
					temp.append(traditional_genre)
					temp.append(thriller_genre)
					temp.append(info_actor['ac_sf_genre'])
					temp.append(info_actor['ac_family_genre'])
					temp.append(info_actor['ac_horror_genre'])
					temp.append(info_actor['ac_docu_genre'])
					temp.append(info_actor['ac_drama_genre'])
					temp.append(info_actor['ac_romance_genre'])
					temp.append(info_actor['ac_mystery_genre'])
					temp.append(info_actor['ac_western_genre'])
					temp.append(info_actor['ac_action_genre'])
					temp.append(info_actor['ac_adventure_genre'])
					temp.append(info_actor['ac_war_genre'])
					temp.append(info_actor['ac_comedy_genre'])
					temp.append(info_actor['ac_fantasy_genre'])
					temp.append(info_actor['ac_criminal_genre'])
					temp.append(info_actor['ac_musical_genre'])
					temp.append(info_actor['ac_traditional_genre'])
					temp.append(info_actor['ac_thriller_genre'])
					temp.append(info_actor['ac_total_movie'])
					temp.append(info_director['di_sf_genre'])
					temp.append(info_director['di_family_genre'])
					temp.append(info_director['di_horror_genre'])
					temp.append(info_director['di_docu_genre'])
					temp.append(info_director['di_drama_genre'])
					temp.append(info_director['di_romance_genre'])
					temp.append(info_director['di_mystery_genre'])
					temp.append(info_director['di_western_genre'])
					temp.append(info_director['di_action_genre'])
					temp.append(info_director['di_adventure_genre'])
					temp.append(info_director['di_war_genre'])
					temp.append(info_director['di_comedy_genre'])
					temp.append(info_director['di_fantasy_genre'])
					temp.append(info_director['di_criminal_genre'])
					temp.append(info_director['di_musical_genre'])
					temp.append(info_director['di_traditional_genre'])
					temp.append(info_director['di_thriller_genre'])
					temp.append(info_director['di_total_movie'])
					temp.append(major_distributor)
					temp.append(is_adult)

					index_sub += 1
					with open(filename, "a", newline='') as outfile:
						writer = csv.writer(outfile)
						writer.writerow(temp)
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
			# break		


# writer.writerow(["film_id", "productYear","openDT", "id_director", "director", "id_actor", "actor", "ac_debut", "ac_bir_y", "ac_sex", "ac_award", "ac_main",
# 					"sf_genre", "family_genre", "horror_genre", "docu_genre", "drama_genre", "romance_genre", "mystery_genre", "western_genre", "action_genre", "adventure_genre", 
# 					"war_genre", "comedy_genre", "fantasy_genre", "criminal_genre", "musical_genre", "traditional_genre", "thriller_genre",
# 					"ac_sf_genre", "ac_family_genre", "ac_horror_genre", "ac_docu_genre", "ac_drama_genre", "ac_romance_genre", 
# 					"ac_mystery_genre", "ac_western_genre", "ac_action_genre", "ac_adventure_genre", 
# 					"ac_war_genre", "ac_comedy_genre", "ac_fantasy_genre", "ac_criminal_genre", "ac_musical_genre", "ac_traditional_genre", "ac_thriller_genre", "ac_total_movie"
# 					"di_sf_genre", "di_family_genre", "di_horror_genre", "di_docu_genre", "di_drama_genre", "di_romance_genre", "di_mystery_genre", 
# 					"di_western_genre", "di_action_genre", "di_adventure_genre", 
# 					"di_war_genre", "di_comedy_genre", "di_fantasy_genre", "di_criminal_genre", "di_musical_genre", "di_traditional_genre", "di_thriller_genre", "di_total_movie",
# 					"major_distributor", "adult"
# 					])
searchMovie()
