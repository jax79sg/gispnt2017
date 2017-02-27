import Gislogging
import sys
import Gui,Cmd
import matplotlib
import Tkinter

"""
Main class to run the program
This class determines the running computer's setup and displays warning if there are potential problems.
This class will take in the arguments and process them.
"""


logger = Gislogging.LoggingHandler()    #For logging purposes
guienabled=True                         #Default setting for GUI
polygonfilepath=''                      #Variable to store the polygon file path arg
pointtestfile=''                        #Variable to store the test points file path arg
pointcoord=''                           #Variable to store the test points arg

# Taking in arguments
# gui=true(default) |false
# polyfile=full pathname
# testptfile=full pathname
# testpt=1,1|2,2|3,3        Pipe of Vertical Bar is the delimiter for each set of coordinates

for i in range(1,len(sys.argv)):        #For each arg taken when program run. The 0th arg is not user arguments, so ignored.
    arg=str(sys.argv[i])                #Convert arg to string and save
    if(len(arg.split("="))==2):         #check if arg pattern is key=value
        key=arg.split("=")[0]           #Split arg into key and value
        value = arg.split("=")[1]
        if(key.lower()=='gui'):         #For key gui, set if GUI mode
            if(value.lower()=='false'):
                guienabled=False
            elif(value.lower()=='true'):
                guienabled=True

        elif(key.lower()=='polyfile'):  #For key polyfile, set path of polygon
            polygonfilepath = value

        elif(key.lower()=='testptfile'): #For key testptfile, set path of test points
            pointtestfile=value

        elif(key.lower()=='testpt'):    #For key testpt, set the test points (In string)
            pointcoord=value

#Warning to user if python doesn't work as expected. (Note: Software doesn't work on native python in MacOS. Need to use the Brew python instead.
# brew install python -universal - framework
# Tested ok with RemoteDesktop@UCL using the ArcGIS installation's python
if ('1.4.3' not in str(matplotlib.__version__)): print("WARNING:PIP program is tested only on matplotlib version 1.4.3, your version is ", str(matplotlib.__version__))
if ('2.7.12' not in str(sys.version)): print("WARNING:PIP program is tested only on python version 2.7.10, your version is ", str(sys.version))
if ('81008' not in str(Tkinter.__version__)): print("WARNING:PIP program is tested only on Tkinter revision 81008, your version is ", str(Tkinter.__version__))
if ('8.5' not in str(Tkinter.TclVersion)): print("WARNING:PIP program is tested only on Tkinter.TclVersion 8.5, your version is ", str(Tkinter.TclVersion))
if ('8.5' not in str(Tkinter.TkVersion)): print("WARNING:PIP program is tested only on Tkinter.TkVersion 8.5, your version is ", str(Tkinter.TkVersion))


#Note: GUI and CMD mode behaves very differently.
#GUI mode is event based, while CMD mode is sequential execution based.
if (guienabled):
    #Run in GUI mode
    logger.info("Running in GUI mode")
    pip = Gui.PipGUI(polygonfilepath,pointtestfile,pointcoord)  #Start GUI instance with the arguments
else:
    #Run in commandline mode
    logger.info("Running in command mode")
    cmd = Cmd.PipCmd(polygonfilepath,pointtestfile,pointcoord)  #Start the CMD line instance with the arguments










