#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import traceback
import random

global conn
global cursor

def download_url_urllib2(url):
    print "Downloading: ", url
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"}
    request = urllib2.Request(url, headers=headers)
    try:
		html = urllib2.urlopen(request).read()
		html = html.decode('gb2312','ignore').encode('utf-8','ignore')
    except urllib2.URLError as e:
        print "Download error: ", e.reason
        html = None
    return html

def download_url_requests(url):
    print "Downloading: ", url
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"}
    request = requests.get(url, headers=headers)
    request.encoding="gb18030"
    html = request.text
    return html

def parse_movie_page(url):
	html = download_url_urllib2(url)
	#print(len(html))
	soup = BeautifulSoup(html, "html.parser")
	#print(html)
	#soup.pretify()
	#print(soup.original_encoding)
	movie_urls = soup.find_all(attrs={"class":"ulink"})
	print "Movie amount: ", len(movie_urls)
	amount = 0
	for item in movie_urls:
		movie_name = item.get_text();
		movie_url = "http://www.dytt8.net"+item.get("href")
		print amount+1, movie_name.encode("gb2312")
		
		sql_query = "select count(*) from movie_list where movie_name = \"%s\""%(movie_name)
		#print sql_query
		cursor.execute(sql_query)
		value = cursor.fetchone()
		if(value[0] == 0 ):
			print "This is new"
			sql_insert = "insert into movie_list(movie_name, movie_url)values(\"%s\",\"%s\")"%(movie_name,movie_url)
			#print sql_insert
			cursor.execute(sql_insert)
		else:
			print "Already record"
		
		cursor.fetchall()
		conn.commit()
		
		amount += 1
		print
try:
	print "Open database dytt.db"
	conn = sqlite3.connect("dytt.db")
	cursor = conn.cursor()

	print "Vist index page"
	url_index = "http://www.dytt8.net/html/gndy/dyzz/index.html"
	html_index = download_url_urllib2(url_index)
	soup_index = BeautifulSoup(html_index, "html.parser")

	page_urls = soup_index.find(attrs={"name":"sldd"}).find_all(["option"])
	print "Page amount: ", len(page_urls)
	page_index = 0
	for item in page_urls:
		page_url = "http://www.dytt8.net/html/gndy/dyzz/"+item.get("value")
		print "Visit page: ", page_index+1
		parse_movie_page(page_url)

		
		page_index += 1
		sleep_second = random.randint(2,8)
		print "Sleep: ", sleep_second
		time.sleep(sleep_second)
	
	cursor.close()
	conn.commit()
	conn.close()
except Exception as e:
	f_err = open("Errors.txt", "a+")
	f_err.write(traceback.format_exc())
	f_err.write("\n")
	f_err.write("\n")
	f_err.close()
	
	cursor.close()
	conn.commit()
	conn.close()
	raise

#soup = BeautifulSoup(movie_html, "html.parser")




        