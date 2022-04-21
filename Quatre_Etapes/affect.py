import win32com.client as win32
import Data.VisumPy.helpers2 as helpers
from Data.A_CstesModus import *
import multiprocessing
import os
import pickle as pkl
# from dossiers_simul import *

from Quatre_Etapes.dossiers_simul import *


def affect(ver, matVP, Iter, H, dir_itern):
    myvisum = win32.Dispatch("Visum.Visum")
    myvisum.LoadVersion(ver)
    helpers.SetODMatrix(myvisum, 'V', matVP)
    myvisum.procedures.Execute()
    mat1 = helpers.GetSkimMatrix(myvisum, 'V', 'V')
    matT = helpers.GetSkimMatrix(myvisum, 'TpsCh', 'V')

    dbfile = open(f'{dir_dataTemp}TV_{H}_scen', 'wb')
    pkl.dump(matT, dbfile)
    dbfile.close()

    # # Kiko - ce que j'ai fait n'a pas de sens, puisque VISUM ne change pas la matrice de demande pendant l'étape.
    # dbfile = open(f'{dir_dataTemp}ModusUVPcarre_{H}_scen', 'wb')
    # pkl.dump(mat1, dbfile)
    # dbfile.close()

    dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen_prec', 'wb')
    pkl.dump(matVP, dbfile)
    dbfile.close()

    myvisum.SaveVersion(os.path.join(dir_itern, f'Vers{H}_scen_iter{Iter}.ver'))
    myvisum = None

    dbfile = open(f'{dir_dataTemp}done_affect{Iter}', 'rb')
    done_affect = pkl.load(dbfile)
    done_affect += 1
    dbfile = open(f'{dir_dataTemp}done_affect{Iter}', 'wb')
    pkl.dump(done_affect, dbfile)
    dbfile.close()
    print(f'Affectation terminé pour {H}')
    return mat1

# # # This is to test the route assignment code above.
# myvisum = win32.Dispatch("Visum.Visum")
# myvisum.LoadVersion(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver')
#
# mat1 = helpers.GetODMatrix(myvisum, 'V')
# mat2 = helpers.GetODMatrix(myvisum, 'P')
# matrand = np.abs(np.random.randn(1327, 1327))
# matVP = mat1 + matrand
# matPL = mat2 + matrand
# myvisum = None
# # myvisum.procedures.Execute()

# mat1 = affect(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver', matVP, matPL)

if __name__ == '__main__':

    mat1 = multiprocessing.Process(name='mat1', target=affect,
                                   args=(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030_editedb.ver', matVP, matPL, result))
    mat2 = multiprocessing.Process(name='mat2', target=affect,
                                   args=(dir_dataScen + '\\210219_ReseauVPv4.6_PPS2030_edited.ver', matVP, matPL, result))
    mat1.start()
    mat2.start()


