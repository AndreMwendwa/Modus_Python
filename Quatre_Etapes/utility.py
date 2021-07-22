
# Importation des modules nécessaires
import numpy as np
import pandas as pd
from collections import defaultdict
from Data import util_data, A_CstesModus, CstesStruct
from Exec_Modus import *

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *

lambda_COUT = 0.16
lambda_TVP = 1.36
lambda_TTC = 1.36
lambda_TAT = 0.74
lambda_CSTAT = -2.35
lambda_TMD = 1
lambda_TCY = 0.67



def utilite(n, hor):
    OD = util_data.OD(n)

    calcul_util = util_data.calcul_util()
    calcul_util.per = hor

    # OD['TR_PPM'] = OD['TRAB_PPM'] + OD['TACC_PPM'] + OD['TMAR_PPM']
    # del OD['TRAB_PPM'], OD['TACC_PPM'], OD['TMAR_PPM']
    # OD['TR_PCJ'] = OD['TRAB_PCJ'] + OD['TACC_PCJ'] + OD['TMAR_PCJ']
    # del OD['TRAB_PCJ'], OD['TACC_PCJ'], OD['TMAR_PCJ']
    # OD['TR_PPS'] = OD['TRAB_PPS'] + OD['TACC_PPS'] + OD['TMAR_PPS']
    # del OD['TRAB_PPS'], OD['TACC_PPS'], OD['TMAR_PPS']
    # OD.rename(columns = {'TVEH_PPM':'TTC_PPM', 'TVEH_PCJ':'TTC_PCJ', 'TVEH_PPS':'TTC_PPS'}, inplace=True)

    # OD['TTC_PCJ'] = (OD['TTC_PCJ'] ** lambda_TTC) / (lambda_TTC - 1)
    # OD['TTC_PPS'] = (OD['TTC_PPS'] ** lambda_TTC) / (lambda_TTC - 1)

    # att = ['INTTC', 'INTVP', 'INTCY', 'TR_PPM', 'TATT_PPM', 'TTC_PPM', 'TR_PPS', 'TATT_PPS', 'TTC_PPS', 'TR_PCJ',
    #        'TATT_PCJ', 'TTC_PCJ', 'TVPM', 'TVPS', 'TVPC', 'TMD', 'TCY', 'CTTKKM', 'CTVP', 'CSTATMOY', 'CAPVELIB']

    def transformationBC(matrice):
        if matrice[['TTC_PPM', 'TTC_PCJ', 'TTC_PPS']].any().any():
            matrice[['TTC_PPM', 'TTC_PCJ', 'TTC_PPS']] = (matrice[['TTC_PPM', 'TTC_PCJ', 'TTC_PPS']] ** lambda_TTC - 1) / lambda_TTC
        if matrice[['TVPM', 'TVPC', 'TVPS']].any().any():
            matrice[['TVPM', 'TVPC', 'TVPS']] = (matrice[['TVPM', 'TVPC', 'TVPS']]**lambda_TVP - 1)/lambda_TVP
        if matrice[['TATT_PPM', 'TATT_PCJ', 'TATT_PPS']].any().any():
            matrice[['TATT_PPM', 'TATT_PCJ', 'TATT_PPS']] = (matrice[['TATT_PPM', 'TATT_PCJ', 'TATT_PPS']]**lambda_TAT - 1)/lambda_TAT
        if matrice['TCY'].any():
            matrice['TCY'] = (matrice['TCY']**lambda_TCY - 1)/lambda_TCY
        if matrice[['CTTKKM', 'CTVP']].any().any():
            matrice[['CTTKKM', 'CTVP']] = (matrice[['CTTKKM', 'CTVP']]**lambda_COUT - 1)/lambda_COUT
        # matrice['CSTATMOY'] = (matrice['CSTATMOY'] + 1)**(lambda_CSTAT - 1)/lambda_CSTAT
        if matrice['CSTATMOY'].any():
            matrice['CSTATMOY'] = ((matrice['CSTATMOY']+1) ** lambda_CSTAT - 1) / lambda_CSTAT
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
    OD_TC = transformationBC(util_data.var_TC(OD, att))
    OD_VP = transformationBC(util_data.var_VP(OD, att))
    OD_CY = transformationBC(util_data.var_CY(OD, att))
    OD_MD = transformationBC(util_data.var_MD(OD, att))

    seU = pd.DataFrame(np.zeros((1289**2, 22)))
    seUD = seU.copy()

    cFactEch_PPM = [1.4, 2.0, 1.0, 0.8, 1.3, 0.5, 1.4, 0.3, 1.0, 1.3, 0.8, 1.5, 1.0, 1.3, 0.5, 1.0, 0.7, 2.0, 0.3, 1.0,
                    1.1, 1.3]
    cFactEch_PPM_diag = np.zeros(((len(cFactEch_PPM)), (len(cFactEch_PPM))))
    for i in range(len(cFactEch_PPM)):
        cFactEch_PPM_diag[i, i] = cFactEch_PPM[i]
    def calc_util(OD_input, seU, seUD):
        U = OD_input @ CM_PAR.T
        eU = np.exp(U)
        eUD = np.exp(U @ cFactEch_PPM_diag)
        seU += eU
        seUD += eUD
        return seU, seUD


    seU, seUD = calc_util(OD_TC, seU, seUD)
    seU, seUD = calc_util(OD_VP, seU, seUD)
    seU, seUD = calc_util(OD_CY, seU, seUD)
    seU, seUD = calc_util(OD_MD, seU, seUD)

    UTM = np.log(seU)
    UTMD = np.log(seUD)
    UMAX = UTM.max(0)
    UMAXD = UTMD.max(0)
    CORRECT = np.where(UMAX>0, UMAX+1, 0)
    CORRECTD = np.where(UMAXD > 0, UMAXD + 1, 0)

    UTM -= CORRECT
    UTMD -= CORRECTD
    
    Motifs_Choix_Dist = defaultdict(list)
    # C'est une nouvelle étape dans laquelle on va décrire la transformation des motifs entre le choix model et 
    # la distribution. Les clés du dictionnaire corréspondent aux motifs - distribution, et les élements aux motifs 
    # génération (selon diapo 6 de la documentation de Modus)

    Motifs_Choix_Dist[1].extend((1, 2))
    Motifs_Choix_Dist[2].extend((3,))
    Motifs_Choix_Dist[3].extend((4,))
    Motifs_Choix_Dist[4].extend((5,))
    Motifs_Choix_Dist[5].extend((6,))
    Motifs_Choix_Dist[6].extend((7,))
    Motifs_Choix_Dist[7].extend((8,))
    Motifs_Choix_Dist[8].extend((9,))
    Motifs_Choix_Dist[9].extend((10,))
    Motifs_Choix_Dist[10].extend((11, 12))
    Motifs_Choix_Dist[11].extend((13, 14))

    Duplication = np.zeros((22, 28))
    for ligne, value in Motifs_Choix_Dist.items():
        for colonne in value:
            Duplication[ligne - 1, colonne - 1] = 1
            Duplication[ligne - 1 + 11, colonne - 1 + 14] = 1

    UTMD = UTMD @ Duplication
    return UTM, UTMD

