# -*- coding:utf-8 -*-
import requests
import csv
import re
from bs4 import BeautifulSoup

def genre(x):
	return{

	}[x]

def actor():
	id_actor = str(10061252)
	id_film = str(19970014)
	productYear = 2015
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
		actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
		    'code': id_actor,
		    'sType': "filmo",
		    'etcParam':p
		}, headers={
		    'Accept': 'application/json'
		})	

		actor_soup = BeautifulSoup(actor.content, "lxml")		

		movie_list = actor_soup.find('ul', attrs={'class':"fmList"})
		movie_list = movie_list.findAll('dd', attrs={'class':'minfo'})
		# print(movie_list)
		for i in movie_list:
			# print(i.text)
			m_list = i.text.split("|")
			# print(m_list)	#m_list[0] - year, m_list[1] - nation, m_list[2] - genre
			print("=============" + m_list[0])
			
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
					print(ac_genre)

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
	actor_stat = requests.post(actor_url, data = {
			'code':id_actor,
			'titleYN':'Y',
			'isOuterReq':'false'
		})

	# with open("actor2.txt", 'w') as outfile:
	# 	outfile.write(actor_stat.content.decode("utf-8"))
	
	actor_soup = BeautifulSoup(actor_stat.content, "lxml")
	actor = actor_soup.find("strong").text
	if(actor_soup.find("dt", text=str(u"성별")) is None):
		print("None type")
	actor_stat_list = actor_soup.find("dt", text=str(u'성별')).findNext("dd").text.strip().split("\r\n")
	actor_stat_list = [ac.strip() for ac in actor_stat_list if ac.strip()]

	if("남" in actor_stat_list[0]): 
		ac_sex = 1 
	else: 
		ac_sex = 0	#sex

	if("해당" in actor_stat_list[0]):
		ac_sex = ""

	ac_bir_y = actor_stat_list[2]
	if("해당" in ac_bir_y):
		ac_bir_y = ""

	# print(actor_soup.find("table", attrs = {'class':'board02'}).findAll("a"))
	award_str = ""
	try:
		for ac in actor_soup.find("table", attrs = {'class':'board02'}).findAll("a"):
			# print(ac)
			award_str += str(ac)
	except:
		award_str = ""

	# search the movie code, return how many times the specific string occur 
	print(len(re.findall(id_film, award_str)))	#film_id should be the value
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
	result['actor'] = actor

	print("debut\t" + result['ac_debut'])

	return result
print(actor())