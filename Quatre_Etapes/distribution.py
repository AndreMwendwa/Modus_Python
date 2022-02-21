from Data import A_CstesModus, CstesStruct
from Quatre_Etapes import generation
from Quatre_Etapes import utility
from Data.distribution_data import dist_data
from Data.A_CstesModus import *
from Quatre_Etapes.dossiers_simul import *

def distribution(n, hor):
    dist_data_instance = dist_data()
    dist_data_instance.per = hor
    dist_data_instance.n = n

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

    dbfile = open(f'{dir_dataTemp}Modus_motcat_{n}_{hor}', 'wb')
    pkl.dump(Modus_motcat, dbfile)
    dbfile.close()
    if n == 'actuel':
        if hor == 'PPM':
            print(f"\t Distribution terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Matin")
        elif hor == 'PCJ':
            print(f"\t Distribution terminé pour l'année de calage du modèle ({actuel}), pour la Période Creuse de la journée")
        else:
            print(f"\t Distribution terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Soir")
    else:
        if hor == 'PPM':
            print(f"\t Distribution terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Matin")
        elif hor == 'PCJ':
            print(f"\t Distribution terminé pour l'année de scénario du modèle ({scen}), pour la Période Creuse de la journée")
        else:
            print(f"\t Distribution terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Soir")
    return Modus_motcat

if __name__ == '__main__':
    # distribution('scen', 'PPM')
    distribution('scen', 'PPS')
    # distribution('actuel', 'PPM')