# Kiko Everything below this can be deleted.

# sorted(list(set(list(OD.columns)).symmetric_difference(set(list(CM_PAR.columns)))))
# set(list(CM_PAR.columns)) - set(list(OD.columns))
# sorted(list(set(list(OD.columns)) - set(list(CM_PAR.columns))))
#
# cols = ['INTTC' ,
# 'INTVP' ,
# 'INTCY' ,
# 'TR_HPM'  ,
# 'TAT_HPM'  ,
# 'TTC_HPM'  ,
# 'TR_HPS'  ,
# 'TAT_HPS'  ,
# 'TTC_HPS'  ,
# 'TR_HC'  ,
# 'TAT_HC'  ,
# 'TTC_HC'  ,
# 'TVP_HPM' ,
# 'TVP_HPS' ,
# 'TVP_HC' ,
# 'TMD'  ,
# 'TCY'  ,
# 'CTKKM' ,
# 'CTVP' ,
# 'CAPVELIB']
# sorted(list(set(list(CM_PAR.columns)).symmetric_difference(set(cols))))



OD_TC_valid = pd.read_sas('Other_files\\eutc2012m.sas7bdat')
OD_TC_valid.columns = range(22)
U = OD_TC @ CM_PAR.T
eU = np.exp(U)

OD_MD_valid = pd.read_sas('Other_files\\eumd2012m.sas7bdat')
OD_MD_valid.columns = range(22)
U = OD_MD @ CM_PAR.T
eUMD = np.exp(U)

