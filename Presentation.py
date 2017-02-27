import Gislogging
"""
This class is used by its subclasses to display messages
"""
class Presentation(Gislogging.LoggingHandler):
    def __init__(self):
        super(Presentation,self).__init__()

    def writePolyfileError(self, _msg=''):
        """
        Default message if loading polygon file hits problem
        :param _msg: custom message
        :return:
        """
        defaultmsg="An error occured loading the polygon file, please check the content"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writePolyfileLoaded(self, _msg=''):
        """
        Default message if polygon file loaded succesfully.
        :param _msg: custom message
        :return:
        """
        defaultmsg="Polygon file loaded successfully"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)


    def writePointTextError(self, _msg=''):
        """
        Default message of the list of test points for problem
        :param _msg: custom message
        :return:
        """
        defaultmsg="The test point list in the text cannot be parsed."
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writePointFileError(self, _msg=''):
        """
        Default message of the list of test points for problem
        :param _msg: custom message
        :return:
        """
        defaultmsg="The test point list in the file cannot be parsed."
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writeNoTestPoint(self, _msg=''):
        """
        Default message for the list of test points empty
        :param _msg: custom message
        :return:
        """
        defaultmsg="There are problems with the test points"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writeOperationCompleted(self, _msg=''):
        """
        Default message when operation completed
        :param _msg:
        :return:
        """
        defaultmsg="Results ran and completed"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writeGoodbye(self, _msg=''):
        """
        Default message when exiting program
        :param _msg:
        :return:
        """
        defaultmsg="\nHope you had fun! Goodbye!"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writePlotRendered(self, _msg=''):
        """
        Default message when plot completed
        :param _msg:
        :return:
        """
        defaultmsg="The plot should be rendered, please click it on the taskbar if its not on the screen. Close it to continue.\n"
        if _msg == '':
            msg =defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writeTestPointsLoaded(self, _msg=''):
        """
        Default message when test points loaded
        :param _msg:
        :return:
        """
        defaultmsg="Test points processed\n"
        if _msg == '':
            msg =defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writeCriticalError(self, _msg=''):
        """
        Default message when there is critical error
        :param _msg:
        :return:
        """
        defaultmsg="Critical Error: Exiting"
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def writePointPIP(self, _msg=''):
        """
        Default message for results
        :param _msg:
        :return:
        """
        defaultmsg="Point "
        if _msg == '':
            msg = defaultmsg
        else:
            msg = defaultmsg+_msg
        self.addmsg(msg)

    def addmsg(self,_msg):
        """
        Has to be implemented by the subclass since each subclass has their own way of displaying messages
        :param _msg:
        :return:
        """
        raise NotImplementedError ('This method must be implemented by subclass')

