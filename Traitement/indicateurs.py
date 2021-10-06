import pickle as pkl
import pandas as pd
import numpy as np
from Data import A_CstesModus, CstesStruct
from Data.A_CstesModus import *
from Data.fonctions_gen import *
import pickle as pkl
from pathlib import Path

# I. MATRICES MODUS
dbfile = open(f'{dir_dataTemp}Classe', 'rb')
Classe = pkl.load(dbfile)



# 1. Préparation des tables d'analyse des matrices MODUS
def treat_modus(n, hor):
    # Lecture des fichiers.
    dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'rb')
    Modus_MD_motcat = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'rb')
    Modus_VP_motcat = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'rb')
    Modus_CY_motcat = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'rb')
    Modus_TC_motcat = pkl.load(dbfile)
    # Kiko - Eventuellement ces fichiers auront hor et n dans leurs noms.

    dbfile = open(f'{dir_dataTemp}bdinter', 'rb')
    bdinter = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}Modus_motcat_{n}_{hor}', 'rb')
    Modus_motcat = pkl.load(dbfile)
    Modus_motcat = pd.DataFrame(Modus_motcat @ Duplication.T)

    # - a. Agrégation des matrices MODUS TM, TC, VP, MD, CY
    def merge_mat(RES_df, mat, mode):
        tmp_somme = mat.sum(1)
        RES_df = pd.concat([RES_df, tmp_somme], axis=1)
        RES_df.rename(columns={0: mode}, inplace=True)
        return RES_df

    def somme_mat(SOMME, mat, mode):
        tmp_somme = mat.sum(0)
        SOMME = pd.concat([SOMME, tmp_somme], axis=1)
        SOMME.rename(columns={0: mode}, inplace=True)
        return SOMME

    def motif_mat(M):
        M_res = M.iloc[:, 0] + M.iloc[:, cNbMotifC - 1]
        for i in range(1, cNbMotifC):
            for j in range(1, cNbCat):
                M_res = pd.concat([M_res, (M.iloc[:, i] + M.iloc[:, i + cNbMotifC * j])], axis=1)
                M_res.columns = range(i + 1)
        return M_res


    RES = pd.DataFrame(ODvide_func(cNbZone), columns=['ZONEO', 'ZONED'])
    RES = merge_mat(RES, Modus_motcat, 'TM')
    RES = merge_mat(RES, Modus_MD_motcat, 'MD')
    RES = merge_mat(RES, Modus_VP_motcat, 'VP')
    RES = merge_mat(RES, Modus_CY_motcat, 'CY')
    RES = merge_mat(RES, Modus_TC_motcat, 'TC')
    RES = pd.concat([RES, Classe['Classe_carte']], axis=1)

    dbfile = open(f'{dir_dataTemp}RES_Modus', 'wb')
    pkl.dump(RES, dbfile)
    dbfile.close()

    SOMME = pd.concat([Modus_MD_motcat.sum(0), Modus_VP_motcat.sum(0)], axis=1)
    SOMME.columns = ['MD', 'VP']
    SOMME = somme_mat(SOMME, Modus_CY_motcat, 'CY')
    SOMME = somme_mat(SOMME, Modus_TC_motcat, 'TC')

    # Dictionnaire pour stocker le résultat des déplacements par motif et mode.
    Modus_motcat_mode_combin = {}

    Modus_MD_motcat_combin = motif_mat(Modus_MD_motcat)
    Modus_VP_motcat_combin = motif_mat(Modus_VP_motcat)
    Modus_CY_motcat_combin = motif_mat(Modus_CY_motcat)
    Modus_TC_motcat_combin = motif_mat(Modus_TC_motcat)
    Modus_TC_motcat_combin = pd.concat([Modus_TC_motcat_combin, Classe['Classe_carte']], axis=1)

    for i in range(cNbMotifC):
        Modus_motcat_mode_combin[i + 1] = pd.DataFrame(ODvide_func(cNbZone), columns=['ZONEO', 'ZONED'])
        Modus_motcat_mode_combin[i + 1]['MD'] = Modus_MD_motcat_combin[i]
        Modus_motcat_mode_combin[i + 1]['VP'] = Modus_VP_motcat_combin[i]
        Modus_motcat_mode_combin[i + 1]['CY'] = Modus_TC_motcat_combin[i]
        Modus_motcat_mode_combin[i + 1]['TC'] = Modus_TC_motcat_combin[i]
        Modus_motcat_mode_combin[i + 1]['Classe'] = Classe['Classe_carte']

    #  Dictionnaire pour stocker les résultats par motif.
    Modus_motcat_combin = {}
    for i in range(cNbMotifC):
        Modus_motcat_combin[i + 1] = pd.DataFrame(ODvide_func(cNbZone), columns=['ZONEO', 'ZONED'])
        Modus_motcat_combin[i + 1] = pd.concat([Modus_motcat_combin[i + 1], Modus_motcat_mode_combin[i + 1]['MD']], axis=1)
        Modus_motcat_combin[i + 1].rename(columns={'MD': 'FLUX'}, inplace=True)
        Modus_motcat_combin[i + 1]['FLUX'] += Modus_motcat_mode_combin[i + 1]['VP']
        Modus_motcat_combin[i + 1]['FLUX'] += Modus_motcat_mode_combin[i + 1]['CY']
        Modus_motcat_combin[i + 1]['FLUX'] += Modus_motcat_mode_combin[i + 1]['TC']

    #  - b. Traitement par classe de portée
    Flux_cl = RES.groupby(by='Classe_carte').sum()
    Flux_cl.drop(labels=['ZONEO', 'ZONED'], inplace=True, axis=1)
    Flux_cl.index = range(1, 9)

