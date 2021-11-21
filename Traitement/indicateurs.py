from dotmap import DotMap
from Data.fonctions_gen import *
import pickle as pkl

# I. MATRICES MODUS




# 1. Préparation des tables d'analyse des matrices MODUS
from Quatre_Etapes.dossiers_simul import dir_dataTemp


def treat_modus(n, hor):
    dbfile = open(f'{dir_dataTemp}Classe', 'rb')
    Classe = pkl.load(dbfile)
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

    dbfile = open(f'{dir_dataTemp}bdinter_{n}', 'rb')
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
    DTM = (bdinter['DVOL'] * RES['TM']).sum()
    DVP = (bdinter['DVOL'] * RES['VP']).sum()
    TVP = (bdinter[f'TVP_{hor}'] * RES['VP']).sum()
    DTC = (bdinter['DVOL'] * RES['TC']).sum()
    TTC = ((bdinter[f'TRAB_{hor}'] + bdinter[f'TVEH_{hor}'] + bdinter[f'TMAR_{hor}'] +
           bdinter[f'TATT_{hor}'] + bdinter[f'TACC_{hor}']) * RES['TC']).sum()
    DMD = (bdinter['DVOL'] * RES['MD']).sum()
    TMD = (1.3 * bdinter['DVOL']/(VMD/60) * RES['MD']).sum()
    DCY = (bdinter['DVOL'] * RES['CY']).sum()
    TCY = (1.3 * bdinter['DVOL'] / (VCY / 60) * RES['CY']).sum()

    #  Dictionnaire de stockage des résultats
    portee = {}

    # Mode TC
    portee['TC'] = {}
    portee['TC']['D_moy_TC'] = DTC/RES['TC'].sum()
    portee['TC']['T_moy_TC'] = TTC / RES['TC'].sum()
    portee['TC']['V_moy_TC'] = portee['TC']['D_moy_TC'] / portee['TC']['T_moy_TC'] * 60

    # Mode VP
    portee['VP'] = {}
    portee['VP']['D_moy_VP'] = DVP / RES['VP'].sum()
    portee['VP']['T_moy_VP'] = TVP / RES['VP'].sum()
    portee['VP']['V_moy_VP'] = portee['VP']['D_moy_VP'] / portee['VP']['T_moy_VP'] * 60

    # Mode CY
    portee['CY'] = {}
    portee['CY']['D_moy_CY'] = DCY / RES['CY'].sum()
    portee['CY']['T_moy_CY'] = TCY / RES['CY'].sum()
    portee['CY']['V_moy_CY'] = portee['CY']['D_moy_CY'] / portee['CY']['T_moy_CY'] * 60

    # Mode MD
    portee['MD'] = {}
    portee['MD']['D_moy_MD'] = DMD / RES['MD'].sum()
    portee['MD']['T_moy_MD'] = TMD / RES['MD'].sum()
    portee['MD']['V_moy_MD'] = portee['MD']['D_moy_MD'] / portee['MD']['T_moy_MD'] * 60

    # Tous les modes
    portee['TM'] = {}
    portee['TM']['D_moy_TM'] = DTM / RES['TM'].sum()
    portee['TM']['T_moy_TM'] = (TTC + TVP + TCY + TMD) / RES['TM'].sum()
    portee['TM']['V_moy_TM'] = portee['TM']['D_moy_TM'] / portee['TM']['T_moy_TM'] * 60

    #  Pickling des portées
    dbfile = open(f'{dir_dataTemp}portee_{n}_{hor}', 'wb')
    pkl.dump(portee, dbfile)
    dbfile.close()

    def EMATT_Zone(n, hor):
        from Data.traitment_data import read_mat
        read_mat = read_mat()
        read_mat.n = 'actuel'
        read_mat.per = hor

        if idVP > 0:
            if n == 'actuel':
                UVP_df = read_mat.CALEUVP()
                UVP_df = UVP_df[(UVP_df['ZONEO'] <= cNbZintsp) & (UVP_df['ZONED'] <= cNbZintsp)]
                UVP_df = UVP_df['FLUX'].to_numpy().reshape((cNbZintsp, cNbZintsp))
            else:
                dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{hor}_scen', 'rb')
                UVP_df = pkl.load(dbfile)
                UVP_df = UVP_df[:cNbZintsp, :cNbZintsp]
        else:
            dbfile = open(f'{dir_dataTemp}ModusUVP_df{hor}_scen', 'rb')
            UVP_df = pkl.load(dbfile)
            UVP_df = UVP_df[(UVP_df['ZONEO'] <= cNbZintsp) & (UVP_df['ZONED'] <= cNbZintsp)]
            UVP_df = UVP_df['FLUX'].to_numpy().reshape((cNbZintsp, cNbZintsp))
        UVP_df2 = pd.DataFrame(UVP_df.reshape(cNbZintsp ** 2))
        # RES = pd.merge(RES, UVP_df, left_on=['ZONEO', 'ZONED'], right_on=['ZONEO', 'ZONED'])
        # RES.rename(columns={'FLUX': 'FLUXVP'}, inplace=True)

        if idTC > 0:
            if n == 'actuel':
                TC_df = read_mat.CALETC()
                TC_df = TC_df[(TC_df['ZONEO'] <= cNbZintsp) & (TC_df['ZONED'] <= cNbZintsp)]
                TC_df = TC_df['FLUX'].to_numpy().reshape((cNbZintsp, cNbZintsp))
            else:
                dbfile = open(f'{dir_dataTemp}MODUSCaleTC_{hor}_scen', 'rb')
                TC_df = pkl.load(dbfile)
                TC_df = TC_df[:cNbZintsp, :cNbZintsp]
        else:
            dbfile = open(f'{dir_dataTemp}ModusTC_df{hor}_scen', 'rb')
            TC_df = pkl.load(dbfile)
            TC_df = TC_df[(TC_df['ZONEO'] <= cNbZintsp) & (TC_df['ZONED'] <= cNbZintsp)]
            TC_df = TC_df['FLUX'].to_numpy().reshape((cNbZintsp, cNbZintsp))

        TC_df2 = pd.DataFrame(TC_df.reshape(cNbZintsp ** 2))
        EmAtt = pd.DataFrame(range(cNbZintsp))

        EmAtt = pd.DataFrame(TC_df.sum(0))
        EmAtt = pd.concat([EmAtt, pd.Series(TC_df.sum(1)), pd.Series(UVP_df.sum(0)), pd.Series(UVP_df.sum(1))], axis=1)
        EmAtt.columns = ['ATTTC', 'EMTC', 'ATTVP', 'EMVP']
        EmAtt = EmAtt[['EMTC', 'EMVP', 'ATTTC', 'ATTVP']]
        # Pickling de EmAtt
        dbfile = open(f'{dir_dataTemp}EmAtt_{n}_{hor}', 'wb')
        pkl.dump(EmAtt, dbfile)
        dbfile.close()

        # # Kiko - pourquoi on a FLUXVP, FLUXTC définis de deux manières différentes ?
        # RES = pd.concat([RES, UVP_df2, TC_df2], axis=1)
        # RES.rename(columns={0: 'FLUXVP', 1: 'FLUXTC'}, inplace=True)

    EMATT_Zone(n, hor)

    dbfile = open(f'{dir_dataTemp}RES_{n}_{hor}', 'wb')
    pkl.dump(RES, dbfile)
    dbfile.close()

        # RES = pd.merge(RES, TC_df, left_on=['ZONEO', 'ZONED'], right_on=['ZONEO', 'ZONED'])
        # RES.rename(columns={'FLUX': 'FLUXTC'}, inplace=True)


        # #  Kiko - temporaire, basé sur ma compréhension actuel de ce que fait Ematt_Zone.
        # UVP_df = UVP_df[(UVP_df['ZONEO'] <= cNbZone)&(UVP_df['ZONED'] <= cNbZone)]
        # UVP_df = UVP_df['FLUX'].to_numpy().reshape((cNbZone, cNbZone))
        # TC_df = TC_df[(TC_df['ZONEO'] <= cNbZone) & (TC_df['ZONED'] <= cNbZone)]
        # TC_df = TC_df['FLUX'].to_numpy().reshape((cNbZone, cNbZone))
        #
        # EmAtt = pd.DataFrame(range(cNbZone))
        #
        # EmAtt = pd.DataFrame(TC_df.sum(0))
        # EmAtt = pd.concat([EmAtt, pd.Series(TC_df.sum(1)), pd.Series(UVP_df.sum(0)), pd.Series(UVP_df.sum(1))], axis=1)
        # EmAtt.columns = ['ATTTC', 'EMTC', 'ATTVP', 'EMVP']


