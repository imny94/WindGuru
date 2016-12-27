from bs4 import BeautifulSoup
import re
import requests
import requests
import csv
from datetime import datetime

class WindGuru:

	def __init__(self,URL):
		self.URL = URL
		self.r = requests.get(self.URL)
		self.soup = BeautifulSoup(self.r.text, 'html.parser')

# mainBody = soup.body
# tablesInBody = mainBody.table.next_sibling
# print tablesInBody

#mainContainer > table.content > tbody > tr > td > table > tbody > tr > td > table.glamor_table > tbody > tr:nth-child(5) > td.glamor_datatemp > span
# print soup.mainContainer.table.content.tbody.tr.td.table.tbody.tr.td.table.glamor_table.tbody.tr:nth-child(5).td.glamor_datatemp.span

# for sibling in soup.table.next_siblings:#.tbody.tr.td.table.tbody.tr.td.table[1].tbody.tr[5].td[2]
# 	print sibling

	def addSeconds(self,withoutSeconds):
		currentSecond = datetime.now().strftime(':%S')#'%Y-%m-%d %H:%M:%S')
		return withoutSeconds+currentSecond

	def getWindData(self):
		narrowedDownSearchForTime = self.soup.find_all('td',attrs={'class':'glamor_timestamp'})
		webTime = self.searchForTime(narrowedDownSearchForTime)
		# webTimeToSeconds = self.addSeconds(webTime)

		narrowedDownSearchForWind = self.soup.find_all('td',attrs={'class':'glamor_datatemp'})
		windIsAt = self.searchForWind(narrowedDownSearchForWind)
		windString = windIsAt.get_text("",strip=True).encode('utf-8')

		windSpeedPattern = re.compile("(\d+)")
		windSpeedList = windSpeedPattern.findall(windString)
		windSpeed = windSpeedList[0]

		directionPattern = re.compile("(N*S*E*W*)")
		directionList = directionPattern.findall(windString)
		direction = directionList[0]

		# print windString
		# print "Wind Speed is : " + windSpeed + " KTs from direction : " + direction + "\n"
		toReturn = {"WindSpeed" : windSpeed , "Direction" : direction , "StationTime" : webTime }
		return toReturn

	def searchForWind(self,searchArea):
		toFindWind=re.compile("[NSEW]")
		for row in searchArea:
			content = row.get_text("",strip=True)
			content = content.encode('utf-8')
			# print type(content)
			# print content
			matchResult = toFindWind.match(content)
			# print matchResult
			if matchResult:
				return row

	def searchForTime(self,searchArea):
		content = searchArea[0].get_text().encode('utf-8').strip()
		toFindTime = re.compile("\d\d:\d\d")
		toFindMonth = re.compile("January|February|March|April|May|June|July|August|September|October|November|December")
		toFindDayAndYear = re.compile("(\d\d), (\d\d\d\d)")
		time = toFindTime.findall(content)[0]
		month = self.convertAlphaMonthToNumer(toFindMonth.findall(content)[0])
		dayYear = toFindDayAndYear.findall(content)[0]
		day = dayYear[0]
		year = dayYear[1]
		# print content
		# print time
		# print month
		# print day
		# print year
		return "%s-%s-%s %s"%(year,month,day,time)

	def convertAlphaMonthToNumer(self,alphaDate):
		# print "for " + alphaDate + " converstion is : "
		if alphaDate == "January":
			return "01"
		elif alphaDate == "February":
			return "02"
		elif alphaDate == "March":
			return "03"
		elif alphaDate == "April":
			return "04"
		elif alphaDate == "May":
			return "05"
		elif alphaDate == "June":
			return "06"
		elif alphaDate == "July":
			return "07"
		elif alphaDate == "August":
			return "08"
		elif alphaDate == "September":
			return "09"
		elif alphaDate == "October":
			return "10"
		elif alphaDate == "November":
			return "11"
		elif alphaDate == "December":
			return "12"
		else:
			return "ERROR"
# print "\n\n\n"
# print soup.find_all('table')