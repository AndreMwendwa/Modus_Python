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
        # VARGEN = PTOT PACT	PACTHQ PACTAQ RETR SCOLSUP SCOLSEC SCOLPRIM PSCOL CHOM PNACTA
        # PNACTACHO ETOT EMPHQ EMPAQ EMPCOM EMPLOI EMPACH SUP_LE SEC_LE PRIM_LE SCOL_LE dans CtesCalibr
        if self.n == 'actuel':
            Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
        elif self.n == 'scen':
            Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))
        #Pop_Emp_temp = pd.read_sas(Pop_Emp[f'{generation.n}'])
        Pop_Emp = pd.DataFrame()  # Un dataframe vide pour permettre de réorganiser le colonnes.

        for VAR in list(VARGEN):
            Pop_Emp[VAR] = Pop_Emp_temp[VAR]
        Pop_Emp.index = range(1, cNbZone + 1)  # Pour donner les mêmes indices que SAS.

        return Pop_Emp

    def EM_PAR(self):
        if self.per == 'PPM':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hpm_par.sas7bdat'))

        elif self.per == 'PCJ':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hc_par.sas7bdat'))

        elif self.per == 'PPS':
            EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                              '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hps_par.sas7bdat'))

        # On fait en sorte que les indices soient les motifs des déplacements
        EM_PAR.index = EM_PAR['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        EM_PAR = EM_PAR[VARGEN]
        return EM_PAR

    def ATT_PAR(self):
        if self.per == 'PPM':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hpm_par.sas7bdat'))
        elif self.per == 'PCJ':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hc_par.sas7bdat'))
        elif self.per == 'PPS':
            ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                                               '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hps_par.sas7bdat'))

        # On fait en sorte que les indices soient les motifs des déplacements
        ATT_PAR.index = ATT_PAR['MOTIF'].astype('int64')

        # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
        ATT_PAR = ATT_PAR[VARGEN]
        return ATT_PAR

    def use_tx(self, type):   # À remplacer par les bonnes localisation:
        # Kiko fonction avec une cc elevé
        if type == 'EM':
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
                                        , sep='\t')
        #tx_desagr = pd.read_csv(tx_desagr[f'{type}_{per}'].path, sep = tx_desagr[f'{type}_{per}'].sep)
        del tx_desagr['MOTIF']
        tx_desagr.index = range(1, 23)

        zone = pd.read_sas(os.path.join(dir_data, 'Zonage\\zone.sas7bdat'))
        zone['DPRT'] = zone['DPRT'].astype('int64')
        depts = zone['DPRT']

        depts.index = range(1, cNbZone+1)
        TX = np.ones((cNbZone, cNbMotif*cNbCat))

        for zon in range(1, cNbZone + 1):
            dep = depts[zon] - 1
            for motif in range(0, cNbMotif):
                TX[zon-1, motif] = tx_desagr.iloc[motif, dep]
                TX[zon - 1, motif+cNbMotif] = 1 - tx_desagr.iloc[motif, dep]
        return TX


# 2. Lecture des donnés interzonales


# IV. DONNES INTERZONALES
OD = pd.DataFrame(np.zeros((cNbZone,cNbZone)))
OD.columns = range(1, cNbZone+1)
OD.index = range(1, cNbZone+1)
OD = OD.stack().reset_index()
OD.map({'level_0': 'ZONEO', 'level_1 ': 'ZONED'})
OD.columns = ['ZONEO', 'ZONED', 0]

@dataclass
class calcul_util:
    per: str = ''
    n: str = ''

    def TTCM(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_M_{n}'].path, sep = Donnees_Interz[f'tps_TC_M_{n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PPM', 'TVEH_PPM', 'TMAR_PPM',
                                                'TATT_PPM', 'TACC_PPM'])

    def TTCS(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_S_{n}'].path, sep = Donnees_Interz[f'tps_TC_S_{n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PPS', 'TVEH_PPS', 'TMAR_PPS',
                                                'TATT_PPS', 'TACC_PPS'])

    def TTCC(self):
        return pd.read_csv(Donnees_Interz[f'tps_TC_C_{n}'].path, sep = Donnees_Interz[f'tps_TC_C_{n}'].sep,
                           header = 0, names = ['ZONEO', 'ZONED', 'TRAB_PCJ', 'TVEH_PCJ', 'TMAR_PCJ',
                                                'TATT_PCJ', 'TACC_PCJ'])

    def TVPM(self):
        return pd.read_csv(Donnees_Interz[f'tps_VP_M_{n}'].path, sep=Donnees_Interz[f'tps_VP_M_{n}'].sep)

    def TVPS(self):
        return pd.read_csv(Donnees_Interz[f'tps_VP_S_{n}'].path, sep=Donnees_Interz[f'tps_VP_S_{n}'].sep)

    def TVPC(self):
        return pd.read_csv(Donnees_Interz[f'tps_VP_C_{n}'].path, sep=Donnees_Interz[f'tps_VP_C_{n}'].sep)

    def DVOL(self):
        return pd.read_csv(Donnees_Interz[f'dist_vol_{n}'].path, sep=Donnees_Interz[f'dist_vol_{n}'].sep)
    def CTTC(self):
        return pd.read_csv(Donnees_Interz[f'couttc_{n}'].path, sep=Donnees_Interz[f'couttc_{n}'].sep)

calcul_util = calcul_util()
generation = generation()
calcul_util.n = 'actuel'
generation.n = 'actuel'

OD = pd.concat([calcul_util.TTCM(), calcul_util.TTCS(), calcul_util.TTCC(), calcul_util.TVPM(), calcul_util.TVPS(),
           calcul_util.TVPC(), calcul_util.DVOL(), calcul_util.CTTC()], axis = 1)

OD['CTATO'] = generation.Pop_Emp()['CSTAT']



OD = OD.loc[:,~OD.columns.duplicated()]




