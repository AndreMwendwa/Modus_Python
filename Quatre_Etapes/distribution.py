

import numpy as np
from numba import jit
import pandas as pd
from collections import defaultdict
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes import generation
from Quatre_Etapes import utility
from Exec_Modus import *

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *
from Data.distribution_data import dist_data


def distribution(n, hor):
    dist_data_instance = dist_data()
    dist_data_instance.per = hor

    DIST_PAR = dist_data_instance.DIST_PAR_FUNC().to_numpy()

    EM, ATT = generation.generation(n, hor)
    UTM ,UTMD = utility.utilite(n, hor)

    UTMD_arr = UTMD.to_numpy().astype(np.float64)




    # @jit(nopython=True)
    def distrib(vEM, vATT, UTIL, a):

        # - a. modèle gravitaire

        M = vEM @ vATT * np.exp(a[2]*UTIL) * (-UTIL)**a[3] * np.ones((1289, 1289))

        # - b.fratar

        iteration = 0
        RMSE = precRMSE

        # rowPos = M.sum(1) > 0
        #
        # colPos = M.sum(0) > 0

        while (iteration < cMaxIterDist and RMSE >= precRMSE):

            Computed_Prod = M.sum(1)
            Computed_Prod[Computed_Prod == 0] = 1
            Orig_Fac = vEM.T/Computed_Prod
            M = M * Orig_Fac.T


            Computed_ATT = M.sum(0)
            Computed_ATT[Computed_ATT == 0] = 1
            Dest_Fac = vATT/Computed_ATT
            M *= Dest_Fac

            # for i in range(len(rowPos)):
            #     if rowPos[i]:
            #         M[i, :] *= vEM[i, :]/M[i, :].sum()
            # # équilibrage en émission sur les lignes non nulles
            # for j in range(len(colPos)):
            #     if colPos[j]:
            #         M[:, j] *= vATT[:, j]/M[:, j].sum()
            # # équilibrage en attraction sur les colonnes non nulles

            RMSE = (np.sqrt(((M.sum(1) - vEM.T)**2).sum()))/(cNbZone - 1)
            iteration = iteration + 1

        return M

    Modus_motcat = np.zeros((cNbZone**2, cNbMotifD*cNbCat))

    # @jit(nopython=True)
    def dist_calc(Modus_motcat):
        for iCat in range(cNbCat):
            for iMotif in range(cNbMotifD):

                id = (iCat)*cNbMotifD + iMotif

                # - a. matrices utilisées
                vPAR = DIST_PAR[id, :]
                vEM = EM[:, id].copy()
                vEM = vEM.reshape(1289, 1)
                vATT = ATT[:, id].copy()
                vATT = vATT.reshape(1, 1289)
                vUTM = UTMD_arr[:, id].copy()
                vUTM = vUTM.reshape(cNbZone, cNbZone, order='C')

                Modus_motcat[:, id] = distrib(vEM, vATT, vUTM, vPAR).reshape((cNbZone ** 2, ))





# Kiko : After this, delete
((np.round(M.sum(1), 0) - np.round(vEM.T, 0))==0).sum()