# - d. Création de la table d'émissions et d'attraction par zone et par mode
    return {'TC': PartTC, 'VP': PartVP, 'MD': PartMD, 'CY': PartCY}


def indic_modus(n, hor):
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

    dbfile = open(f'{dir_dataTemp}RES_{n}_{hor}', 'rb')
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
    PART_MOT['VP'] = RES['VP'].sum() / (RES['TC'].sum() + RES['VP'].sum())

    # Sauvegarde des parts - modaux
    PART_tmp = DotMap()
    PART_tmp.PART = PART
    PART_tmp.PART_MOT = PART_MOT

    dbfile = open(f'{dir_dataTemp}PART_{n}_{hor}', 'wb')
    pkl.dump(PART_tmp, dbfile)
    dbfile.close()

    #  Sauvegarde du dataframe MOB, contenant les résultats spécifiques de mobilité
    dbfile = open(f'{dir_dataTemp}MOB_{n}_{hor}', 'wb')
    pkl.dump(MOB, dbfile)
    dbfile.close()



def MOT_CL_EVOL(hor):
    dbfile = open(f'{dir_dataTemp}RES_actuel_{hor}', 'rb')
    RES_actuel = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}RES_scen_{hor}', 'rb')
    RES_scen = pkl.load(dbfile)

    EVOL = RES_scen[['TM', 'MD', 'VP', 'CY', 'TC']] - RES_actuel[['TM', 'MD', 'VP', 'CY', 'TC']]
    EVOL.columns = ['evolTM', 'evolMD', 'evolVP', 'evolCY', 'evolTC']

    mask = EVOL['evolTM'] != 0
    EVOL['PctevolTM'] = EVOL[mask].loc[:, 'evolTM'] / RES_actuel[mask].loc[:, 'TM']
    mask = EVOL['evolMD'] != 0
    EVOL['PctevolMD'] = EVOL[mask].loc[:, 'evolMD'] / RES_actuel[mask].loc[:, 'MD']
    mask = EVOL['evolVP'] != 0
    EVOL['PctevolVP'] = EVOL[mask].loc[:, 'evolVP'] / RES_actuel[mask].loc[:, 'VP']
    mask = EVOL['evolCY'] != 0
    EVOL['PctevolCY'] = EVOL[mask].loc[:, 'evolCY'] / RES_actuel[mask].loc[:, 'CY']
    mask = EVOL['evolTC'] != 0
    EVOL['PctevolTC'] = EVOL[mask].loc[:, 'evolTC'] / RES_actuel[mask].loc[:, 'TC']

    dbfile = open(f'{dir_dataTemp}EVOL_{hor}', 'wb')
    pkl.dump(EVOL, dbfile)
    dbfile.close()

