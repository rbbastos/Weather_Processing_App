"""Module: Creates a DBOperations class with functions."""
import sqlite3
import urllib.request
import datetime
from scrape_weather import WeatherScraper


class DBOperations():
    """This class contains working with db functions."""
    def create_db(self):
        """Creates the table in db."""
        try:
            connection = sqlite3.connect("weather.sqlite")
            cur = connection.cursor()
            dropTableStatement = "DROP TABLE samples"
            cur.execute(dropTableStatement)
            print("create_db - Opened the db successfully.")
        except Exception as e:
            print("Error opening DB:", e)

        try:
            cur = connection.cursor()
            # dropTableStatement = "DROP TABLE samples"
            # cur.execute(dropTableStatement)
            cur.execute("""create table if not exists samples
                (id integer primary key autoincrement not null,
                sample_date text not null,
                location text not null,
                min_temp real not null,
                max_temp real not null,
                avg_temp real not null);""")
                # unique on conflict fail
            cur.execute("""create unique index idx_positions_sample_date ON samples (sample_date);""")
            connection.commit()
            print("create_db - Table created successfully.")

        except Exception as e:
            print("Error creating table:", e)

        connection.close()

    def process(self, my_Dictionary):
        """Populate the table with dictionary received."""
        self.create_db()
        myLocation = "Winnipeg"
        for d in my_Dictionary.keys():
            sample_date = d

            for v in my_Dictionary.values():
                # values = v.values()
                # values = list(v.values())
                try:
                    max_temp = float(my_Dictionary[sample_date]["max"])
                except Exception as e:
                    print("Error:", e)
                try:
                    min_temp = float(my_Dictionary[sample_date]["min"])
                except Exception as e:
                    print("Error:", e)
                try:
                    avg_temp = float(my_Dictionary[sample_date]["mean"])
                except Exception as e:
                    print("Error:", e)
                try:
                    location = myLocation
                except Exception as e:
                    print("Error:", e)

            connection = sqlite3.connect("weather.sqlite")
            # print("process - Opened the db successfully.")
            cur = connection.cursor()
            try:
                cur.execute("""replace into samples
            (sample_date, location, min_temp, max_temp, avg_temp)
            values (?,?,?,?,?)""", (sample_date, location, min_temp, max_temp, avg_temp))

                connection.commit()
                connection.close()
            # print("process - added sample successfully.")
            except Exception as e:
                print("Error:", e)
        self.print_infos()
        self.query_infos()

    def print_infos(self):
        """Print the information for checking purpose."""
        connection = sqlite3.connect("weather.sqlite")
        cur = connection.cursor()
        # for row in cur.execute("select * from samples"):
        #     print(row)
        connection.commit()
        connection.close()

    def query_infos(self):
        """Query db according to user input."""
        connection = sqlite3.connect("weather.sqlite")
        cur = connection.cursor()
        fromYear = '2018'
        # toYear = '2019'
        # t = "samples"
        # for row in cur.execute("select * from samples where sample_date like ?", ('%'+fromYear+'%',)):
        #     print(f"row {row}")
        dictOuter = {}
        myMean = []
        #for row in cur.execute("select * from samples where sample_date between '2019/02/%' and '2019/04/%'"):
        # for row in cur.execute("select * from samples where sample_date like ?", ('%'+fromYear+'%',)):
        for row in cur.execute("select * from samples where sample_date like '%2018%'"):
            print(f"row {row}")
            myMonth = datetime.datetime.strptime(row[1], '%Y/%m/%d').month
            # https://stackoverflow.com/questions/12905999/python-dict-how-to-create-key-or-append-an-element-to-key
            dictOuter.setdefault(myMonth, []).append(row[5])
            # myMean.append(row[5])
            # dictOuter[myMonth] = myMean
            # myMean = []
            # print(f"row {row}")
            # print(f"date in row: {row[1]}")
        print(dictOuter)
        return dictOuter
        connection.commit()
        connection.close()


# myparser = WeatherScraper()
# now = datetime.datetime.now()
# for i in range(now.year, 2015, -1):
#     climateWeather_year = i
#     for j in range(12, 0, -1):
#         climateWeather_month = j
#         with urllib.request.urlopen(f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={climateWeather_year}&Month={climateWeather_month}#") as response:
#             html = str(response.read())
#
#         myparser.feed(html)

myInstance = DBOperations()
# myInstance.process(myparser.dictOuter)
# print(myparser.dictOuter)
# myInstance.read_from_db()
# myInstance.print_infos()
# myInstance.create_db()
myInstance.query_infos()
