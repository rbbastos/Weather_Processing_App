"""Module: Creates a WeatherScraper class to scrape data from website."""
import urllib.request
import datetime
from html.parser import HTMLParser
from html.entities import name2codepoint


class WeatherScraper(HTMLParser):
    """This class contains HTMLParser functions."""

    def __init__(self):
        """Create an instance of WeatherScraper."""
        HTMLParser.__init__(self)
        self.inTr = self.inTh = self.inAabr = self.inA = self.inTd = self.isDate = False
        self.inMean = self.inMin = self.inMax = self.inAvg = self.inMyDate = False
        self.i = self.j = 0
        self.keys = ["max", "min", "mean"]
        self.dictInner = {}
        self.dictOuter = {}
        self.myDate = ''

    def handle_starttag(self, tag, attrs):
        """Handle the starttag in a website."""

        if tag == 'tr':
            """Only data in table - total of 33 (depending of number of days in month, it will vary)"""
            try:
                self.inTr = True
            except Exception as e:
                print("Error:", e)

        if tag == 'td':
            """First td is first temp in the table, under column MAX and DAY 1"""
            try:
                """i = 1 -> column MAX TEMP; i = 2 -> column MIN TEMP; i = 3 -> column MEAN TEMP"""
                self.i += 1
                self.inTd = True
            except Exception as e:
                print("Error:", e)

        if tag == 'th':
            """First th = DAY(0,0) in table. Date is inside a td>th>abbr(attr[1]). Total: 43 """
            try:
                self.inTh = True
            except Exception as e:
                print("Error:", e)

        if tag == 'abbr':
            """Date is located in here, attr[1]. Total: 62"""
            try:
                self.inAabr = True
            except Exception as e:
                print("Error:", e)

        for attr in attrs:
            """attrs are inside a tag. E.g id='test'."""
            self.inMean = True
            if self.inTh and self.inAabr and attr[0] == 'title':
                if attr[1] == 'kilometres per hour':
                    self.inMyDate = True
                # print("     attrrrrr:", attr[1])
                try:
                    if self.inMyDate:
                        self.myDate = (datetime.datetime.strptime(attr[1], '%B %d, %Y')
                                                    .date()).strftime('%Y/%m/%d')
                        self.isDate = True
                except Exception as e:
                    print("Error:", e)

    def handle_endtag(self, tag):
        """Handle the endtag in a website."""
        if tag == 'tr':
            try:
                self.i = 0
                self.inTr = False
            except Exception as e:
                print("Error:", e)

        if tag == 'td':
            try:
                self.inTd = False
            except Exception as e:
                print("Error:", e)

        if tag == 'th':
            try:
                self.inTh = False
            except Exception as e:
                print("Error:", e)

        if tag == 'abbr':
            try:
                self.inMean = False
                self.inAabr = False
            except Exception as e:
                print("Error:", e)


    def handle_data(self, data):
        """Handle the data inside a tag in a website and return dictionary."""
        if data == 'Sum':
            self.inMyDate = False
        if self.inMyDate and self.inTd and self.i == 1:
            try:
                floatedMaxData = data
                # print("Max  Inner:", floatedMaxData)
                self.dictInner[self.keys[0]] = floatedMaxData
            except Exception as e:
                self.dictInner[self.keys[0]] = 0
                print("Error:", e)

        if self.inMyDate and self.inTd and self.i == 2:
            try:
                floatedMinData = data
                # print("Min  Inner:", floatedMinData)
                self.dictInner[self.keys[1]] = floatedMinData
            except Exception as e:
                self.dictInner[self.keys[1]] = 0
                print("Error:", e)

        if self.inMyDate and self.inTd and self.i == 3:
            try:
                floatedMeanData = data
                # print("Mean  Inner:", floatedMeanData)
                self.dictInner[self.keys[2]] = data
            except Exception as e:
                self.dictInner[self.keys[2]] = 0
                print("Error:", e)
        if self.inMyDate:
            self.dictOuter[self.myDate] = dict(self.dictInner)


myparser = WeatherScraper()
now = datetime.datetime.now()
#
#
# climateWeather_year = 2019
# climateWeather_month = 5
# #
# # # climateWeather_url = 'https://climate.weather.gc.ca/'
# # # cimateWeather_data = 'climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&'
# # # with urllib.request.urlopen(climateWeather_url+cimateWeather_data+climateWeather_year+climateWeather_month) as response:
# with urllib.request.urlopen(f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={climateWeather_year}&Month={climateWeather_month}#") as response:
#
# # with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year=2018&Month=5#') as response:
#     html = str(response.read())
#
# myparser.feed(html)

for i in range(now.year, 2017, -1):
    climateWeather_year = i
    for j in range(12, 0, -1):
        climateWeather_month = j
        # climateWeather_url = 'https://climate.weather.gc.ca/'
        # cimateWeather_data = 'climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&'
        # with urllib.request.urlopen(climateWeather_url+cimateWeather_data+climateWeather_year+climateWeather_month) as response:
        with urllib.request.urlopen(f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={climateWeather_year}&Month={climateWeather_month}#") as response:
        # with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year=2018&Month=5#') as response:
            html = str(response.read())

        myparser.feed(html)
print(f"inner{myparser.dictInner}")
print(f"outer{myparser.dictOuter}")