def EMATT_EVOL(hor):
    dbfile = open(f'{dir_dataTemp}EmAtt_actuel_{hor}', 'rb')
    EmAtt_actuel = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}EmAtt_scen_{hor}', 'rb')
    EmAtt_scen = pkl.load(dbfile)

    EmAtt_Evol = EmAtt_scen - EmAtt_actuel
    EmAtt_Evol.columns = ['evolEMTC', 'evolEMVP', 'evolATTTC',  'evolATTVP']

    mask = EmAtt_Evol['evolEMTC'] != 0
    EmAtt_Evol['Pct_evolEMTC'] = EmAtt_Evol[mask].loc[:, 'evolEMTC'] / EmAtt_actuel[mask].loc[:, 'EMTC']
    mask = EmAtt_Evol['evolEMVP'] != 0
    EmAtt_Evol['Pct_evolEMVP'] = EmAtt_Evol[mask].loc[:, 'evolEMVP'] / EmAtt_actuel[mask].loc[:, 'EMVP']
    mask = EmAtt_Evol['evolATTTC'] != 0
    EmAtt_Evol['Pct_evolATTTC'] = EmAtt_Evol[mask].loc[:, 'evolATTTC'] / EmAtt_actuel[mask].loc[:, 'ATTTC']
    mask = EmAtt_Evol['evolATTVP'] != 0
    EmAtt_Evol['Pct_evolATTVP'] = EmAtt_Evol[mask].loc[:, 'evolATTVP'] / EmAtt_actuel[mask].loc[:, 'ATTVP']

    dbfile = open(f'{dir_dataTemp}EMATT_EVOL_{hor}', 'wb')
    pkl.dump(EmAtt_Evol, dbfile)
    dbfile.close()

    EmAtt_actuel.columns = [f'EMTC{hor}{actuel}', f'EMVP{hor}{actuel}', f'ATTTC{hor}{actuel}', f'ATTVP{hor}{actuel}']
    EmAtt_scen.columns = [f'EMTC{hor}{scen}', f'EMVP{hor}{scen}', f'ATTTC{hor}{scen}', f'ATTVP{hor}{scen}']

    Zone = pd.DataFrame(range(1, cNbZintsp + 1), columns=['ZONE'])
    Em_Att_Synth = pd.concat([Zone, EmAtt_actuel, EmAtt_scen, EmAtt_Evol], axis=1)
    Em_Att_Synth.to_excel(f'{dir_dataTemp}EmAtt_{hor}.xlsx')


def analyse_modus():
    if PPM == 1:
        #  Préparation des tables
        treat_modus('actuel', 'PPM')
        treat_modus('scen', 'PPM')
        MOT_CL_EVOL('PPM')
        EMATT_EVOL('PPM')

        #  Sortie des indicaturs
        indic_modus('actuel', 'PPM')
        indic_modus('scen', 'PPM')

    if PCJ == 1:
        #  Préparation des tables
        treat_modus('actuel', 'PCJ')
        treat_modus('scen', 'PCJ')
        MOT_CL_EVOL('PCJ')
        EMATT_EVOL('PCJ')

        #  Sortie des indicaturs
        indic_modus('actuel', 'PCJ')
        indic_modus('scen', 'PCJ')

    if PPS == 1:
        #  Préparation des tables
        treat_modus('actuel', 'PPS')
        treat_modus('scen', 'PPS')
        MOT_CL_EVOL('PPS')
        EMATT_EVOL('PPS')

        #  Sortie des indicaturs
        indic_modus('actuel', 'PPS')
        indic_modus('scen', 'PPS')

