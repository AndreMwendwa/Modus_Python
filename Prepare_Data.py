import pandas as pd
import numpy as np
from dataclasses import dataclass
import os
from collections import defaultdict
import CstesStruct
import A_CstesModus

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from A_CstesModus import *
from CstesStruct import *


# I. LECTURE DES DONNEES


# 1. Lecture des donnés zonales

@dataclass
class generation:
# Kiko -> can perhaps be done like the other dataclass, with instead of if statements, a dictionary with names and,
# based on what is entered as n and per different values are read.
    per: str = ''
    n: str = ''

    def Pop_Emp(self):

        Pop_Emp_temp = pd.read_sas(Pop_Emp[self.n])
        Pop_Emp_df = pd.DataFrame()  # Un dataframe vide pour permettre de réorganiser le colonnes.

        for VAR in list(VARGEN):
            Pop_Emp_df[VAR] = Pop_Emp_temp[VAR]
        Pop_Emp_df.index = range(1, cNbZone + 1)  # Pour donner les mêmes indices que SAS.

        return Pop_Emp_df

    def EM_PAR(self):

        # On fait en sorte que les indices soient les motifs des déplacements
        EM_PAR_df = pd.read_sas(EM_PAR[self.per])
        EM_PAR_df.index = EM_PAR_df['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        EM_PAR_df = EM_PAR_df[VARGEN]
        return EM_PAR_df

    def ATT_PAR(self):

        # On fait en sorte que les indices soient les motifs des déplacements
        ATT_PAR_df = pd.read_sas(ATT_PAR[self.per])
        ATT_PAR_df.index = ATT_PAR_df['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        ATT_PAR_df = ATT_PAR_df[VARGEN]
        return ATT_PAR_df

    def use_tx(self, type):   # À remplacer par les bonnes localisation:
        # Kiko fonction avec une cc elevé
        tx_desagr_df = pd.read_csv(tx_desagr[f'{type}_{self.per}'].path, sep = tx_desagr[f'{type}_{self.per}'].sep)
        del tx_desagr_df['MOTIF']
        tx_desagr_df.index = range(1, 23)

        zone = pd.read_sas(os.path.join(dir_data, 'Zonage\\zone.sas7bdat'))
        zone['DPRT'] = zone['DPRT'].astype('int64')
        depts = zone['DPRT']

        depts.index = range(1, cNbZone+1)
        TX = np.ones((cNbZone, cNbMotif*cNbCat))

        for zon in range(1, cNbZone + 1):
            dep = depts[zon] - 1
            for motif in range(0, cNbMotif):
                TX[zon-1, motif] = tx_desagr_df.iloc[motif, dep]
                TX[zon - 1, motif+cNbMotif] = 1 - tx_desagr_df.iloc[motif, dep]
        return TX

    def Pop_Emp_All_Cols(self):
        Pop_Emp_df = pd.read_sas(Pop_Emp[self.n])
        return Pop_Emp_df




'''# 2. Lecture des donnés interzonales

# Kiko - mets tout ça dans une classe.

# IV. DONNES INTERZONALES
OD = pd.DataFrame(np.zeros((cNbZone,cNbZone)))
OD.columns = range(1, cNbZone+1)
OD.index = range(1, cNbZone+1)
OD = OD.stack().reset_index()
OD.columns = ['ZONEO', 'ZONED', 0]

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
        df.rename(columns={"TVPM":"TVPC"}, inplace=True)
        return df

    def DVOL(self):
        return pd.read_csv(Donnees_Interz[f'dist_vol_{self.n}'].path, sep=Donnees_Interz[f'dist_vol_{self.n}'].sep)

    def CTTC(self):
        return pd.read_csv(Donnees_Interz[f'couttc_{self.n}'].path, sep=Donnees_Interz[f'couttc_{self.n}'].sep)

    def NBVELIB(self):
        NBVELIB = pd.read_csv(Capa_Velib[self.n].path, sep=Capa_Velib[self.n].sep)
        NBVELIB.index = range(1, cNbZone+1)
        return NBVELIB

calcul_util = calcul_util()
generation = generation()
calcul_util.n = 'actuel'
generation.n = 'actuel'

OD = pd.concat([calcul_util.TTCM(), calcul_util.TTCS(), calcul_util.TTCC(), calcul_util.TVPM(), calcul_util.TVPS(),
           calcul_util.TVPC(), calcul_util.DVOL(), calcul_util.CTTC()], axis = 1)
OD = OD.loc[:,~OD.columns.duplicated()]

Pop_Emp_All_colsdf = generation.Pop_Emp_All_Cols()  #Dataframe de tous les 34 colonnes, contrairement au dataframe
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
OD['CSTAT'] = (OD['CSTAT_x'] + OD['CSTAT_y'])/2
del OD['CSTAT_x'], OD['CSTAT_y']

OD = pd.merge(OD, ClasseAcc, left_on='ZONEO', right_index=True, how = 'left')
OD = pd.merge(OD, ClasseAcc, left_on='ZONED', right_index=True, how = 'left')

OD = OD.rename(columns = {'ClasseAcc_x': 'ORCLACC', 'ClasseAcc_y': 'DESTCLACC'})

# import de la capacité des stations vélib
NBVELIB = calcul_util.NBVELIB()
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
                     (OD['TATT_PPS']>seuilAtt)|(OD['TVEH_PPS'] == 0)
                      ), 0, 1)


# 6. Agrégation des données zonales utiles pour la BDD interzonale
OD = pd.merge(OD, DENSH, left_on='ZONEO', right_index=True, how='left')
OD = OD.rename(columns = {'DENSH': 'DENSHO'})
OD = pd.merge(OD, DENSH, left_on='ZONED', right_index=True, how='left')
OD = pd.merge(OD, PTOT, left_on='ZONED', right_index=True, how='left')
OD = pd.merge(OD, ETOT, left_on='ZONED', right_index=True, how='left')
OD = OD.rename(columns = {'DENSH': 'DENSHD', 'PTOT':'PTOTD', 'ETOT': 'ETOTD'})
OD.fillna(0, inplace=True)
OD.replace(np.nan, 0, inplace=True)

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

OD_3_proches = pd.concat([OD1ST, OD2ND, OD3RD], axis = 0)
OD_3_proches = OD_3_proches.sort_values(by = ['ZONEO'])
# Kiko -> Beaucoup des résultats sont 0 pour la DVOL -> est-ce qu'il y a un problème?

# - b. calcul d'une distance caractéristique et du temps intrazonal d'après MODUSv2.0
DCAR = OD_3_proches.groupby(by = 'ZONEO').mean().loc[:, 'DVOL']
DINTRA = 0.09*np.sqrt(Pop_Emp_All_colsdf['STOT']) + 0.2*np.sqrt(Pop_Emp_All_colsdf['SBAT']) + 0.05

# -  Calcul des temps minimaux au départ d'une zone : préciser "Tab" en 1ère lecture des tempsVP, puis à chaque iter

def TVPMIN(type):
    OD1 = OD_sans_intra.sort_values(by=[f'TVP{type}'])
    OD1ST = OD1.drop_duplicates(subset='ZONEO', keep='first')
    OD1 = OD1[~OD1.isin(OD1ST)].dropna()
    OD2ND = OD1.drop_duplicates(subset='ZONEO', keep='first')
    OD1 = OD1[~OD1.isin(OD2ND)].dropna()
    OD3RD = OD1.drop_duplicates(subset='ZONEO', keep='first')

    OD_3_proches = pd.concat([OD1ST, OD2ND, OD3RD], axis = 0)
    OD_3_proches = OD_3_proches.sort_values(by = ['ZONEO'])
    TCAR = OD_3_proches.groupby(by = 'ZONEO').mean().loc[:, f'TVP{type}']
    return TCAR

def prepare_TVPintra(n):
    TVPMCAR = TVPMIN('M')
    TVPSCAR = TVPMIN('S')
    TVPCCAR = TVPMIN('C')
    TVPINTRA = pd.concat([TVPMCAR, TVPSCAR, TVPCCAR], axis = 1)
    TVPINTRA['TVPM'] *= DINTRA/DCAR     # temps HPM intra par "homothétie"
    TVPINTRA['TVPS'] *= DINTRA / DCAR   # temps HPS intra par "homothétie"
    TVPINTRA['TVPC'] *= DINTRA / DCAR   # temps HC intra par "homothétie"
    TVPINTRA = TVPINTRA[TVPINTRA.notna().any(axis = 1)]     # Kiko - > On se retrouve finalement avec une série de
    # colonnes difficiles à expliquer. Pourquoi 0 à 1273 ?

def prepare_TTCintra(n):


#Kiko -> groupby DVOL mean'''




