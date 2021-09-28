#
import matplotlib.pyplot as plt
import seaborn as sns

mypath = 'C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'

bdinter = pd.read_sas(mypath + '\\Other_files\\bdinter2012.sas7bdat')

util_TC_SAS = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\vartbc_tc.sas7bdat')

util_TC_SAS.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)

util_CY_SAS = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\vartbc_cy.sas7bdat')

util_CY_SAS.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)
statusCY = util_CY_SAS == util_CY
statusCY.sum()
util_CY_SAS['CAPVELIB'].sum()
util_CY['CAPVELIB'].sum()
# list_col = list(util_TC.columns)
# util_TC_SAS = util_TC_SAS[list_col]

statusTC = util_TC_SAS == util_TC
statusTC = np.abs(util_TC - util_TC_SAS)
statusTC.sum()
util_TC_SAS['TTC_PPM'].sum()
util_TC['TTC_PPM'].sum()
util_TC_SAS2['TTC_PPM'].sum()
(0.9 ** lambda_TTC - 1/lambda_TTC)
(1.1 ** lambda_TTC - 1)/lambda_TTC

statusTC.sum()

util_TC_SAS2 = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\var_tc.sas7bdat')

util_TC_SAS2.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)
util_TC2 = util_data.var_TC(OD, att)
statusTC = np.abs(util_TC2 - util_TC_SAS2)
statusTC.sum()
rowmax = []
for i in list(statusTC.columns):
    rowmax.append(np.argmax(statusTC[i]))
statusTC.iloc[3891, :]
util_TC.iloc[3891, :]
util_TC.iloc[3891, :]
util_TC_SAS.iloc[3891, :] - util_TC.iloc[3891, :]

statusTC['TATT_PPM'].plot()
statusTC['TTC_PCJ'].plot()

util_VP_SAS = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\vartbc_vp.sas7bdat')

util_VP_SAS.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
                            'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
                            'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
                            'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
                            'CTKKM': 'CTTKKM'}, inplace=True)
statusVP = np.abs(util_VP_SAS - util_VP)
statusVP.sum()




## util_TC[['TATT_PPM', 'TTC_PPM', 'TATT_PPS', 'TTC_PPS', 'TATT_PCJ', 'TTC_PCJ']]
## util_TC_SAS[['TATT_PPM', 'TTC_PPM', 'TATT_PPS', 'TTC_PPS', 'TATT_PCJ', 'TTC_PCJ']]
#
# df = pd.concat([util_TC[['CTTKKM']], util_TC_SAS[['CTTKKM']]], axis=1)
# df['difference'] = (util_TC['CTTKKM'] - util_TC_SAS['CTTKKM'])
# df['difference'].sum()
#
# df = pd.concat([util_TC[util_TC['CTTKKM'] != util_TC_SAS['CTTKKM']].loc[:, 'CTTKKM'],
#                util_TC_SAS[util_TC['CTTKKM'] != util_TC_SAS['CTTKKM']].loc[:, 'CTTKKM']], axis=1)
#
# df.iloc[259, :]
# df.iloc[259, 0] - df.iloc[259, 1]
# # Before TBC
# util_TCb = util_data.var_TC(OD, att)
# util_TCb_SAS = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'
#                           'Other_files\\Confirmation distribution\\var_tc_beforetbc.sas7bdat')
# util_TCb_SAS.rename(columns= {'TVP_HPM': 'TVPM', 'TVP_HC': 'TVPC', 'TVP_HPS': 'TVPS',
#                             'TTC_HPM':'TTC_PPM', 'TTC_HC':'TTC_PCJ', 'TTC_HPS':'TTC_PPS',
#                             'TR_HPM': 'TR_PPM', 'TR_HC': 'TR_PCJ', 'TR_HPS': 'TR_PPS',
#                             'TAT_HPM': 'TATT_PPM', 'TAT_HC': 'TATT_PCJ', 'TAT_HPS': 'TATT_PPS',
#                             'CTKKM': 'CTTKKM'}, inplace=True)
# list_col = list(util_TCb.columns)
# util_TCb_SAS = util_TCb_SAS[list_col]
#
# statusTCb = util_TCb_SAS==util_TCb
# util_TCb[['TATT_PPM', 'TTC_PPM', 'TATT_PPS', 'TTC_PPS', 'TATT_PCJ', 'TTC_PCJ']]
# util_TCb_SAS[['TATT_PPM', 'TTC_PPM', 'TATT_PPS', 'TTC_PPS', 'TATT_PCJ', 'TTC_PCJ']]
#
# statusTCb.sum()
#
# util_TCc = util_TCb.copy()
# util_TCc['TTC_PPM'] = (util_TCc['TTC_PPM'] ** lambda_TTC - 1) / lambda_TTC
#
# statusTCc = util_TCb['TTC_PPM'] == util_TC_SAS['TTC_PPM']
# statusTCc.sum()
# statusTCc
# sorted(set(util_TC_SAS.columns).symmetric_difference(set(util_TC.columns)))
#
#
U_valid = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\utc_df.sas7bdat')
U_valid.columns = range(22)
util_TC_SAS.loc[1489251, 'CTTKKM']

