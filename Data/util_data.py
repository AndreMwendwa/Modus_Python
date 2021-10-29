import pandas as pd
import numpy as np
import pickle as pkl
from dataclasses import dataclass
from Data import A_CstesModus, CstesStruct

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *
from Data.generation_data import generation

# att = ['INTTC', 'INTVP', 'INTCY', 'TR_PPM', 'TATT_PPM', 'TTC_PPM', 'TR_PPS', 'TATT_PPS', 'TTC_PPS', 'TR_PCJ',
#        'TATT_PCJ', 'TTC_PCJ', 'TVPM', 'TVPS', 'TVPC', 'TMD', 'TCY', 'CTTKKM', 'CTVP', 'CSTATMOY', 'CAPVELIB']
# 2. Lecture des donnés interzonales

# Kiko - mets tout ça dans une classe.

# IV. DONNES INTERZONALES
OD = pd.DataFrame(np.zeros((cNbZone,cNbZone)))
OD.columns = range(1, cNbZone+1)
OD.index = range(1, cNbZone+1)
OD = OD.stack().reset_index()
OD.columns = ['ZONEO', 'ZONED', 0]

# Dataclass utilisé dans la calcul utilitaire
@dataclass
class calcul_util:
    per: str = ''
    n: str = ''

    def TTCM(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_M_{self.n}'].path, sep = Donnees_Interz[f'tps_TC_M_{self.n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PPM', 'TVEH_PPM', 'TMAR_PPM',
                                                'TATT_PPM', 'TACC_PPM'])

    def TTCS(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_S_{self.n}'].path, sep = Donnees_Interz[f'tps_TC_S_{self.n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PPS', 'TVEH_PPS', 'TMAR_PPS',
                                                'TATT_PPS', 'TACC_PPS'])

    def TTCC(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_C_{self.n}'].path, sep = Donnees_Interz[f'tps_TC_C_{self.n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PCJ', 'TVEH_PCJ', 'TMAR_PCJ',
                                                'TATT_PCJ', 'TACC_PCJ'])

    def TVPM(self):
        return pd.read_csv(Donnees_Interz[f'tps_VP_M_{self.n}'].path, sep=Donnees_Interz[f'tps_VP_M_{self.n}'].sep)

    def TVPS(self):
        return pd.read_csv(Donnees_Interz[f'tps_VP_S_{self.n}'].path, sep=Donnees_Interz[f'tps_VP_S_{self.n}'].sep)

    def TVPC(self):
        df = pd.read_csv(Donnees_Interz[f'tps_VP_C_{self.n}'].path, sep=Donnees_Interz[f'tps_VP_C_{self.n}'].sep)
        return df

    def DVOL(self):
        return pd.read_csv(Donnees_Interz[f'dist_vol_{self.n}'].path, sep=Donnees_Interz[f'dist_vol_{self.n}'].sep)

    def CTTC(self):
        return pd.read_csv(Donnees_Interz[f'couttc_{self.n}'].path, sep=Donnees_Interz[f'couttc_{self.n}'].sep)

    def NBVELIB(self):
        NBVELIB = pd.read_csv(Capa_Velib[self.n].path, sep=Capa_Velib[self.n].sep)
        NBVELIB.index = range(1, cNbZone+1)
        return NBVELIB

    def CM_PAR_read(self):
        CM_PAR_df = pd.read_sas(CM_PAR_DICT[self.per])
        return CM_PAR_df


