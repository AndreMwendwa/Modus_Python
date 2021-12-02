# -*- coding: iso-8859-15 -*-
"""
 Contains helper functions to change the python system path
"""

import sys
import os
import _winreg

def __CloseRegistryKey(registryKey):
    if registryKey != None:
        try:
            _winreg.CloseKey(registryKey)
        except:
            return

def __GetEnumValueRegistry32_64(keyStr, registryKey):
    reg = None
    try:
        reg = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, keyStr, 0, registryKey)
        if reg != None:
            value = _winreg.EnumValue(reg, 0)
            return value[1]
        else:
            return False
    except:
        return False
    finally:
        __CloseRegistryKey(reg)

def __GetEnumValue(keyStr, index):
    reg = None
    try:
        reg = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, keyStr)
        if reg != None:
            value = _winreg.EnumValue(reg, index)
            return value[1]
        else:
            return False
    except:
        return False
    finally:
        __CloseRegistryKey(reg)

def __GetVISUMPath(clsid, bit):
    if clsid != False:
        if bit == "32":
            path = __GetEnumValueRegistry32_64('CLSID\\' + clsid + '\\LocalServer32', 0x0201)
        elif bit == "64":
            path = __GetEnumValueRegistry32_64('CLSID\\' + clsid + '\\LocalServer32', 0x0101)
        else:
            return False

        if len(path) > 0:
            path = str(path).strip('"')
            index = str(path).rfind('\\')
            return path[0:index]
        else:
            return False
    else:
        return False

def __CheckPythonPath(pathList):
    for path in pathList:
        if os.path.exists(path) == False:
            return False

    return True

def __GetPythonPathList(VISUMPath):
    PythonModulesPath = VISUMPath + "\\Python27Modules\\Lib\\site-packages"
    
    pathList = []
    pathList.append(PythonModulesPath)
    pathList.append(PythonModulesPath + "\\matplotlib")
    pathList.append(PythonModulesPath + "\\osgeo")
    pathList.append(PythonModulesPath + "\\pyproj")
    pathList.append(PythonModulesPath + "\\VisumPy")
    return pathList

def __SetSysPath(pathList):
    for i in range(len(pathList)):
        path = pathList[i]
        sys.path.insert(i, path)

def ChangePythonSysPath(visum, bit):
    """Inserts all directories below 'PythonModules' of the specified Visum version at the beginning of the Windows system path variable.
    Already existent entries are not changed.

    visum - The number of the Visum version (e.g. 170 or 160)
    bit - The number of the bit version (e.g. 32 or 64)

    return - true or false
    """
    try:
        key = "Visum.Visum-" + bit + "." + visum
        clsid = __GetEnumValue(key + '\\CLSID', 0)
        if clsid != False:
            VISUMPath = __GetVISUMPath(clsid, bit)
            if VISUMPath != False:
                pathList = __GetPythonPathList(VISUMPath)
                if __CheckPythonPath(pathList) == True:
                    __SetSysPath(pathList)
                    return True
                else:
                    return False

        return False
    except:
        return False