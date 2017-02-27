#Import user lib
import Gislogging

#Import system libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import math

"""
Basic class for all geometries
"""
class Geom(Gislogging.LoggingHandler):
    #Set fixed figures for this class and subclasses
    BOUNDARY="BOUNDARY"
    INSIDE="INSIDE"
    OUTSIDE="OUTSIDE"

    def __init__(self):
        super(Geom,self).__init__()

    def getStartPoint(self):
        return self.coords[0]       #Get first coord

    def getEndPoint(self):
        return self.coords[-1]      #Get last coord

    def tostring(self):
        """
        To print useful human readable information about the coordinates
        :return: String
        """
        output=""
        for pt in self.coords:
            output=output+"["+str(pt[0])+","+str(pt[1])+"],"    #String out the coords
        return output

    """
        Exercise 2 Part 1
    """
    def getNumPoints(self):
        return self.coords.shape[0]     #Return the size of the array

    """
        Exercise 2 Part 2
    """
    # def addPoint(self, _pointcoord):
    #     self.coords = np.vstack([self.coords,_pointcoord])

    def addPoint(self, _point):
        pointcoord=_point.coords
        self.coords = np.vstack([self.coords,pointcoord])


    def contain(self, _testpoint):
        raise NotImplementedError("Subclass must implement abstract method")


    def getEdges(self):
        raise NotImplementedError("Subclass must implement abstract method")








class Point(Geom):
    """
        A Point object must be instantiated with at least one coordinate set. Else it would default to [Zero, Zero] coordinate
    """
    def __init__(self, _x=0.0, _y=0.0, _z=float('nan')):
        super(Point,self).__init__()
        try:
            x=float(_x)                             #Set x and y for point.
            y=float(_y)
        except ValueError:
            self.log.fatal("A point cannot accept ")


        self.__coords=np.array([_x, _y, _z], dtype=float)
        self.__coords.shape=(1, 3) #Fix the array to be 1 row, 3 col (Row is the coordinate set, Col is the X, Y , Z)

    """
        Exercise 2 Part 2
    """
    def addPoint(self, _point):
        self.log.error("Can't add a point to a point, no changes made")
        return -1

    @property
    def x(self):
        return self.__coords[0][0]

    @x.setter
    def x(self,_x):
        self.__coords[0][0]=_x

    @property
    def y(self):
        return self.__coords[0][1]

    @y.setter
    def y(self,_y):
        self.__coords[0][1]=_y

    @property
    def z(self):
        """
        This property is typically unused
        :return:
        """
        return self.__coords[0][2]

    @y.setter
    def z(self,_z):
        self.__coords[0][2]=_z

    @property
    def coords(self):
        return self.__coords

    def contain(self, _testpoint):
        """
        Do not use this method on this class
        :param _testpoint:
        :return:
        """
        self.log.error("A point cannot contain another point")
        raise AssertionError("A point cannot contain another point")

    def tostring(self):
        return "("+str(self.x)+","+str(self.y)+")"












