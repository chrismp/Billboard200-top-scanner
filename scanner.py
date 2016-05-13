from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date

def getSoup(url):
	html=	urlopen(url).read()
	soup=	BeautifulSoup(html,"lxml")
	return soup


BASE_URL=	"https://en.wikipedia.org"

year=	1945
while year <= date.today().year:
	yearURL=	BASE_URL+"/wiki/List_of_Billboard_200_number-one_albums_of_"+str(year)
	yearPage=	getSoup(yearURL)

	wikitable=			yearPage.find("table",{"class": "wikitable"})
	wikitableChildren=	wikitable.findChildren("tr")
	for tr in wikitableChildren:
		print tr,"\n==="

	year += 1
	break