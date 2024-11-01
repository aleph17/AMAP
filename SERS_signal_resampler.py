"""

This file contains the code used to resample/interpolate the data
obtained from SERS signals to be further utilised to make 
conclusions suing the PCA technique

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import os


#defining the reading and saving directory variables
save_dir = ""
read_dir = ""


#reading the data
frames = []
for dirname, _, filenames in os.walk(read_dir):
    for filename in filenames:
        file = open(os.path.join(dirname, filename))
        data = []

        for line in file:
            adj =[]
            adj = [float(i) for i in line.split()]
            data.append(adj)

        data = pd.DataFrame(data)
        frames.append(data)


#finding the max and min extremes
max = frames[0][0].max()
min = frames[0][0].min()
for frame in frames:
    if frame[0].min() > min:
        min = frame[0].min()
    if frame[0].max() < max:
        max = frame[0].max()
div = int((max- min)//2.01)


#resampling/interpolasting the data
result = []
xi_ = np.linspace(max, min, div)
for frame in frames:
    temp = pd.DataFrame()
    temp[0] = xi_[::-1]
    x = frame[0]
    for i in range(1,frame.shape[1]):
        y = frame[i]
        f = interp1d(x,y, kind="cubic")
        yi = f(xi_)
        temp[i] = yi[::-1]
    result.append(temp)


#visualizing the results
#plt.plot(frames[0][0], frames[0][2])
#xi_ = np.linspace(max, min, div)
# plt.plot(xi_,first[2], label="cubic spline")


#saving the results
result[4].to_csv(save_dir, index = False)
