import Gislogging

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as polyplot
from matplotlib.patches import Circle as circleplot
import Geom

"""
This class handles all the plotting operations
"""

class Plotter(Gislogging.LoggingHandler):
    #Fixed variables for the coloring
    INSIDECOLOR='#7CFC00'
    OUTSIDECOLOR='red'
    BOUNDARYCOLOR='black'
    POLYGONCOLOR='blueviolet'
    DEFAULTCOLOR='blue'

    def __init__(self):
        self.__patches=[]       #This patches will be used to fill the elemnets to be plotted

    # def ion(self):
    #     plt.ion()

    def closeplot(self):
        """
        Close the plot
        :return:
        """
        plt.close('all')


    def unfreeze(self):
        """
        Needed for breaking blocks in lopping plots in CMD mode
        :return:
        """
        plt.pause(0.001)

    def cleanup(self):
        """
        Remove all drawing elements on plot
        :return:
        """
        self.__patches = []



    def addInsidePoint(self, _point):
        """
        Add a point that represents an INSIDE point for plotting
        :param _coordList:
        :return:
        """
        self.__addPoint(_point,_color=self.INSIDECOLOR)




    def addOutsidePoint(self, _point):
        """
        Add a point that represents an OUTSIDE point for plotting
        :param _coordList:
        :return:
        """
        self.__addPoint(_point, _color=self.OUTSIDECOLOR)



    def addBoundaryPoint(self, _point):
        """
        Add a point that represents a BOUNDARY point for plotting
        :param _coordList:
        :return:
        """
        self.__addPoint(_point, _color=self.BOUNDARYCOLOR)



    def addTestPolygon(self,_polygon):
        """
        Add a polygon that represents the test polygon for plotting
        :param _coordList:
        :return:
        """
        self.__addPolygon(_polygon, _color=self.POLYGONCOLOR)


    def addLine(self,_line):
        """
        Originally used to plot ray cast, but deprecating this method as it clutters the plot when there are many test points.
        Now mainly used when testing
        :param _coordList:
        :return:
        """
        self.__addLine(_line,_color='purple')



    def __addLine(self,_line, _color=DEFAULTCOLOR):
        """
        Originally used to plot ray cast, but deprecating this method as it clutters the plot when there are many test points.
        Now mainly used when testing
        :param _coordlist:
        :param _color:
        :return:
        """
        verts = np.array([_line.coords[0][0],_line.coords[0][1]])
        for i in range(1,len(_line.coords)):
           newvert = np.array([_line.coords[i][0], _line.coords[i][1]])
           verts=np.vstack([verts,newvert])

        plotline = polyplot(verts, False, color=_color)
        self.__patches.append(plotline)





    def __addPolygon(self,_polygon, _color=DEFAULTCOLOR):
        """
        Baseline for plotting polygons
        :param _coordlist:
        :param _color:
        :return:
        """
        verts = np.array([_polygon.coords[0][0],_polygon.coords[0][1]])   #Create the first point coords
        for i in range(1,len(_polygon.coords)):
            newvert = np.array([_polygon.coords[i][0], _polygon.coords[i][1]])    #Stack the rest of the points into the first and repeat
            verts=np.vstack([verts,newvert])

        plotpolygon = polyplot(verts, True, color=_color)       #Instantiate a matlibplot polygon based on my polygon points.
        self.__patches.append(plotpolygon)                      #Append the matlibplot polygon into patches list


    def __addPoint(self,_point, _color=DEFAULTCOLOR):
        """
        Baseline for plotting points
        :param _coordlist:
        :param _color:
        :return:
        """
        verts = np.zeros(shape=(1, 2))                          #Create an empty nparray with shape 1,2
        verts = np.vstack([_point.coords[0][0], _point.coords[0][1]])     #Place the coordinates
        plotcircle=circleplot(verts, 0.2, color=_color)            #Instantiate a matlibplot circle based on my points as center, with diameter 0.2
        self.__patches.append(plotcircle)                       #Append the matlibplot circle into patches list

    def setup(self):
        """
        Baseline setup for the plotting
        :return:
        """
        self.__fig, self.__ax = plt.subplots()              #Setup matlibplot
        for patch in self.__patches:
            self.__ax.add_patch(patch)                      #For each matlibplot element in patches, add it into plot.
        insidelegend = plt.Line2D(range(1),range(1), markersize=15, marker='o',color='white', markerfacecolor=self.INSIDECOLOR)     #Add legend for INSIDE circle
        outsidelegend = plt.Line2D(range(1),range(1), markersize=15, marker='o',color='white', markerfacecolor=self.OUTSIDECOLOR)   #Add legend for OUTSIDE circle
        boundarylegend = plt.Line2D(range(1),range(1), markersize=15, marker='o',color='white', markerfacecolor=self.BOUNDARYCOLOR) #Add legend for BOUNDARY circle
        self.__ax.legend([insidelegend, outsidelegend, boundarylegend], ['Inside','Outside','Boundary'],numpoints=1, loc='best')    #Setup the legend, position is dynamic to avoid covering points
        self.__ax.autoscale_view(True, True, True)          #Auto scale the graph
        return self.__fig


    def render(self):
        """
        Special code for rendering in CMD mode
        :return:
        """
        plt.draw()                                          #Draw and display the plot in new window
        plt.show()