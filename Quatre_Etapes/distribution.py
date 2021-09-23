import numpy as np
import pandas as pd
from collections import defaultdict
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes import generation
from Quatre_Etapes import utility
from Data.distribution_data import dist_data

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *

dbfile = open(f'{dir_dataTemp}params_user', 'rb')
params_user = pkl.load(dbfile)

def distribution(n, hor):
    dist_data_instance = dist_data()
    dist_data_instance.per = hor

    DIST_PAR = dist_data_instance.DIST_PAR_FUNC().to_numpy()

    EM, ATT = generation.generation(n, hor)

    UTM ,UTMD = utility.utilite(n, hor)

    UTMD_arr = UTMD.to_numpy().astype(np.float64)




    # @jit(nopython=True)
    def distrib(vEM, vATT, vUTM, vPAR):

        # - a. modèle gravitaire

        M = vEM @ vATT * np.exp(vPAR[2] * vUTM) * (-vUTM) ** vPAR[3]

        # - b.fratar

        iteration = 0
        RMSE = precRMSE

        # rowPos = M.sum(1) > 0

        # colPos = M.sum(0) > 0

        # while (iteration < cMaxIterDist and RMSE >= precRMSE):
        while (iteration < cMaxIterDist and RMSE >= precRMSE):

            Computed_Prod = M.sum(1)
            Computed_Prod[Computed_Prod == 0] = 1
            Orig_Fac = vEM.T/Computed_Prod
            M = M * Orig_Fac.T


            Computed_ATT = M.sum(0)
            Computed_ATT[Computed_ATT == 0] = 1
            Dest_Fac = vATT/Computed_ATT
            M *= Dest_Fac


            RMSE = np.sqrt((((M.sum(1) - vEM.T)**2)).sum()/(cNbZone - 1))

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
                vEM = vEM.reshape(cNbZone, 1)
                vATT = ATT[:, id].copy()
                vATT = vATT.reshape(1, cNbZone)
                vUTM = UTMD_arr[:, id].copy()
                vUTM = vUTM.reshape(cNbZone, cNbZone, order='C')

                Modus_motcat[:, id] = distrib(vEM, vATT, vUTM, vPAR).reshape((cNbZone ** 2, ))
    dist_calc(Modus_motcat)
    return Modus_motcat

# # Modus_motcat = distribution('actuel', 'PPM')
# import pandas as pd
# Modus_motcat = pd.DataFrame(Modus_motcat)
# # import numpy as np
# Motcat_valid = pd.read_sas('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python'
#                            '\\Other_files\\modus_motcat_2012_hpm.sas7bdat')
# motcat60 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcat60.sas7bdat')
# motcatseU0 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcatseU0.sas7bdat')
# #
# Motcat_valid = motcat60
# Motcat_valid = motcatseU0
# #
# Motcat_valid.columns = range(28)
# DIFF = np.abs(Modus_motcat - Motcat_valid)/Motcat_valid
# # DIFF = np.abs(Modus_motcat - Motcat_valid)
# #
# DIFF.sum().sum()
# #
# # diffsas = np.abs(Motcat_valid - motcat60)
# # diffsas.sum().sum()