#     - Traitement par motif
    PartTC = SOMME['TC']/SOMME.sum(1)
    PartVP = SOMME['VP'] / SOMME.sum(1)
    PartCY = SOMME['CY'] / SOMME.sum(1)
    PartMD = SOMME['MD'] / SOMME.sum(1)


#     - c. Traitement par portée et temps
    bdinter.rename(columns={'TVPM':'TVP_PPM', 'TVPC':'TVP_PCJ', 'TVPS':'TVP_PPS'}, inplace=True)
    DTM = bdinter['DVOL'] * RES['TM']
    DVP = bdinter['DVOL'] * RES['VP']
    TVP = bdinter[f'TVP_{hor}'] * RES['VP']
    DTC = bdinter['DVOL'] * RES['TC']
    TTC = (bdinter[f'TRAB_{hor}'] + bdinter[f'TVEH_{hor}'] + bdinter[f'TMAR_{hor}'] +
           bdinter[f'TATT_{hor}'] + bdinter[f'TACC_{hor}']) * RES['TC']
    DMD = bdinter['DVOL'] * RES['MD']
    TMD = 1.3 * bdinter['DVOL']/(VMD/60) * RES['MD']
    DCY = bdinter['DVOL'] * RES['CY']
    TCY = 1.3 * bdinter['DVOL'] / (VCY / 60) * RES['CY']

    # Mode TC
    D_moy_TC = DTC/RES['TC']
    T_moy_TC = TTC / RES['TC']
    V_moy_TC = D_moy_TC / T_moy_TC * 60

    # Mode VP
    D_moy_VP = DVP / RES['VP']
    T_moy_VP = TVP / RES['VP']
    V_moy_VP = D_moy_VP / T_moy_VP * 60

    # Mode CY
    D_moy_CY = DCY / RES['CY']
    T_moy_CY = TCY / RES['CY']
    V_moy_CY = D_moy_CY / T_moy_CY * 60

    # Mode MD
    D_moy_MD = DMD / RES['MD']
    T_moy_MD = TMD / RES['MD']
    V_moy_MD = D_moy_MD / T_moy_MD * 60

    # Tous les modes
    D_moy_TM = DTM / RES['TM']
    T_moy_TM = (TTC + TVP + TCY + TMD) / RES['TM']
    V_moy_TM = D_moy_TM / T_moy_TM * 60

    def EMATT_Zone(RES):
        from Data.traitment_data import read_mat
        read_mat = read_mat()
        read_mat.n = 'actuel'
        read_mat.per = hor

        if idVP > 0:
            UVP_df = read_mat.CALEUVP()
        else:
            dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_scen', 'rb')
            UVP_df = pkl.load(dbfile)
        RES = pd.merge(RES, UVP_df, left_on=['ZONEO', 'ZONED'], right_on=['ZONEO', 'ZONED'])
        RES.rename(columns={'FLUX': 'FLUXVP'}, inplace=True)

        if idTC > 0:
            TC_df = read_mat.CALETC()
        else:
            dbfile = open(f'{dir_dataTemp}ModusTC_df{H}_scen', 'rb')
            TC_df = pkl.load(dbfile)
        RES = pd.merge(RES, TC_df, left_on=['ZONEO', 'ZONED'], right_on=['ZONEO', 'ZONED'])
        RES.rename(columns={'FLUX': 'FLUXTC'}, inplace=True)










