# -*- coding:utf-8 -*-
import requests
import csv
import re
from bs4 import BeautifulSoup

def genre(x):
	return{

	}[x]

def director_search():
	id_actor = str(10019069)
	id_film = str(20127192)
	productYear = 2012
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

		for i in movie_list:
			if("감독" not in i.parent.find("dd").text):
				continue
			# print(i.parent.find("dd").text)
			m_list = i.text.split("|")
			# print(m_list)	#m_list[0] - year, m_list[1] - nation, m_list[2] - genre
			# print("=============" + m_list[0])
			ac_debut = m_list[0]
			if(productYear > int(m_list[0])):
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

print(director_search())