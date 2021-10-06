import os
from datetime import date

import numpy
import numpy as np
import pandas as pd

from Data.A_CstesModus import *

# Fonctions copiées du fichier des Macros

# Générer la table ODvide {ZONEO ZONED} de taille voulue (indicateur size)
#     la numérotation peut être discontinue
#       size = 1 : ODvide pour matrice totale ZoneModus+VS+Cordons
#       size = 2 : Odvide pour matrice carrée ZoneModus+VS
#       size = 3 : ODvide(1)-ODvide(2)

# def complete(tblin, tblout,cNbZone,cDebZSpec,cNbZSpec,cDebZext,cNbZext,size):
#     ODVide = ODvide_func_b()

#   per =  heure de pointe : PPM ou PPS
# 	n = horizon de travail
# 	ZoneEmpCDG = numéro de la zone spécifique emploi de CDG
# 	ZoneEmpOrly = numéro de la zone spécifique emploi de Orly

def ODvide_func_b(cNbZone,cDebZSpec,cNbZspec,cDebZext,cNbZext,size):
    if size == 1:
        m = cNbZone + cNbZspec + cNbZext
        n = cNbZone + cNbZspec + cNbZext
        ODvide = np.ones((n * m, 2))
        for i in range(m):
            for j in range(n):
                k = (i) * m + j
                ODvide[k, 0] = i + 1
                ODvide[k, 1] = j + 1
    elif size == 2:
        m = cNbZone + cNbZspec
        n = cNbZone + cNbZspec
        ODvide = np.ones((n * m, 2))
        for i in range(m):
            for j in range(n):
                k = (i) * m + j
                ODvide[k, 0] = i + 1
                ODvide[k, 1] = j + 1
    elif size == 3:
        m = cNbZspec + cNbZext
        n = cNbZspec + cNbZext
        ODvide = np.ones((n * m, 2))
        for i in range(m):
            for j in range(n):
                k = (i) * m + j
                ODvide[k, 0] = i + cDebZext + 1
                ODvide[k, 1] = j + cDebZext + 1
    return pd.DataFrame(ODvide, columns=['ZONEO', 'ZONED'])


def complete(tblin, cNbZone,cDebZSpec,cNbZSpec,cDebZext,cNbZext,size):
    ODVide = ODvide_func_b(cNbZone,cDebZSpec,cNbZSpec,cDebZext,cNbZext,size)
    tblout = pd.merge(ODVide, tblin, on=['ZONEO', 'ZONED'], how='outer')
    tblout.fillna(0, inplace=True)
    return tblout


def ecriredavisum(base, dir, nom, type, hor1, hor2):
    # base: matrice sous format SAS en 3 colonnes O D FLUX
    # 	dir: répertoire de stockage (sans " ")
    # 	nom: nom du fichier de sortie sans l'extension
    # 	type: VP ou TC
    dateentiere = date.today().strftime("%d/%m/%Y")
    #     a. Cas VP
    if type == 'VP':
        with open(os.path.join(dir, f'{nom}.fma'), 'w') as f:
            f.writelines(["$OMR;D3", '\n* NumMoyenTr', '\n4', '\n* De  A', '\n', str(hor1), ', ', str(hor2), '* Fact', '\n1.00', '\n*',
                          '\n* NumMoyenTr 4', '\n*    3 MoyenTr TC', '\n*    4 MoyenTr TI',
                          "\n* DRIEA Direction Régionale et Interdépartementale de l'Equipement et de l'Aménagement",
                          '\n', * dateentiere, ' \n'])
            f.close()
        base.to_csv(os.path.join(dir, f'{nom}.fma'), mode='a', index=False, header=False)


