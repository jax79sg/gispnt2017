import csv
import Tkinter as tk
import tkFileDialog
import Geom
import os.path
import Gislogging




"""
    Utitly classes for simple stuff
"""


"""
    Utility class to validate test points
"""
class TestPointValidator(Gislogging.LoggingHandler):
    def validatemanualtestpoints(self, _testpoints='', _testpointlist=[]):
        """
        # Check if point test text exists and valid, if yes, add to test point list.
        :param _testpoints:
        :param _testpointlist:
        :return: tstpoint list and status
        """

        manualtestpoints = _testpoints                      #Placing arg into var
        try:
            listofpoints = manualtestpoints.split("|")      #Using pipe as delimiter, get the coord sets
            for pointstr in listofpoints:                   #For each coord
                pointxy = pointstr.split(",")               #Get the x and y in array
                point = Geom.Point(pointxy[0], pointxy[1])  #Create a Geometry Point
                _testpointlist.append(point)                #Add the geometry Point into the list of test points
            return _testpointlist, True
        except Exception:
            return _testpointlist, False
        pass



"""
    class to load polygon file
"""
class CsvPolygonLoader(Gislogging.LoggingHandler):

    def __init__(self):
        super(CsvPolygonLoader,self).__init__()
        self.__filepath=''

    def loadcsvptUI(self, _fullfilepath=''):
        """
        For GUI mode only
        1. Check if a file path is given, if not, call private method to allow user to select file
        2. Call private method to read in the file and process into list of test Points
        3. Return the list of points as a list
        :param _fullfilepath:
        :return:
        """
        loadedPointlist=[]
        # if _fullfilepath=='':
        #     self.__filepath=self.__get_csv_filepath()       #If filepath is empty, request for it
        # # elif(os.path.exists(_fullfilepath)==False):
        # #     self.__filepath = self.__get_csv_filepath()
        # else:
        #     self.__filepath=_fullfilepath
        pointlist, status=self.__read_csv_data(_fullfilepath)            #Read the content
        if (status!=-1):
            loadedPointlist=pointlist           #If content ok, save the results as Point list
        return loadedPointlist, _fullfilepath,status


    def loadcsvpolygonUI(self, _fullfilepath=''):
        """
        Public method
        For GUI mode only
        1. Check if a file path is given, if not, call private method to allow user to select file
        2. Call private method to read in the file and process into list of Points
        3. Return the list of points as a Polygon
        :param _fullfilepath:
        :return:
        """
        loadedPolygon=''
        if _fullfilepath=='':
            _fullfilepath=self.__get_csv_filepath()       #If filepath is empty, request for it
        elif(os.path.exists(_fullfilepath)==False):
            self.log.error("Invalid file: " + _fullfilepath)          #If path is invalid, request again
            _fullfilepath = self.__get_csv_filepath()
        # else:
        #     self.__filepath=_fullfilepath
        pointlist, status=self.__read_csv_data(_fullfilepath)            #Read the content
        if (status!=-1):
            loadedPolygon=Geom.Polygon(pointlist)           #If content ok, save the results as Polygon class
        return loadedPolygon, _fullfilepath,status

    def loadcsvpolygonCMD(self, _fullfilepath=''):
        """
        Public method
        For CMD mode only
        1. Check if a file path is given, if not, call private method to allow user to select file
        2. Call private method to read in the file and process into list of Points
        3. Return the list of points as a Polygon
        :param _fullfilepath:
        :return:
        """
        while (os.path.exists(_fullfilepath) == False):
            print "Invalid polygon file in argument: " + _fullfilepath              #Ask until a valid file path available
            _fullfilepath = raw_input("Please enter the correct polygon file path:")



        pointlist, status = self.__read_csv_data(_fullfilepath)          #Read the contents
        if (status!=-1):
            loadedPolygon=Geom.Polygon(pointlist)           #If ok, load the points into Polygon class
        return loadedPolygon, _fullfilepath,status


    def loadcsvtestptCMD(self, _fullfilepath=''):
        """
        Public method
        For CMD mode only
        1. Check if a file path is given, if not, call private method to allow user to select file
        2. Call private method to read in the file and process into list of Points
        3. Return the list of points
        :param _fullfilepath:
        :return:
        """
        loadedtestpt=[]
        if (os.path.exists(_fullfilepath) == False):
            print "Invalid polygon file in argument: " + _fullfilepath              #Ask until a valid file path available
            return loadedtestpt, _fullfilepath, False


        pointlist, status = self.__read_csv_data(_fullfilepath)          #Read the contents
        if (status!=-1):
            loadedtestpt=pointlist           #If ok, load the points into Polygon class
        return loadedtestpt, _fullfilepath,status

    def __get_csv_filepath(self):
        """
        This call,
        1. Performs opening of file dialog
        2. Returns absolute file path
        :return:
        """
        root = tk.Tk()
        root.withdraw()     #Just to get rid of the small window
        filename=tkFileDialog.askopenfilename(title="Please select a valid polygon file")   #Request user to select file
        return filename


    def __read_csv_data(self, _filepath):
        """
        This call,
        1. Read the CSV file and perform simple validation of content
        2. Returns a list of points
        :param _inputfilepath:
        :return:
        """
        status = 0
        pointsList=[]
        try:
            with open(_filepath, 'r') as csvFile:         #Open csv file read only
                readin = csv.reader(csvFile, delimiter=',')     #Use csvreader
                for row in readin: #Each row has x,y only
                    if (len(row)>=2):
                        newPoint = Geom.Point(_x=row[0],_y=row[1])  #If each row has 2 elements, then use the 1st and 2nd elements as Point
                        pointsList.append(newPoint)          #Append into list
                    else:
                        self.log.warning("Found blank lines in the csv, skipping it")
            csvFile.close()
        except:
            self.log.error("The content of the polygon csv is invalid")
            status= -1
        return pointsList, status

