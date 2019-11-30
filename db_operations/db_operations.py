"""Module: Creates a DBOperations class with functions."""
import sqlite3
import urllib.request
import datetime
from scrape_weather import WeatherScraper


class DBOperations():
    """This class contains working with db functions."""

    def create_db(self):
        """Create the table in db."""
        try:
            connection = sqlite3.connect("weather.sqlite")
            cur = connection.cursor()
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
            print("create_db - Table created successfully.")
        except Exception as e:
            print("Error creating table:", e)
        try:
            cur.execute("""create unique index idx_positions_sample_date \
                        ON samples (sample_date);""")
            connection.commit()
            print("create_db - Index created successfully.")
        except Exception as e:
            print("Index already exists:", e)

        connection.close()

    def process(self, my_Dictionary):
        """Populate the table with dictionary received."""
        self.create_db()
        myLocation = "Winnipeg"
        for d in my_Dictionary.keys():
            try:
                sample_date = d
            except Exception as e:
                print("Error mean:", e)
            for v in my_Dictionary.values():
                # values = v.values()
                # values = list(v.values())
                try:
                    if my_Dictionary[sample_date]["max"] != 'M' and \
                       my_Dictionary[sample_date]["max"] != 'E':
                        max_temp = float(my_Dictionary[sample_date]["max"])
                except Exception as e:
                    print("Error max:", e)
                try:
                    if my_Dictionary[sample_date]["min"] != 'M' and \
                       my_Dictionary[sample_date]["min"] != 'E':
                        min_temp = float(my_Dictionary[sample_date]["min"])
                except Exception as e:
                    print("Error min:", e)
                try:
                    if my_Dictionary[sample_date]["mean"] != 'M' and \
                       my_Dictionary[sample_date]["mean"] != 'E':
                        avg_temp = float(my_Dictionary[sample_date]["mean"])
                except Exception as e:
                    print("Error mean:", e)
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
            values (?,?,?,?,?)""", (sample_date, location, min_temp, max_temp,
                                    avg_temp))

                connection.commit()
                connection.close()
            # print("process - added sample successfully.")
            except Exception as e:
                print("Error:", e)
        self.print_infos()

    def print_infos(self):
        """Print the information for checking purpose."""
        connection = sqlite3.connect("weather.sqlite")
        cur = connection.cursor()
        connection.commit()
        connection.close()

    def query_infos(self, fromYear, toYear):
        """Query db according to user input."""
        connection = sqlite3.connect("weather.sqlite")
        cur = connection.cursor()
        toYear = int(toYear) + 1
        dictOuter = {}
        for row in cur.execute("select * from samples where \
                                sample_date between ? and ?",
                               (str(fromYear)+'%', str(toYear)+'%')):
            print(f"row {row}")
            myMonth = datetime.datetime.strptime(row[1], '%Y/%m/%d').month
            dictOuter.setdefault(myMonth, []).append(row[5])
        print(dictOuter)
        return dictOuter
        connection.commit()
        connection.close()