#  II. MATRICES D'AFFECTATION
#  1. Préparation des tables d'analyse des matrices d'affectation

def indic_affect(hor):
    #  a. préparation d'une table de base
    base_comp = DotMap()
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = 'actuel'
    read_mat.per = hor

    if idTC == 0:
        dbfile = open(f'{dir_dataTemp}ModusTC_df{hor}_actuel', 'rb')
        base_comp.TC_horiz1 = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}ModusTC_df{hor}_scen', 'rb')
        base_comp.TC_horiz2 = pkl.load(dbfile)
        horiz1_TC = caleTC
        horiz2_TC = scen

    else:
        CaleTC_df_actuel = read_mat.CALETC()
        CaleTC_df_actuel = CaleTC_df_actuel[(CaleTC_df_actuel['ZONEO'] <=cNbZone) & (CaleTC_df_actuel['ZONED'] <=cNbZone)]
        base_comp.TC_horiz1 = CaleTC_df_actuel.reset_index(drop=True)
        dbfile = open(f'{dir_dataTemp}MODUSCaleTC_df_{hor}_scen', 'rb')
        base_comp.TC_horiz2 = pkl.load(dbfile)
        horiz1_TC = actuel
        horiz2_TC = scen

    if idVP == 0:
        dbfile = open(f'{dir_dataTemp}ModusUVP_df{hor}_actuel', 'rb')
        base_comp.UVP_horiz1 = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}ModusUVP_df{hor}_scen', 'rb')
        base_comp.UVP_horiz2 = pkl.load(dbfile)
        horiz1_VP = caleVP
        horiz2_VP = scen

    else:
        CaleUVP_df_actuel = read_mat.CALEUVP()
        CaleUVP_df_actuel = CaleUVP_df_actuel[(CaleUVP_df_actuel['ZONEO'] <=cNbZone) & (CaleUVP_df_actuel['ZONED'] <=cNbZone)]
        base_comp.UVP_horiz1 = CaleUVP_df_actuel.reset_index(drop=True)
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_df_{hor}_scen', 'rb')
        base_comp.UVP_horiz2 = pkl.load(dbfile)
        horiz1_VP = caleVP
        horiz2_VP = scen

        #  b. volume sans Intrazonaux UVP
        Diff_UVP = base_comp.UVP_horiz2.loc[:, 'FLUX'] - base_comp.UVP_horiz1.loc[:, 'FLUX']
        base_comp.Evol_vol_UVP1 = Diff_UVP.where(base_comp.UVP_horiz2['ZONEO'] != base_comp.UVP_horiz2['ZONED'], 0)


        base_comp.Evol_vol_UVP1 = base_comp.UVP_horiz2[base_comp.UVP_horiz2['ZONEO'] != base_comp.UVP_horiz2['ZONED']].loc[:, 'FLUX'] \
                                  - base_comp.UVP_horiz1[base_comp.UVP_horiz1['ZONEO'] != base_comp.UVP_horiz1['ZONED']].loc[:, 'FLUX']
        base_comp.Evol_vol_UVP1 = base_comp.Evol_vol_UVP1.sum()
        base_comp.Evol_tot_UVP1 = base_comp.Evol_vol_UVP1.sum() / base_comp.UVP_horiz1['FLUX'].sum()
        base_comp.Evol_an_UVP1 = (1 + base_comp.Evol_tot_UVP1) ** (1 / (horiz2_VP - horiz1_VP)) - 1
        
        base_comp.UVP_horiz1_total_sans = base_comp.UVP_horiz1[base_comp.UVP_horiz1['ZONEO'] != 
                                                  base_comp.UVP_horiz1['ZONED']].loc[:, 'FLUX'].sum()
        base_comp.UVP_horiz2_total_sans = base_comp.UVP_horiz2[base_comp.UVP_horiz2['ZONEO'] != 
                                                  base_comp.UVP_horiz2['ZONED']].loc[:, 'FLUX'].sum()
        
        # - c. volume avec Intrazonaux UVP
        base_comp.Evol_vol_UVP2 = base_comp.UVP_horiz2.loc[:, 'FLUX'] - base_comp.UVP_horiz1.loc[:, 'FLUX']
        base_comp.Evol_vol_UVP2 = base_comp.Evol_vol_UVP2.sum()
        base_comp.Evol_tot_UVP2 = base_comp.Evol_vol_UVP2.sum() / base_comp.UVP_horiz1['FLUX'].sum()
        base_comp.Evol_an_UVP2 = (1 + base_comp.Evol_tot_UVP2) ** (1 / (horiz2_VP - horiz1_VP)) - 1
        base_comp.UVP_horiz1_total_avec = base_comp.UVP_horiz1['FLUX'].sum()
        base_comp.UVP_horiz2_total_avec = base_comp.UVP_horiz2['FLUX'].sum()
        
        #  c. volume sans Intrazonaux TC
        Diff_TC = base_comp.TC_horiz2.loc[:, 'FLUX'] - base_comp.TC_horiz1.loc[:, 'FLUX']
        base_comp.Evol_vol_TC1 = Diff_TC.where(base_comp.TC_horiz2['ZONEO'] != base_comp.TC_horiz2['ZONED'], 0)


        base_comp.Evol_vol_TC1 = base_comp.TC_horiz2[base_comp.TC_horiz2['ZONEO'] != base_comp.TC_horiz2['ZONED']].loc[:, 'FLUX'] \
                                 - base_comp.TC_horiz1[base_comp.TC_horiz1['ZONEO'] != base_comp.TC_horiz1['ZONED']].loc[:, 'FLUX']
        base_comp.Evol_vol_TC1 = base_comp.Evol_vol_TC1.sum()
        base_comp.Evol_tot_TC1 = base_comp.Evol_vol_TC1.sum() / base_comp.TC_horiz1['FLUX'].sum()
        base_comp.Evol_an_TC1 = (1 + base_comp.Evol_tot_TC1) ** (1 / (horiz2_VP - horiz1_VP)) - 1

        base_comp.TC_horiz1_total_sans = base_comp.TC_horiz1[base_comp.TC_horiz1['ZONEO'] != 
                                                  base_comp.TC_horiz1['ZONED']].loc[:, 'FLUX'].sum()
        base_comp.TC_horiz2_total_sans = base_comp.TC_horiz2[base_comp.TC_horiz2['ZONEO'] != 
                                                  base_comp.TC_horiz2['ZONED']].loc[:, 'FLUX'].sum()
        # - d. volume avec Intrazonaux TC
        base_comp.Evol_vol_TC2 = base_comp.TC_horiz2.loc[:, 'FLUX'] - base_comp.TC_horiz1.loc[:, 'FLUX']
        base_comp.Evol_vol_TC2 = base_comp.Evol_vol_TC2.sum()
        base_comp.Evol_tot_TC2 = base_comp.Evol_vol_TC2.sum() / base_comp.TC_horiz1['FLUX'].sum()
        base_comp.Evol_an_TC2 = (1 + base_comp.Evol_tot_TC2) ** (1 / (horiz2_VP - horiz1_VP)) - 1

        base_comp.TC_horiz1_total_avec = base_comp.TC_horiz1['FLUX'].sum()
        base_comp.TC_horiz2_total_avec = base_comp.TC_horiz2['FLUX'].sum()
        
        # Pickling de EmAtt
        dbfile = open(f'{dir_dataTemp}base_comp_{hor}', 'wb')
        pkl.dump(base_comp, dbfile)
        dbfile.close()



