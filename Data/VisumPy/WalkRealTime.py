# -*- coding: iso-8859-15 -*-
"""
Contains a class for the setting the walk real time of links
"""
class WalkRealTimeDefaultSetting(object):
    """
    The class include functions for
    the setting the walk real time of links
    """
    def __init__(self,addin,linkType = 99):
        """
        Constructor
        """
        self.__addIn = addin
        self.__linkType = linkType
        self.__TSysWalkCode = "" 


    def __getDefaultWalkVelocity(self):
        """
        Get the default walk velocity for a link type
        Return Default walk velocity
        """
        try:
            defaultWalkVelocity = float(self.__addIn.VISUM.Net.LinkTypes.ItemByKey(self.__linkType).AttValue("VDef_PUTSys(%s)" %self.__TSysWalkCode))
            if defaultWalkVelocity == 0.0:
                defaultWalkVelocity = 4.0
            return defaultWalkVelocity
        except:
            return 4.0


    def __getLinkLengthPoly(self):
        """
        Get the poly link length
        Return a list of poly link length
        """
        return self.__addIn.VISUM.Net.Links.GetMultiAttValues("LENGTHPOLY",True)


    def __calculateWalkRealTime(self,linkPolyLengthList):
        """
        Calculate the walk real time
        Argument: linkPolyLengthList List of poly link length
        Return a list of walk real times in sec.
        """
        resList =[]
        defaultWalkVelocity = self.__getDefaultWalkVelocity()
        for link in linkPolyLengthList:
            resList.append((link[0],float(link[1]) / defaultWalkVelocity * 3600))
        return resList


    def setWalkRealTime(self):
        """
        Set the walk real time
        """
        try:
            if not self.__getTSysCodeWalk():
                return False
            linkAttrList = self.__getLinkLengthPoly()
            linkAttrList = self.__calculateWalkRealTime(linkAttrList)
            self.__addIn.VISUM.Net.Links.SetMultiAttValues("T_PUTSYS(%s)" %self.__TSysWalkCode,linkAttrList,False)
            return True
        except:
            return False

    def __getTSysCodeWalk(self):
        """
        Get the tsys code for walk
        """
        try:
            for tsys in self.__addIn.VISUM.Net.TSystems:
                if tsys.AttValue("TYPE") == "PUTWALK":
                    self.__TSysWalkCode = tsys.AttValue("CODE")
                    return True       
            return False
        except:
            return False

