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
