from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date, datetime

def getSoup(url):
	print "Opening "+url
	html=	urlopen(url).read()
	soup=	BeautifulSoup(html,"lxml")
	return soup

def tagToText(tag):
	return tag.find(text=True).strip()

BASE_URL=	"https://en.wikipedia.org"

year=	1945
while year <= date.today().year:
	yearURL=	BASE_URL+"/wiki/List_of_Billboard_200_number-one_albums_of_"+str(year)
	yearPage=	getSoup(yearURL)

	wikitable=			yearPage.find("table",{"class": "wikitable"})
	wikitableChildren=	wikitable.findChildren("tr")
	album=	None
	artist=	None
	label=	None	
	for tr in wikitableChildren:
		tdList=			tr.findChildren("td")	# `td` elements containing info on dates, album titles, artists and labels
		tdListLength=	len(tdList)
		
		if tdListLength > 0:	# If there are `td` elements, we can be sure we are reading data about the Billboard 200 
			chartDate=		tdList[0].find(text=True).strip() + ' ' + str(year)
			chartDatePython=datetime.strptime(chartDate,"%B %d %Y").date()

			tdHasAlbumInfo=	tdListLength == 4
			if tdHasAlbumInfo:
				album=	tagToText(tdList[1])
				artist=	tagToText(tdList[2])
				label=	tagToText(tdList[3])
				
			print chartDatePython, album, artist, label

	year += 1
	break