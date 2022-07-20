'''Created to deal with the problem of a circular import afflicting the read_mat that was in traitement_data'''

import pandas as pd
from dataclasses import dataclass
from Data.fonctions_gen import *


@dataclass
class read_mat:
    per: str = ''
    n: str = ''


    def CORDVP_func(self):
        CORDVP = pd.read_csv(Mat_Calees[f'CORDVP_{self.per}_{self.n}'].path,
                              sep=Mat_Calees[f'CORDVP_{self.per}_{self.n}'].sep,
                              skiprows=Mat_Calees[f'CORDVP_{self.per}_{self.n}'].skip,
                             encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
        # ODVide = ODvide_func_b(cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
        # CORDVP = pd.merge(ODVide, CORDVP, on=['ZONEO', 'ZONED'], how='outer')
        CORDVP = complete(CORDVP, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
        CORDVP['FLUX'].fillna(0, inplace=True)
        CORDVP = CORDVP.loc[(CORDVP['ZONEO'] > cNbZone + cNbZspec)|(CORDVP['ZONED'] > cNbZone + cNbZspec), :]
        return CORDVP

    def CORDPL_func(self):
        CORDPL = pd.read_csv(Mat_Calees[f'CORDPL_{self.per}_{self.n}'].path,
                              sep=Mat_Calees[f'CORDPL_{self.per}_{self.n}'].sep,
                              skiprows=Mat_Calees[f'CORDPL_{self.per}_{self.n}'].skip,
                             encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
        CORDPL = complete(CORDPL, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
        CORDPL['FLUX'].fillna(0, inplace=True)
        CORDPL = CORDPL.loc[(CORDPL['ZONEO'] > cNbZone + cNbZspec)|(CORDPL['ZONED'] > cNbZone + cNbZspec), :]
        return CORDPL

    def CALEPL_func(self):
        if self.per == 'PPM':
            hor = (6.00, 10.00)
        elif self.per == 'PCJ':
            hor = (10.00, 16.00)
        else:
            hor = (16.00, 20.00)
        if self.n == 'scen':
            if idPL == 1:
                CALEPL = pd.read_csv(Mat_Calees[f'CALEPL_{self.per}_actuel'].path,
                                     sep=Mat_Calees[f'CALEPL_{self.per}_actuel'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_{self.per}_actuel'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL = complete(CALEPL, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL['FLUX'].fillna(0, inplace=True)
                CALEPL['FLUX'] = CALEPL['FLUX'] * (1 + CroisPIB/100) ** (scen - actuel)
                # Kiko - Waiting for SAS licence to run %ecriredavisum to see what it does.
                ecriredavisum(CALEPL, Quatre_Etapes.main.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
                return CALEPL
            elif idPL == 2:
                CALEPL = pd.read_csv(Mat_Calees[f'CALEPL_J_actuel'].path,
                                     sep=Mat_Calees[f'CALEPL_J_actuel'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_J_actuel'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL_scen = pd.read_csv(Mat_Calees[f'CALEPL_J_scen'].path,
                                     sep=Mat_Calees[f'CALEPL_J_scen'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_J_scen'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL = complete(CALEPL, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL_scen = complete(CALEPL_scen, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                # EvolPL = pd.merge(CALEPL, CALEPL_scen, on=['ZONEO', 'ZONED'])
                EvolPL = np.where(CALEPL['FLUX'] != 0, CALEPL_scen['FLUX']/CALEPL['FLUX'], 1)
                # Kiko - I think only one of these two calcs should be applied, but which one !!??
                CALEPL_per = pd.read_csv(Mat_Calees[f'CALEPL_{self.per}_actuel'].path,
                                     sep=Mat_Calees[f'CALEPL_{self.per}_actuel'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_{self.per}_actuel'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL_per_scen = pd.read_csv(Mat_Calees[f'CALEPL_{self.per}_scen'].path,
                                         sep=Mat_Calees[f'CALEPL_{self.per}_scen'].sep,
                                         skiprows=Mat_Calees[f'CALEPL_{self.per}_scen'].skip,
                                         encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL_per = complete(CALEPL_per, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL_per = complete(CALEPL_per, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                # CALEPL_per_scen = complete(CALEPL_per_scen, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL_per_scen = complete(CALEPL_per_scen, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1,
                                           cNbZext, 1)
                # EvolPL_per = pd.merge(CALEPL_per, CALEPL_per_scen, on=['ZONEO', 'ZONED'])
                EvolPL_per = np.where(CALEPL_per['FLUX'] != 0, CALEPL_per_scen['FLUX'] / CALEPL_per['FLUX'], 1)
                CALEPL_per['FLUX'] *= EvolPL_per
                # ecriredavisum(CALEPL, Quatre_Etapes.main.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
                # Pas besoin d'ecriredavisum, car on travaille directement avec l'API de VISUM pour mettre les flux dedans.
                return CALEPL_per['FLUX'].to_numpy().reshape(cNbZtot, cNbZtot)
            elif idPL == 3:
                CALEPL = pd.read_csv(Mat_Calees[f'CALEPL_{self.per}_scen'].path,
                                     sep=Mat_Calees[f'CALEPL_{self.per}_scen'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_{self.per}_scen'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL = complete(CALEPL, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL['FLUX'].fillna(0, inplace=True)
                ecriredavisum(CALEPL, Quatre_Etapes.main.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
                return CALEPL