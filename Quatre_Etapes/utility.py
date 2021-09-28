
# Importation des modules nécessaires
import pandas as pd
import pickle as pkl
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes.exec_Modus import *

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *

dbfile = open(f'{dir_dataTemp}params_user', 'rb')
params_user = pkl.load(dbfile)

lambda_COUT = 0.16
lambda_TVP = 1.36
lambda_TTC = 1.36
lambda_TAT = 0.74
lambda_CSTAT = -2.35
lambda_TMD = 1
lambda_TCY = 0.67



def utilite(n, hor):
    if params_user['modus_mode'] == 1:
        OD = util_data.OD(n)

    else:
        # bdinter = pd.read_sas(dir_root + '\\M3_Chaine\\Modus_Python\\bdinter2012.sas7bdat')
        # bdinter = pd.read_sas(bdinter)

        # bdinter.rename(
        #     columns={'TMAR_HC': 'TMAR_PCJ', 'TACC_HC': 'TACC_PCJ', 'TMAR_HPS': 'TMAR_PPS', 'TVEH_HC': 'TVEH_PCJ',
        #              'TACC_HPS': 'TACC_PPS', 'TRAB_HPM': 'TRAB_PPM', 'TATT_HPS': 'TATT_PPS', 'TRAB_HPS': 'TRAB_PPS',
        #              'TMAR_HPM': 'TMAR_PPM', 'TVEH_HPS': 'TVEH_PPS', 'TRAB_HC': 'TRAB_PCJ', 'TVEH_HPM': 'TVEH_PPM',
        #              'TACC_HPM': 'TACC_PPM', 'TATT_HC': 'TATT_PCJ', 'TATT_HPM': 'TATT_PPM', 'CTKKM': 'CTTKKM'},
        #     inplace=True)
        dbfile = open(f'{dir_dataTemp}bdinter', 'rb')
        bdinter = pkl.load(dbfile)
        # for i in range(1, 19):
        #     bdinter.drop(columns=f'CO{i}', inplace=True)

        OD = bdinter.copy()



    calcul_util = util_data.calcul_util()
    calcul_util.per = hor



    def transformationBC(matrice):
        # # if matrice['TTC_PPM'].any():
        # #     matrice['TTC_PPM'] = (matrice['TTC_PPM'] ** lambda_TTC - 1) / lambda_TTC
        #
        # # mask = matrice['TTC_PPM'] != 0
        # # matrice.loc[mask, 'TTC_PPM'] = (matrice.loc[mask, 'TTC_PPM'] ** lambda_COUT - 1) / lambda_COUT
        # matrice['TTC_PPM'] = np.where(matrice['TTC_PPM'] != 0, (matrice['TTC_PPM'] ** lambda_COUT - 1) / lambda_COUT, 0)
        # if matrice['TTC_PCJ'].any():
        #     matrice['TTC_PCJ'] = (matrice['TTC_PCJ'] ** lambda_TTC - 1) / lambda_TTC
        # if matrice['TTC_PPS'].any():
        #     matrice['TTC_PPS'] = (matrice['TTC_PPS'] ** lambda_TTC - 1) / lambda_TTC
        #
        # if matrice['TVPM'].any():
        #     matrice['TVPM'] = (matrice['TVPM']**lambda_TVP - 1)/lambda_TVP
        # if matrice['TVPC'].any():
        #     matrice['TVPC'] = (matrice['TVPC']**lambda_TVP - 1)/lambda_TVP
        # # mask = matrice['TVPC'] != 0   # Kiko - to change
        # # matrice.loc[mask, 'TVPC'] = (matrice.loc[mask, 'TVPC'] ** lambda_COUT - 1) / lambda_COUT
        # if matrice['TVPS'].any():
        #     matrice['TVPS'] = (matrice['TVPS']**lambda_TVP - 1)/lambda_TVP
        #
        # # if matrice['TATT_PPM'].any():
        # #     matrice['TATT_PPM'] = (matrice['TATT_PPM']**lambda_TAT - 1)/lambda_TAT
        # mask = matrice['TATT_PPM'] != 0
        # matrice.loc[mask, 'TATT_PPM'] = (matrice.loc[mask, 'TATT_PPM'] ** lambda_COUT - 1) / lambda_COUT
        # del mask
        # if matrice['TATT_PPS'].any():
        #     matrice['TATT_PPS'] = (matrice['TATT_PPS']**lambda_TAT - 1)/lambda_TAT
        # if matrice['TATT_PCJ'].any():
        #     matrice['TATT_PPS'] = (matrice['TATT_PCJ']**lambda_TAT - 1)/lambda_TAT  # Kiko -> why this?
        #
        # if matrice['TCY'].any():
        #     matrice['TCY'] = (matrice['TCY']**lambda_TCY - 1)/lambda_TCY
        # # if matrice['CTTKKM'].any():
        # #     matrice['CTTKKM'] = (matrice['CTTKKM']**lambda_COUT - 1)/lambda_COUT
        #
        # mask = matrice['CTTKKM'] != 0
        # matrice.loc[mask, 'CTTKKM'] = (matrice.loc[mask, 'CTTKKM'] ** lambda_COUT - 1) / lambda_COUT
        #
        # if matrice['CTVP'].any():
        #     matrice['CTVP'] = (matrice['CTVP']**lambda_COUT - 1)/lambda_COUT
        #
        # # matrice['CSTATMOY'] = (matrice['CSTATMOY'] + 1)**(lambda_CSTAT - 1)/lambda_CSTAT
        # if matrice['CSTATMOY'].any():
        #     matrice['CSTATMOY'] = ((matrice['CSTATMOY']+1) ** lambda_CSTAT - 1) / lambda_CSTAT
        #
        # mask = matrice['CAPVELIB'] != 0
        # matrice.loc[mask, 'CAPVELIB'] = (matrice.loc[mask, 'CAPVELIB'] * capvelib)

        mask = matrice['TTC_PPM'] != 0
        matrice.loc[mask, 'TTC_PPM'] = (matrice.loc[mask, 'TTC_PPM'] ** lambda_TTC - 1) / lambda_TTC
        mask = matrice['TTC_PCJ'] != 0
        matrice.loc[mask, 'TTC_PCJ'] = (matrice.loc[mask, 'TTC_PCJ'] ** lambda_TTC - 1) / lambda_TTC
        mask = matrice['TTC_PPS'] != 0
        matrice.loc[mask, 'TTC_PPS'] = (matrice.loc[mask, 'TTC_PPS'] ** lambda_TTC - 1) / lambda_TTC
        mask = matrice['TVPM'] != 0
        matrice.loc[mask, 'TVPM'] = (matrice.loc[mask, 'TVPM'] ** lambda_TVP - 1) / lambda_TVP
        mask = matrice['TVPC'] != 0
        matrice.loc[mask, 'TVPC'] = (matrice.loc[mask, 'TVPC'] ** lambda_TVP - 1) / lambda_TVP
        mask = matrice['TVPS'] != 0
        matrice.loc[mask, 'TVPS'] = (matrice.loc[mask, 'TVPS'] ** lambda_TVP - 1) / lambda_TVP
        mask = matrice['TATT_PPM'] != 0
        matrice.loc[mask, 'TATT_PPM'] = (matrice.loc[mask, 'TATT_PPM'] ** lambda_TAT - 1) / lambda_TAT
        mask = matrice['TATT_PPS'] != 0
        matrice.loc[mask, 'TATT_PPS'] = (matrice.loc[mask, 'TATT_PPS'] ** lambda_TAT - 1) / lambda_TAT
        mask = matrice['TATT_PCJ'] != 0
        matrice.loc[mask, 'TATT_PPS'] = (matrice.loc[mask, 'TATT_PCJ'] ** lambda_TAT - 1) / lambda_TAT
        mask = matrice['TCY'] != 0
        matrice.loc[mask, 'TCY'] = (matrice.loc[mask, 'TCY'] ** lambda_TCY - 1) / lambda_TCY
        mask = matrice['CTTKKM'] != 0
        matrice.loc[mask, 'CTTKKM'] = (matrice.loc[mask, 'CTTKKM'] ** lambda_COUT - 1) / lambda_COUT

        mask = matrice['CTVP'] != 0
        matrice.loc[mask, 'CTVP'] = (matrice.loc[mask, 'CTVP'] ** lambda_COUT - 1) / lambda_COUT

        matrice['CSTATMOY'] = ((matrice['CSTATMOY'] + 1) ** lambda_CSTAT - 1) / lambda_CSTAT
        mask = matrice['CAPVELIB'] != 0
        matrice.loc[mask, 'CAPVELIB'] = (matrice.loc[mask, 'CAPVELIB'] * capvelib)

        if n == 'scen' and idvelo == 1:
            if idBcl == 0 or iter_count != 1:
                matrice['INTCY'] = intcy
                matrice['CAPVELIB'] = capvelib
        # matrice.replace([np.inf, -np.inf], 0, inplace=True)
        return matrice




    # if n == 'scen' and idvelo == 1 and (idBcl == 0 or iter != 1):
    # Kiko Then what?
    CM_PAR = calcul_util.CM_PAR_read()
    CM_PAR.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)
    CM_PAR.drop(columns='ID_C', inplace=True)   # Puisque c'est le même que les indices par défaut.

    # Kiko -> Get these to work, since the individual functions are currently working.
    util_TC = transformationBC(util_data.var_TC(OD, att))
    util_VP = transformationBC(util_data.var_VP(OD, att, n, idcoutvp))
    util_CY = transformationBC(util_data.var_CY(OD, att))
    util_MD = transformationBC(util_data.var_MD(OD, att))

    seU = pd.DataFrame(np.zeros((1289**2, 22)))
    seUD = seU.copy()

    cFactEch_PPM = [1.00, 1.00, 0.40, 0.10, 1.00, 0.30, 0.55, 0.15, 0.15, 0.60,  0.60,  1.00,  1.00, 1.00, 1.00, 1.00,
                    1.00, 1.50, 0.15, 1.00, 0.70, 1.00]
    cFactEch_PPM_diag = np.zeros(((len(cFactEch_PPM)), (len(cFactEch_PPM))))
    for i in range(len(cFactEch_PPM)):
        cFactEch_PPM_diag[i, i] = cFactEch_PPM[i]

    list_fichiers = ['util_TC', 'util_VP', 'util_CY', 'util_MD']    # List des noms des fichiers qui va être utilisé pour
    # les 'pickler', c'est le même que l'ordre des fichiers dans les lignes ci-dessous.
    num_list = 0

    def calc_util(OD_input, seU, seUD):
        U = OD_input @ CM_PAR.T
        eU = np.exp(U)
        eUD = np.exp(U @ cFactEch_PPM_diag)
        seU += eU
        seUD += eUD
        return seU, seUD, eU

    UTIL_DB = {}        # Un dictionnaire vide dans lequel seront stockés les résultats du calcul utilitaire picklés
    seU, seUD, eU = calc_util(util_TC, seU, seUD)
    UTIL_DB['util_TC'] = eU
    seU, seUD, eU = calc_util(util_VP, seU, seUD)
    UTIL_DB['util_VP'] = eU
    seU, seUD, eU = calc_util(util_CY, seU, seUD)
    UTIL_DB['util_CY'] = eU
    seU, seUD, eU = calc_util(util_MD, seU, seUD)
    UTIL_DB['util_MD'] = eU

    # Ici on va pickler the dataframes eU
    dbfile = open(f'{dir_dataTemp}UTIL_DB', 'wb')
    pkl.dump(UTIL_DB, dbfile)
    dbfile.close()

    UTM = np.log(seU)
    UTMD = np.log(seUD)
    UMAX = UTM.max(0)
    UMAXD = UTMD.max(0)
    CORRECT = np.where(UMAX > 0, UMAX + 1, 0)
    CORRECTD = np.where(UMAXD > 0, UMAXD + 1, 0)

    UTM -= CORRECT
    UTMD -= CORRECTD
    
    UTMD = UTMD @ Duplication
    return UTM, UTMD

