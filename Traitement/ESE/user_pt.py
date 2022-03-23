import pickle as pkl
import pandas as pd
from pathlib import Path
from Data.A_CstesModus import *


def user_pt_fn(fichier1, fichier2):
    # Les BDD interzonales pour les deux scénarios
    dbfile = open(f'{Path(fichier1)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    bdinter1 = pkl.load(dbfile)
    dbfile = open(f'{Path(fichier2)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    bdinter2 = pkl.load(dbfile)

    user_pt_somme = 0    # On initialize pour rajouter chaque période séparément
    if PPM:
    # Les flux interzonales pour les deux scénarios
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/ModusTC_PPM_scen'), 'rb')
        TC_PPM = pkl.load(dbfile)
        Temps_in_veh2 = pd.merge(TC_PPM, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh2 = Temps_in_veh2.loc[:, ['FLUX', 'TVEH_PPM', 'TMAR_PPM', 'TATT_PPM', 'TACC_PPM']]
        IVT_PPM = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TVEH_PPM']).sum()
        Wait_PPM = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TATT_PPM'] * yaml_content['multiplier_wait']).sum()
        Access_PPM = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TACC_PPM'] * yaml_content['multiplier_access']).sum()
        Transfer_PPM = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TMAR_PPM'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare2 = IVT_PPM + Wait_PPM + Access_PPM + Transfer_PPM

        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/ModusTC_PPM_scen'), 'rb')
        TC_PPM = pkl.load(dbfile)
        Temps_in_veh1 = pd.merge(TC_PPM, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh1 = Temps_in_veh1.loc[:, ['FLUX', 'TVEH_PPM', 'TMAR_PPM', 'TATT_PPM', 'TACC_PPM']]
        IVT_PPM = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TVEH_PPM']).sum()
        Wait_PPM = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TATT_PPM'] * yaml_content['multiplier_wait']).sum()
        Access_PPM = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TACC_PPM'] * yaml_content['multiplier_access']).sum()
        Transfer_PPM = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TMAR_PPM'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare1 = IVT_PPM + Wait_PPM + Access_PPM + Transfer_PPM

        somme_intermediare = somme_intermediare2 - somme_intermediare1
        user_pt_somme += somme_intermediare  # On ajoute la somme des différences de temps
    if PCJ:
    # Les flux interzonales pour les deux scénarios
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/ModusTC_PCJ_scen'), 'rb')
        TC_PCJ = pkl.load(dbfile)
        Temps_in_veh2 = pd.merge(TC_PCJ, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh2 = Temps_in_veh2.loc[:, ['FLUX', 'TVEH_PCJ', 'TMAR_PCJ', 'TATT_PCJ', 'TACC_PCJ']]
        IVT_PCJ = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TVEH_PCJ']).sum()
        Wait_PCJ = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TATT_PCJ'] * yaml_content['multiplier_wait']).sum()
        Access_PCJ = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TACC_PCJ'] * yaml_content['multiplier_access']).sum()
        Transfer_PCJ = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TMAR_PCJ'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare2 = IVT_PCJ + Wait_PCJ + Access_PCJ + Transfer_PCJ
    
        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/ModusTC_PCJ_scen'), 'rb')
        TC_PCJ = pkl.load(dbfile)
        Temps_in_veh1 = pd.merge(TC_PCJ, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh1 = Temps_in_veh1.loc[:, ['FLUX', 'TVEH_PCJ', 'TMAR_PCJ', 'TATT_PCJ', 'TACC_PCJ']]
        IVT_PCJ = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TVEH_PCJ']).sum()
        Wait_PCJ = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TATT_PCJ'] * yaml_content['multiplier_wait']).sum()
        Access_PCJ = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TACC_PCJ'] * yaml_content['multiplier_access']).sum()
        Transfer_PCJ = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TMAR_PCJ'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare1 = IVT_PCJ + Wait_PCJ + Access_PCJ + Transfer_PCJ
    
        somme_intermediare = somme_intermediare2 - somme_intermediare1
        user_pt_somme += somme_intermediare  # On ajoute la somme des différences de temps

    if PPS:
    # Les flux interzonales pour les deux scénarios
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/ModusTC_PPS_scen'), 'rb')
        TC_PPS = pkl.load(dbfile)

        Temps_in_veh2 = pd.merge(TC_PPS, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh2 = Temps_in_veh2.loc[:, ['FLUX', 'TVEH_PPS', 'TMAR_PPS', 'TATT_PPS', 'TACC_PPS']]
        IVT_PPS = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TVEH_PPS']).sum()
        Wait_PPS = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TATT_PPS'] * yaml_content['multiplier_wait']).sum()
        Access_PPS = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TACC_PPS'] * yaml_content['multiplier_access']).sum()
        Transfer_PPS = (Temps_in_veh2['FLUX'] * Temps_in_veh2['TMAR_PPS'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare2 = IVT_PPS + Wait_PPS + Access_PPS + Transfer_PPS
    
        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/ModusTC_PPS_scen'), 'rb')
        TC_PPS = pkl.load(dbfile)
        Temps_in_veh1 = pd.merge(TC_PPS, bdinter1, on=['ZONEO', 'ZONED'])
        Temps_in_veh1 = Temps_in_veh1.loc[:, ['FLUX', 'TVEH_PPS', 'TMAR_PPS', 'TATT_PPS', 'TACC_PPS']]
        IVT_PPS = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TVEH_PPS']).sum()
        Wait_PPS = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TATT_PPS'] * yaml_content['multiplier_wait']).sum()
        Access_PPS = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TACC_PPS'] * yaml_content['multiplier_access']).sum()
        Transfer_PPS = (Temps_in_veh1['FLUX'] * Temps_in_veh1['TMAR_PPS'] * yaml_content['multiplier_transfer']).sum()
        somme_intermediare1 = IVT_PPS + Wait_PPS + Access_PPS + Transfer_PPS
    
        somme_intermediare = somme_intermediare2 - somme_intermediare1
        user_pt_somme += somme_intermediare  # On ajoute la somme des différences de temps

    user_pt_somme /= 60 ** 2         # Valeurs de bdinter en sécondes
    # TODO: Ca n'a aucun sens. Avec ces valeurs divisés par 3600 on obtient des effets tellement minimes
    #  pour la valeur du temps.

    user_pt_time ={}         # Valeur du temps pour les usagers des TC
    user_pt_time[list_cols_ESE.Item] = 'VTTS - passenger trips (TC)'
    user_pt_time[list_cols_ESE.Diff_scenarios] = user_pt_somme * yaml_content['taux_occupation']
    user_pt_time[list_cols_ESE.Val_tutelaires] = yaml_content['VTTS']
    user_pt_time = pd.Series(user_pt_time)
    user_pt_time[list_cols_ESE.Val_econ] = user_pt_time[list_cols_ESE.Val_tutelaires] * user_pt_time[list_cols_ESE.Diff_scenarios]
    return pd.DataFrame(user_pt_time)

if __name__ == '__main__':
    f1 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite'
    f2 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite'
    user_pt_fn(f1, f2)
