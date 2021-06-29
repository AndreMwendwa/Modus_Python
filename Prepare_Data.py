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
        '''# VARGEN = PTOT PACT	PACTHQ PACTAQ RETR SCOLSUP SCOLSEC SCOLPRIM PSCOL CHOM PNACTA
        # PNACTACHO ETOT EMPHQ EMPAQ EMPCOM EMPLOI EMPACH SUP_LE SEC_LE PRIM_LE SCOL_LE dans CtesCalibr
        if self.n == 'actuel':
        #Attention! n est la variable d'instance ici, pas la variable de classe.
            Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
        elif self.n == 'scen':
            Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))'''

        Pop_Emp_temp = pd.read_sas(Pop_Emp[self.n])
        Pop_Emp_df = pd.DataFrame()  # Un dataframe vide pour permettre de réorganiser le colonnes.

        for VAR in list(VARGEN):
            Pop_Emp_df[VAR] = Pop_Emp_temp[VAR]
        Pop_Emp_df.index = range(1, cNbZone + 1)  # Pour donner les mêmes indices que SAS.

        return Pop_Emp_df

    def EM_PAR(self):
        '''if self.per == 'PPM':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hpm_par.sas7bdat'))

        elif self.per == 'PCJ':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hc_par.sas7bdat'))

        elif self.per == 'PPS':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hps_par.sas7bdat'))'''

        # On fait en sorte que les indices soient les motifs des déplacements
        EM_PAR_df = pd.read_sas(EM_PAR[self.per])
        EM_PAR_df.index = EM_PAR_df['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        EM_PAR_df = EM_PAR_df[VARGEN]
        return EM_PAR_df

    def ATT_PAR(self):
        '''if self.per == 'PPM':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hpm_par.sas7bdat'))
        elif self.per == 'PCJ':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hc_par.sas7bdat'))
        elif self.per == 'PPS':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hps_par.sas7bdat'))'''

        # On fait en sorte que les indices soient les motifs des déplacements
        ATT_PAR_df = pd.read_sas(ATT_PAR[self.per])
        ATT_PAR_df.index = ATT_PAR_df['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        ATT_PAR_df = ATT_PAR_df[VARGEN]
        return ATT_PAR_df

    def use_tx(self, type):   # À remplacer par les bonnes localisation:
        # Kiko fonction avec une cc elevé
        '''if type == 'EM':
            if self.per == 'PPM':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                        '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hpm.txt')
                                        , sep = '\t')
                # Kiko - C'est quoi la différence entre tx_desagr_em1 et tx_desagr_em2 ?
            elif self.per == 'PCJ':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hc.txt')
                                            , sep='\t')
            elif self.per == 'PPS':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hps.txt')
                                        , sep='\t')

        if type == 'ATT':
            if self.per == 'PPM':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                        '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hpm.txt')
                                        , sep = '\t')
            elif self.per == 'PCJ':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hc.txt')
                                        , sep='\t')
            elif self.per == 'PPS':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hps.txt')
                                        , sep='\t')'''
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
        temp_df = pd.read_sas(Pop_Emp[self.n])
        CSTAT = temp_df.CSTAT
        ClasseAcc = temp_df.ClasseAcc
        DENSH = temp_df.DENSH
        PTOT = temp_df.PTOT
        ETOT = temp_df.ETOT
        CSTAT.index = range(1, cNbZone+1)
        ClasseAcc.index = range(1, cNbZone + 1)
        DENSH.index = range(1, cNbZone+1)
        PTOT.index = range(1, cNbZone+1)
        ETOT.index = range(1, cNbZone + 1)
        return CSTAT, ClasseAcc, DENSH, PTOT, ETOT



# 2. Lecture des donnés interzonales

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
        return pd.read_csv(Donnees_Interz[f'tps_VP_C_{self.n}'].path, sep=Donnees_Interz[f'tps_VP_C_{self.n}'].sep)

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

CSTAT, ClasseAcc, DENSH, PTOT, ETOT = generation.Pop_Emp_All_Cols()
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
# Trouver les trois zones les plus proches, sans faire d'itération, plutôt en utilisant les opérations de pandas.
OD1 = OD.sort_values(by=['DVOL'])
OD1ST = OD1.drop_duplicates(subset='ZONEO', keep='first')
#OD1ST.sort_values(by=['ZONEO'], inplace = True)
OD1 = OD1[~OD1.isin(OD1ST)].dropna()
#Repeat to get second and third closest.
# OD3 = OD1.loc[OD2.index]
# cond = OD3['Email'].isin(df2['Email'])
# OD1 = OD1.sort_values(by=['DVOL'])
OD2ND = OD1.drop_duplicates(subset='ZONEO', keep='first')
OD1 = OD1[~OD1.isin(OD2ND)].dropna()
OD3RD = OD1.drop_duplicates(subset='ZONEO', keep='first')

OD_3_proches = pd.concat([OD1ST, OD2ND, OD3RD], axis = 0)
OD_3_proches = OD_3_proches.sort_values(by = ['ZONEO'])
# Kiko -> Beaucoup des résultats sont 0 pour la DVOL -> est-ce qu'il y a un problème?

DCAR = OD_3_proches.groupby(by = 'ZONEO').mean().loc[:, 'DVOL']




#Kiko -> groupby DVOL mean




