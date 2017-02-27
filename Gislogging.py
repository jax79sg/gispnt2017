import logging

#Logging class for all of the classes
#Purely for debugging purposes, normal user should not see it.
class LoggingHandler (object):
    def __init__(self):
        #Logging will be logged into pip.log in running folder
        #All logs will be overwritten on a fresh run of program
        #All Debug and above calls will be logged.
        #Format: Time, Python Filename, LineNo, Name of Function, Log level, The message
        logging.basicConfig(filename='pip.log',level=logging.DEBUG, filemode='w',format='%(asctime)s %(module)s.py line:%(lineno)d %(name)s.%(funcName)s %(levelname)s %(message)s')
        self.log = logging.getLogger(self.__class__.__name__)

    def debug(self,_msg):
        self.log.debug(_msg)    #Debug level log

    def error(self,_msg):
        self.log.error(_msg)    #Error level log

    def info(self,_msg):
        self.log.info(_msg)     #Info level log

    def fatal(self,_msg):
        self.log.fatal(_msg)    #Fatal level log

    def warning(self,_msg):
        self.log.warning(_msg)  #Warning level log