util_TC.loc[1489251, 'CTTKKM']
util_TC['CTTKKM'].replace({-6.25:0}, inplace=True)


OD_TC_valid = pd.read_sas('Other_files\\eutc2012m.sas7bdat')
OD_TC_valid.columns = range(22)

diff_SAS = OD_TC_valid - euTC
diff_SAS.sum().sum()    # Kiko Very small figure, proving that my eu calc and Guillaume's give the same output.

U = util_TC @ CM_PAR.T
eU = np.exp(U)
diffTC = np.abs(eU - OD_TC_valid) / OD_TC_valid
sommediffTC = diffTC.mean().mean()

OD_CY_valid = pd.read_sas('Other_files\\eucy2012m.sas7bdat')
OD_CY_valid.columns = range(22)
U = util_CY @ CM_PAR.T
eU = np.exp(U)
diffCY = np.abs(eU - OD_CY_valid) / OD_CY_valid
sommediffCY = diffCY.mean().mean()

OD_CY = util_data.var_CY(OD, att)
U_valid = pd.read_sas(mypath + 'Other_files\\Confirmation distribution\\udf_cy.sas7bdat')
U_valid.columns = range(22)
U = util_CY @ CM_PAR.T
diffCYU = np.abs(U - U_valid)/U_valid
sommediffCY

OD_MD_valid = pd.read_sas('Other_files\\eumd2012m.sas7bdat')
OD_MD_valid.columns = range(22)
U = util_MD @ CM_PAR.T
eU = np.exp(U)
diffMD = np.abs(eU - OD_MD_valid) / OD_MD_valid
sommediffMD = diffMD.mean().mean()

OD_VP_valid = pd.read_sas('Other_files\\euvp2012m.sas7bdat')
OD_VP_valid.columns = range(22)
U = util_VP @ CM_PAR.T
eU = np.exp(U)
diffVP = np.abs(eU - OD_VP_valid) / OD_VP_valid

sommediffVP = diffVP.mean().mean()
diffVP.max()


rowmax = []
for i in range(22):
    rowmax.append(np.argmax(diffTC[i]))
# plt.pcolor(diffTC.iloc[1480000:1490000, :])
sns.heatmap(diffTC.iloc[1489000:1489500, :], annot=False)

diffT = util_TC_SAS - util_TC
diffT.max()
sns.heatmap(diffT.iloc[:, :], annot=False)

diffTC.mean(1).plot()
diffTC.iloc[1480000:1487000, :].plot()

# Debugging CTKKM in TBC
matrice = pd.DataFrame([0,1,2,3])
if matrice[0].any():
    matrice['CTTKKM'] = (matrice[0] ** lambda_COUT - 1) / lambda_COUT