OD_CY_valid = pd.read_sas('Other_files\\eucy2012m.sas7bdat')
OD_CY_valid.columns = range(22)
U = OD_CY @ CM_PAR.T
eUCY = np.exp(U)

OD_VP_valid = pd.read_sas('Other_files\\euvp2012m.sas7bdat')
OD_VP_valid.columns = range(22)
U = OD_VP @ CM_PAR.T
eUVP = np.exp(U)

np.log(OD_VP_valid)

diff = np.abs((eUCY - OD_CY_valid)) / OD_CY_valid
diff = (eUVP - OD_VP_valid) / OD_VP_valid
diff = (eU - OD_TC_valid) / OD_TC_valid
diff = np.abs((eU - OD_TC_valid)) / OD_TC_valid
diff = (eUMD - OD_MD_valid) / OD_MD_valid
diff.max()

for col in diff.columns:
    diff[col][diff[col] > diff[col].quantile(0.95)] = 0

sommediff = diff.mean().mean()


eU.mean().plot()
t = 100000*OD_TC_valid.mean()
t.plot()
plt.show()

OD_TC_test = np.exp(OD_TC)

OD_TC_valid.mean()
eU.max()


OD_CY = util_data.var_CY(bdinter, att)
OD_CY['TCY'] = (OD_CY['TCY']**lambda_TCY - 1)/lambda_TCY
OD_CY['CSTATMOY'] = ((OD_CY['CSTATMOY']+1) ** lambda_CSTAT - 1) / lambda_CSTAT
OD_CY.iloc[0, :] @ CM_PAR.iloc[0, :].T
OD_TC.iloc[0, :] @ CM_PAR.iloc[0, :].T

transformationBC(OD_CY)

OD_CY['INTCY'] = 0
OD_CY.max()

bdinter = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\bdinter2012.sas7bdat')
bdinter.rename(
            columns={'TMAR_HC': 'TMAR_PCJ', 'TACC_HC': 'TACC_PCJ', 'TMAR_HPS': 'TMAR_PPS', 'TVEH_HC': 'TVEH_PCJ',
                     'TACC_HPS': 'TACC_PPS', 'TRAB_HPM': 'TRAB_PPM', 'TATT_HPS': 'TATT_PPS', 'TRAB_HPS': 'TRAB_PPS',
                     'TMAR_HPM': 'TMAR_PPM', 'TVEH_HPS': 'TVEH_PPS', 'TRAB_HC': 'TRAB_PCJ', 'TVEH_HPM': 'TVEH_PPM',
                     'TACC_HPM': 'TACC_PPM', 'TATT_HC': 'TATT_PCJ', 'TATT_HPM': 'TATT_PPM', 'CTKKM': 'CTTKKM'},
            inplace=True)
for i in range(1, 19):
    bdinter.drop(columns=f'CO{i}', inplace=True)

OD_VP = transformationBC(util_data.var_VP(bdinter, att))
OD_VP = util_data.var_VP(bdinter, att)
OD_VP.iloc[0, :] @ CM_PAR.iloc[0, :].T
for col in diff.columns:
    print(diff[col].to_numpy().argmax())

diff.max()