# Crée les variables utilisés dans le calcul utilitaire pour les TC
def var_TC(OD, att):
    OD_input = OD.copy()
    OD_input['INTTC'] = 1
    OD_input['TR_PPM'] = OD_input['TRAB_PPM'] + OD_input['TACC_PPM'] + OD_input['TMAR_PPM']
    del OD_input['TRAB_PPM'], OD_input['TACC_PPM'], OD_input['TMAR_PPM']
    OD_input['TR_PCJ'] = OD_input['TRAB_PCJ'] + OD_input['TACC_PCJ'] + OD_input['TMAR_PCJ']
    del OD_input['TRAB_PCJ'], OD_input['TACC_PCJ'], OD_input['TMAR_PCJ']
    OD_input['TR_PPS'] = OD_input['TRAB_PPS'] + OD_input['TACC_PPS'] + OD_input['TMAR_PPS']
    del OD_input['TRAB_PPS'], OD_input['TACC_PPS'], OD_input['TMAR_PPS']
    OD_input.rename(columns={'TVEH_PPM': 'TTC_PPM', 'TVEH_PCJ': 'TTC_PCJ', 'TVEH_PPS': 'TTC_PPS'}, inplace=True)

    OD_input[['TVPM', 'TVPC', 'TVPS', 'TMD', 'TCY', 'CTVP', 'CSTATMOY', 'CAPVELIB', 'INTCY', 'INTVP']] = 0
    OD_input2 = OD_input[att]
    return OD_input2

# Crée les variables utilisés dans le calcul utilitaire pour les VP
def var_VP(OD, att, n, idcoutvp):
    OD_input = OD.copy()
    OD_input['INTVP'] = 1
    OD_input[['TR_PPM', 'TR_PCJ', 'TR_PPS', 'TATT_PPM', 'TATT_PCJ', 'TATT_PPS', 'TTC_PPM', 'TTC_PCJ', 'TTC_PPS', 'TMD',
        'TCY', 'CTTKKM', 'CAPVELIB', 'INTTC', 'INTCY']] = 0
    OD_input['CTVP'] = 1.3 * OD_input['DVOL'] * CVPkm
    if n == 'scen' and idcoutvp == 1:
        OD_input['CTVP'] *= croiscoutVP
    OD_input2 = OD_input[att]
    return OD_input2

# Crée les variables utilisés dans le calcul utilitaire pour les MD
def var_MD(OD, att):
    OD_input = OD.copy()
    DVOL_col = OD_input.loc[:, 'DVOL'].copy()
    for col in att:
        OD_input[col] = 0
    OD_input['TMD'] = 1.3 * DVOL_col /(VMD/60)
    OD_input2 = OD_input[att]
    return OD_input2

# def var_CY(OD, att):
#     OD_input = OD.copy()
#     att2 = att.copy()
#     att2.remove('CAPVELIB')
#     DVOL_col = OD_input.loc[:, 'DVOL'].copy()
#     for col in att2:
#         OD_input[col] = 0
#     OD_input['INTCY'] = 1
#     OD_input['TCY'] = 1.3 * DVOL_col /(VCY/60)
#     OD_input2 = OD_input[att2]
#     return OD_input2

# Crée les variables utilisés dans le calcul utilitaire pour les vélos
def var_CY(OD, att):
    OD_input = OD.copy()

    DVOL_col = OD_input.loc[:, 'DVOL'].copy()
    OD_input[['INTTC', 'INTVP', 'TR_PPM', 'TR_PCJ', 'TR_PPS', 'TATT_PPM', 'TATT_PCJ', 'TATT_PPS', 'TTC_PPM', 'TTC_PCJ',
              'TTC_PPS', 'TMD', 'TVPS', 'TVPC', 'TVPM', 'CTTKKM', 'CTVP', 'CSTATMOY']] = 0
    OD_input['INTCY'] = 1
    OD_input['TCY'] = 1.3 * DVOL_col /(VCY/60)
    OD_input2 = OD_input[att]
    return OD_input2

