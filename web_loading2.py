# -*- coding:utf-8 -*-
import requests
import sys
import ast
import json
import csv
from bs4 import BeautifulSoup

# reload(sys)
# sys.setdefaultencoding('utf-8')

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
def spider(max_pages):
	page = 1

	while page < max_pages:
		url = 'http://creativeworks.tistory.com/' + str(page)
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text, 'lxml')
		print(soup)
		page += 1


def loading2(max_pages):
	page = 7

	movie_data = {'id_movie':[], 'kor_movieNM':[], 'en_movieNM':[], 'productYear':[], 
		'openDT':[], 'prdstate':[], 'nation_all':[], 'genre_all':[], 'repGenre':[], 
		'id_director':[], 'directors':[], 
		'maker_all':[], 'id_maker':[], 'makerNM':[],
		'distributorNM':[], 'importerNM':[],
		'main_actors_name':[], 'main_id_actors':[], 
		'sub_actors_name':[], 'sub_id_actors':[],
		'how_many_times':[]}

	with open("test.csv", 'w', newline='') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(["id_movie", "kor_movieNM", "en_movieNM", "productYear", "openDT", "prdstate", "nation_all", 
				"genre_all", "repGenre", "id_director", "directors", "maker_all", "id_maker", "main_actors_name", 
				"main_id_actors", "sub_actors_name", "sub_id_actors", "how_many_times"])
			
	while page < max_pages:
		url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do'
		source_code = requests.post(url, {'curPage' : page})
		
		encoding = source_code.encoding if 'charset' in source_code.headers.get('content-type', '').lower() else None
		soup = BeautifulSoup(source_code.content, "lxml", from_encoding=encoding)
		
		data = []
		movie_table = soup.find('table', attrs={'class':'boardList03'})
		table_body = movie_table.find('tbody')
		rows = table_body.findAll('tr')

		for row in rows:
			cols = row.findAll('td')
			all_nation = cols[3]['title']	#nation_all
			
			all_genre = cols[5]['title']	#genre_all

			id_directors_list = cols[7].findAll('a')
			ids_dir = ''
			for id_d in id_directors_list:
				ids_dir = ids_dir + id_d['onclick'].split('\'')[3] + ','	#id_director

			movie_id = cols[0].find('a')['onclick'].split('\'')[3]

			cols = [ele.text.strip() for ele in cols]

			movieNM_kor = cols[0].strip()	#kor_movieNM
			movieNM_en = cols[1].strip()	#en_movieNM
			yearProduct = cols[2].strip()	#productYear
			
			if(len(cols[5].strip().split('(')) > 1):
				genreRep = cols[5].strip().split('(')[0]
			else:
				genreRep = cols[5].strip()	#repGenre
			
			stateprd = cols[6].strip()	#prdstate
			
			#directors
			if(len(cols[7].split(',')) > 1):
				directors_split = cols[7].split(',')
				directors = ''
				for director in directors_split:
					directors = directors + director.strip() + ','
			else:
				directors = cols[7]

			#load movie detail page		
			movie_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			movie_source = requests.post(movie_url, {'code' : movie_id})
			movie_soup = BeautifulSoup(movie_source.content, "lxml")

			#openDT, actors_name, id_actors_name, how_many_times, companyNM
			#openDT
			print("==================" + str(page))
			print(movie_id)
			
			try:
				DTopen = movie_soup.find("dt", text=str(u'개봉일')).findNext("dd").text.strip().split("\r\n")[0]
				DTopen = DTopen.replace("-", "")
			except:
				DTopen = movie_soup.find("dt", text=str(u'개봉(예정)일')).findNext("dd").text.strip().split("\r\n")[0]
				DTopen = DTopen.replace("-", "")

			
			#company
			# 'maker_all':[], 'id_maker':[], 'makerNM':[],
			# 'distributorNM':[], 'importerNM':[],
			all_maker = ""
			all_maker_id = ""

			all_dist = ""
			all_dist_id = ""
			try:
				makers = movie_soup.find("li", text=str(u'제작사')).findNext("li").findAll("a")
				for maker in makers:
					all_maker = all_maker + maker.text.strip() + ","
					all_maker_id = all_maker_id + maker['onclick'].split('\'')[3] + ","

				# print("해외세일즈사" + movie_soup.find("li", text=str(u'해외세일즈사')).findNext("li").text.strip())
			except AttributeError:
				print("Maker Error or Empty movie_id\t" + movie_id)
				all_maker = ""
				all_maker_id = ""

			try:
				distributors = movie_soup.find("li", text=str(u'배급사')).findNext("li").findAll("a")
				for dist in distributors:
					all_dist = all_dist + dist.text.strip() + ","
					all_dist_id = all_dist_id + dist['onclick'].split('\'')[3] + ","
			except AttributeError:
				print("Distributor Error or Empty movie_id\t" + movie_id)
				all_dist = ""
				all_dist_id = ""
			
			#award
			try:
				num_award = len(movie_soup.find("h3", text=str(u'영화제 출품정보')).findNext("tbody").findAll("tr"))
			except:
				num_award = 0
			

			# filename = "test.txt"
			# text_file = open(filename, "w")
			# text_file.write("%s\n" % movie_soup)
			# text_file.close()
			

			#actors_name
			movie_staff = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovActorLists.do', data={
			    'movieCd': movie_id,
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

			##### check the value
			# print(movieNM_kor)
			# print(movieNM_en)
			# print(yearProduct)
			# print(genreRep)
			# print(stateprd)
			# print(movie_id)
			# print(all_nation)
			# print(all_genre)
			# print(ids_dir)
			# print(directors)
			# print("%s" % main_actors)
			# print(main_actors_id)
			# print(DTopen)
			# print(all_maker)
			# print(all_maker_id)
			# print(all_dist)
			# print(all_dist_id)
			# print(num_award)

		# 		movie_data = {'id_movie':[], 'kor_movieNM':[], 'en_movieNM':[], 'productYear':[], 
		# 'openDT':[], 'prdstate':[], 'nation_all':[], 'genre_all':[], 'repGenre':[], 
		# 'id_director':[], 'directors':[], 
		# 'maker_all':[], 'id_maker':[], 'makerNM':[],
		# 'distributorNM':[], 'importerNM':[],
		# 'main_actors_name':[], 'main_id_actors':[], 
		# 'sub_actors_name':[], 'sub_id_actors':[],
		# 'how_many_times':[]}

			

			movie_data['id_movie'] += str(movie_id)
			movie_data['kor_movieNM'] += movieNM_kor
			movie_data['en_movieNM'] += movieNM_en
			movie_data['productYear'] += yearProduct
			movie_data['openDT'] += DTopen
			movie_data['prdstate'] += stateprd
			movie_data['nation_all'] += all_nation
			movie_data['genre_all'] += all_genre
			movie_data['repGenre'] += genreRep
			movie_data['id_director'] += ids_dir
			movie_data['directors'] += directors
			movie_data['maker_all'] += all_maker
			movie_data['id_maker'] += all_maker_id
			movie_data['main_actors_name'] += main_actors
			movie_data['main_id_actors'] += main_actors_id
			movie_data['sub_actors_name'] += sub_actors
			movie_data['sub_id_actors'] += sub_actors_id
			movie_data['how_many_times'] += str(num_award)
			

			# filename = "test.txt"
			# text_file = open(filename, "w")
			# text_file.write("%s\n" % movie_data)
			# text_file.close()



			temp = []
			temp.append(str(movie_id))
			temp.append(str(movieNM_kor))
			temp.append(str(movieNM_en).replace(u"\u00E8", "e"))
			temp.append(str(yearProduct))
			temp.append(str(DTopen))
			temp.append(str(stateprd))
			temp.append(str(all_nation))
			temp.append(str(all_genre))
			temp.append(str(genreRep))
			temp.append(str(ids_dir))
			temp.append(str(directors))
			temp.append(str(all_maker))
			temp.append(str(all_maker_id))
			temp.append(str(main_actors))
			temp.append(str(main_actors_id))
			temp.append(str(sub_actors))
			temp.append(str(sub_actors_id))
			temp.append(str(num_award))
			temp.append(str(directors))
			
			with open("test.csv", 'a', newline='') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(temp)


			# for col in cols:
				# print(col)
			# data.append([ele for ele in cols]) #Get rid of empty values
			

		# filename = "output" + str(page) + ".txt"
		# text_file = open(filename, "w")
		# for item in data:
		# 	item_str = ','.join(item)
		# 	print("%s\n" % item_str)
		# 	text_file.write("%s\n" % item_str)
		# text_file.write(data)
		# text_file.close()
		page += 1

	print("======\tEXIT\t======")
	# df = pd.DataFrame(movie_data)
	# df.to_csv("test.csv", sep="\t")