def readVS(per, n, ZoneEmpCDG, ZoneEmpOrly, ZoneVoyCDG, ZoneVoyOrly):
    VS = pd.read_csv(Vect_spec[f'VS_{per}_{n}'].path, sep=Vect_spec[f'VS_{per}_{n}'].sep)

    VStot = VS.loc[VS['ZONEADP'] != VS['Zone']].groupby(by = 'Nom').sum().loc[:, ('Flux_Em', 'Flux_Att')]
    VStot.reset_index(inplace=True)

    VS_Emp_CDG = VS.loc[VS['ZONEADP'] == ZoneEmpCDG, ('Zone', 'Flux_Em', 'Flux_Att')]
    VS_Emp_CDG.reset_index(inplace=True)
    VS_Emp_ORLY = VS.loc[VS['ZONEADP'] == ZoneEmpOrly, ('Zone', 'Flux_Em', 'Flux_Att')]
    VS_Emp_ORLY.reset_index(inplace=True)
    VS_Voy_CDG = VS.loc[VS['ZONEADP'] == ZoneVoyCDG, ('Zone', 'Flux_Em', 'Flux_Att')]
    VS_Voy_CDG.reset_index(inplace=True)
    VS_Voy_ORLY = VS.loc[VS['ZONEADP'] == ZoneVoyOrly, ('Zone', 'Flux_Em', 'Flux_Att')]
    VS_Voy_ORLY.reset_index(inplace=True)

    VS1 = VS.rename(columns={'ZONEADP': 'ZONEO', 'Zone': 'ZONED', 'Flux_Em': 'FLUX'}).loc[:, ('ZONEO', 'ZONED', 'FLUX')]
    VS2 = VS.rename(columns={'ZONEADP': 'ZONED', 'Zone': 'ZONEO', 'Flux_Att': 'FLUX'}).loc[:,
          ('ZONEO', 'ZONED', 'FLUX')]
    VS = pd.concat([VS1, VS2])
    VS.sort_values(by=['ZONEO', 'ZONED'], inplace=True)
    VS.drop_duplicates(subset=['ZONEO', 'ZONED'], inplace=True)

    if IdcorADP == 1:
        VStot[['corCDG_Em', 'corCDG_Att']] = 0
        if per == 'PPM':
            VStot.loc[VStot['Nom'] == 'CDG', 'corCDG_Em'] = (6100 * 0.97 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) \
                                                      / VStot.loc[VStot['Nom'] == 'CDG', 'Flux_Em']
            # 6100 UVP/h émis par la plateforme en HPM 2018 dans l'étude d'impact
            VStot.loc[VStot['Nom'] == 'CDG', 'corCDG_Att'] = (7840 * 0.93 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) \
                                                      / VStot.loc[VStot['Nom'] == 'CDG', 'Flux_Att']
            # 7840 UVP/h attirés par la plateforme en HPM 2018 dans l'étude d'impact
        elif per == 'PPS':
            VStot.loc[VStot['Nom'] == 'CDG', 'corCDG_Em'] = (7680 * 0.97 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) \
                                                      / VStot.loc[VStot['Nom'] == 'CDG', 'Flux_Em']
            VStot.loc[VStot['Nom'] == 'CDG', 'corCDG_Att'] = (4910 * 0.93 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) \
                                                       / VStot.loc[VStot['Nom'] == 'CDG', 'Flux_Att']
        VS.loc[(VS['ZONEO'] == 1290) | (VS['ZONEO'] == 1291), 'FLUX'] *= VStot.loc[0, 'corCDG_Em']
        VS.loc[(VS['ZONED'] == 1290) | (VS['ZONED'] == 1291), 'FLUX'] *= VStot.loc[0, 'corCDG_Att']

        VS_Emp_CDG.loc[:, 'Flux_Em'] *= VStot.loc[0, 'corCDG_Em']
        VS_Emp_CDG.loc[:, 'Flux_Att'] *= VStot.loc[0, 'corCDG_Att']
        VS.reset_index(inplace=True, drop=True)
    # VS = VS[['ZONEO', 'ZONED', 'FLUX']].copy()

    return VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY

# # Kiko - 17_09_21 il semble qu'on n'a plus besoin de ce macro
# def corVSADP(per):
#     if n == 'actuel':
#         if per == 'PPM':
#             corCDG_Em = (6100 * 0.97 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) / Flux_Em   # 6100 UVP/h émis par
#             # la plateforme en HPM 2018 dans l'étude d'impact
#             corCDG_Att = (7840 * 0.93 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) / Flux_Att  # 7840 UVP/h attirés
#             # par la plateforme en HPM 2018 dans l'étude d'impact
#         elif per == 'PPS':
#             corCDG_Em = (7680 * 0.97 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) / Flux_Em  # 7680 UVP/h émis par
#             # la plateforme en HPM 2018 dans l'étude d'impact
#             corCDG_Att = (4910 * 0.93 / (92.7 + 70.8) * (EmpCDGactuel + PaxCDGactuel)) / Flux_Att  # 4910 UVP/h attirés
#             # par la plateforme en HPM 2018 dans l'étude d'impact
#     elif n == 'scen':
#         if per == 'PPM':
#             corCDG_Em = (6100 * 0.97 / (92.7 + 70.8) * (EmpCDGscen + PaxCDGscen)) / Flux_Em   # 6100 UVP/h émis par
#             # la plateforme en HPM 2018 dans l'étude d'impact
#             corCDG_Att = (7840 * 0.93 / (92.7 + 70.8) * (EmpCDGscen + PaxCDGscen)) / Flux_Att  # 7840 UVP/h attirés
#             # par la plateforme en HPM 2018 dans l'étude d'impact
#         elif per == 'PPS':
#             corCDG_Em = (7680 * 0.97 / (92.7 + 70.8) * (EmpCDGscen + PaxCDGscen)) / Flux_Em  # 7680 UVP/h émis par
#             # la plateforme en HPM 2018 dans l'étude d'impact
#             corCDG_Att = (4910 * 0.93 / (92.7 + 70.8) * (EmpCDGscen + PaxCDGscen)) / Flux_Att  # 4910 UVP/h attirés
#             # par la plateforme en HPM 2018 dans l'étude d'impact

# Kiko - Qu'est-ce que ce macro essaye de faire?

# def retranche_VS(M,VS1,VS2,Zones1,Zones2,Zemp1,Zemp2,Poids):




# Brouillons

# VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = readVS('PPM', 'actuel', cZEmpCDG, cZEmpOrly, cZVoyCDG, cZVoyOrly)
def ODvide_func(n):
    ODvide = np.ones((n**2, 2))
    for i in range(n):
        for j in range(n):
            k = (i) * n + j
            ODvide[k, 0] = i + 1
            ODvide[k, 1] = j + 1
    return ODvide