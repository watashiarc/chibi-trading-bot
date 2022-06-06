import codecs
import csv
import io
import requests
from contextlib import closing
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
from PIL import Image

def get_image_buffer(): 
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf;

def get_sqz_analysis():
    # Input variables
    startDate = '2020-07-01' #YYYY-MM-DD
    days = 3
    scatterPeriod2D = 3
    scatterPeriod3D = 3

    # creating empty lists
    currentDate = ''
    SPX = []
    DIX = []
    GEX = []
    returns = []

    # set the colormap and norm to use for graphs
    cmap = mpl.cm.seismic.reversed()
    #cmap = mpl.cm.bwr.reversed()
    norm = mpl.colors.Normalize(vmin=-0.04, vmax=0.04)

    # Send a GET request to squeezemetrics.com to obtain data
    url = 'https://squeezemetrics.com/monitor/static/DIX.csv'
    response = requests.get(url)
    reader = []
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
        for row in reader:
            # skip lines until we reach startDate
            if row['date'] < startDate:
                continue
            SPX.append(float(row['price']))
            DIX.append(float(row['dix']) * 100)
            GEX.append(float(row['gex']) / 1000000000)
            currentDate = row['date']

    chart_images = []

    print(f'current date: {currentDate}')

    # calculate returns
    for i in range(len(SPX)-days):
        returns.append ((SPX[i+days] - SPX[i]) / SPX[i])
        #print(f'{SPX[i]}, {DIX[i]}, {GEX[i]}, returns:{returns[i]}')

    # Create 2D graph
    fig, axes = plt.subplots(layout='constrained')  # a figure with a single axes
    axes.set_title(f'DIX/GEX to {days}-Day SPX return ({startDate}~)')
    axes.set_xlabel("DIX")
    axes.set_ylabel("GEX")

    # Add color bar
    fig.subplots_adjust(right=0.8)
    cbar_axes = fig.add_axes([0.85, 0.11, 0.025, 0.78])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_axes)

    # contour
    resolution = 80
    x = np.array(DIX[:-days])
    y = np.array(GEX[:-days])
    z = np.array(returns)

    # using interpolation to use contourf
    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(), x.max(), resolution), np.linspace(y.min(), y.max(), resolution)
    xi, yi = np.meshgrid(xi, yi)

    '''
    # normalize before interpolating
    # Normalize coordinate system
    def normalize_x(data):
        data = data.astype(np.float)
        return (data - xmin) / (xmax - xmin)

    def normalize_y(data):
        data = data.astype(np.float)
        return (data - ymin) / (ymax - ymin)

    x = 
    x_new, xi_new = normalize_x(x), normalize_x(xi)
    y_new, yi_new = normalize_y(y), normalize_y(yi)
    '''
    # Interpolate
    rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    zi = rbf(xi, yi)
    #rbf = scipy.interpolate.Rbf(x_new, y_new, z, function='linear')
    #zi = rbf(xi_new, yi_new)

    # Draw color mesh graph
    axes.pcolormesh(xi,yi,zi, cmap=cmap, norm=norm, shading='gouraud')

    # Draw scatter plot
    #axes.scatter(x, y, c=z, s=25, facecolors='none', edgecolors='black', cmap=cmap, norm=norm)
    startingPos = len(x) - scatterPeriod2D # Draw points only for the last {scatterPeriod} amount of days
    axes.scatter(x[startingPos:], y[startingPos:], c=z[startingPos:], s=25, facecolors='none', edgecolors='black', cmap=cmap, norm=norm)

    # Draw current DIX/GEX
    axes.scatter(DIX[-1], GEX[-1], s=50, c='lime', edgecolor='black')
    #plt.colorbar()
    chart_images.append(get_image_buffer())
    plt.close()

    # Create 3D graph
    fig2 = plt.figure()
    ax = fig2.add_subplot(projection='3d')
    ax.set_title(f'DIX/GEX to {days}-Day SPX return ({startDate}~)')
    ax.set_xlabel("DIX")
    ax.set_ylabel("GEX")
    ax.set_zlabel("SPX return")

    # Draw 3D surface plot
    ax.plot_surface(xi,yi,zi, cmap=cmap, norm=norm, alpha=0.5)

    # Draw 3D scatter plot
    startingPos = len(DIX)- days - scatterPeriod3D # Draw points only for the last {scatterPeriod} amount of days
    ax.scatter3D(x[startingPos:], y[startingPos:], z[startingPos:], c=z[startingPos:], cmap=cmap, norm=norm, s=50, alpha=1, edgecolor="black")
    ax.scatter3D(DIX[-1], GEX[-1], 0, s=100, c='lime', edgecolor='black')

    # Display on screen
    # plt.show()
    
    chart_images.append(get_image_buffer())
    
    return chart_images