# OD_TC_valid = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'
#                           'Other_files\\Confirmation distribution\\eutc_df.sas7bdat')
#
# U_valid = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'
#                           'Other_files\\Confirmation distribution\\utc_df.sas7bdat')
# U_valid.columns = range(22)
# diffTCU = np.abs(U - U_valid)/U_valid
# sommediffTCU = diffTCU.mean().mean()
# stddiff = diffTCU.std().std()
# diffTCU.max().max()
#
#
#
#
#
# # Simulating effect of variations
# test = np.ones((1661521, 22))
# test_dev = test + np.random.normal(loc=-1.6e-5, scale=0.003, size=(1661521, 22))
# for i in range(10):
#     test_dev[i,1] = -5
# test_dev.min()
# test_dev.mean()
# diffmean = 1 - test_dev.mean()
#
# exptest_dev = np.exp(test_dev)
# exptest = np.exp(test)
# diff = (exptest_dev - exptest)/exptest
# diff.std().std()
# diff.min()
# diff.mean()
#
# U = util_VP @ CM_PAR.T
# eU = np.exp(U)
#
# # OD_TC_valid = pd.read_sas('Other_files\\eutc2012m.sas7bdat')
# OD_VP_valid = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'
#                           'Other_files\\Confirmation distribution\\eudf_vp.sas7bdat')
#
# U_valid = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\'
#                           'Other_files\\Confirmation distribution\\udf_vp.sas7bdat')
# U_valid.columns = range(22)
# diffVPU = np.abs(U - U_valid)/U_valid
# sommediffVPU = diffVPU.mean().mean()
#
# diffVP = np.abs(eU - OD_VP_valid) / OD_VP_valid
# sommediffVP = diffVP.mean().mean()
# diffVP.max()


def test_diff(mode, util):
    U_valid = pd.read_sas(f"mypath + ""
                          f"Other_files\\Confirmation distribution\\udf_{mode}.sas7bdat")
    eU_valid = pd.read_sas(f'D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine'
                           f'\\Modus_Python\\Other_files\\Confirmation distribution\\eudf_{mode}.sas7bdat')
    U_valid.columns = range(22)
    eU_valid.columns = range(22)
    U = util @ CM_PAR.T
    eU = np.exp(U)
    diffU = np.abs(U - U_valid)/U_valid
    diffeU = np.abs(eU - eU_valid)/eU_valid
    diffmeanU = diffU.mean().mean()
    diffmeaneU = diffeU.mean().mean()
    return diffU, diffeU

diffU, diffeU = test_diff('cy', util_CY)



# Choix modal confirmation
import numpy as np
import pandas as pd
import pickle as pkl
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes import distribution

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
from Data.A_CstesModus import *


euTC = pd.read_sas(dir_root + '\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_tc.sas7bdat')
euTC.columns = range(22)
euCY = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_cy.sas7bdat')
euCY.columns = range(22)
euMD = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_md.sas7bdat')
euMD.columns = range(22)
euVP = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_vp.sas7bdat')
euVP.columns = range(22)




def choix_modal(n, hor):
    Modus_motcat = pd.read_sas(mypath + 'Other_files\\modus_motcat_2012_hpm.sas7bdat')
    Modus_motcat.columns = range(28)
    Modus_motcat = Modus_motcat @ Duplication.T

    seU = euTC + euVP + euCY + euMD

    itern = 0   # Kiko: Sentinel temporaire, à supprimer

    if n == 'actuel':

        BASE = Modus_motcat/seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl < 3 and itern > 1:
        BASE = Modus_motcat / seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl == 3 and itern > 1:
        BASE = (Modus_motcat - Modus_MD_motcat - Modus_CY_motcat)/seU
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl == 4 and itern > 1:
        BASE = (Modus_motcat - Modus_MD_motcat) / seU
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    return Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat

Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat = choix_modal('actuel', 'PPM')

Modus_MD_motcat_valid = pd.read_sas(mypath + 'Other_files'
                              '\\Confirmation distribution\\motcatmd.sas7bdat')
Modus_MD_motcat_valid.columns = range(22)
Modus_CY_motcat_valid = pd.read_sas(mypath + 'Other_files'
                              '\\Confirmation distribution\\motcatcy.sas7bdat')
Modus_CY_motcat_valid.columns = range(22)
Modus_VP_motcat_valid = pd.read_sas(mypath + 'Other_files'
                              '\\Confirmation distribution\\motcatvp.sas7bdat')
Modus_VP_motcat_valid.columns = range(22)
Modus_TC_motcat_valid = pd.read_sas(mypath + 'Other_files'
                              '\\Confirmation distribution\\motcattc.sas7bdat')