# Crée la BDD inter- et intra-zonale
def OD(n):
    calcul_util_instance = calcul_util()
    generation_instance = generation()
    calcul_util_instance.n = n
    generation_instance.n = n

    OD = pd.concat([calcul_util_instance.TTCM(), calcul_util_instance.TTCS(), calcul_util_instance.TTCC()], axis = 1)
    OD = OD.loc[:,~OD.columns.duplicated()]
    OD.drop(OD.index[OD['ZONEO'].isin([1290, 1291.0, 1292.0, 1293.0, 1328.0, 1329.0, 1330.0, 1331.0, 1332.0, 1333.0, 1334.0,
                                       1335.0, 1336.0, 1337.0, 1338.0, 1339.0])], inplace = True)
    OD.drop(OD.index[OD['ZONED'].isin([1290, 1291.0, 1292.0, 1293.0, 1328.0, 1329.0, 1330.0, 1331.0, 1332.0, 1333.0, 1334.0,
                                       1335.0, 1336.0, 1337.0, 1338.0, 1339.0])], inplace = True)
    OD.reset_index(inplace=True)
    del OD['index']

    OD = pd.concat([OD, calcul_util_instance.TVPM(), calcul_util_instance.TVPS(), calcul_util_instance.TVPC(),
                    calcul_util_instance.DVOL(), calcul_util_instance.CTTC()], axis = 1)
    OD = OD.loc[:,~OD.columns.duplicated()]

    Pop_Emp_All_colsdf = generation_instance.Pop_Emp_All_Cols()  #Dataframe de tous les 34 colonnes, contrairement au dataframe
    # Pop-Emp, qui ne contient que 28
    Pop_Emp_All_colsdf.index = range(1, cNbZone+1)
    CSTAT = Pop_Emp_All_colsdf.CSTAT
    ClasseAcc = Pop_Emp_All_colsdf.ClasseAcc
    DENSH = Pop_Emp_All_colsdf.DENSH
    PTOT = Pop_Emp_All_colsdf.PTOT
    ETOT = Pop_Emp_All_colsdf.ETOT
    CSTAT.index = range(1, cNbZone+1)
    OD = pd.merge(OD, CSTAT, left_on='ZONEO', right_index=True, how = 'left')
    OD = pd.merge(OD, CSTAT, left_on='ZONED', right_index=True, how = 'left')
    OD['CSTATMOY'] = (OD['CSTAT_x'] + OD['CSTAT_y'])/2
    OD.rename(columns={'CSTAT_x':'CSTATO', 'CSTAT_y':'CSTATD'}, inplace=True)

    OD = pd.merge(OD, ClasseAcc, left_on='ZONEO', right_index=True, how = 'left')
    OD = pd.merge(OD, ClasseAcc, left_on='ZONED', right_index=True, how = 'left')

    OD = OD.rename(columns = {'ClasseAcc_x': 'ORCLACC', 'ClasseAcc_y': 'DESTCLACC'})

    # import de la capacité des stations vélib
    NBVELIB = calcul_util_instance.NBVELIB()
    OD = pd.merge(OD, NBVELIB['CAPA'], left_on='ZONEO', right_index=True, how='left')
    OD = pd.merge(OD, NBVELIB['NBSTAT'], left_on='ZONEO', right_index=True, how='left')
    OD = OD.rename(columns = {'CAPA': 'CAPAO', 'NBSTAT':'NBSTATO'})

    OD = pd.merge(OD, NBVELIB['CAPA'], left_on='ZONED', right_index=True, how='left')
    OD = pd.merge(OD, NBVELIB['NBSTAT'], left_on='ZONED', right_index=True, how='left')
    OD = OD.rename(columns = {'CAPA': 'CAPAD', 'NBSTAT':'NBSTATD'})

    OD['CAPVELIB'] = (OD['CAPAO'] * OD['CAPAD'])**0.5
    OD['NBVELIB'] = (OD['NBSTATO']*OD['NBSTATD'])**0.5

    del OD['CAPAO'], OD['CAPAD'], OD['NBSTATO'], OD['NBSTATD']

    # 3. Remplacement des valeurs manquantes par des 0
    OD.fillna(0, inplace=True)

    # 5. Qualité des données interzonales
    OD['QBD'] = np.where((
                         (OD['TRAB_PPM']>seuilRab)|(OD['TVEH_PPM']>seuilVeh)|(OD['TMAR_PPM']>seuilMar)|(OD['TACC_PPM']>seuilRab)|
                         (OD['TATT_PPM']>seuilAtt)|(OD['TVEH_PPM'] == 0)|
                         (OD['TRAB_PCJ']>seuilRab)|(OD['TVEH_PCJ']>seuilVeh)|(OD['TMAR_PCJ']>seuilMar)|(OD['TACC_PCJ']>seuilRab)|
                         (OD['TATT_PCJ']>seuilAtt)|(OD['TVEH_PCJ'] == 0)|
                         (OD['TRAB_PPS']>seuilRab)|(OD['TVEH_PPS']>seuilVeh)|(OD['TMAR_PPS']>seuilMar)|(OD['TACC_PPS']>seuilRab)|
                         (OD['TATT_PPS']>seuilAtt)|(OD['TVEH_PPS'] == 0)|(OD['ZONEO']==OD['ZONED'])
                          ), 0, 1)

    # OD['QBD'] = np.where((
    #                      (OD['TRAB_PPM']>seuilRab)|(OD['TVEH_PPM']>seuilVeh)|(OD['TMAR_PPM']>seuilMar)|(OD['TACC_PPM']>seuilRab)|
    #                      (OD['TATT_PPM']>seuilAtt)|(OD['TVEH_PPM'] == 0)
    #                     ), 0, 1)
    # OD['QBD'] = np.where(((OD['TRAB_PCJ']>seuilRab)|(OD['TVEH_PCJ']>seuilVeh)|(OD['TMAR_PCJ']>seuilMar)|(OD['TACC_PCJ']>seuilRab)|
    #                      (OD['TATT_PCJ']>seuilAtt)|(OD['TVEH_PCJ'] == 0)
    #                     ), 0, 1)
    #                      (OD['TRAB_PPS']>seuilRab)|(OD['TVEH_PPS']>seuilVeh)|(OD['TMAR_PPS']>seuilMar)|(OD['TACC_PPS']>seuilRab)|
    #                      (OD['TATT_PPS']>seuilAtt)|(OD['TVEH_PPS'] == 0)|
    #                      (OD['ZONEO']==OD['ZONED'])
    #                       ), 0, 1)


    # 6. Agrégation des données zonales utiles pour la BDD interzonale
    OD = pd.merge(OD, DENSH, left_on='ZONEO', right_index=True, how='left')
    OD = OD.rename(columns = {'DENSH': 'DENSHO'})
    OD = pd.merge(OD, DENSH, left_on='ZONED', right_index=True, how='left')
    OD = pd.merge(OD, PTOT, left_on='ZONED', right_index=True, how='left')
    OD = pd.merge(OD, ETOT, left_on='ZONED', right_index=True, how='left')
    OD = OD.rename(columns = {'DENSH': 'DENSHD', 'PTOT':'PTOTD', 'ETOT': 'ETOTD'})
    OD.fillna(0, inplace=True)
    OD.replace(np.nan, 0, inplace=True)
    # OD.drop(OD.index[OD['ZONEO'].isin([1290, 1291.0, 1292.0, 1293.0, 1328.0, 1329.0, 1330.0, 1331.0, 1332.0, 1333.0, 1334.0,
    #                                    1335.0, 1336.0, 1337.0, 1338.0, 1339.0])], inplace = True)
    # OD.drop(OD.index[OD['ZONED'].isin([1290, 1291.0, 1292.0, 1293.0, 1328.0, 1329.0, 1330.0, 1331.0, 1332.0, 1333.0, 1334.0,
    #                                    1335.0, 1336.0, 1337.0, 1338.0, 1339.0])], inplace = True)

    # IV. DONNEES INTRAZONALES
    # - a. identification des 3 zones les plus proches au départ d'une zone
    # Trouver les trois zones les plus proches, sans faire d'itération, plutôt en utilisant les opérations de pandas.
    OD_sans_intra = OD[OD['ZONEO'] != OD['ZONED']]
    OD1 = OD_sans_intra.sort_values(by=['DVOL'])
    OD1ST = OD1.drop_duplicates(subset='ZONEO', keep='first')
    OD1 = OD1[~OD1.isin(OD1ST)].dropna()
    OD2ND = OD1.drop_duplicates(subset='ZONEO', keep='first')
    OD1 = OD1[~OD1.isin(OD2ND)].dropna()
    OD3RD = OD1.drop_duplicates(subset='ZONEO', keep='first')

    OD_proche_dvol = pd.concat([OD1ST, OD2ND, OD3RD], axis = 0)
    OD_proche_dvol = OD_proche_dvol.sort_values(by = ['ZONEO'])
    # Kiko -> Beaucoup des résultats sont 0 pour la DVOL -> est-ce qu'il y a un problème?

    # - b. calcul d'une distance caractéristique et du temps intrazonal d'après MODUSv2.0
    DCAR = OD_proche_dvol.groupby(by = 'ZONEO').mean().loc[:, 'DVOL']
    DINTRA = 0.09*np.sqrt(Pop_Emp_All_colsdf['STOT']) + 0.2*np.sqrt(Pop_Emp_All_colsdf['SBAT']) + 0.05

    # -  Calcul des temps minimaux au départ d'une zone : préciser "Tab" en 1ère lecture des tempsVP, puis à chaque iter

    def TVPMIN(type):
        OD1 = OD_sans_intra.sort_values(by=[f'TVP{type}'])
        OD1ST = OD1.drop_duplicates(subset='ZONEO', keep='first')
        OD1 = OD1[~OD1.isin(OD1ST)].dropna()
        OD2ND = OD1.drop_duplicates(subset='ZONEO', keep='first')
        OD1 = OD1[~OD1.isin(OD2ND)].dropna()
        OD3RD = OD1.drop_duplicates(subset='ZONEO', keep='first')

        OD_proche_temps = pd.concat([OD1ST, OD2ND, OD3RD], axis = 0)
        OD_proche_temps = OD_proche_temps.sort_values(by = ['ZONEO'])
        TCAR = OD_proche_temps.groupby(by = 'ZONEO').mean().loc[:, f'TVP{type}']
        return TCAR

    def prepare_TVPintra():
        TVPMCAR = TVPMIN('M')
        TVPSCAR = TVPMIN('S')
        TVPCCAR = TVPMIN('C')
        TVPINTRA = pd.concat([TVPMCAR, TVPSCAR, TVPCCAR], axis = 1)
        TVPINTRA['TVPM'] *= DINTRA/DCAR     # temps HPM intra par "homothétie"
        TVPINTRA['TVPS'] *= DINTRA / DCAR   # temps HPS intra par "homothétie"
        TVPINTRA['TVPC'] *= DINTRA / DCAR   # temps HC intra par "homothétie"
        TVPINTRA.fillna(value=0, inplace=True)
        #TVPINTRA = TVPINTRA[TVPINTRA.notna().any(axis = 1)]     # Kiko - > On se retrouve finalement avec une série de
        # colonnes difficiles à expliquer. Pourquoi 0 à 1273 ?
        return TVPINTRA

    def prepare_TTCintra():
        OD_sans_intra2 = OD[(OD['ZONEO'] != OD['ZONED']) & (OD['TVEH_PPM'] != 0)]
        OD1 = OD_sans_intra2.sort_values(by=['DVOL'])
        OD1ST = OD1.drop_duplicates(subset='ZONEO', keep='first')
        OD1 = OD1[~OD1.isin(OD1ST)].dropna()
        OD2ND = OD1.drop_duplicates(subset='ZONEO', keep='first')
        OD1 = OD1[~OD1.isin(OD2ND)].dropna()
        OD3RD = OD1.drop_duplicates(subset='ZONEO', keep='first')
        # OD1 = OD1[~OD1.isin(OD3RD)].dropna()
        # OD4TH = OD1.drop_duplicates(subset='ZONEO', keep='first')
        OD_proche_dvol = pd.concat([OD1ST, OD2ND, OD3RD], axis=0)
        # OD_proche_dvol = pd.concat([OD1ST, OD2ND, OD3RD, OD4TH], axis=0)

        OD_proche_TTC = OD_proche_dvol.sort_values(by=['ZONEO'])
        OD_proche_TTC['TTOT'] = OD_proche_TTC['TRAB_PPM'] + OD_proche_TTC['TVEH_PPM'] + OD_proche_TTC['TATT_PPM'] + \
                                OD_proche_TTC['TMAR_PPM'] + OD_proche_TTC['TACC_PPM']
        # OD_proche_TTC['TTOTS'] = OD_proche_TTC['TRAB_PPS'] + OD_proche_TTC['TVEH_PPS'] + OD_proche_TTC['TATT_PPS'] + \
        #                         OD_proche_TTC['TMAR_PPS'] + OD_proche_TTC['TACC_PPS']
        #
        # OD_proche_TTC = OD_proche_TTC.sort_values(by = ['TTOT', 'TTOTS'])
        OD_proche_TTC = OD_proche_TTC.sort_values(by=['TTOT'])
        OD_proche_TTC = OD_proche_TTC.drop_duplicates(subset='ZONEO', keep='first')
        OD_proche_TTC = OD_proche_TTC.sort_values(by = ['ZONEO'])
        TTCINTRA = OD_proche_TTC[['ZONEO', 'TRAB_PPM', 'TVEH_PPM', 'TMAR_PPM', 'TATT_PPM', 'TACC_PPM', 'TRAB_PPS', 'TVEH_PPS',
                                 'TMAR_PPS', 'TATT_PPS', 'TACC_PPS', 'TRAB_PCJ', 'TVEH_PCJ', 'TMAR_PCJ', 'TATT_PCJ',
                                  'TACC_PCJ']].copy()
        # TTCINTRA.loc[:, 'TACC_PPM'] = TTCINTRA['TRAB_PPM']
        TTCINTRA[['TACC_PPM', 'TACC_PCJ', 'TACC_PPS']] = TTCINTRA[['TRAB_PPM', 'TRAB_PCJ', 'TRAB_PPS']]
        # TTCINTRA = TTCINTRA.sort_values(by = ['ZONEO'])
        return TTCINTRA

    TVPINTRA = prepare_TVPintra()
    TTCINTRA = prepare_TTCintra()
    TVPINTRA.index = TVPINTRA.index.astype('int64')
    TTCINTRA['ZONEO'] = TTCINTRA['ZONEO'].astype('int64')
    TTCINTRA.index = TTCINTRA['ZONEO']
    del TTCINTRA['ZONEO']
    list_cols_TTC = list(TTCINTRA.columns)

    # for index, row in OD.iterrows():
    #     if row['ZONEO'] == row['ZONED']:
    #         row['DVOL'] = DINTRA[row['ZONEO']]
    #         row[['TVPM', 'TVPS', 'TVPC']] = TVPINTRA.loc[row['ZONEO'], ['TVPM', 'TVPS', 'TVPC']]
    #         row[list_cols_TTC] = TTCINTRA.loc[row['ZONEO'], list_cols_TTC]
    # OD.reset_index(inplace = True)
    # del OD['index']

    OD.index = OD['ZONEO']
    # OD['DVOL'].where(OD['ZONEO'] == OD['ZONED'], DINTRA, OD['DVOL'])


    OD.loc[OD['ZONEO'] == OD['ZONED'], 'DVOL'] = DINTRA
    OD.loc[OD['ZONEO'] == OD['ZONED'], ['TVPM', 'TVPS', 'TVPC']] = TVPINTRA
    OD.loc[OD['ZONEO'] == OD['ZONED'], list_cols_TTC] = TTCINTRA
    del OD['ZONEO']
    OD.reset_index(inplace=True)
    dbfile = open(f'{dir_dataTemp}bdinter_{n}', 'wb')
    pkl.dump(OD, dbfile)
    dbfile.close()
    return OD

if __name__ == '__main__':
    # OD('actuel')
    OD('scen')
