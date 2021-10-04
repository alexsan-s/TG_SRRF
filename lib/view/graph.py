
import matplotlib.pyplot as plt
import pandas as pd

def plotGraphAlgorithms(data):
    df = pd.DataFrame(data)
    # plotting graph
    df.plot(x="Algorithms", y=["Found", "Total"], kind="bar")
    

    for index, value in enumerate(data['Algorithms']):
        plt.text(index, data['Found'][index], "Found: {}\nTotal:{}".format(str(data['Found'][index]), str(data['Total'][index])))
    plt.show()