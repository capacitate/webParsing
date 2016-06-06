# -*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

def actor():
	actor = requests.post('http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do', data={
	    'code': 20127192,
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
	
	#1. parse movie list
	#2. get text from span tag
	movie_list = actor_soup.find('ul', attrs={'class':"fmList"})
	movie_list = movie_list.findAll('dd', attrs={'class':'minfo'})
	# print(movie_list)
	for i in movie_list:
		# print(i.text)
		m_list = i.text.split("|")
		# print(m_list)	#m_list[0] - year, m_list[1] - nation, m_list[2] - genre
		print("=============" + m_list[0])
		print("멜로" in m_list[2])
		for j in m_list:
			print(j.strip())
			# print(j.find('span'))


actor()	