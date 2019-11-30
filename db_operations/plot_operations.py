"""Module: Creates a PlotOperations class to scrape data from website."""
import matplotlib.pyplot as plt


class PlotOperations():
    """This class display a boxplot."""

    def diplay_box_plot(self, myList):
        """Display a boxplot of PlotOperations."""
        myMean = []
        try:
            for key, values in myList.items():
                try:
                    myMean.append(values)
                    plt.boxplot(myMean)
                except Exception as e:
                    print("Error:", e)
            try:
                plt.show()
            except Exception as e:
                print("Error:", e)
        except Exception as e:
            print("Error:", e)