"""
    Exercise 1
"""
class Line(Geom):

    def __init__(self,_points=[]):
        super(Line, self).__init__()
        self.__assignCoords(_points)        #Open up points and add in into line
        self.minboundrect_simple()          #Create a MBR on initialise

    @property
    def coords(self):
        return self.__coords;

    @coords.setter
    def coords(self,_points=[]):
        self.__assignCoords(_points)

    def contain(self, _testpoint):
        """
        Do not use this method on this class. There is a more relevant method called isIntersectPoint()
        :param _testpoint:
        :return:
        """
        self.log.error("A line cannot contain another point, try isIntersectPoint() method")
        raise AssertionError("A line cannot contain another point, try isIntersectPoint() method")


    def __assignCoords(self,_points):
        """
        #class should have an __init__ method that creates an empty line object (i.e. coords is an empty list) when no coordinates are specified.
        #class shall not accept incomplete entries too (E.g. just one point).

        :param _points:
        :return:
        """

        if len(_points)>1:
            # self.__coords=np.vstack(_points)
            # return 0

            listofpoints =[]
            for pt  in _points:
                listofpoints.append(pt.coords)
            self.__coords=np.vstack(listofpoints)
            return 0

        else:
            self.log.warning("A line needs at least 2 points, no changes made")
            return -1

    def isIntersectPoint(self,_point):
        """
        Determine if the point lies on this line.
        :param _point:
        :return:
        """


        lp1x=self.coords[0][0]
        lp1y = self.coords[0][1]
        lp2x = self.coords[1][0]
        lp2y = self.coords[1][1]
        tpx=_point.x
        tpy=_point.y

        # http://stackoverflow.com/questions/11907947/how-to-check-if-a-point-lies-on-a-line-between-2-other-points
        dxp = tpx - lp1x;
        dyp = tpy - lp1y;
        dxl = lp2x - lp1x;
        dyl = lp2y - lp1y;
        cross = dxp * dyl - dyp * dxl;      #Formula to determine intersect
        self.log.debug("Processing point intersect, cross="+str(cross))
        if cross==0:
            #The point lies somewhere along the line (can be extended line), now to check if its on the line itself
            gradient= dyp/dxp
            if (not math.isinf(gradient)):
                if(lp1x>lp2x):
                    #lp1x is bigger
                    if(tpx>lp1x or tpx<lp2x):
                        #No intersect
                        return False
                    else:
                        #Intersect
                        return True
                else:
                    #lp2x is bigger
                    if(tpx>=lp2x or tpx<lp1x):
                        #No intersect
                        return False
                    else:
                        #Intersect
                        return True

        else:
            return False


    def isIntersectline(self, _line):
        """
        Determine if this line intersects with another line
        http://stackoverflow.com/questions/29854085/line-segments-intersectionintersection-point
        :param _line:
        :return:
        """
        self.debug("Processing line intersect")
        ax = self.coords[0][0]
        ay = self.coords[0][1]
        bx = self.coords[1][0]
        by = self.coords[1][1]
        cx = _line.coords[0][0]
        cy = _line.coords[0][1]
        dx = _line.coords[1][0]
        dy = _line.coords[1][1]

        cp1=(bx-ax)*(cy-by)-(by-ay)*(cx-bx)     #DET of A,B,C
        cp2=(bx-ax)*(dy-by)-(by-ay)*(dx-bx)     #DET of A,B,D

        cp3=(dx-cx)*(ay-dy)-(dy-cy)*(ax-dx)     #DET of C,D,A
        cp4=(dx-cx)*(by-dy)-(dy-cy)*(bx-dx)     #DET of C,D,B

        return ((cp1*cp2)<0 and (cp3*cp4)<0)    #Intersect IFF both return less than zero.



    def getEdges(self):
        """
        Gets all the edges of this Line object as list of lines
        :return:
        """
        listoflines=[]
        # print self.coords
        for ptpos in range(0,len(self.coords)-1):       #For each point in coordinates
            pt1=Point(self.coords[ptpos][0],self.coords[ptpos][1])      #First point
            pt2 = Point(self.coords[ptpos+1][0],self.coords[ptpos+1][1])  # Next point
            line=Line([pt1,pt2])
            listoflines.append(line)
        return listoflines


    def minboundrect_simple(self):
        """
        Upon creation of the object, a simple min boundary rect is immediately generated.
        Create MBR as in notes.
        :return:
        """
        minx=float("inf")
        miny=float("inf")
        maxx=-1*float("inf")
        maxy=-1*float("inf")
        for nparray in self.coords:
            x=nparray[0]
            y=nparray[1]
            if x < minx:  minx = x
            if y < miny:  miny = y
            if x > maxx:  maxx = x
            if y > maxy:  maxy = y

        self.boundrect=self.BoundRectangle(minx,miny,maxx,maxy)

    #Subclass of Line, to store MBR information
    class BoundRectangle(object):
        def __init__(self,_minx=0,_miny=0,_maxx=0,_maxy=0):
            self.__minx =_minx
            self.__miny = _miny
            self.__maxx =_maxx
            self.__maxy = _maxy

        @property
        def minx(self):
            return self.__minx
        @property
        def miny(self):
            return self.__miny
        @property
        def maxx(self):
            return self.__maxx
        @property
        def maxy(self):
            return self.__maxy

        @minx.setter
        def minx(self,_minx):
            self.__minx=_minx
        @miny.setter
        def miny(self,_miny):
            self.__miny=_miny
        @maxx.setter
        def maxx(self,_maxx):
            self.__maxx=_maxx
        @maxy.setter
        def maxy(self,_maxy):
            self.__maxy=_maxy