#### from jonghwan, GOD jonghwan

def loading(max_pages):
	page = 1

	movie_data = {'id_movie':[], 'kor_movieNM':[], 'en_movieNM':[], 'productYear':[], 
		'openDT':[], 'prdstate':[], 'nation_all':[], 'genre_all':[], 'repGenre':[], 
		'id_director':[], 'directors':[], 'company_all':[], 'id_company':[], 'companyNM':[],
		'actors_name':[], 'id_actors_name':[], 'how_many_times':[]}

	while page < max_pages:
		url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do'
		source_code = requests.post(url, {'curPage' : page})
		# print(source_code.text)
		encoding = source_code.encoding if 'charset' in source_code.headers.get('content-type', '').lower() else None
		soup = BeautifulSoup(source_code.content, "lxml", from_encoding=encoding)
		# soup = BeautifulSoup(source_code.text, "html.parser")
		# print(soup.prettify())
		data = []
		movie_table = soup.find('table', attrs={'class':'boardList03'})
		table_body = movie_table.find('tbody')
		rows = table_body.findAll('tr')
		for row in rows:
			cols = row.findAll('td')
			### should get movie id and send another request 
			movie_id = cols[0].find('a')['onclick'].split('\'')[3]
			movie_url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do'
			print(movie_id)	#id_movie
			movie_source = requests.post(movie_url, {'code' : 19950366})	#movie information
			# print("%s" % str(movie_source.text))
			movie_soup = BeautifulSoup(movie_source.content, "lxml", from_encoding=encoding)
			movie_dd = movie_soup.findAll('dd')
			# print(movie_dd[1].text.strip())	#A.K.A
			
			# genre_all, repGenere, nation_all
			movie_dd_sp = movie_dd[2].text.strip().split('\r\n')
			movie_detail = []
			for ele in movie_dd_sp:
				if ele.strip():
					movie_detail.append(ele)

			# if a moive have multiple genres
			genreRep = movie_detail[2].split(',')[0].strip()
			numGenre = len(movie_detail[2].split(','))
			index = 2
			maxIndex = 2 + numGenre
			if(numGenre > 1):
				all_genre = ''
				for i in range(index, maxIndex):
					all_genre = all_genre + movie_detail[i].strip()
			else:
				all_genre = genreRep

			print(movie_detail[2])
			numNation = len(movie_detail[index].split(','))
			maxIndex = index + numNation
			if(numNation > 1):
				all_nation = ''
				for i in range(index, maxIndex):
					all_nation = all_nation + movie_detail[i].strip()
			else:
				all_nation = movie_detail[index].strip()

			print(all_genre)	#genre_all
			print(genreRep)	#repGenre
			print(all_nation)	#nation_all
			
			# openDT, productYear, prdstate
			# print(movie_dd[3].text.strip().split('\r\n'))
			movie_dd_sp2 = movie_dd[3].text.strip().split('\r\n')
			print(movie_dd_sp2)
			movie_detail2 = []
			for ele in movie_dd_sp2:
				if ele.strip():
					movie_detail2.append(ele)

			print(len(movie_dd))

			
			break	#debug
			cols = [ele.text.strip() for ele in cols]
			data.append([ele for ele in cols]) #Get rid of empty values

		# since the item is list object, it shows as raw-unicode
		# after making this as string object, it has to be seen as a normal string
		### in the data: kor_movieNM, en_movieNM, productYear, prdstate, repGenere, 
		### directors, companyNM. 
		filename = "output" + str(page) + ".txt"
		text_file = open(filename, "w")
		for item in data:
			item_str = ','.join(item)
			print("%s\n" % item_str)
			text_file.write("%s\n" % item_str)
		# text_file.write(data)
		text_file.close()
		page += 1

		### id_movie, openDT, nation_all, genre_all, id_director, company_all, id_company,
		### actors_name, id_actors_name, how_many_times?


		### data sequence
		### id_movie // kor_movieNM // en_movieNM // productYear // openDT // prdstate //
		### nation_all // genre_all // repGenre // id_director // directors // company_all //
		### id_company // companyNM // actors_name // id_actors_name // how many times?

#spider(2)
# loading(2)
loading2(12)