# -*- coding: iso-8859-15 -*-
"""
Contains methods and functionality used for VISUM AddIns.
See example AddIn named 'AddInClassTest' for further information.
"""
import logging
import gettext
import win32com.client as com
import sys
import wx
import os
import re
from cPickle import dumps, loads
from types import StringTypes, StringType, UnicodeType
import codecs

def isStringTypes(value):
    """
    Check if input value is from type StringTypes Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return isinstance(value, StringTypes)

def isStringType(value):
    """
    Check if input value is from type StringType Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return isinstance(value, StringType)

def isUnicodeType(value):
    """
    Check if input value is from type StringType Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return isinstance(value, UnicodeType)

def convertToUnicode(value, encodingCode="iso-8859-15", errorsType="replace"):
    """
    Convert input value to unicode in Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    if isinstance(value, int) or isinstance(value, float):
        value = str(value)

    return unicode(value, encoding=encodingCode, errors=errorsType)


def d_(text):
    """
    Translate text and decode it with iso-8859-15 for Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return _(text).decode('iso-8859-15')


def decode8859_15(text):
    """
    Decode text with iso-8859-15 for Python 2.7
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return text.decode('iso-8859-15')


def encode8859_15(text):
    """
    Encodes a string with iso-8859-15 for Python 2.7 - string will be a byte string afterwards
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return text.encode('iso-8859-15', 'replace')


def replaceVisumSpecialCharacters(inString):
    """
    returns inString with replaced characters for $ and ;
    : is only needed to be replaced for attribute Ids - but here we have only values as inString
    """
    if isinstance(inString, str):
        resString = inString.replace("$", "$")
        resString = resString.replace(";", ",")
        #resString = resString.replace(":", "-")
    else:
        resString = inString.replace(u"$", u"§")
        resString = resString.replace(u";", u",")
        #resString = resString.replace(u":", u"-")
    return resString


def getUTF8Bom():
    """
    gets the BOM for UTF 8 file in correct coding
    (This function is used to make it possible to use the same AddIn code
    for Python 2.7 and Python 3.)
    """
    return unicode(codecs.BOM_UTF8, encoding="utf-8", errors="replace")


# Use getscriptdir if Visum has supplied it, otherwise fall back to previous
# logic that depended on the current working directory. This is required for
# AddIn Debug Mode (which runs outside of Visum).
if not hasattr(os, "getscriptdir"):
    os.getscriptdir = os.getcwd

class AddIn(object):
    """ Use this class in Code of VISUM AddIns. The main features are:
        - determines if an AddIn is executed in DebugMode (e.g. from Eclipse)
        - creates a VISUM instance if AddIn is executed in DebugMode
        - Installs Gettext translations
        - checks if the translation already got installed and prevents installing
          an AddIn translation twice (e.g. in Dialog and the same again in Body script)
        - Logging functionality (writing into VISUM logging and/or displaying an message box)
    """
    def __init__(self, VISUM = None, installTranslation = True, name = ""):
        self.State = AddInState.OK
        self.LanguageCode = LanguageCode.English
        self.Language = Language.English
        self.Name = name
        self.translation = None
        self.ErrorObjects = list()
        self.VISUM = VISUM
        self.InstallTranslation = installTranslation
        self.IsInDebugMode = self.__IsInDebugMode()
        if self.State == AddInState.OK:
            self.__Prepare()

        self.Embedded = self.VISUM.Embedded
        self.ProceduresIsExecuting = self.VISUM.Procedures.IsExecuting

        self.TemplateText = TemplateText(self.Language)
        self.__progressDialog = None
        self.ExecutionCanceled = False
        self.DirectoryPath = os.getscriptdir() + '\\'
        self.argvLen = 0

    def __del__(self):
        """destructor"""
        self.__logger.removeHandler(self.__VISUMLogHandler)


    def GetNetFileHeader(self,unit = 'KM'):
        """
        Generate the header of the visum net file
        """
        return '$VISION\n* PTVA INTERNAL\n* 10/29/13\n*\n* Table: Version block\n*\n$VERSION:VERSNR;FILETYPE;LANGUAGE;UNIT\n8.200;Net;ENG;%s\n\n' % unit

    def __IsInDebugMode(self):
        """ Checks if AddIn is in Debug Mode. This is done via command line arguments.
        In DebugMode there must be the command line arguments:
        1. 'Visum.Visum' (or any other VISUM installation e.g. 'Visum.Visum-32.1152')
        2. Full file path to a VISUM version file (this parameter is optional)
        """
        self.argvLen = len(sys.argv)

        if self.argvLen == 2 or self.argvLen == 3:
            return True
        elif self.argvLen == 1:
            return False

        self.ErrorObjects.append(ErrorObject(ErrorType.VISUM, "Invalid number of command line arguments. Please use this command line arguments [VisumVersion] and [Path to VISUM version file](optional)"))
        self.State = AddInState.Error
        return True

    def ClearErrors(self):
        """Removes all error objects from list """
        self.State = AddInState.OK
        self.ErrorObjects = list()


    def __Prepare(self):
        """ Functionality to initialize AddIn instance"""
        # Create VISUM Object if AddIn is in Debug-Modus
        if self.IsInDebugMode:
            try:
                self.VISUM = com.Dispatch(sys.argv[1]) #"Visum.Visum.115"
            except Exception, e:
                self.ErrorObjects.append(ErrorObject(ErrorType.VISUM, "CanŽt start VISUM. Error: " + str(e)))
                self.State = AddInState.Error
                return
        else:
            if self.VISUM is None:
                msg = "VISUM instance not available. AddIn must be started out of VISUM."
                self.ErrorObjects.append(ErrorObject(ErrorType.VISUM, msg))
                self.State = AddInState.Error
                return

        # Load VISUM Version if VISUM is in Debug-Modus
        if self.IsInDebugMode and len(sys.argv) == 3 and self.VISUM:
            try:
                self.VISUM.LoadVersion(sys.argv[2]) # *.ver file name
            except Exception, e:
                msg = "VISUM Version could not be loaded. Error: %s" %str(e)
                self.ErrorObjects.append(ErrorObject(ErrorType.VISUMVersion, msg))
                self.State = AddInState.Error
                return

        try:
            self.Language, self.LanguageCode = self.__GetLanguage()
        except Exception, e:
            self.Language = Language.English
            self.LanguageCode = LanguageCode.English
            msg = "Could not load language settings. Error: %s" %str(e)
            self.ErrorObjects.append(ErrorObject(ErrorType.Translation, msg))
            self.State = AddInState.Error
            return

        # Install gettext translations
        (dummy, folderName) = os.path.split(os.getscriptdir())
        localeFolderPath = os.getscriptdir() + os.sep + "locale"


        if self.InstallTranslation:
            if not self.__TranlationAlreadyInstalled(localeFolderPath):
                try:
                    '''
                    clear translation, old languages will be removed
                    (otherwise maybe the wrong language will be used)
                    '''
                    gettext._translations.clear()
                    gettext.install(folderName, localeFolderPath)
                    translation = gettext.translation(folderName, localeFolderPath, languages = [self.LanguageCode])
                    translation.install()
                except Exception, e:
                    msg ="Could not load translation files (gettext-files) from directory: %s. Error: %s" \
                          % (localeFolderPath, str(e))
                    self.ErrorObjects.append(ErrorObject(ErrorType.GetText, msg))
                    self.translation = None
                    self.State = AddInState.Error
                    return

        try:
            self.__VISUMLogHandler = LogHandler(VISUM = self.VISUM)
            self.__logger = logging.getLogger()
            self.__logger.addHandler(self.__VISUMLogHandler)
        except Exception, e:
            self.ErrorObjects.append(ErrorObject(ErrorType.Logging, str(e)))
            self.State = AddInState.Error

        if self.Name == "":
            self.Name = folderName

    def __TranlationAlreadyInstalled(self, localeFolderPath):
        """ Checks if a translation is installed"""
        pathToLanguageFolder = localeFolderPath + os.sep + self.LanguageCode
        for key, dummy in gettext._translations.iteritems():
            if key[1].lower().startswith(pathToLanguageFolder.lower()):
                return True
        return False

    def __GetLanguage(self):
        """ Reads the language from VISUM """
        languagemap = {"DEU":LanguageCode.German}
        # if language not available, use English
        code = languagemap.get(self.VISUM.GetCurrentLanguage(), LanguageCode.English)
        if code.lower() == LanguageCode.German:
            return Language.German, LanguageCode.German
        else:
            return Language.English, LanguageCode.English

    def ReportMessage(self, message, messageType = 1, captionText = None):
        """ Writes an error message into VISUM log or trace file (if AddIn is not executed from Script-Menu, otherwise
        a MessageBox is shown)"""
        if self.ProceduresIsExecuting == True and self.Embedded == True:
            # Extra case: AddIn is started not from Visum and runs as part of Procedure
            # show neither the messages or write the logs
            return

        if messageType == MessageType.Error:
            if self.ProceduresIsExecuting or self.Embedded:
                # AddIn is started not directly from Visum -> avoid message boxes
                self.WriteToVisumLog("AddIn %s: %s" % (self.Name, message), messageType)
            else:
                # Default case: AddIn is started directly from Visum
                if captionText is None:
                    if self.Language == Language.German:
                        captionText = "Fehler"
                    else:
                        captionText = "Error"
                wx.MessageBox(message, captionText, wx.OK | wx.ICON_ERROR)

        elif messageType == MessageType.Warning:
            if self.ProceduresIsExecuting or self.Embedded:
                self.WriteToVisumLog("AddIn %s: %s" % (self.Name, message), messageType)
            else:
                if captionText is None:
                    if self.Language == Language.German:
                        captionText = "Warnung"
                    else:
                        captionText = "Warning"
                wx.MessageBox(message, captionText, wx.OK | wx.ICON_EXCLAMATION)

        else:
            if self.ProceduresIsExecuting or self.Embedded:
                self.WriteToVisumLog("AddIn %s: %s" % (self.Name, message), messageType)
            else:
                wx.MessageBox(message, "Info", wx.OK | wx.ICON_INFORMATION)

    def GetAddInLanguage(self):
        """
        Get the Add-In language
        """
        return self.Language

    def HandleException(self, prefixText = ""):
        """
        Handle the exception
        Arguments: the prefix text
        """
        try:
            # First close progress dialog
            self.CloseProgressDialog()
            if isinstance(prefixText, str):
                prefixText = prefixText.decode('iso-8859-15')

            if self.Language == Language.German:
                moreInfoText = u"Weitere Informationen könnten Sie im Fenster 'Meldungen' finden."
            else:
                moreInfoText = u"You might find more information in the window 'Messages'."

            addInException = AddInException(3, self.Language)
            msg = "%s%s\n%s" % (prefixText, addInException.Text, moreInfoText)
            self.ReportMessage(msg, MessageType.Error, addInException.Name)
        except Exception, e:
            self.ReportMessage(str(e))

    # The function WriteToTraceFile and WriteToErrorFile
    # would be replaced with function WriteToVisumLog.
    def WriteToTraceFile(self, message):
        """ Writes a message into VISUM trace file"""
        self.WriteToVisumLog(message, MessageType.Warning)

    def WriteToErrorFile(self, message):
        """ Writes a message into VISUM error file"""
        self.WriteToVisumLog(message, MessageType.Error)

    def WriteToVisumLog(self, message, messageType = 1):
        """ Writes a message into VISUM logging"""
        try:
            if messageType == MessageType.Error:
                self.VISUM.PostFailure(message)
            elif messageType == MessageType.Warning:
                self.VISUM.Log(MessagePriority.Warning, message)
            else:
                self.VISUM.Log(MessagePriority.Info, message)

        except Exception:
            pass


    def ShowProgressDialog(self, captionText, infoText, maxCounter, setTimeMode = False):
        """
        Progress dialog can not be used out of procedures. VISUM procedures are executed modal,
        so clicking the cancel button of
        progress dialog will have no effect
        """
        if not self.VISUM.Procedures.IsExecuting:
            if setTimeMode:
                self.__progressDialog = wx.ProgressDialog(captionText, infoText, maxCounter,
                                         style = wx.PD_CAN_ABORT |
                                         wx.PD_ELAPSED_TIME |
                                         wx.PD_REMAINING_TIME |
                                         wx.PD_AUTO_HIDE)
            else:
                self.__progressDialog = wx.ProgressDialog(captionText, infoText, maxCounter,
                                          style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE)
    def CloseProgressDialog(self):
        """
        Closes the progress dialog
        """
        if self.__progressDialog is not None:
            self.__progressDialog.Destroy()
            self.__progressDialog = None

    def UpdateProgressDialog(self, counter, messageText = None):
        """
        Update the progress dialog
        Arguments: A counter,
                   the message text
        """
        if not self.VISUM.Procedures.IsExecuting:
            if self.__progressDialog is None and not self.ExecutionCanceled:
                if self.Language == Language.German:
                    self.ReportMessage("Der ProgressDialog wurde nicht initialisiert, "
                                       "aus diesem Grund kann 'ProgressDialog.Update(counter)' nicht ausgeführt "
                                       "werden. Bitte initialisieren Sie den ProgressDialog durch den Aufruf "
                                       "der Funktion 'AddIn.ShowProgressDialog(captionText, infoText, maxCounter)'.")
                else:
                    self.ReportMessage("ProgressDialog not initialized, for this 'ProgressDialog.Update' "
                                       "can not be executed. Please initialize the ProgressDialog via calling "
                                       "the function ''AddIn.ShowProgressDialog(captionText, infoText, maxCounter)'.")
            elif self.__progressDialog is None and self.ExecutionCanceled:
                return
            else:
                if messageText is None:
                    self.ExecutionCanceled = (self.__progressDialog.Update(counter)[0] == False)
                else:
                    self.ExecutionCanceled = (self.__progressDialog.Update(counter, messageText)[0] == False)
                if self.ExecutionCanceled:
                    self.__progressDialog.Destroy()
                    self.__progressDialog = None


    @staticmethod
    def GetVisumObjectAttributeIds(visumContainer):
        """
        Get all attribute ids from a Visum object
        :param visumContainer: Com object from the Visum object
        :return: list with the attribute Ids
        """
        attrIdList = list()
        if visumContainer:
            attributes = visumContainer.Attributes.GetAll
            for attribute in attributes:
                attrIdList.append(attribute.ID)

        return attrIdList


    @staticmethod
    def ContainsAttribute(visumContainer, attributeId):
        """
        get all attribute Ids from COM container, compare them to the given attributeId
        :param visumContainer: Com object from the Visum object
        :param attributeId: string as attribute ID to be searched for
        :return: if same attributeId exists -> return true, else: false
        """
        attrIdList = AddIn.GetVisumObjectAttributeIds(visumContainer)
        for existingAttrId in attrIdList:
            if existingAttrId == attributeId:
                return True

        return False


    def VersionContainsValidMatrix(self):
        """
        Checks if version (the VISUM net) contains at least one data matrix.
        If itŽs a zone matrix there also must be at least
        one zone and if itŽs a mainzone matrix there must be at least one main zone.
        Reports message to user if not such a matrix exists.
        """
        # Check if a data matrix exists
        typeValues = self.VISUM.Net.Matrices.GetMultiAttValues("DataSourceType", False)
        valid = False
        if len(typeValues) > 0:
            for typeVal in typeValues:
                if typeVal[1] == "DATA":
                    valid = True
                    break

        if self.Name != "":
            nameText = "AddIn '%s'" % self.Name
        else:
            nameText = "AddIn"

        if not valid:
            if self.LanguageCode == LanguageCode.German:
                self.ReportMessage("Die VISUM Version enthält keine Matrizen. "
                                   "Bitte legen Sie zuerst eine Datenmatrix an und starten Sie das %s erneut."
                                   .decode('iso-8859-15') % nameText)
            else:
                self.ReportMessage("The VISUM Version contains no matrices. "
                                   "Please create a data matrix first and restart the %s.".decode('iso-8859-15')
                                   % nameText)
            return False

        # At least one data matrix exists. Now check if itŽs a zone or a main zone matrix and
        # if a zone or main zone exists
        zonesCount = self.VISUM.Net.Zones.Count
        mainZonesCount = self.VISUM.Net.MainZones.Count
        checkZones = False
        checkMainZones = False
        # if zones and main zones exists this means that all matrices (zone matrices and main zone matrices)
        # do have rows and columns
        if zonesCount > 0 and mainZonesCount > 0:
            return True
        elif zonesCount == 0 and mainZonesCount == 0:
            if self.LanguageCode == LanguageCode.German:
                self.ReportMessage("Die VISUM Version enthält Bezirks- oder Oberbezirksmatrizen jedoch keinen Bezirk "
                                   "und Oberbezirk. Bitte legen Sie zuerst einen Bezirk oder einen Oberbezirk an und "
                                   "starten Sie das %s erneut.".decode('iso-8859-15') % nameText)
            else:
                self.ReportMessage("The VISUM Version contains zone or main zone matrices but no zone or mainzone. "
                                   "Please create a zone or mainzone and restart the %s.".decode('iso-8859-15')
                                   % nameText)
            return False
        elif zonesCount == 0:
            checkMainZones = True
        else:
            checkZones = True

        for matObject in self.VISUM.Net.Matrices:
            if matObject.AttValue("ObjectTypeRef") == 'OBJECTTYPEREF_MAINZONE' and checkMainZones:
                return True
            elif matObject.AttValue("ObjectTypeRef") == 'OBJECTTYPEREF_ZONE' and checkZones:
                return True

        if checkMainZones:
            if self.LanguageCode == LanguageCode.German:
                self.ReportMessage("Die VISUM Version enthält Bezirksmatrizen jedoch keinen Bezirk. Bitte legen "
                                   "Sie zuerst einen Bezirk an und starten "
                                   "Sie das %s erneut.".decode('iso-8859-15') % nameText)
            else:
                self.ReportMessage("The VISUM Version contains zone matrices but no zone. "
                                   "Please create a zone and restart the %s.".decode('iso-8859-15') % nameText)
        else:
            if self.LanguageCode == LanguageCode.German:
                self.ReportMessage("Die VISUM Version enthält Oberbezirksmatrizen jedoch keinen Oberbezirk. "
                                   "Bitte legen Sie zuerst einen Oberbezirk an und starten Sie das %s erneut."
                                   .decode('iso-8859-15') % nameText)
            else:
                self.ReportMessage("The VISUM Version contains main zone matrices but no mainzone. "
                                   "Please create a mainzone and restart the %s.".decode('iso-8859-15') % nameText)

        return False

    def MatchMatrixTypeStringToIntValue(self, matrixTypeString):
        """
        Match the string of the matrix attribute matrix type to the integer value
        Arguments: The string of the matrix type attribute
        Returns: None or the integer value of the matrix type attribute
        """
        matrixTypes = {
                        "MATRIXTYPE_ANY": 2,
                        "MATRIXTYPE_DEMAND": 3,
                        "MatrixType_End": 5,
                        "MATRIXTYPE_INVALID": 0,
                        "MATRIXTYPE_NONE": 1,
                        "MATRIXTYPE_SKIM": 4
                      }

        return matrixTypes.get(matrixTypeString)

    def MatchMatrixTypeIntValueToString(self, matrixTypeValue):
        """
        Match the value of the matrix attribute matrix type to the string
        Arguments: The string of the matrix type attribute
        Returns: None or the string of the matrix type attribute
        """
        matrixTypes = {
                        2: "MATRIXTYPE_ANY",
                        3: "MATRIXTYPE_DEMAND",
                        5: "MatrixType_End",
                        0:"MATRIXTYPE_INVALID",
                        1: "MATRIXTYPE_NONE",
                        4: "MATRIXTYPE_SKIM"
                      }

        return matrixTypes.get(matrixTypeValue)

class AddInParameter(object):
    """Class holding methods and values of VISUM parameter"""
    def __init__(self, addIn, visumParameter):
        self.Dependencies = {}
        self.addIn = addIn
        self.visumParameter = visumParameter
        self.__visumProjectPaths = dict()

    def GetVisumProjectPath(self, visumProjectFileType):
        """ Get the Visum project path an save them in a dictionary"""
        projectPath = ""
        try:
            projectPath = self.__visumProjectPaths.get(visumProjectFileType)
            if projectPath is None:
                projectPath = self.addIn.VISUM.GetPath(visumProjectFileType)
                self.__visumProjectPaths[visumProjectFileType] = projectPath
            return projectPath
        except:
            return projectPath

    def AddDependency(self, originAttribute, dependentAttribute, checkValue):
        """
        Add the dependency from the parameters
        Arguments: the origin attribute
                   the dependent attribute
                   the check value
        """
        dependentFilter = {dependentAttribute: checkValue}
        self.Dependencies[originAttribute] = dependentFilter

    def SaveParameter(self, param):
        """
        Save the Add-In parameters as Visum parameters
        Arguments: the Add-In parameters
        """
        if not self.addIn.IsInDebugMode:
            self.visumParameter.Data = dumps(param).decode("iso-8859-15")
            self.visumParameter.OK = True

    def Check(self, isBody, defaultParameter = None):
        """
        Check the Add-In parameter
        Arguments: Call the check fom body or from dialog
                   the default parameter from the Add-In
        returns: The valid Add-In parameter or throw an exception
        """
        param = defaultParameter
        if not self.addIn.IsInDebugMode:
            if self.visumParameter is not None and self.visumParameter.Data != "":
                tmppara = self.visumParameter.Data.encode("iso-8859-15")
                storedparam = loads(tmppara)
                param.update(storedparam)
            elif isBody:
                msg = ""
                if self.addIn.Language == Language.German:
                    msg = u"%s %s" %("Es wurden keine Add In Parameter gefunden.",
                                    "Bitte definieren Sie die Parameter bevor Sie das Add In ausführen.")
                else:
                    msg = u"No add-in parameters found. Please define parameters before usage."
                raise Exception(msg)

        if param is None or (len(param) == 0 and isBody == True):
            msg = ""
            if self.addIn.Language == Language.German:
                msg = u"%s %s" %("Es wurden keine Add In Parameter gefunden.",
                                 "Bitte definieren Sie die Parameter bevor Sie das Add In ausführen.")
            else:
                msg = u"No add-in parameters found. Please define parameters before usage."
            raise Exception(msg)

        errStr = ""
        for paramId in param:
            if param[paramId] is None:
                if not self.__checkDependencies(paramId, param):
                    errStr = self.__createCheckResultText(errStr, paramId)
            elif isinstance(param[paramId], str) or isinstance(param[paramId], unicode):
                if param[paramId] == "" or param[paramId] == "...":
                    if not self.__checkDependencies(paramId, param):
                        errStr = self.__createCheckResultText(errStr, paramId)
        if errStr != "":
            if isBody:
                msg = ""
                if self.addIn.Language == Language.German:
                    msg = u"Die folgenden AddIn-Parameter haben keinen Wert: "
                    msg = u"%s'%s'. Bitte geben Sie einen Wert für die Parameter an." % (msg, errStr)
                else:
                    msg = u"The following add-in parameter/s have no value: "
                    msg = u"%s'%s'. Please define the value for those parameter/s before usage." % (msg, errStr)
                raise Exception(msg)

        return param


    def GetRelativPath(self, absolutePath, visumProjectFileType):
        """
        The function returns relative path representation.
        The calculated path is relative to the project directory of the given
        project type.

        Return:
            If the path starts withe the project directory belonging to the
            given file type, the relative representation of this path
            is returned ('.'). In other case, the given input path is returned.
        """
        try:
            if not absolutePath:
                return ""

            projectPath = os.path.normpath(self.GetVisumProjectPath(visumProjectFileType))
            absPath = os.path.normpath(absolutePath)

            # replace project path to '.', so if you are in the project path directly,
            # you will get a valid relative path - '.'
            relPath = absPath.replace(projectPath, ".\\")

            # second normalize path call to cut '.\'
            # '.\abc'  ->  'abc'
            return os.path.normpath(relPath)
        except Exception:
            return absolutePath


    def GetDefaultDirectoryPath(self, inputFile, visumProjectFileType):
        """
        The function returns a checked, normalized (absolute) path, if it exists,
        or the default directory path for the given file type.

        The function works with the
         - project directory - default path of the VISUM project file type
         - input file - relative or absolute file path.

        The function calculates the absolute path out of project and input path.

        Return calculated path, if it exists. In all other cases, the function
        returns project directory.
        Note: The returned path is always absolute.

        Parameter:
            inputFile:  file or directory path
            visumProjectFileType: Visum file type, see COM documentation
        """
        projectPath = self.GetVisumProjectPath(visumProjectFileType)

        try:
            norm_path = self.__getNormAbsPath(projectPath, inputFile)
            file_ext = os.path.splitext(norm_path)[1]

            # get the directory path
            if os.path.isfile(norm_path) or file_ext != '':
                norm_path = os.path.split(norm_path)[0]

            # if resulted path is a valid, return this path,
            # else return default path
            if os.path.exists(norm_path):
                return norm_path
            else:
                return projectPath

        except Exception:
            return projectPath

    def GetAndCheckPathAndFileName(self, inputFile, visumProjectFileType, allowedFileTypes = None):
        """
        The function validates the input file path.
        The check order is:
         - Directory path exists.
         - File type - file extension is in allowed file types.
           All types are allowed, if the allowed types list is not specified.
         - File exists.

        If one of the steps fails, the corresponding CheckPathMessageType
        is returned.

        Return:
            CheckPathResult object, containing the CheckPathMessageType and
            the generated absolute path.

        Parameter:
            inputFile: path to file
            visumProjectFileType: see COM documentation
            allowedFileTypes: optional, string with list of allowed file extensions
        """
        projectPath = self.GetVisumProjectPath(visumProjectFileType)

        if not inputFile:
            return CheckPathResult(CheckPathMessageType.PathError, "")

        abs_path = self.__getNormAbsPath(projectPath, inputFile)
        file_ext = os.path.splitext(abs_path)[1]

        # extruct the directory path
        if os.path.isfile(abs_path) or file_ext != '':
            dir_path = os.path.split(abs_path)[0]
        else:
            dir_path = abs_path

        # check if directory path exists
        if not os.path.exists(dir_path):
            return CheckPathResult(CheckPathMessageType.PathError, abs_path)

        # check the file type
        if allowedFileTypes:
            extensions = re.findall("\.[A-Za-z]+", allowedFileTypes)
            if file_ext not in extensions:
                return CheckPathResult(CheckPathMessageType.FileTypeError, abs_path)

        # check if path is a file path and if it exists
        if not os.path.isfile(abs_path):
            return CheckPathResult(CheckPathMessageType.FileError, abs_path)

        return CheckPathResult(CheckPathMessageType.OK, abs_path)

    @classmethod
    def CreatePathDirectories(cls, path):
        """
        Check, if path exists and create all missed directories in the path.
        """
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def __getNormAbsPath(self, basisPath, inputPath):
        """
        The function return normalized, absolute path.
        If input path is relative, the function joints basis and input path
        together.

        Absolute path:
        starts with (back)slash or drive letter
        'C:\\', '\\', '/', '\\\\' Network Path

        Relative path:
        starts with directory/file name, './' or '../'
        './../', '../../'
        """
        # strip the spaces
        inPath = inputPath.strip()

        # create absolute path - join input path with basis path
        concatPath = os.path.join(basisPath, inPath)

        # normalize path (separators, remove '../v.'-parts )
        return os.path.normpath(concatPath)


    def __checkDependencies(self, paramId, values):
        """
        Check the allowed values of dependencies Add-In parameters
        Arguments: ID of the Add-In Parameter
                   The allowed values of the Add-In parameter
        Returns: True or False
        ''"""
        if len(self.Dependencies) == 0:
            return False
        if not paramId in self.Dependencies:
            return False
        else:

            for depValue in self.Dependencies[paramId]:
                if not depValue in values:
                    return False
                else:
                    try:
                        if self.Dependencies[paramId][depValue] != values[depValue]:
                            return False
                    except:
                        return False

        return True

    def __createCheckResultText(self, errStr, attrString):
        """
        Create the check error text
        Arguments: Error text
                   the attribute string
        Returns:Error text
        """
        if errStr == "":
            errStr = attrString
        else:
            errStr = errStr + ", " + attrString
        return  errStr


class ErrorObject(object):
    """
    Class holding further information about an error
    """
    def __init__(self, errorType, errorMessage):
        self.ErrorType = errorType
        self.ErrorMessage = errorMessage

class AddInState(object):
    """ Enum object application state"""
    OK = 0
    Warning = 1
    Error = 2

class MessageType(object):
    """ Enum object message type"""
    Warning = 0
    Error = 1
    Info = 2

class MessagePriority(object):
    """ Enum object message type"""
    Warning = 16384
    Error = 12288
    Info = 20480
    Debug = 28672

class ErrorType(object):
    """ Enum object error type """
    GetText = 0
    VISUM = 1
    VISUMVersion = 2
    Logging = 3
    Translation = 4

class Language(object):
    """ Enum object language """
    English = 0
    German = 1

class LanguageCode(object):
    """ Enum object language code """
    English = "en_us"
    German = "de_de"

class CheckPathMessageType(object):
    """Enum object File error type"""
    OK = 0
    PathError = 1
    FileTypeError = 2
    FileError = 3

class CheckPathResult(object):
    """The class encapsulates the results of the file path valitation."""
    def __init__(self, checkPathMessageType, abs_path):
        self.checkPathMessageType = checkPathMessageType
        self.absolutePath = abs_path

    def IsOK(self):
        """
        Is the path message type correct
        Returns: True or False
        """
        return self.checkPathMessageType == CheckPathMessageType.OK

    def IsPathError(self):
        """
        Is the path correct
        Returns: True or False
        """
        return self.checkPathMessageType == CheckPathMessageType.PathError

    def IsFileTypeError(self):
        """
        Is the file type correct
        Returns: True or False
        """
        return self.checkPathMessageType == CheckPathMessageType.FileTypeError

    def IsFileError(self):
        """
        Is the file correct
        Returns: True or False
        """
        return self.checkPathMessageType == CheckPathMessageType.FileError

class LogHandler(logging.Handler):
    """Logging-handler which writes to the VISUM trace or orror file"""
    def __init__(self, VISUM = None, level = logging.INFO):
        logging.Handler.__init__(self)
        if VISUM is not None:
            self.visumInst = VISUM
        else:
            try:
                self.visumInst = Visum
            except NameError:
                raise StandardError, "No VISUM instance given/found. Can't set up logging"
        self.setLevel(level)

    def emit(self, record):
        if record.levelno == logging.INFO:
            self.visumInst.Log(MessagePriority.Info,record.getMessage())
        elif record.levelno == logging.WARNING or record.levelno == logging.WARN:
            self.visumInst.Log(MessagePriority.Warning,record.getMessage())
        elif record.levelno == logging.DEBUG:
            self.visumInst.Log(MessagePriority.Debug,record.getMessage())
        else:
            self.visumInst.PostFailure(record.getMessage())


class TemplateText(object):
    """
    Class for the creating a tmplate text
    """
    def __init__(self, language = Language.English):
        self.Language = language

    def __get_mainApplicationError(self):
        if self.Language == Language.German:
            return u"Es kam zu einem Fehler in der Hauptanwendung des AddIns: "
        else:
            return u"An Error in the main application of the AddIn occurred: "

    MainApplicationError = property(__get_mainApplicationError)


class AddInException(Exception):
    """
    Class of the Add-In exceptuions
    """
    def __init__(self, textSearchLevel = 3, language = Language.English):

        self.TextSearchLevel = textSearchLevel
        self.Language = language
        try:
            self.__Prepare()
        except Exception:
            if self.Language == Language.German:
                self.Name = u"Unbekannter Fehler"
                self.Text = u"Der Fehlertext kann nicht ausgelesen werden."
            else:
                self.Name = u"Unspecific Error"
                self.Text = u"The error text can not be read."

    def __Prepare(self):
        """
        Prepare
        """
        exeptionType, exceptionArgs = sys.exc_info()[:2]

        # if the exception was throws via: raise "Some exception text"
        # the exceptionArgs is None and the text "Some exception text" is stored into the name of the exception-object
        if (isinstance(exeptionType, str) or isinstance(exeptionType, unicode)) and exceptionArgs is None:
            self.Text = exeptionType
            self.Name = ""  # will be set to default value in code lines below
        else: # there exists an exception object with args and exception name
            self.Text = self.__getExceptionText(exceptionArgs, 0)
            try:
                exceptionName = exeptionType.__name__
            except:
                exceptionName = "" # will be set to default value in code lines below
            self.Name = exceptionName

        if self.Name is None or self.Name.strip() == "":
            if self.Language == Language.German:
                self.Name = u"Fehler"
            else:
                self.Name = u"Error"
        else:
            if isinstance(self.Name, str):
                self.Name = self.Name.decode('iso-8859-15')

        if self.Text is None or self.Text.strip() == "":
            if self.Language == Language.German:
                self.Text = u"Es ist kein Fehlertext verfügbar."
            else:
                self.Text = u"No error text available."
        elif isinstance(self.Text, str):
            self.Text = self.Text.decode('iso-8859-15')


    def __getExceptionText(self, exceptionText, currentSearchLevel):
        """
        Get the text of the exception
        Arguments: The text of the exception
                   the current search level
        Returns: text of the exception
        """
        unicodeText = u""
        stringText = ""
        textFromNextLevel = ""
        if exceptionText is None or currentSearchLevel >= self.TextSearchLevel:
            return unicodeText

        for exText in exceptionText:
            if isinstance(exText, unicode):
                unicodeText += " " + exText
            elif isinstance(exText, str):
                stringText += " " + exText
            else:
                try:
                    tupleLength = len(exText)
                    if tupleLength > 0:
                        textFromNextLevel += " " + self.__getExceptionText(exText, currentSearchLevel + 1)
                except:
                    continue
        if unicodeText.strip() != "":
            return unicodeText.strip() + u" " + textFromNextLevel.strip()
        elif stringText.strip() != "":
            return stringText.strip() + " " + textFromNextLevel.strip()
        else:
            textFromNextLevel.strip()

