import win32com.client as win32
import Data.VisumPy.helpers as helpers
from Data import CstesStruct
from Data.CstesStruct import *
from Data.A_CstesModus import *
import multiprocessing
import numpy as np
from collections import defaultdict


result = defaultdict(np.ndarray)

def affect(ver, matVP, matPL, result):
    myvisum = win32.Dispatch("Visum.Visum")
    myvisum.LoadVersion(ver)
    helpers.SetODMatrix(myvisum, 'V', matVP)
    helpers.SetODMatrix(myvisum, 'P', matPL)
    myvisum.procedures.Execute()
    mat1 = helpers.GetSkimMatrix(myvisum, 'V')
    result[ver] = mat1
    myvisum = None


# # This is to test the route assignment code above.
myvisum = win32.Dispatch("Visum.Visum")
myvisum.LoadVersion(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver')

mat1 = helpers.GetODMatrix(myvisum, 'V')
mat2 = helpers.GetODMatrix(myvisum, 'P')
matrand = np.abs(np.random.randn(1327, 1327))
matVP = mat1 + matrand
matPL = mat2 + matrand
myvisum = None
# myvisum.procedures.Execute()

# mat1 = affect(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver', matVP, matPL)

if __name__ == '__main__':

    mat1 = multiprocessing.Process(name='mat1', target=affect,
                                   args=(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver', matVP, matPL, result))
    mat2 = multiprocessing.Process(name='mat2', target=affect,
                                   args=(dir_dataScen + '\\210219_ReseauVPv4.6_PPS2030_edited.ver', matVP, matPL, result))
    mat1.start()
    mat2.start()


