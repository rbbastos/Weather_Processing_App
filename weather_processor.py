"""Module: Creates a WeatherProcessor class to prompt user interaction."""
import urllib.request
import datetime
from time import strptime
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor():
    """This class is for user interaction."""

    def main(self):
        """Create the function for user interaction."""
        print("1. UPDATE the db up to today's date\n2. DOWNLOAD a full set of weather data\n3. RANGE of your interest")
        mySelection = '0'
        while mySelection == '0':
            mySelection = input("Select an option: ")
            # myUpdate = input("Do you want to UPDATE the db up to today's date? (yes or no):")
            # print(myUpdate)
            # if myUpdate == 'yes':
            print(mySelection == '1')
            if mySelection == '1':
                myparser = WeatherScraper()
                now = datetime.datetime.now()
                x_loop_must_break = False
                for i in range(now.year, now.year - 1, -1):
                    myparser.url_year = i
                    if x_loop_must_break:
                        break
                    # climateWeather_year = i
                    for j in range(now.month - 2, now.month + 1):
                        myparser.url_month = j
                        # climateWeather_month = j
                        passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={myparser.url_year}&Month={myparser.url_month}#"
                        # passedUrl = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year=2018&Month=5#'
                        with urllib.request.urlopen(passedUrl) as response:
                            html = str(response.read())

                        myparser.feed(html)
                        # print(f"after feed {myparser.EqualData}")
                        if myparser.EqualData is False:
                            x_loop_must_break = True
                            break
                print(f"inner{myparser.dictInner}")
                print(f"outer{myparser.dictOuter}")
                myOperations = DBOperations()
                myOperations.process(myparser.dictOuter)
            # myDownload = input("Do you want to DOWNLOAD a full set of weather data? (yes or no): ")
            # print(myDownload)
            # if myDownload == 'yes':
            elif mySelection == '2':
                myparser = WeatherScraper()
                now = datetime.datetime.now()
                x_loop_must_break = False
                for i in reversed(range(now.year)):
                    myparser.url_year = i
                    if x_loop_must_break:
                        break
                    # climateWeather_year = i
                    for j in range(0, 13):
                        myparser.url_month = j
                        # climateWeather_month = j
                        passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={myparser.url_year}&Month={myparser.url_month}#"
                        # passedUrl = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year=2018&Month=5#'
                        with urllib.request.urlopen(passedUrl) as response:
                            html = str(response.read())

                        myparser.feed(html)
                        # print(f"after feed {myparser.EqualData}")
                        if myparser.EqualData is False:
                            x_loop_must_break = True
                            break
                print(f"inner{myparser.dictInner}")
                print(f"outer{myparser.dictOuter}")
                myOperations = DBOperations()
                myOperations.process(myparser.dictOuter)
            elif mySelection == '3':
                myRange = input("Please select a RANGE of your interest? (e.g 2017 2019): ")
                myRange = myRange.split()
                print(myRange[0])
                myInstance = DBOperations()
                myDict = myInstance.query_infos(myRange[0], myRange[1])
                myPlot = PlotOperations()
                myPlot.diplay_box_plot(myDict)
            else:
                print("Invalid choice")


myProcessor = WeatherProcessor()
myProcessor.main()
