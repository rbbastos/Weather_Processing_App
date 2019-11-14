"""Module: Creates a PlotOperations class to scrape data from website."""
import matplotlib.pyplot as plt
import numpy as np


class PlotOperations():
    """This class display a boxplot."""

    def diplay_box_plot(self, myList):
        myMean = []
        for key, values in myList.items():
            print(f"values {values}")
            print(f"type values{type(values)}")
            print(f"key {key}")
            myMean.append(values)
            print(f"myMean {myMean}")
            plt.boxplot(myMean)
        plt.show()


# weather_data_test = [[1.1, 5.5, 6.2, 7.1, 8.0, 8.3, 7.8, 6.9, 6.0, 6.0, 5.3, 9.0, 10, 13, 15.7, 13.2, 8.0, 6.0, 2.0, 8.0, 10, 13],
#                     [1.5, 7.5, 6.2, 9.1, 10, 10.3, 10.8, 13.9, 6, 8, 1.3, 10, 15, 11, 19.7, 16.2, 10, 8, 3, 10, 13, 16],
#                     [1.5, 7.5, 6.2, 9.1, 10, 10.3, 10.8, 13.9, 6, 8, 1.3, 10, 15, 11, 19.7, 16.2, 10, 8, 3, 10, 13, 16]]
# for i in weather_data_test:
#     # print(values[1])
#     print(i)
#     myTest = i
#     # print(key)
# # plt.boxplot(myTest)
#     # for v in values:
#     #     print(key, " : ", v)
# spread = np.random.rand(50) * 100
# print(f"spread {spread}")
# print(type(spread))
# spread = np.random.rand(50)
# print(f"spread {spread}")
# center = np.ones(25) * 50
# print(f"center {center}")
# flier_high = np.random.rand(10) * 100 + 100
# print(f"flier_high {flier_high}")
# flier_low = np.random.rand(10) * -100
# print(f"flier_low {flier_low}")
# data = np.concatenate((spread, center, flier_high, flier_low), 0)
# print(type(data))
# print(f"data {data}")
#
#
# spread = np.random.rand(50) * 100
# center = np.ones(25) * 40
# flier_high = np.random.rand(10) * 100 + 100
# flier_low = np.random.rand(10) * -100
# d2 = np.concatenate((spread, center, flier_high, flier_low), 0)
# # A 2-dimensional array of size 2 x 3, x.shape(2x3)
# data.shape = (-1, 1)
# d2.shape = (-1, 1)
# print(f"d2 {d2}")
# print(f"d2[::2, 0] {d2[::2, 0]}")
# data3 = [data, d2, d2[::2, 0]]
# fig7, ax7 = plt.subplots()
# ax7.set_title('Multiple Samples with Different sizes')
# ax7.boxplot(data3)

myPlot = PlotOperations()


weather_data_mean = {1: [1.1, 5.5, 6.2, 7.1, 8.0, 8.3, 7.8, 6.9, 6, 6, 15.3], 2: [0.1, 3.5, 4.2, 5.1, 5.0, 4.3, 5.8, 4.9, 4.0, 3.0], 3: [0.1, 3.5, 4.2, 5.1, 5.0, 4.3, 5.8, 4.9, 4.0, 3.0]}
weather_data_min = {1: [0.1, 3.5, 4.2, 5.1, 5.0, 4.3, 5.8, 4.9, 4.0, 3.0]}
weather_data_max = {1: [2.1, 7.5, 8.2, 9.1, 10.0, 11.3, 9.8, 8.9, 9.0, 9.3]}

myPlot.diplay_box_plot(weather_data_mean)