Modus_TC_motcat_valid.columns = range(22)

diffMD = np.abs(Modus_MD_motcat - Modus_MD_motcat_valid)/Modus_MD_motcat_valid
diffabsMD = np.abs(Modus_MD_motcat - Modus_MD_motcat_valid)
sommediffabsMD = diffabsMD.mean().mean()
sommediffMD = diffMD.mean().mean()

diffTC = np.abs(Modus_TC_motcat - Modus_TC_motcat_valid)/Modus_TC_motcat_valid
sommediffTC = diffTC.mean().mean()

diffVP = np.abs(Modus_VP_motcat - Modus_VP_motcat_valid)/Modus_VP_motcat_valid
sommediffVP = diffVP.mean().mean()

diffCY = np.abs(Modus_CY_motcat - Modus_CY_motcat_valid)/Modus_CY_motcat_valid
sommediffCY = diffCY.mean().mean()



diffMD.mean(1).plot()
diffabsMD.mean(1).plot()
diffTC.mean(1).plot()


# Testing precision of SAS
test = np.ones((1661521, 22))
test_dev = test + np.random.normal(loc=-1.6e-5, scale=0.003, size=(1661521, 22))

eudf_cy = pd.read_sas(mypath + 'Other_files\\'
                      'Confirmation distribution\\eudf_cy.sas7bdat')
eudf_cy.columns = range(22)
cm_par = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Calibrage\\2_Resultats\\'
                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\cm_parhpm.sas7bdat')
test_res = eudf_cy @ cm_par
test_res.columns = range(22)
test_res_valid = pd.read_sas(mypath + 'Other_files\\'
                      'Confirmation distribution\\test.sas7bdat')
test_res_valid.columns = range(22)
diff = (test_res - test_res_valid)/test_res_valid
diff.mean(1).plot()

# Test TC seulement
import pandas as pd
from Data.A_CstesModus import *

euTC = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_tc.sas7bdat')  # Your own path
euTC.columns = range(22)
euCY = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_cy.sas7bdat')  # Your own path
euCY.columns = range(22)
euMD = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_md.sas7bdat')  # Your own path
euMD.columns = range(22)
euVP = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_vp.sas7bdat')  # Your own path
euVP.columns = range(22)
seU = euTC + euVP + euCY + euMD
Modus_motcat = pd.read_sas(mypath + 'Other_files'
                               '\\modus_motcat_2012_hpm.sas7bdat')  # Your own path
Duplication = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\dupplication.sas7bdat')  # Your own path
Duplication.columns = range(28)
Modus_motcat.columns = range(28)
Modus_motcat = Modus_motcat @ Duplication.T
BASE = Modus_motcat/seU
Modus_MD_motcat = BASE * euMD
Modus_MD_motcat_valid = pd.read_sas(mypath + 'Other_files'
                              '\\Confirmation distribution\\motcatmd.sas7bdat')   # The dataset created by the SAS code
Modus_MD_motcat_valid.columns = range(22)
diffMD = np.abs(Modus_MD_motcat - Modus_MD_motcat_valid)/Modus_MD_motcat_valid
meandiffMD = diffMD.mean().mean()

diffMD.mean(1).plot()




M = pd.DataFrame(M)
UTMD.isna().sum().sum()


matrice = util_data.var_TC(OD, att)
matrice['TTC_PPM'] = np.where(matrice['TTC_PPM'] != 0, (matrice['TTC_PPM'] ** lambda_COUT - 1) / lambda_COUT, 0)
if matrice['TTC_PCJ'].any():
    matrice['TTC_PCJ'] = (matrice['TTC_PCJ'] ** lambda_TTC - 1) / lambda_TTC
if matrice['TTC_PPS'].any():
    matrice['TTC_PPS'] = (matrice['TTC_PPS'] ** lambda_TTC - 1) / lambda_TTC

if matrice['TVPM'].any():
    matrice['TVPM'] = (matrice['TVPM']**lambda_TVP - 1)/lambda_TVP
if matrice['TVPC'].any():
    matrice['TVPC'] = (matrice['TVPC']**lambda_TVP - 1)/lambda_TVP
