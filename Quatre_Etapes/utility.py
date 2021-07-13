
# Importation des modules nécessaires
from Data import util_data, A_CstesModus, CstesStruct

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

    OD[['TTC_PPM', 'TTC_PCJ', 'TTC_PPS']] = (OD[['TTC_PPM', 'TTC_PCJ', 'TTC_PPS']] ** lambda_TTC) / (lambda_TTC - 1)
    OD[['TVPM', 'TVPC', 'TVPS']] = (OD[['TVPM', 'TVPC', 'TVPS']]**lambda_TVP)/(lambda_TVP - 1)
    OD[['TATT_PPM', 'TATT_PCJ', 'TATT_PPS']] = (OD[['TATT_PPM', 'TATT_PCJ', 'TATT_PPS']]**lambda_TAT)/(lambda_TAT - 1)
    OD['TCY'] = (1.3 * OD['DVOL']/VCY/60)**(lambda_TCY - 1)/lambda_TCY
    OD['CTVP'] = 1.3 * OD['DVOL'] * CVPkm
    OD[['CTTKKM', 'CTVP']] = OD[['CTTKKM', 'CTVP']]**(lambda_COUT - 1)/lambda_COUT
    OD['CSTATMOY'] = (OD['CSTATMOY'] + 1)**(lambda_CSTAT - 1)/lambda_CSTAT

    # if n == 'scen' and idvelo == 1 and (idBcl == 0 or iter != 1):
    # Kiko Then what?
    CM_PAR = calcul_util.CM_PAR_read()
    CM_PAR.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)
    CM_PAR.drop(columns='ID_C', inplace=True)   # Puisque c'est le même que les indices par défaut.

# Kiko Everything below this can be deleted.

sorted(list(set(list(OD.columns)).symmetric_difference(set(list(CM_PAR.columns)))))
set(list(CM_PAR.columns)) - set(list(OD.columns))
sorted(list(set(list(OD.columns)) - set(list(CM_PAR.columns))))

cols = ['INTTC' ,
'INTVP' ,
'INTCY' ,
'TR_HPM'  ,
'TAT_HPM'  ,
'TTC_HPM'  ,
'TR_HPS'  ,
'TAT_HPS'  ,
'TTC_HPS'  ,
'TR_HC'  ,
'TAT_HC'  ,
'TTC_HC'  ,
'TVP_HPM' ,
'TVP_HPS' ,
'TVP_HC' ,
'TMD'  ,
'TCY'  ,
'CTKKM' ,
'CTVP' ,
'CAPVELIB']
sorted(list(set(list(CM_PAR.columns)).symmetric_difference(set(cols))))