#  3. Regroupement: macro d'exécution
def analyse_affect():
    if PPM == 1:
        indic_affect('PPM')
    if PCJ == 1:
        indic_affect('PCJ')
    if PPS == 1:
        indic_affect('PPS')

def indicateurs_func():
    analyse_modus()
    analyse_affect()


def print_typo():
    if PPM and not PCJ and not PPS:
        PERIODE = "PPM seule"
    elif not PPM and PCJ and not PPS:
        PERIODE = "PCJ seule"
    elif not PPM and not PCJ and PPS:
        PERIODE = "PPS seule"
    elif PPM and not PCJ and PPS:
        PERIODE = "PPM & PPS"
    elif PPM and PCJ and not PPS:
        PERIODE = "PPM & PCJ"
    elif not PPM and PCJ and PPS:
        PERIODE = "PCJ & PPS"
    elif PPM and PCJ and PPS:
        PERIODE = "PPM & PCJ & PPS"

    if not idVGTC:
        VGTC = "sans"
    else:
        VGTC = "avec"

    if not idVGVP:
        VGVP = "sans"
    else:
        VGVP = "avec"

    if not idVSTC:
        VSTC = "sans"
    else:
        VSTC = "avec"

    if not idVSVP:
        VSVP = "sans"
    else:
        VSVP = "avec"

    if not idTC:
        TC = "sans"
        horiz1TC = actuel
    else:
        TC = "avec"
        horiz1TC = caleTC

    if not idVP:
        VP = "sans"
        horiz1UVP = actuel
    else:
        VP = "avec"
        horiz1UVP = caleVP
    if idPL == 1:
        PL = "+ &CroisPIB % par an"
    elif idPL == 2:
        PL = "à la journée"
    else:
        PL = "à la période"

    if idBcl == 0:
        Simul = "sans bouclage"
    elif idBcl == 1:
        Simul = "bouclage sur la distribution"
    elif idBcl == 2:
        Simul = "bouclage sur le choix modal"
    elif idBcl == 3:
        Simul = "bouclage sur le choix modal motorisé"
    else:
        Simul = "bouclage sur le choix modal véhiculé"

    # Dictionnaire des chiffres clés de mobilité à stocker pour le notebook Jupyter
    tous_mobs = DotMap()

    #  Dictionnaire qui contient les infos sur la simulation
    simul = {}
    simul['Période(s) simulée(s)'] = PERIODE
    simul['Vecteurs gares TC'] = VGTC
    simul['Vecteurs gares VP'] = VGVP
    simul['Vecteurs aéroports TC'] = VSTC
    simul['Vecteurs aéroports VP'] = VSVP
    simul['Report de calage TC'] = TC
    simul['Report de calage VP'] = VP
    simul['Projection matrice PL'] = PL
    simul['Type de simulation'] = Simul

    simul_df = pd.DataFrame(simul, index=[0])

    # Sauvegarde de ce résultat dans le dictionnaire des résultats à stocker
    tous_mobs.simul = simul_df

    #   b. Affichage des indicateurs des matrices d'affectation
    #  indicateurs de mobilité des matrices MODUS
    Motifs = ["Tous motifs", "Accompagnement", "Accompagnement", "Professionnel et Travail", "Professionnel et Travail",
              "Maternelle et primaire", "Enseignement secondaire", "Etudes supérieures", "Achats-loisirs",
              "Achats-loisirs"]
    Emetteur = ["Population totale", "Actifs employés", "Collégiens et lycéens", "Employés haute qualif",
                "Employés autre qualif", "Elève primaire et maternelle", "Collégiens et lycéens",
                "Etudiants et stagiaires", "Employés et étudiants", "Inactifs et mineurs"]
    Attracteur = ["Emploi total", "Effectifs scolaires", "Effectifs scolaires", "Emploi haute qualif",
                  "Emploi autre qualif", "Effectif primaire et maternel", "Effectif secondaire", "Effectif étudiant",
                  "Emploi de commerce et loisirs", "Emploi de commerce"]

    # DataFrame des indicateurs clés de la mobilité (flux, population, émissions, attractions, evolution)
    #  Les indices des différentes colonnes dans MOB:
    #  Population = 0
    #  Emploi = 1
    #  Flux = 2
    #  Mobilité = 3
    def printmob(hor, periode):
        dbfile = open(f'{dir_dataTemp}MOB_actuel_{hor}', 'rb')
        MOB_actuel = pkl.load(dbfile).T
        dbfile = open(f'{dir_dataTemp}MOB_scen_{hor}', 'rb')
        MOB_scen = pkl.load(dbfile).T
        MOB_hor = pd.DataFrame({'Motif de déplacement' : Motifs, f'Flux {actuel} {hor}': MOB_actuel[2],
                                f'Flux {scen} {hor}': MOB_scen[2], ' 	Segment emetteur' : Emetteur,
                                f'Population {actuel}' : MOB_actuel[0], f'Population {scen}' : MOB_scen[0],
                                'Segment attracteur' : Attracteur, f'Activité {actuel}' : MOB_actuel[1],
                                f'Activité {scen}' : MOB_scen[1], f'Mobilité {actuel} {hor}' : MOB_actuel[3],
                                f'Mobilité {scen} {hor}' : MOB_scen[3],
                                f'Evolution population {actuel} - {scen}' : MOB_scen[0]/MOB_actuel[0] - 1,
                                f'Evolution activité {actuel} - {scen}' : MOB_scen[1]/MOB_actuel[1] - 1,
                                f'Evolution Flux {actuel} - {scen}' : MOB_scen[2]/MOB_actuel[2] - 1})
        return MOB_hor

    #  indicateurs de portées, temps et vitesses moyennes des matrices MODUS
    Modes = ["Tous modes confondus", "Transports collectifs", "Véhicules particuliers",
             "Marche, trottinette et rollers", "Vélos et Velibs"]

    dbfile = open(f'{dir_dataTemp}portee_actuel_PPM', 'rb')
    portee_actuel = pkl.load(dbfile)
    all_portee = pd.DataFrame(portee_actuel['TC'], index=[0])


    def print_portee(hor, periode):
        dbfile = open(f'{dir_dataTemp}portee_actuel_{hor}', 'rb')
        portee_actuel = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}portee_scen_{hor}', 'rb')
        portee_scen = pkl.load(dbfile)
        TM_actuel = [item for key, item in portee_actuel['TM'].items()]
        TC_actuel = [item for key, item in portee_actuel['TC'].items()]
        VP_actuel = [item for key, item in portee_actuel['VP'].items()]
        MD_actuel = [item for key, item in portee_actuel['MD'].items()]
        CY_actuel = [item for key, item in portee_actuel['CY'].items()]
        
        TM_scen = [item for key, item in portee_scen['TM'].items()]
        TC_scen = [item for key, item in portee_scen['TC'].items()]
        VP_scen = [item for key, item in portee_scen['VP'].items()]
        MD_scen = [item for key, item in portee_scen['MD'].items()]
        CY_scen = [item for key, item in portee_scen['CY'].items()]

        all_portee = pd.DataFrame({"Tous modes confondus" : TM_actuel + TM_scen,
                                   "Transports collectifs" : TC_actuel + TC_scen,
                                   "Véhicules particuliers": VP_actuel + VP_scen,
                                   "Marche, trottinette et rollers" : MD_actuel + MD_scen,
                                   "Vélos et Velibs" : CY_actuel + CY_scen})
        all_portee = all_portee.T
        all_portee = all_portee[[0, 3, 1, 4, 2, 5]]
        all_portee[6] = all_portee[3]/all_portee[0] - 1
        all_portee[7] = all_portee[4]/all_portee[1] - 1
        all_portee[8] = all_portee[5]/all_portee[2] - 1
        all_portee.columns = [f"Portée moyenne {actuel} {periode}", f"Portée moyenne {scen} {periode}",
                              f"Temps moyen {actuel} {periode}", f"Temps moyen {scen} {periode}",
                              f"Vitesse moyenne {actuel} {periode}", f"Vitesse moyenne {scen} {periode}",
                              f"Evolution portée {actuel} - {scen} {periode}", 
                              f"Evolution temps {actuel} - {scen} {periode}", 
                              f"Evolution vitesse {actuel} - {scen} {periode}"]
        return all_portee

        #   -- indicateurs des déplacements des matrices d'affectation
    def print_affect(hor):
        dbfile = open(f'{dir_dataTemp}base_comp_{hor}', 'rb')
        base_comp = pkl.load(dbfile)
        Evol_TC1 = pd.DataFrame(
            {f'TC {hor} {horiz1TC}': base_comp.TC_horiz1_total_sans, f'TC {hor} {scen}': base_comp.TC_horiz2_total_sans,
             f'EVOL {horiz1TC} - {scen}': base_comp.Evol_vol_TC1, f"% d'evol {horiz1TC} - {scen}":
                 base_comp.Evol_tot_TC1, "% d'evol annuelle": base_comp.Evol_an_TC1
             }, index=[0])
        Evol_TC2 = pd.DataFrame(
            {f'TC {hor} {horiz1TC}': base_comp.TC_horiz1_total_avec, f'TC {hor} {scen}': base_comp.TC_horiz2_total_avec,
             f'EVOL {horiz1TC} - {scen}': base_comp.Evol_vol_TC2, f"% d'evol {horiz1TC} - {scen}":
                 base_comp.Evol_tot_TC2, "% d'evol annuelle": base_comp.Evol_an_TC2
             }, index=[0])
        Evol_UVP1 = pd.DataFrame(
            {f'UVP {hor} {horiz1UVP}': base_comp.UVP_horiz1_total_sans, f'UVP {hor} {scen}': base_comp.UVP_horiz2_total_sans,
             f'EVOL {horiz1UVP} - {scen}': base_comp.Evol_vol_UVP1, f"% d'evol {horiz1UVP} - {scen}":
                 base_comp.Evol_tot_UVP1, "% d'evol annuelle": base_comp.Evol_an_UVP1
             }, index=[0])
        Evol_UVP2 = pd.DataFrame(
            {f'UVP {hor} {horiz1UVP}': base_comp.UVP_horiz1_total_avec, f'UVP {hor} {scen}': base_comp.UVP_horiz2_total_avec,
             f'EVOL {horiz1UVP} - {scen}': base_comp.Evol_vol_UVP2, f"% d'evol {horiz1UVP} - {scen}":
                 base_comp.Evol_tot_UVP2, "% d'evol annuelle": base_comp.Evol_an_UVP2
             }, index=[0])
        return [Evol_TC1, Evol_TC2, Evol_UVP1, Evol_UVP2]

    def print_part(n, hor):
        dbfile = open(f'{dir_dataTemp}PART_{n}_{hor}', 'rb')
        PART_tous = pkl.load(dbfile)
        PART = PART_tous.PART
        PART_MOT = PART_tous.PART_MOT
        PART_df = pd.DataFrame(PART, index=[0])
        PART_df.columns = [f"Part TC {n} {hor}", f"Part VP {n} {hor}", f"Part CY {n} {hor}", f"Part MD {n} {hor}"]
        PART_MOT_df = pd.DataFrame(PART_MOT, index=[0])
        PART_MOT_df.columns = [f"Part TC {n} {hor}", f"Part VP {n} {hor}"]
        return [PART_df, PART_MOT_df]

    # 2. Indicateurs graphiques des matrices MODUS
    def graph_modus(hor, mode):

        #  - a. Analyse des volumes globaux
        dbfile = open(f'{dir_dataTemp}RES_actuel_{hor}', 'rb')
        RES1 = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}RES_scen_{hor}', 'rb')
        RES2 = pkl.load(dbfile)

        FLUX1 = pd.DataFrame(RES1.groupby(by='Classe_carte').sum().loc[:, mode])
        FLUX1['X'] = tous_classes
        FLUX2 = pd.DataFrame(RES2.groupby(by='Classe_carte').sum().loc[:, mode])
        FLUX2['X'] = tous_classes
        df = pd.concat([FLUX1, FLUX2[mode]], axis=1)
        df.columns = [f'{actuel}', 'PORTEE', f'{scen}']
        df = pd.melt(df, id_vars=['PORTEE']).rename(columns=str.title)
        return df

    #   - b. Analyse des parts modales
    def graph_parts(hor, n):
        dbfile = open(f'{dir_dataTemp}RES_{n}_{hor}', 'rb')
        RES = pkl.load(dbfile)
        RESb = RES.groupby(by='Classe_carte').sum().loc[:, ('TM', 'MD', 'VP', 'CY', 'TC')]
        for i in range(1, len(RESb.columns)):
            RESb.iloc[:, i] /= RESb.loc[:, 'TM']
        RESb = RESb[['MD', 'VP', 'CY', 'TC']]
        RESb['Portee'] = tous_classes
        for i in range(1, len(RESb.columns) - 1):
            RESb.iloc[:, i] += RESb.iloc[:, i - 1]
        return RESb

    if PPM == 1:
        tous_mobs.mob_PPM = printmob('PPM', '6-10h')
        tous_mobs.port_PPM = print_portee('PPM', '6-10h')
        tous_mobs.part_actuel_PPM = print_part('actuel', 'PPM')
        tous_mobs.part_scen_PPM = print_part('scen', 'PPM')
        tous_mobs.affect_PPM = print_affect('PPM')
        tous_mobs.graph_UVP_PPM = graph_modus('PPM', 'VP')
        tous_mobs.graph_TC_PPM = graph_modus('PPM', 'TC')
        tous_mobs.graph_MD_PPM = graph_modus('PPM', 'MD')
        tous_mobs.graph_CY_PPM = graph_modus('PPM', 'CY')
        tous_mobs.graph_TM_PPM = graph_modus('PPM', 'TM')
        tous_mobs.graph_parts_actuel_PPM = graph_parts('PPM', 'actuel')
        tous_mobs.graph_parts_scen_PPM = graph_parts('PPM', 'scen')
    if PCJ == 1:
        tous_mobs.mob_PCJ = printmob('PCJ', '10h-16h')
        tous_mobs.port_PCJ = print_portee('PCJ', '10h-16h')
        tous_mobs.part_actuel_PCJ = print_part('actuel', 'PCJ')
        tous_mobs.part_scen_PCJ = print_part('scen', 'PCJ')
        tous_mobs.affect_PCJ = print_affect('PCJ')
        tous_mobs.graph_UVP_PCJ = graph_modus('PCJ', 'VP')
        tous_mobs.graph_TC_PCJ = graph_modus('PCJ', 'TC')
        tous_mobs.graph_MD_PCJ = graph_modus('PCJ', 'MD')
        tous_mobs.graph_CY_PCJ = graph_modus('PCJ', 'CY')
        tous_mobs.graph_TM_PCJ = graph_modus('PCJ', 'TM')
        tous_mobs.graph_parts_actuel_PCJ = graph_parts('PCJ', 'actuel')
        tous_mobs.graph_parts_scen_PCJ = graph_parts('PCJ', 'scen')
    if PPS == 1:
        tous_mobs.mob_PPS = printmob('PPS', '16h-20h')
        tous_mobs.port_PPS = print_portee('PPS', '16h-20h')
        tous_mobs.part_actuel_PPS = print_part('actuel', 'PPS')
        tous_mobs.part_scen_PPS = print_part('scen', 'PPS')
        tous_mobs.affect_PPS = print_affect('PPS')
        tous_mobs.graph_UVP_PPS = graph_modus('PPS', 'VP')
        tous_mobs.graph_TC_PPS = graph_modus('PPS', 'TC')
        tous_mobs.graph_MD_PPS = graph_modus('PPS', 'MD')
        tous_mobs.graph_CY_PPS = graph_modus('PPS', 'CY')
        tous_mobs.graph_TM_PPS = graph_modus('PPS', 'TM')
        tous_mobs.graph_parts_actuel_PPS = graph_parts('PPS', 'actuel')
        tous_mobs.graph_parts_scen_PPS = graph_parts('PPS', 'scen')

    dbfile = open(f'{dir_dataTemp}tous_mobs', 'wb')
    pkl.dump(tous_mobs, dbfile)
    dbfile.close()



if __name__ == '__main__':
    indicateurs_func()
    print_typo()



