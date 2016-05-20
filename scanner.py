from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date, datetime
import csv

def getSoup(url):
	print "Opening "+url
	html=	urlopen(url).read()
	soup=	BeautifulSoup(html,"lxml")
	return soup

def tagToText(tag):
	print tag
	txt=	tag.find(text=True)
	return None if txt==None else txt.encode("utf-8").strip()

def getHref(tag):
	return None if tag.find('a')==None else tag.find('a').get("href")

def getDate(tag):
	return tag.find(text=True).strip() + ' ' + str(year)


outputFile=	"Billboard200Data.csv"
with open(outputFile, "wb") as csvFile:
	headers=	[
				"Date",
				"Album",
				"AlbumURL",
				"AlbumImageURL",
				"Artist",
				"ArtistURL"
			]
	writer=		csv.DictWriter(csvFile, fieldnames=headers, quotechar='"')
	writer.writeheader()


BASE_URL=	"https://en.wikipedia.org"
year=		1945
while year <= date.today().year:
	year=	1964 if year==1960 else year	# 1960-63 charts are split between mono and stereo sound. I have not yet figured out how to make my script scrape ONLY data from the mono charts.
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

				if albumHref != None:
					albumPage=	getSoup(BASE_URL + albumHref)
					albumFileHref=	albumPage.find("div",{"id":"mw-content-text"}).find("img").parent.get("href")

					if albumFileHref == None:
						albumImageURL=	None
					else:
						albumFilePage=	getSoup(BASE_URL + albumFileHref)
						albumImageURL=	 albumFilePage.find("div",{"id":"file"}).find('a').get("href")
						albumImageURL=	"http:"+albumImageURL

				with open(outputFile) as csvFile:
					reader=	csv.DictReader(csvFile)
					for row in reader:
						if album == row["Album"] and artist == row["Artist"]:
							print [album, row["Album"], artist, row["Artist"]]
							albumHref=		row["AlbumURL"]
							artistHref=		row["ArtistURL"]
							albumImageURL=	row["AlbumImageURL"]
							break

				with open(outputFile,"ab") as csvFile:
					writer=		csv.writer(csvFile, quotechar='"')
					listData=	[chartDatePython, album, albumHref, albumImageURL, artist, artistHref]
					writer.writerow(listData)
					print listData
					print "========="
	year += 1