class Polygon(Line):

    def __init__(self,_pointlist):
        super(Polygon,self).__init__(_pointlist)

    def mbr(self,_testpoint):
        # Check if point is within MBR
        if (_testpoint.x < self.boundrect.minx or _testpoint.x > self.boundrect.maxx or _testpoint.y < self.boundrect.miny or _testpoint.y > self.boundrect.maxy):
            self.log.debug("Test point is outside MBR")
            return self.OUTSIDE
        else:
            return self.INSIDE

    def pip(self, _testpoint):
        """
        The main juice of this assignment. This works only for simple polygons
        Check if the point is within this polygon
        :param _testpoint:
        :return:
        """
        if isinstance(_testpoint,Point):        #Just to make sure the object is Point class
            if self.mbr(_testpoint)==self.OUTSIDE:
                return self.OUTSIDE
            else:
                #Point is within MBR, now to use ray casting to determine if within polygon
                return self.raycast(_testpoint)
        else:
            raise AttributeError("Polygon contain currently only support Geom.Point as an argument")

    def raycast(self, _testpoint):
        """
        To also handle 2 special cases.
        1. If point falls on edge of polygon
        2. If the Ray casted falls on vertices of polygon
        :param _testpoint:
        :return:
        """
        tolerance=0.001 #This is used to adjust angle of ray should there be inconsistency of computation

        OUTSIDE=-1
        INSIDE=1
        status=OUTSIDE

        #Special case - If point falls on edges, then its actually on the boundary
        edges=self.getEdges()
        for edge in edges:
            #Test point if it lies on any edges, if yes, then boundary
            if edge.isIntersectPoint(_testpoint):
                self.info("Test point" + _testpoint.tostring()+" is on edge "+ edge.tostring())
                return self.BOUNDARY


        #Special case - If ray intersect with vertex
        # The results may be inconsistent, in this case, adjust the end point of the ray a little tiny bit up (y axis), till no vertex intersect. Then retry ray cast algo.
        farpoint = Point(self.boundrect.maxx,_testpoint.y)  #Genenate a far point for the ray
        ray = Line([_testpoint,farpoint])   #Create the ray
        suitableray=False
        while (not suitableray):
            suitableray = True
            for pt in self.coords:              #For each vertex in this polygon
                vertex=Point(pt[0],pt[1])
                if ray.isIntersectPoint(vertex):    #Check if vertex intersect with ray
                    suitableray=False               #If intersect with ray, then this ray is not suitable as it will give inconsistency
                    farpoint = Point(self.boundrect.maxx, _testpoint.y+tolerance)       #Recreate a new far point for ray (Plus Y axis by tolerance)
                    tolerance=tolerance+tolerance           #Increase tolerance further in case this ray still not good enough
                    ray = Line([_testpoint, farpoint])
                    self.log.info("The generated ray is intersecting with vertex " + vertex.tostring() +", adjusting ray angle to " + ray.tostring())
                    break

        # Suitbale ray achieved
        #Ray cast algo.
        edges=self.getEdges()
        for edge in edges:          #For each edge of polygon
            if (ray.isIntersectline(edge)): #If ray intersect the edge, then flip status
                self.log.debug("Ray intersected with edge " + edge.tostring())
                status=-1*status
        return self.OUTSIDE if status==OUTSIDE else self.INSIDE

    def getEdges(self):
        """
        Polygons have one extra edge compared to normal polylines (Or lines in this case)
        :return:
        """
        listoflines=super(Polygon,self).getEdges();
        lastlinept1=Point(self.coords[len(self.coords)-1][0],self.coords[len(self.coords)-1][1])    #Polygons has one extra line back to origin
        lastlinept2=Point(self.coords[0][0],self.coords[0][1])  #Polygons has one extra line back to origin
        lastline = Line([lastlinept1,lastlinept2])
        listoflines.append(lastline)
        self.log.debug("Listing edges:" )
        for line in listoflines:
            self.log.debug("Returning edges:"+line.tostring())
        return listoflines












