"""Module: Creates a WeatherProcessor class to prompt user interaction."""
import urllib.request
import datetime
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor():
    """This class is for user interaction."""

    def main(self):
        """Create the function for user interaction."""
        mySelection = ''
        while mySelection != '4':
            try:
                print("1. UPDATE the db up to today's date\n2.DOWNLOAD a full set of weather data\n3. RANGE of your interest\n4. EXIT")
                mySelection = input("Select an option: ")
                if mySelection == '1':
                    try:
                        myparser = WeatherScraper()
                        now = datetime.datetime.now()
                        x_loop_must_break = False
                        for i in range(now.year, now.year - 1, -1):
                            myparser.url_year = i
                            if x_loop_must_break:
                                break
                            for j in range(now.month - 2, now.month + 1):
                                myparser.url_month = j
                                # climateWeather_month = j
                                passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={myparser.url_year}&Month={myparser.url_month}#"
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
                    except Exception as e:
                        print("Error:", e)
                elif mySelection == '2':
                    try:
                        myparser = WeatherScraper()
                        now = datetime.datetime.now()
                        x_loop_must_break = False
                        for i in reversed(range(now.year)):
                            myparser.url_year = i
                            if x_loop_must_break:
                                break
                            for j in range(0, 13):
                                myparser.url_month = j
                                passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={myparser.url_year}&Month={myparser.url_month}#"
                                with urllib.request.urlopen(passedUrl) as response:
                                    html = str(response.read())
                                myparser.feed(html)
                                if myparser.EqualData is False:
                                    x_loop_must_break = True
                                    break
                        print(f"inner{myparser.dictInner}")
                        print(f"outer{myparser.dictOuter}")
                        myOperations = DBOperations()
                        myOperations.process(myparser.dictOuter)
                    except Exception as e:
                        print("Error:", e)
                elif mySelection == '3':
                    try:
                        myRange = input("Please select a RANGE of your interest? (e.g 2017 2019): ")
                        myRange = myRange.split()
                        # print(myRange[0])
                        myInstance = DBOperations()
                        myDict = myInstance.query_infos(myRange[0], myRange[1])
                        myPlot = PlotOperations()
                        myPlot.diplay_box_plot(myDict)
                    except Exception as e:
                        print("Error:", e)
                elif mySelection == '4':
                    break
                else:
                    print("Invalid choice")
            except Exception as e:
                print("Error:", e)


def weather_app():
    """Create instance of WeatherProcessor."""
    myProcessor = WeatherProcessor()
    myProcessor.main()


if __name__ == '__main__':
    weather_app()
