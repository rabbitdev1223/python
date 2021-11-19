import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from IPython.display import Image
import os

def Function1():
    # load dataset
    if os.path.isfile('DataTest.xlsx') == True:
        data = pd.read_excel('DataTest.xlsx', index_col=0)
    elif os.path.isfile('DataTest.csv') == True:
        data = pd.read_csv('DataTest.csv')
    else:
        print ('data file is of unknown file format')
    # Generate dimension and review with boxplot
    data['Self'] = data.Column_1
    data.to_csv('Function1Output.csv')
    data.boxplot(by='Self', layout = (2,9),figsize=(15,10))
    plt.savefig('figure_1.png')
def Function2():
    # load dataset
    if os.path.isfile('DataTest.xlsx') == True:
        data = pd.read_excel('DataTest.xlsx', index_col=0)
    elif os.path.isfile('DataTest.csv') == True:
        data = pd.read_csv('DataTest.csv')
    else:
        print ('data file is of unknown file format')
    # Generate dimension and review with boxplot
    data['Square'] = data.Column_1 ** 2
    data.to_csv('Function2Output.csv')
    data.boxplot(by='Square', layout = (2,9),figsize=(45,40))
    plt.savefig('figure_2.png')

    print('ok')
def Function3():
    # load dataset
    if os.path.isfile('DataTest.xlsx') == True:
        data = pd.read_excel('DataTest.xlsx', index_col=0)
    elif os.path.isfile('DataTest.csv') == True:
        data = pd.read_csv('DataTest.csv')
    else:
        print ('data file is of unknown file format')
    # Generate dimension and review with boxplot
    data['Cube'] = data.Column_1 ** 2
    data.to_csv('Function3Output.csv')
    data.boxplot(by='Cube', layout = (2,9),figsize=(15,10))
    plt.savefig('figure_3.png')
Function1()
Function2()
Function3()
