
#Import system libs
import Tkinter, sys

#Import user libs
import Utils, Geom, Gislogging,Plotting,Presentation


class PipCmd(Presentation.Presentation):

    def addmsg(self,_msg):
        """
        Overriden to print information to the CMD console
        :param _msg:
        :return:
        """
        print _msg+"\n"     #In CMD line mode, only need to println



    def __init__(self,_polygonfilepath,_pointtestfile,_pointcoord):
        """
        #Clean up actions

        #Check if polygon file exists and valid, if not cancel action
        #Check if point test file exists and valid, if yes, add to test point list.
        #Check if point test text exists and valid, if yes, add to test point list.
        #if no test points, cancel action

        #for each test point, test PIP with polygon
        #For each result, add to plot

        #Update plot
        :param _polygonfilepath:
        :param _pointtestfile:
        :param _pointcoord:
        """

        print "\n\nWelcome to Point In Polygon program (CMD mode)\nAUTHOR: Tan Kah Siong (UCL 2016)" \
              "\nThe command mode is only recommended if the machine is not configured properly for GUI mode." \
              "\nYou are Strongly Encouraged to run in GUI mode for a better experience" \
              "\nUsage: python Main.py gui=true polyfile=testdata/testPoly.csv testpt=1,1|2,2|3,3\n\n"

        #Initialise clas variables
        super(PipCmd,self).__init__()       #Init inherited class
        self.__polygonfilepath=_polygonfilepath #Putting the arg into local variables
        self.__pointtestfile=_pointtestfile #Putting the arg into local variables
        self.__pointcoord=_pointcoord   #Putting the arg into local variables
        self.__testpointlist=[]         #Initialise the test point list
        self.__plotter = Plotting.Plotter() #Instantiate the plotting class

        # Check if polygon file exists and valid, if not prevent progress
        csvholder = Utils.CsvPolygonLoader()        #Instantiate the polygon loader class
        try:
            self.__tgtpolygon, self.__polygonfilepath, status=csvholder.loadcsvpolygonCMD(self.__polygonfilepath)   #Load the polygon
            if (isinstance(self.__tgtpolygon, Geom.Polygon)):
                self.log.info("Polygon loaded:"+self.__tgtpolygon.tostring()+ "\nSize:"+str(self.__tgtpolygon.coords.shape))
                self.writePolyfileLoaded("Polygon loaded:"+self.__tgtpolygon.tostring()+ "\nSize:"+str(self.__tgtpolygon.coords.shape)) #Write to message console
        except IOError:
            self.log.error(str(sys.exc_info()[0])+" "+ str(sys.exc_info()[1]))

        #Check if point test file exists and valid, if yes, add to test point list.
        self.__testpointlist, self.__pointtestfile, status = csvholder.loadcsvtestptCMD(self.__pointtestfile) #Load the point list file and return results
        if (status == -1):
            self.writePointFileError()  # The point test file not loaded correctly
        self.log.info("Test Points loaded:")


        #Check if point test text exists and valid, if yes, add to test point list.
        testpointvalidator = Utils.TestPointValidator() #Instantiate the testpointvalidator class
        self.__testpointlist,manualtestptstatus= testpointvalidator.validatemanualtestpoints(self.__pointcoord,self.__testpointlist)    #Validate the test points
        if (not manualtestptstatus):    #If there were something wrong during validtion, write message
            self.writeNoTestPoint()

        #From here on, its interactive
        while(True):

            #if no test points found available to use, ask till get it
            while(len(self.__testpointlist) == 0):
                input = raw_input("\nEnter test points in pattern of 1,1|2,2|3,3|4,4 to continue: " + "\nOR\nType QUIT to quit\n>>")    #Get user input
                if (input.lower() == 'quit'):      #Quit if user wishes to
                    self.writeGoodbye()             #Print to message console
                    sys.exit(0)                     #Exit program
                else:
                    self.__pointcoord=input         #Place user input into var
                    self.__testpointlist, manualtestptstatus = testpointvalidator.validatemanualtestpoints(self.__pointcoord, self.__testpointlist) #Validate test points
                    if (not manualtestptstatus):        #If there were something wrong during validtion, write message
                        self.writeNoTestPoint()
            self.writeTestPointsLoaded(self.__pointcoord)   #If reach here means the test points is ok.


            #for each test point, test PIP with polygon
            #For each result, add to plot
            self.__plotter.addTestPolygon(self.__tgtpolygon)     #Add the test polygon into plot
            for pt in self.__testpointlist:                             #For each point in test point list
                result=self.__tgtpolygon.pip(pt)                    #Test pt for PIP
                self.writePointPIP(pt.tostring() + "-->" + result)
                if(result==self.__tgtpolygon.BOUNDARY):                 #If result boundary, add as boundary point
                    self.__plotter.addBoundaryPoint(pt)
                elif (result==self.__tgtpolygon.INSIDE):                #If result inside, add as inside point
                    self.__plotter.addInsidePoint(pt)
                elif (result == self.__tgtpolygon.OUTSIDE):             #If result outside, add as outside point
                    self.__plotter.addOutsidePoint(pt)



            #Update plot
            self.writePlotRendered()    #Write info to message console
            self.__plotter.setup()      #Setup graph
            self.__plotter.render()     #Show the graph
            self.__plotter.unfreeze()   #Needed to unblock the plot thread after closing plot


            #Flush
            self.__testpointlist=[]     #Clean up the test point list for fresh start
            self.__plotter.cleanup()    #Clean up the plot