# mask = matrice['TVPC'] != 0   # Kiko - to change
# matrice.loc[mask, 'TVPC'] = (matrice.loc[mask, 'TVPC'] ** lambda_COUT - 1) / lambda_COUT
if matrice['TVPS'].any():
    matrice['TVPS'] = (matrice['TVPS']**lambda_TVP - 1)/lambda_TVP

# if matrice['TATT_PPM'].any():
#     matrice['TATT_PPM'] = (matrice['TATT_PPM']**lambda_TAT - 1)/lambda_TAT
mask = matrice['TATT_PPM'] != 0
matrice.loc[mask, 'TATT_PPM'] = (matrice.loc[mask, 'TATT_PPM'] ** lambda_COUT - 1) / lambda_COUT
del mask
if matrice['TATT_PPS'].any():
    matrice['TATT_PPS'] = (matrice['TATT_PPS']**lambda_TAT - 1)/lambda_TAT
if matrice['TATT_PCJ'].any():
    matrice['TATT_PPS'] = (matrice['TATT_PCJ']**lambda_TAT - 1)/lambda_TAT  # Kiko -> why this?

if matrice['TCY'].any():
    matrice['TCY'] = (matrice['TCY']**lambda_TCY - 1)/lambda_TCY
# if matrice['CTTKKM'].any():
#     matrice['CTTKKM'] = (matrice['CTTKKM']**lambda_COUT - 1)/lambda_COUT

mask = matrice['CTTKKM'] != 0
matrice.loc[mask, 'CTTKKM'] = (matrice.loc[mask, 'CTTKKM'] ** lambda_COUT - 1) / lambda_COUT

if matrice['CTVP'].any():
    matrice['CTVP'] = (matrice['CTVP']**lambda_COUT - 1)/lambda_COUT

# matrice['CSTATMOY'] = (matrice['CSTATMOY'] + 1)**(lambda_CSTAT - 1)/lambda_CSTAT
if matrice['CSTATMOY'].any():
    matrice['CSTATMOY'] = ((matrice['CSTATMOY']+1) ** lambda_CSTAT - 1) / lambda_CSTAT

mask = matrice['CAPVELIB'] != 0
matrice.loc[mask, 'CAPVELIB'] = (matrice.loc[mask, 'CAPVELIB'] * capvelib)

# mask = matrice['TTC_PPM'] != 0
# matrice.loc[mask, 'TTC_PPM'] = (matrice.loc[mask, 'TTC_PPM'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TTC_PCJ'] != 0
# matrice.loc[mask, 'TTC_PCJ'] = (matrice.loc[mask, 'TTC_PCJ'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TTC_PPS'] != 0
# matrice.loc[mask, 'TTC_PPS'] = (matrice.loc[mask, 'TTC_PPS'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TVPM'] != 0
# matrice.loc[mask, 'TVPM'] = (matrice.loc[mask, 'TVPM'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TVPC'] != 0
# matrice.loc[mask, 'TVPC'] = (matrice.loc[mask, 'TVPC'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TVPS'] != 0
# matrice.loc[mask, 'TVPS'] = (matrice.loc[mask, 'TVPS'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TATT_PPM'] != 0
# matrice.loc[mask, 'TATT_PPM'] = (matrice.loc[mask, 'TATT_PPM'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TATT_PPS'] != 0
# matrice.loc[mask, 'TATT_PPS'] = (matrice.loc[mask, 'TATT_PPS'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TATT_PCJ'] != 0
# matrice.loc[mask, 'TATT_PPS'] = (matrice.loc[mask, 'TATT_PCJ'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['TCY'] != 0
# matrice.loc[mask, 'TCY'] = (matrice.loc[mask, 'TCY'] ** lambda_COUT - 1) / lambda_COUT
# mask = matrice['CTTKKM'] != 0
# matrice.loc[mask, 'CTTKKM'] = (matrice.loc[mask, 'CTTKKM'] ** lambda_COUT - 1) / lambda_COUT
#
# mask = matrice['CTVP'] != 0
# matrice.loc[mask, 'CTVP'] = (matrice.loc[mask, 'CTVP']** lambda_COUT - 1) / lambda_COUT
#
# matrice.loc[:, 'CSTATMOY'] = ((matrice.loc[:, 'CSTATMOY'] + 1)** lambda_COUT - 1) / lambda_COUT

