import urllib2
import requests
from bs4 import BeautifulSoup

def download_url_urllib2(url):
    print "Downloading: ", url
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
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

url = "http://www.dytt8.net/html/gndy/dyzz/list_23_1.html"

html = download_url_urllib2(url)
print(len(html))
#print(html)
soup = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
print(soup.original_encoding)
movie_urls = soup.find_all(attrs={"class":"ulink"})
print "Total amount: ", len(movie_urls)
amount = 1
for item in movie_urls:
    print amount, item.encode("gb18030")
    #print(item.get_text().encode(soup.original_encoding))
    #print(item.get("href"))
    #amount = amount + 1

#soup = BeautifulSoup(movie_html, "html.parser")




        