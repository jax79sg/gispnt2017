#This set of import MUST come first
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#System lib import
import Tkinter
from Tkinter import *
import tkFileDialog

#User lib import
import Utils, Geom,Plotting,Presentation


class PipGUI(Presentation.Presentation):

    def update(self):
        """
        To update the Plot on the canvas
        :return:
        """
        self.__figure=self.__plotter.setup()        #Setup the plotting graph
        self.canvas = FigureCanvasTkAgg(self.__figure, master=self.interactframe)   #Set the plot into the canvas
        self.plotwidget = self.canvas.get_tk_widget()
        self.plotwidget.grid(row=6, column=0, columnspan=3, sticky='WE')    #Set the position
        self.__figure.canvas.draw()     #Draw the canvas

    def addmsg(self,_msg):
        """
        Overridden to print information to the GUI console
        :param _msg:
        :return:
        """
        self.consoletxt.insert(INSERT,_msg+"\n")        #Insert to the Text UI

    def __init__(self,_polygonfilepath,_pointtestfile,_pointcoord):
        """
        Initialise the layout of GUI and matlibplot
        Start the UI
        :param _polygonfilepath: Path to the polygon file
        :param _pointtestfile: Path to the test point file
        :param _pointcoord: Set of coordinates x,y|x,y|x,y|...
        """

        #Class variables, all private
        super(PipGUI,self).__init__()   #Run the init of inherited class Presentation
        self.__plotter = Plotting.Plotter() #Instantiate the class that's in charge of Matlibplot
        self.__testpointvalidator = Utils.TestPointValidator()  # Instantiate the testpointvalidator class
        self.__figure=self.__plotter.setup()    #Setup the graph, axis, and legend
        self.__master = Tkinter.Tk()    #Instantiate the Tkinter GUI
        self.__polyfilepath=_polygonfilepath    #Save the arg in var
        self.__testptfilepath=_pointtestfile    #Save the arg in var
        self.__testpttext=_pointcoord           #Save the arg in var

        def openpolyfileCallback():
            """
            Call back function for the select polygon file button, event clicked.
            :return:
            """
            #Get user to select a file
            self.__polyfilepath=tkFileDialog.askopenfilename(title='Select a csv file with the polygon points')

            # Update UI on selected file
            self.polyfiletxt.delete("1.0",END)
            self.polyfiletxt.insert('end',self.__polyfilepath+"\n")
            ## End of call back function

        def opentestptfileCallback():
            """
            Call back function for the select test point file button, event clicked.
            :return:
            """
            #Get user to select file
            self.__testptfilepath = tkFileDialog.askopenfilename(title='Select a csv file with the test points')

            #Update UI on selected file
            self.testptfiletxt.delete('1.0',END)
            self.testptfiletxt.insert('end',self.__testptfilepath)
            ## End of call back function

        def quitpipCallback():
            """
            Call back function for the quit button, event clicked
            :return:
            """
            sys.exit(0) #Exit the program.
            ## End of call back function


        def runpipCallback():
            """
            Call back  function for the Run PIP button, event clicked.
            #Clean up actions

            #Check if polygon file exists and valid, if not cancel action
            #Check if point test file exists and valid, if yes, add to test point list.
            #Check if point test text exists and valid, if yes, add to test point list.
            #if no test points, cancel action

            #for each test point, test PIP with polygon
            #For each result, add to plot

            #Update plot
            :return:
            """
            # Clean up actions
            self.__testpointlist=[] #Clear the existing test points
            self.__plotter.cleanup()    #Clean up the current plot
            self.consoletxt.delete('1.0',END)   #Clean up the message console
            self.update()  # Update the UIcanvas jax

            # Check if polygon file exists and valid, if not cancel action
            csvholder = Utils.CsvPolygonLoader()    #Instantiate utility class for polygon loading
            self.__tgtpolygon, self.__polyfilepath,status=csvholder.loadcsvpolygonUI(self.__polyfilepath) #Load the polygon file and return results
            self.polyfiletxt.delete('1.0',END)  #Update the UI Text and insert the file path
            self.polyfiletxt.insert('end',self.__polyfilepath)
            if(status==-1):
                self.writePolyfileError()   #The polygon file not loaded correctly, end this prematurely.
                return -1
            self.log.info("Polygon loaded:" + self.__tgtpolygon.tostring() + "\nSize:" + str(self.__tgtpolygon.coords.shape))


            # Check if point test text exists and valid, if yes, add to test point list. jax
            self.__testpointlist, self.__testptfilepath, status = csvholder.loadcsvptUI(self.__testptfilepath) #Load the point list file and return results
            self.testptfiletxt.delete('1.0', END)  # Update the UI Text and insert the file path
            self.testptfiletxt.insert('end', self.__testptfilepath)
            if (status == -1):
                self.writePointFileError()  # The polygon file not loaded correctly, write to inform user.
            self.log.info("Test Points loaded:")


            manualtestpoints=self.manualtestpttxt.get() #Get the list of test points from Text UI.

            self.__testpointlist, manualtestptstatus = self.__testpointvalidator.validatemanualtestpoints(manualtestpoints,self.__testpointlist)  # Validate the test points
            if (not manualtestptstatus):
                self.writePointTextError()  # Capture errors with the test points


            #if no test points loaded so far, cancel action
            if  len(self.__testpointlist)==0:
                self.writeNoTestPoint()         #Write message to message console
                return -1                       #No usable test points loaded, cancel prematurely

            # for each test point, test PIP with polygon
            # For each result, add to plot
            self.__plotter.addTestPolygon(self.__tgtpolygon) #Add polygon coords into the plot
            for pt in self.__testpointlist:                     #For each point in the test points list
                result=self.__tgtpolygon.pip(pt)            #Perform PIP
                self.writePointPIP(pt.tostring()+"-->"+result)
                if(result==self.__tgtpolygon.BOUNDARY):         #If result is boundary, add boundary point in plot
                    self.__plotter.addBoundaryPoint(pt)
                elif (result==self.__tgtpolygon.INSIDE):        #If result is inside, add inside point in plot
                    self.__plotter.addInsidePoint(pt)
                elif (result == self.__tgtpolygon.OUTSIDE):     #If result is outside, add outside point in plot
                    self.__plotter.addOutsidePoint(pt)
            self.writeOperationCompleted()                      #Write message to message console

            # Update plot
            self.update()

            ## End of call back function

        #Initialise and lay out the UI components
        self.root = Tkinter.Tk()
        self.root.withdraw()            #To remove the funny small window

        self.interactframe=Frame(self.__master)         #Setup Tkinter frame
        self.interactframe.pack(side=TOP)               #Frame layout

        self.polyfilelbl=Label(self.interactframe,text="Choose Polygon file:", fg="black", anchor="w")  #"Choose polygon file" Label UI, anchor to west side
        self.polyfilelbl.grid(row=0,column=0)         #"Choose polygon file" position it on first row, first col.
        self.polyfiletxt = Text(self.interactframe,height=1)    #"Choose polygon file" Text UI
        self.polyfiletxt.insert('end',self.__polyfilepath)  #"Choose polygon file" Text UI default to arg polyfilepath
        self.polyfiletxt.grid(row=0, column=1)              #"Choose polygon file" Text UI position on first row 2nd col
        self.polyfilebut= Button(self.interactframe, text="...", anchor="e", command=openpolyfileCallback)      #"Choose polygon file" Button UI, anchor to east and set call back function as above
        self.polyfilebut.grid(row=0, column=2)      #"Choose polygon file" Text UI position on first row 3rd col

        self.testptfilelbl=Label(self.interactframe,text="Choose TestPoint file:", fg="black", anchor="w") #"Choose testpoint file" Label UI, anchor to west side
        self.testptfilelbl.grid(row=1,column=0)         #"Choose testpoint file" position it on 2nd row, first col.
        self.testptfiletxt = Text(self.interactframe,height=1)  #"Choose testpoint file" Text UI
        self.testptfiletxt.insert('end',self.__testptfilepath)  #"Choose testpoint file" Text UI default to arg testptfilepath
        self.testptfiletxt.grid(row=1, column=1)                #"Choose testpoint file" Text UI position on 2nd row 2nd col
        self.testptfilebut = Button(self.interactframe, text="...", anchor="e", command=opentestptfileCallback)     #"Choose testpoint file" Button UI, anchor to east and set call back function as above
        self.testptfilebut.grid(row=1, column=2)                 #"Choose testpoint file" Text UI position on 2nd row 3rd col

        self.manualtestptlbl=Label(self.interactframe, text="Enter TestPoints (E.g. 1,20 45,52):", fg="black", anchor="w")  #"Choose manual testpoint file" Label UI, anchor to west side
        self.manualtestptlbl.grid(row=2, column=0)      #"Choose manual testpoint file" position it on 3nd row, first col.
        self.manualtestpttxt = Entry(self.interactframe)         #"Choose manual testpoint file" Text UI
        self.manualtestpttxt.insert('end','1,2|3,4|5,6' if self.__testpttext=='' else self.__testpttext)   #"Choose manual testpoint file" Text UI, default to 1,2|3,4|5,6 as example
        self.manualtestpttxt.grid(row=2, column=1, columnspan=2, sticky='WE')    #"Choose manual testpoint file" Text UI position on 3nd row 3rd col

        self.submitbut = Button(self.interactframe, text="Run PIP", command=runpipCallback, anchor="e")  #Submit button UI, set callback function as above
        self.submitbut.grid(row=3, column=2)        #Submit button UI, positin to 4th row, 3rd col

        self.quitbut = Button(self.interactframe, text="Quit PIP", command=quitpipCallback, anchor="e") #Quit button UI, set callback function as above
        self.quitbut.grid(row=4, column=2)  #Submit button UI, positin to 5th row, 3rd col

        self.consoletxt = Text(self.interactframe, height=5)        #Message console Text UI
        self.consoletxt.grid(row=5, column=0, columnspan=3,sticky='WE') #Message console Text UI position span across 6th row

        self.canvas = FigureCanvasTkAgg(self.__figure, master=self.interactframe)   #Matlibplot canvas UI
        self.plotwidget=self.canvas.get_tk_widget()
        self.plotwidget.grid(row=6, column=0, columnspan=3, sticky='WE')        #Matlibplot canvas UI position span across 7th row

        self.headerlbl = Label(self.interactframe, text="Point In Polygon program\nAUTHOR: Tan Kah Siong (UCL 2016)", fg="black", anchor="w")     #Info Label UI
        self.headerlbl.grid(row=7, column=0, columnspan=3, sticky='WE')     #Info Label UI position 8th row span across

        #Start UI
        self.__master.mainloop()        #Start the UI run