# - d. Création de la table d'émissions et d'attraction par zone et par mode
    return {'TC': PartTC, 'VP': PartVP, 'MD': PartMD, 'CY': PartCY}


def incic_modus(n, hor):
    from Data.generation_data import generation
    generation = generation()
    generation.n = n
    generation.per = hor
    # - a. Calcul de la mobilité

    # -- Mobilité simulée
    MOB = np.zeros((10, 4))

    BDZone = generation.Pop_Emp()
    list_col_pop = ['PTOT', 'PACT', 'SCOLSEC', 'PACTHQ', 'PACTAQ', 'SCOLPRIM', 'SCOLSEC', 'SCOLSUP', 'PACT', 'PINACT']
    Pop = BDZone.loc[:, list_col_pop]
    MOB[:, 0] = Pop.sum(0)
    MOB[8, 0] = MOB[8, 0] + MOB[7, 0]
    MOB[9, 0] = MOB[9, 0] + MOB[5, 0] + MOB[6, 0]

    list_col_emp = ['ETOT', 'SCOL_LE', 'SCOL_LE', 'EMPHQ', 'EMPAQ', 'PRIM_LE', 'SEC_LE', 'SUP_LE', 'EMPACH', 'EMPCOM']

    Emp = BDZone.loc[:, list_col_emp]
    MOB[:, 1] = Emp.sum(0)

    dbfile = open(f'{dir_dataTemp}RES_Modus', 'rb')
    RES = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}Modus_motcat_{n}_{hor}', 'rb')
    Modus_motcat = pd.DataFrame(pkl.load(dbfile))

    MOB[0, 2] = RES['TM'].sum()
    MOB[1, 2] = Modus_motcat.iloc[:, [0, 1, 14, 15]].sum().sum()
    MOB[2, 2] = Modus_motcat.iloc[:, [2, 16]].sum().sum()
    MOB[3, 2] = Modus_motcat.iloc[:, [3, 17, 5, 19]].sum().sum()
    MOB[4, 2] = Modus_motcat.iloc[:, [4, 18, 6, 20]].sum().sum()
    MOB[5, 2] = Modus_motcat.iloc[:, [7, 21]].sum().sum()
    MOB[6, 2] = Modus_motcat.iloc[:, [8, 22]].sum().sum()
    MOB[7, 2] = Modus_motcat.iloc[:, [9, 23]].sum().sum()
    MOB[8, 2] = Modus_motcat.iloc[:, [10, 11, 24, 25]].sum().sum()
    MOB[9, 2] = Modus_motcat.iloc[:, [12, 13, 26, 27]].sum().sum()

    MOB[:, 3] = MOB[:, 2]/MOB[:, 0]

    # b. Calcul des parts modales
    FLUXTOT = RES['TM'].sum()
    PART = {}
    PART['TC'] = RES['TC'].sum() / FLUXTOT
    PART['VP'] = RES['VP'].sum() / FLUXTOT
    PART['CY'] = RES['CY'].sum() / FLUXTOT
    PART['MD'] = RES['MD'].sum() / FLUXTOT

    # - c. Calcul des parts modales motorisées
    PART_MOT = {}
    PART_MOT['TC'] = RES['TC'].sum()/(RES['TC'].sum() + RES['VP'].sum())
    PART_MOT['VP'] = RES['TC'].sum() / (RES['TC'].sum() + RES['VP'].sum())

    # 2-b. Indicateurs numériques des émissions et attractions par zone
    def EMATT_Evol(hor):
        dbfile = open(f'{dir_dataTemp}gen_results_actuel_{hor}', 'rb')
        gen_results_actuel = pkl.load(dbfile)
        EM_actuel = gen_results_actuel['EM']
        ATT_actuel = gen_results_actuel['ATT']

        dbfile = open(f'{dir_dataTemp}gen_results_scen_{hor}', 'rb')
        gen_results_scen = pkl.load(dbfile)
        EM_scen = gen_results_scen['EM']
        ATT_scen = gen_results_scen['ATT']

    def MOT_CL_EVOL(hor):



