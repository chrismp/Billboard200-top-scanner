from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date, datetime

def getSoup(url):
	print "Opening "+url
	html=	urlopen(url).read()
	soup=	BeautifulSoup(html,"lxml")
	return soup

def tagToText(tag):
	txt=	tag.find(text=True)
	return None if txt==None else txt.encode("utf-8").strip()

def getHref(tag):
	return None if tag.find('a')==None else tag.find('a').get("href")

def getDate(tag):
	return tag.find(text=True).strip() + ' ' + str(year)


BASE_URL=	"https://en.wikipedia.org"
year=		1945
while year <= date.today().year:
	year=	1964 if year==1960 else year
	yearURL=	BASE_URL+"/wiki/List_of_Billboard_200_number-one_albums_of_"+str(year)
	yearPage=	getSoup(yearURL)

	wikitables=	yearPage.findAll("table",{"class": "wikitable"})
	for wikitable in wikitables:
		wikitableChildren=	wikitable.findChildren("tr")

		if len(wikitableChildren) <= 1:
			continue

		album=	None
		artist=	None
		label=	None
		for tr in wikitableChildren:
			tdList=			tr.findChildren("td")	# `td` elements containing info on dates, album titles, artists and labels
			tdListLength=	len(tdList)
			if tdListLength > 0:	# If there are `td` elements, we can be sure we are reading data about the Billboard 200 
				if tagToText(tdList[0]) == "Issue Date":
					continue

				chartDate=	getDate(tr.findChildren("th")[0]) if len(tr.findChildren("th"))==1 else getDate(tdList[0])	# This ternary statement is necessary because startng with 2014, date is stored in `th`
				chartDatePython=datetime.strptime(chartDate,"%B %d %Y").date()
				tdHasAlbumInfo=	tdListLength > 1	# `tdListLength` is `1` when only the date is available
				if tdHasAlbumInfo:					
					if tdListLength > 2:
						albumTag=	tdList[1] if year < 2014 else tdList[0]
						album=		tagToText(albumTag)
						albumHref=	getHref(albumTag)
						artistTag=	tdList[2] if year < 2014 else tdList[1]
						artist=		tagToText(artistTag)
						artistHref=	getHref(artistTag)
				print chartDatePython, album, albumHref, artist, artistHref
				# print "=="

	print "==="
	year += 1