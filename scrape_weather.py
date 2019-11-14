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
        self.inTr = self.inTh = self.inAabr = self.inA = self.inTd = self.tbody = self.isDate = False
        self.inMean = self.inMin = self.inMax = self.inAvg = False
        self.i = 0
        self.keys = ["max", "min", "mean"]
        self.dictInner = {}
        self.dictOuter = {}
        self.myDate = ''

    def handle_starttag(self, tag, attrs):
        """Handle the starttag in a website."""
        # print("Start tag:", tag)
        # for attr in attrs:
        #     print("     attr:", attr)
        if tag == 'tr':
            try:
                self.inTr = True
            except Exception as e:
                print("Error:", e)
        if tag == 'td':
            try:
                # print("Start tag:", tag)
                self.i += 1
                self.inTd = True
            except Exception as e:
                print("Error:", e)
        if tag == 'th':
            try:
                self.inTh = True
            except Exception as e:
                print("Error:", e)
        if tag == 'abbr':
            try:
                self.inAabr = True
            except Exception as e:
                print("Error:", e)
            for attr in attrs:
                self.inMean = True
                if self.inTh and not self.inTd:
                    print("     attrrrrr:", attr[1])
                    try:
                        # https://stackoverflow.com/questions/42980662/convert-string-with-month-name-to-datetime
                        # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
                        #print(datetime.datetime.strptime(attr[1], '%B %d, %Y').date())
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
        if data == 'Mean Temp':
            try:
                self.inAvg = True
            except Exception as e:
                print("Error:", e)
        if data == 'Min Temp':
            try:
                self.inMin = True
            except Exception as e:
                print("Error:", e)
        if data == 'Max Temp':
            try:
                self.inMax = True
            except Exception as e:
                print("Error:", e)
        if self.inTd and self.i == 3 and self.inAvg:
            try:
                floatedMeanData = data
                print("Mean  Inner:", floatedMeanData)
                self.dictInner[self.keys[2]] = floatedMeanData
            except Exception as e:
                self.dictInner[self.keys[2]] = 0
                print("Error:", e)
        if self.inTd and self.i == 2 and self.inMin:
            try:
                floatedMinData = data
                print("Min  Inner:", floatedMinData)
                self.dictInner[self.keys[1]] = floatedMinData
            except Exception as e:
                self.dictInner[self.keys[1]] = 0
                print("Error:", e)
        if self.inTd and self.i == 1 and self.inMax:
            try:
                floatedMaxData = data
                print("Max  Inner:", floatedMaxData)
                self.dictInner[self.keys[0]] = floatedMaxData
            except Exception as e:
                self.dictInner[self.keys[0]] = 0
                print("Error:", e)

        # this if statement will print only Avg value
        # if self.inTd and self.i == 3 and self.inAvg:
        #     try:
        #         print("Avg  :", float(data))
        #     except Exception as e:
        #         print("Error:", e)
        if self.isDate:
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

for i in range(now.year, 2018, -1):
    climateWeather_year = i
    for j in range(12, 1, -1):
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
