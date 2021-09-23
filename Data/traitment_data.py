import pandas as pd
from dataclasses import dataclass
from Data.A_CstesModus import *
from Data.fonctions_gen import *
from Quatre_Etapes import Exec_Modus



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
                ecriredavisum(CALEPL, Exec_Modus.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
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
                CALEPL_per = pd.read_csv(Mat_Calees[f'CALEPL_{per}_actuel'].path,
                                     sep=Mat_Calees[f'CALEPL_{per}_actuel'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_{per}_actuel'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL_per_scen = pd.read_csv(Mat_Calees[f'CALEPL_{per}_scen'].path,
                                         sep=Mat_Calees[f'CALEPL_{per}_scen'].sep,
                                         skiprows=Mat_Calees[f'CALEPL_{per}_scen'].skip,
                                         encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL_per = complete(CALEPL_per, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL_per = complete(CALEPL_per, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL_per_scen = complete(CALEPL_per_scen, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                # EvolPL_per = pd.merge(CALEPL_per, CALEPL_per_scen, on=['ZONEO', 'ZONED'])
                EvolPL_per = np.where(CALEPL_per['FLUX'] != 0, CALEPL_per_scen['FLUX'] / CALEPL_per['FLUX'], 1)
                CALEPL_per['FLUX'] *= EvolPL_per
                ecriredavisum(CALEPL, Exec_Modus.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
                return CALEPL_per
            elif idPL == 3:
                CALEPL = pd.read_csv(Mat_Calees[f'CALEPL_{self.per}_scen'].path,
                                     sep=Mat_Calees[f'CALEPL_{self.per}_scen'].sep,
                                     skiprows=Mat_Calees[f'CALEPL_{self.per}_scen'].skip,
                                     encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])
                CALEPL = complete(CALEPL, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
                CALEPL['FLUX'].fillna(0, inplace=True)
                ecriredavisum(CALEPL, Exec_Modus.out_mat, 'PL_S_scen', 'VP', hor[0], hor[1])
                return CALEPL
            #   4-a. Lecture et mise en forme des vecteurs spécifiques
    def vect_spec(self):
        VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = readVS(self.per, self.n, cZEmpCDG, cZEmpOrly,
                                                                      cZVoyCDG, cZVoyOrly)
        PoidsVS = pd.read_csv(Vect_spec[f'Poids_VS_{self.n}'].path, sep=Vect_spec[f'Poids_VS_{self.n}'].sep)
        PoidsVS.rename(columns={'Em_HPS': 'Em_PPS', 'Em_HPC': 'Em_PCJ', 'Em_HPM': 'Em_PPM',
                                              'Att_HPS': 'Att_PPS', 'Att_HPC': 'Att_PCJ', 'Att_HPM': 'Att_PPM'},
                                 inplace=True)
        # 4-b. Lecture et mise en forme des Poids VS :
        # 			on sépare les HPM des HPS et on créé un vecteur Poids VS de 1327 lignes
        PoidsVS = PoidsVS.loc[:, ('ZONE', f'Em_{self.per}', f'Att_{self.per}')].copy()
        return PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY
    def VSTC(self):
        VSTCCDG = pd.read_csv(Vect_spec[f'VSTC_CDG_{self.per}_{self.n}'].path,
                              sep=Vect_spec[f'VSTC_CDG_{self.per}_{self.n}'].sep)
        VSTCCDG.rename(columns={'flux': 'FLUX'}, inplace=True)
        VSTCORLY = pd.read_csv(Vect_spec[f'VSTC_ORLY_{self.per}_{self.n}'].path,
                              sep=Vect_spec[f'VSTC_ORLY_{self.per}_{self.n}'].sep)
        VSTCORLY.rename(columns={'flux': 'FLUX'}, inplace=True)
        return VSTCCDG, VSTCORLY

#     6. Lecture des vecteurs voyageurs émis et attirés par les gares TC
    def read_VGTC(self):
        VGTC = pd.read_csv(Vect_gare[f'VGTC_{self.per}_{self.n}'].path, sep=Vect_gare[f'VGTC_{self.per}_{self.n}'].path)
        return VGTC

    def read_VGVP(self):
        VGVP = pd.read_csv(Vect_gare[f'VGTC_{self.per}_{self.n}'].path, sep=Vect_gare[f'VGTC_{self.per}_{self.n}'].path)
        return VGVP


# read_mat = read_mat()
# read_mat.n = 'actuel'
# read_mat.per = 'PPS'
#
# CORDVP = read_mat.CORDVP_func()
# CORDPL = read_mat.CORDPL_func()
# CORDVP.FLUX.notna().sum()
#
# read_mat = read_mat()
# read_mat.per = 'PPS'
# read_mat.n = 'actuel'
# CALEPL = read_mat.CALEPL_func()
# CALEPL.FLUX.notna().sum()
# PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = read_mat.vect_spec()
#
# CALEPL_per
#
# CALEPL = pd.read_csv(Mat_Calees[f'CALEPL_PPS_scen'].path,
#                                      sep=Mat_Calees[f'CALEPL_PPS_scen'].sep,
#                                      skiprows=Mat_Calees[f'CALEPL_PPS_scen'].skip,
#                                      encoding='latin-1', names=['ZONEO', 'ZONED', 'FLUX'])