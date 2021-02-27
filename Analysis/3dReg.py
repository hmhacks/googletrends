"""
This script visualizes key word search data vs. EPOP in 3D.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import  axes3d, Axes3D

cwd = os.getcwd()
inData = '../Data/workingData.csv'
data = pd.read_csv(inData)
state = "New York"
data = data[data['stname']==state]
plt.rc('font',family='Karla')
my_dpi=96

def choice():
    x = input('Image(i) or GIF?(g)?:')
    return x

def normal():
    threedee = plt.figure(figsize=(940/my_dpi, 840/my_dpi), dpi=my_dpi).gca(projection='3d')
    threedee.tick_params(colors="#1A1B41")
    threedee.grid(color='#1A1B41', linestyle='-', linewidth=0.5)
    threedee.scatter(data['google_unemployment'], data['googleflights'], data['unemployment_rate'])
    threedee.set_xlabel('"unemployment"')
    threedee.set_ylabel('"google flights"')
    threedee.set_zlabel('EPOP')
    plt.title("Google Searches for 'Unemployment' and 'Google Flights' vs. EPOP" + " (" + str(state)+ ")")
    plt.show()

def vis():
    """
    Visualizes the df.
    """
    for angle in range(70,210,2):
        threedee = plt.figure(figsize=(940/my_dpi, 840/my_dpi), dpi=my_dpi).gca(projection='3d')
        threedee.tick_params(colors="#1A1B41")
        threedee.grid(color='#1A1B41', linestyle='-', linewidth=0.5)
        threedee.scatter(data['google_unemployment'], data['googleflights'], data['unemployment_rate'])
        threedee.set_xlabel('"unemployment"')
        threedee.set_ylabel('"google flights"')
        threedee.set_zlabel('EPOP')
        plt.title("Google Searches for 'Unemployment' and 'Google Flights' vs. EPOP" + " (" + str(state)+ ")")
        threedee.view_init(30,angle)
        filename= cwd +  '/Visualization/Image'+str(angle)+'.png'
        plt.savefig(filename, dpi=96)
        plt.gca()


def compileGif():
    path = cwd + "/Visualization"
    dirs = os.listdir(path)

    bashCommand = "convert -delay 50 Image*.png scatter.gif"
    os.system(bashCommand)

    for file in dirs:
        if file[:5] == "Image":
            os.remove(path + "/" + file)


if __name__ == "__main__":
    x = choice()

    if x == 'i':
        normal()
    elif x=='g':
        vis()
        compileGif()