if n == 'scen' and idvelo == 1:
    if idBcl == 0 or iter_count != 1:
        matrice['INTCY'] = intcy
        matrice['CAPVELIB'] = capvelib
# matrice.replace([np.inf, -np.inf], 0, inplace=True)

# SAS distribution résultats
motcat100 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcat100.sas7bdat')
motcat60 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcat60.sas7bdat')
motcatseU0 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcatseU0.sas7bdat')

motcatmd_seu0 = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcatmd_seu0.sas7bdat')
motcatmd_seusum = pd.read_sas(dir_root+'\\M3_Chaine\\Modus_Python\\Other_files\\Confirmation distribution\\motcatmd_seusum.sas7bdat')

motcatmddiff = motcatmd_seusum == motcatmd_seu0
motcatmddiff.sum()

motcatdiff =  np.abs(motcat100 - motcatseU0)/motcat100
motcatdiff.mean(1).plot()
motcat100.sum().sum()



convvp = pd.read_sas('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\Donnees\\Zonage\\convvp_modus313.sas7bdat')



# Benford's law
BEN1 = pd.read_csv('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\Donnees\\Input\\2_Scenario\\2030\\121011_VSVoyTC2030ORLY_HC.txt', sep='\t')
FLUX = BEN1.Flux
FLUX = FLUX.astype('str')
FLUX2 = FLUX.str.split('.', expand=True)
FLUX3 = FLUX2[1].to_list()
FLUX4 = []
for i in FLUX3:
    for j in list(i):
        FLUX4.append(j)

from collections import Counter
import matplotlib.pyplot as plt

Benfords_law = Counter(FLUX4)
plt.bar(sorted(Benfords_law.keys()), sorted(Benfords_law.values(), key=lambda key))
plt.show()



# euTC.query(euTC.col == )
for col in list(euTC.columns):
    print(euTC.loc[euTC[col].isin([0.0229131059])])

euTC[np.abs(euTC['COL1'] - 0.0229131059) < 1e-6]


# Affectation
import win32com.client as win32
myvisum = win32.Dispatch("Visum.Visum")
myvisum.LoadVersion(dir_dataScen + '\\210219_ReseauVPv4.6_PPS2030.ver')
# MatV = Visum.Net.DemandSegments.ItemByKey("V")
# myvisum.INet.DemandSegments.GetAll()
# myvisum.Filters.InitAll
MatV = myvisum.Net.DemandSegments.ItemByKey('V')

MatV.ODMatrix = 'ModusUVP'
# myvisum.DemandSegments.GetAll()
Proc = myvisum.Procedures

DSeg_Selection= DSeg_Combo.GetValue()


links = []

for x in myvisum.Net.Links.GetAll:
    links.append(x.AttValue("NO"))  # AttValue( "Name of the attribute")

print(links)

attributeList = ["CODE", "NAME"]
for dSeg in myvisum.Net.DemandSegments.GetMultipleAttributes(attributeList):
    print(dSeg)

myvisum = None


import pywin32



# Random
import matplotlib.pyplot as plt
plt.clf()
ODvide = pd.DataFrame(ODvide)
ODvide[0].plot()

ModusUVP_tmp.loc[:, 'ZONEO'].plot()
plt.show()



M = ModusUVP

# Affectation 2ème tentative
import win32com.client as win32

import Data.VisumPy.helpers as helpers
import numpy
myvisum = win32.Dispatch("Visum.Visum")
myvisum.LoadVersion(dir_dataScen + '\\210219_ReseauVPv4.6_PPM2030.ver')
mat1 = helpers.GetODMatrix(myvisum, 'V')
mat2 = helpers.GetODMatrix(myvisum, 'P')
mat3 = helpers.GetODMatrix(myvisum, 'VI86')

mat1 = myvisum.Net.ODMatrices.ItemByKey(1).GetValues()

mat1.sum().sum()
mat2.sum().sum()
mat3.sum().sum()

type(mat1)

# Checking shapefile
import geopandas as gpd

