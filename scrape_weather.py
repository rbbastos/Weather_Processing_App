"""Module: Creates a WeatherScraper class to scrape data from website."""
import urllib.request
import datetime
import time
from time import strptime
from html.parser import HTMLParser
from html.entities import name2codepoint


class WeatherScraper(HTMLParser):
    """This class contains HTMLParser functions."""

    def __init__(self):
        """Create an instance of WeatherScraper."""
        HTMLParser.__init__(self)
        self.inTr = self.inTh = self.inAabr = self.inA = self.inTd = self.isDate = self.inCaption = self.inTbody = False
        self.inMean = self.inMin = self.inMax = self.inAvg = self.inMyDate = False
        self.EqualData = True
        self.i = self.j = 0
        self.keys = ["max", "min", "mean"]
        self.dictInner = {}
        self.dictOuter = {}
        self.myDate = ''
        self.myCaptionYear = ''
        self.myCaption = []
        self.url_year= self.url_month = None

    def handle_starttag(self, tag, attrs):
        """Handle the starttag in a website."""

        if tag == 'caption':
            """Only one caption in html"""
            try:
                self.inCaption = True
            except Exception as e:
                print("Error:", e)

        if tag == 'tbody':
            """Only one <tbody> in html"""
            try:
                self.inTbody = True
            except Exception as e:
                print("Error:", e)

        if tag == 'tr':
            """There are a total of 35 (depending of number of days in month, it will vary)"""
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

        if tag == 'a':
            """Set tag <a> to true"""
            try:
                self.inA = True
            except Exception as e:
                print("Error:", e)

        for attr in attrs:
            """attrs are inside a tag. E.g id='test'."""
            self.inMean = True
            # print(self.inTbody)
            if self.inTbody and self.inTr and self.inTh and self.inAabr and attr[0] == 'title' and not attr[0] == 'href' and not attr[1] == 'Average' and not attr[1] == 'Extreme':
                # print(attr)
                self.inMyDate = True
                try:
                    # print(f" attr[1] {attr[1]}")
                    self.myDate = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
                    print(f" self.myDate {self.myDate}")
                    self.isDate = True
                except Exception as e:
                    print(f"Error: {attr[1]}", e)
                # try:
                #     self.myDate = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
                # except Exception as e:
                #     print(f"Error: {attr[1]}", e)
            # if self.inTbody and self.inTr and self.inTh and self.inAabr:
            #     print(attr)
                # if attr[1] == 'kilometres per hour':
                #     self.inMyDate = True
                # # print("     attrrrrr:", attr[1])
                # # try:
                # if self.inMyDate:
                #     # print(f" attr[1] {attr[1]}")
                #     try:
                #         print(f" attr[1] {attr[1]}")
                #         self.myDate = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
                #         self.isDate = True
                #     except Exception as e:
                #         print(f"Error: {attr[1]}", e)
            # if self.inTh and self.inAabr and attr[0] == 'title':
            #
            #     if attr[1] == 'kilometres per hour':
            #         self.inMyDate = True
            #     # print("     attrrrrr:", attr[1])
            #     # try:
            #     if self.inMyDate:
            #         # print(f" attr[1] {attr[1]}")
            #         try:
            #             print(f" attr[1] {attr[1]}")
            #             self.myDate = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
            #             self.isDate = True
            #         except Exception as e:
            #             print(f"Error: {attr[1]}", e)

    def handle_endtag(self, tag):
        """Handle the endtag in a website."""
        if tag == 'caption':
            try:
                self.inCaption = False
            except Exception as e:
                print("Error:", e)

        if tag == 'tbody':
            """Only one <tbody> in html"""
            try:
                self.inTbody = False
            except Exception as e:
                print("Error:", e)

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

        if tag == 'a':
            """Set all tag <a>"""
            try:
                self.inA = False
            except Exception as e:
                print("Error:", e)

    def handle_data(self, data):
        """Handle the data inside a tag in a website and return dictionary."""
        if data == 'Sum':
            self.inMyDate = False
        if self.inMyDate and self.inTd and self.i == 1:
            try:
                # print("Max  Inner:", data)
                self.dictInner[self.keys[0]] = data
            except Exception as e:
                self.dictInner[self.keys[0]] = 0
                print("Error:", e)

        if self.inMyDate and self.inTd and self.i == 2:
            try:
                # print("Min  Inner:", data)
                self.dictInner[self.keys[1]] = data
            except Exception as e:
                self.dictInner[self.keys[1]] = 0
                print("Error:", e)

        if self.inMyDate and self.inTd and self.i == 3:
            try:
                # print("Mean  Inner:", data)
                self.dictInner[self.keys[2]] = data
            except Exception as e:
                self.dictInner[self.keys[2]] = 0
                print("Error:", e)
        if self.inMyDate:
            self.dictOuter[self.myDate] = dict(self.dictInner)

        if self.inCaption:
            self.myCaption = data.split()
            self.myCaptionYear = self.myCaption[5]
            # print(f"inCaption - YEAR {self.myCaptionYear}")
            self.myCaptionMonth = self.myCaption[4]
            # print(f"inCaption - MONTH {self.myCaptionMonth}")
            m = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
            s = self.myCaption[4].strip()[:3].lower()
            # print(datetime.datetime.strptime(self.myCaption[4], '%B')
            #                        .date().strftime('%m'))
            # self.url_month = str(datetime.datetime.strptime(self.myCaption[4], '%B').date().strftime('%m'))
            # print(strptime('Fev', '%B').tm_mon)
            # print(f"url_year {self.url_year}")
            # print(f"url_month {m[s]}")
            # print(f" self.url_year {type(str(self.url_year))}")
            # print(f" self.myCaptionYear {type(self.myCaptionYear)}")
            # print(f" self.url_month {self.url_month}")
            # print(f" self.url_month {m[s]}")
            # print(f" self.url_month {type(self.url_month)}")
            # print(f" self.myCaptionMonth {type(self.myCaptionMonth)}")
            # print(str(self.url_month) in m[s])
            # print(str(self.url_year) in self.myCaptionYear)
            if str(self.url_month).zfill(2) == m[s] and str(self.url_year) in self.myCaptionYear:
                # print("EQUALLLLLL")
                self.EqualData = True
            else:
                # print("NOT EQUAL")
                self.EqualData = False


# myparser = WeatherScraper()
# # myparser.url_year = 2100
# # in website, scrape for caption Month and Year to compare to myparser.url_year and myparser.url_month. Set boolean to true/false
# now = datetime.datetime.now()
# x_loop_must_break = False
# # for i in range(now.year, 2017, -1):
# for i in reversed(range(now.year)):
#     myparser.url_year = i
#     if x_loop_must_break:
#         break
#     # climateWeather_year = i
#     for j in range(12, 0, -1):
#         myparser.url_month = j
#         # climateWeather_month = j
#         passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={myparser.url_year}&Month={myparser.url_month}#"
#         # passedUrl = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year=2018&Month=5#'
#         with urllib.request.urlopen(passedUrl) as response:
#             html = str(response.read())
#
#         myparser.feed(html)
#         print(f"after feed {myparser.EqualData}")
#         if myparser.EqualData is False:
#             x_loop_must_break = True
#             break
#
#
#
# # y = myparser.myCaptionYear
# # print(f"Outside {y}")
# print(f"inner{myparser.dictInner}")
# print(f"outer{myparser.dictOuter}")
