"""Module: Creates a PlotOperations class to scrape data from website."""
import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations


class PlotOperations():
    """This class display a boxplot."""

    def diplay_box_plot(self, myList):
        myMean = []
        for key, values in myList.items():
            # print(f"values {values}")
            # print(f"type values{type(values)}")
            # print(f"key {key}")
            myMean.append(values)
            # print(f"myMean {myMean}")
            plt.boxplot(myMean)
        plt.show()


# myInstance = DBOperations()
# myDict = myInstance.query_infos()
# print(f" MYDICT {myDict}")
#
# myPlot = PlotOperations()
# myPlot.diplay_box_plot(myDict)
