import pandas as pd
import numpy as np
from dataclasses import dataclass
from Data import A_CstesModus, CstesStruct

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)
from Data.A_CstesModus import *
from Data.CstesStruct import *


# I. LECTURE DES DONNEES


# 1. Lecture des données zonales

@dataclass
class generation:
    per: str = ''
    n: str = ''

    # Création du fichier P + E à partir des fichiers individuels de données zonales.

    def Pop_Emp(self):
        OS = pd.read_csv(Donnees_Zonales[f'OS_{self.n}'].path, sep=Donnees_Zonales[f'OS_{self.n}'].sep)
        Surf = pd.read_csv(Donnees_Zonales[f'Surf_{self.n}'].path, sep=Donnees_Zonales[f'Surf_{self.n}'].sep)
        CTSTAT = pd.read_csv(Donnees_Zonales[f'CTSTAT_{self.n}'].path, sep=Donnees_Zonales[f'CTSTAT_{self.n}'].sep)
        # VELIB = pd.read_csv(Donnees_Zonales[f'VELIB_{self.n}'].path, sep=Donnees_Zonales[f'VELIB_{self.n}'].sep)
        AccessTC = pd.read_csv(Donnees_Zonales[f'AccessTC_{self.n}'].path,
                               sep=Donnees_Zonales[f'AccessTC_{self.n}'].sep)
        Zone = pd.read_sas(f'{dir_zonage}\\zone.sas7bdat')
        BDZonetemp = pd.concat([OS, Surf.iloc[:, 1:], CTSTAT.iloc[:, 1:]], axis=1)
        BDZonetemp['DENSH'] = (BDZonetemp['PTOT'] + BDZonetemp['ETOT']) / BDZonetemp['SBAT']
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 35) & (AccessTC['DPOPSECT'] > 16000), 1, 0)
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 35) & (AccessTC['DPOPSECT'] > 16000), 2,
                                           BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 50) & (AccessTC['DPOPSECT'] > 8000)
                                           & (AccessTC['DPOPSECT'] <= 16000), 3, BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 50) & (AccessTC['DPOPSECT'] > 8000)
                                           & (AccessTC['DPOPSECT'] <= 16000), 4, BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 90) & (AccessTC['DPOPSECT'] <= 8000), 5,
                                           BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 90) & (AccessTC['DPOPSECT'] <= 8000), 6,
                                           BDZonetemp['ClasseAcc'])
        Pop_Emp_temp = pd.concat([BDZonetemp, Zone['DPRT']], axis=1)

        # Pop_Emp_temp = pd.read_sas(Pop_Emp[self.n])
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
        OS = pd.read_csv(Donnees_Zonales[f'OS_{self.n}'].path, sep=Donnees_Zonales[f'OS_{self.n}'].sep)
        Surf = pd.read_csv(Donnees_Zonales[f'Surf_{self.n}'].path, sep=Donnees_Zonales[f'Surf_{self.n}'].sep)
        CTSTAT = pd.read_csv(Donnees_Zonales[f'CTSTAT_{self.n}'].path, sep=Donnees_Zonales[f'CTSTAT_{self.n}'].sep)
        # VELIB = pd.read_csv(Donnees_Zonales[f'VELIB_{self.n}'].path, sep=Donnees_Zonales[f'VELIB_{self.n}'].sep)
        AccessTC = pd.read_csv(Donnees_Zonales[f'AccessTC_{self.n}'].path, sep=Donnees_Zonales[f'AccessTC_{self.n}'].sep)
        Zone = pd.read_sas(f'{dir_zonage}\\zone.sas7bdat')
        BDZonetemp = pd.concat([OS, Surf.iloc[:, 1:], CTSTAT.iloc[:, 1:]], axis=1)
        BDZonetemp['DENSH'] = (BDZonetemp['PTOT'] + BDZonetemp['ETOT'])/BDZonetemp['SBAT']
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 35) & (AccessTC['DPOPSECT'] > 16000), 1, 0)
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 35) & (AccessTC['DPOPSECT'] > 16000), 2,
                                           BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 50) & (AccessTC['DPOPSECT'] > 8000)
                                           & (AccessTC['DPOPSECT'] <= 16000), 3, BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 50) & (AccessTC['DPOPSECT'] > 8000)
                                           & (AccessTC['DPOPSECT'] <= 16000), 4, BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] <= 90) & (AccessTC['DPOPSECT'] <= 8000), 5,
                                           BDZonetemp['ClasseAcc'])
        BDZonetemp['ClasseAcc'] = np.where((AccessTC['TTCACC'] > 90) & (AccessTC['DPOPSECT'] <= 8000), 6,
                                           BDZonetemp['ClasseAcc'])
        BDZonetemp = pd.concat([BDZonetemp, Zone['DPRT']], axis=1)
        return BDZonetemp

if __name__ == '__main__':
    # generation = generation()
    # generation.n = 'actuel'
    # generation.per = 'PPM'
    # a0 = generation.Pop_Emp_All_Cols()
    # a1 = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
    # a2 = set(a0.columns).symmetric_difference(set(a1.columns))
    # assert np.abs(a0 - a1).sum().sum() <= 1e-10

    generation = generation()
    generation.n = 'scen'
    generation.per = 'PPM'
    a0 = generation.Pop_Emp_All_Cols()
    a1 = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))
    a2 = set(a0.columns).symmetric_difference(set(a1.columns))
    diff = np.abs(a0 - a1).sum().sum()
    assert diff <= 1e-10