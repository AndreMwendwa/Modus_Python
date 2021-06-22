'''
IMPLEMENTATION COMPLETE DE LA CHAINE MODUS 3.1 SOUS PYTHON

BASÉ SUR LE TRAVAIL DE Guillaume Tremblin

MWENDWA KIKO    19 juin 2021

'''

# Importation des modules nécessaires
import pandas as pd
import numpy as np
from collections import defaultdict
import CstesStruct
import CstesModus_0

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(CstesModus_0)
reload(CstesStruct)
from CstesModus_0 import *
from CstesStruct import *

# ------------
# 0. TELETRAVAIL
# ------------

def teletravail(hor):   # Kiko - Il me semble que scen et n parlent finalement de la même chose. À confirmer. 

    TTVAQ = pd.read_csv(tauxTTVAQ.path, sep=tauxTTVAQ.sep)
    Modus_BD_zone = pd.DataFrame()      # Crées un dataframe vide pour aider à mettre les colonnes dans le bon ordre.
    if hor == 'actuel':
        Modus_BD_zone_Temp = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
    elif hor == 'scen':
        Modus_BD_zone_Temp = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))

    for var in ['ZONE', 'PACT', 'PACTHQ', 'PACTAQ', 'ETOT', 'EMPHQ', 'EMPAQ']:
        Modus_BD_zone[var] = Modus_BD_zone_Temp[var]

    Modus_BD_zone = pd.merge(TTVAQ, Modus_BD_zone, on = 'ZONE')     # Equivalent du merge sur la ligne 22 de
    # 2_Modus entre TTVAQ et Modus.BDzone&scen

    Modus_BD_zone['tauxTTVact'] = np.where(Modus_BD_zone.PACT > 0,
                                    (Modus_BD_zone.PACTHQ * tauxTTVHQ + Modus_BD_zone.PACTAQ * tauxTTVAQact)/Modus_BD_zone.PACT,
                                    1)      # Si Modus_BD_zone.PACT > 0, il met le résultat du calcul, sinon 1
    Modus_BD_zone['tauxTTVemp'] = np.where(Modus_BD_zone.PACT > 0,
                                    (Modus_BD_zone.EMPHQ * tauxTTVHQ + Modus_BD_zone.EMPAQ * tauxTTVAQact)/Modus_BD_zone.PACT,
                                    1)
    Result = pd.DataFrame()     # Nouveau variable, pas dans les fichier sas, utilisé à sauvegarder les résultats du
    # calcul

    Result['ZONE'] = Modus_BD_zone['ZONE']
    Result['HQpro'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVHQ
    Result['AQproact'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQact
    Result['AQproemp'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQemp
    Result['ACTacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVact']
    Result['EMPacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVemp']
    Result['ACTaut'] = 1 + ((jourTTV * varJTTVaut + (1 - jourTTV) * varJLTHaut) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVact']
    Result.index = Result['ZONE']
    del Result['ZONE']

    return Result

# ------------
# I. GENERATION
# ------------

def generation(n, per):

    # 0. Lecture des données de base
    # - a. Lecture des OS utilisées pour la génération

    if n == 'actuel':         # Ce sont les résultats du modèle P + E (diapo 8 - chaine modus).
        Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
    elif n == 'scen':
        Pop_Emp_temp = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))

    # VARGEN = PTOT PACT	PACTHQ PACTAQ RETR SCOLSUP SCOLSEC SCOLPRIM PSCOL CHOM PNACTA
    # PNACTACHO ETOT EMPHQ EMPAQ EMPCOM EMPLOI EMPACH SUP_LE SEC_LE PRIM_LE SCOL_LE dans CtesCalibr
    Pop_Emp = pd.DataFrame()    # Comme précedemment, un dataframe vide pour permettre de réorganiser le colonnes.
    for VAR in list(VARGEN):
        Pop_Emp[VAR] = Pop_Emp_temp[VAR]

    Pop_Emp.index = range(1, cNbZone + 1)  # Pour donner les mêmes indices que SAS.

    # - b. Lecture des paramètres de génération

    if per == 'PPM':
        EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hpm_par.sas7bdat'))
        ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hpm_par.sas7bdat'))
    elif per == 'PCJ':
        EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hc_par.sas7bdat'))
        ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hc_par.sas7bdat'))
    elif per =='PPS':
        EM_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hps_par.sas7bdat'))
        ATT_PAR = pd.read_sas(os.path.join(dir_resultCalibrage,
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hps_par.sas7bdat'))

    # On fait en sorte que les indices soient les motifs des déplacements
    EM_PAR.index = EM_PAR['MOTIF'].astype('int64')
    ATT_PAR.index = ATT_PAR['MOTIF'].astype('int64')

    # La même que la ligne 55 du code SAS, permettant de garder le même ordre de colonnes que dans VARGEN.
    EM_PAR = EM_PAR[VARGEN]
    ATT_PAR = ATT_PAR[VARGEN]


    # - c. Lecture des taux de désagrégation en différentes catégories d'usagers

    # Combinés dans une seule fonction avec l'étape de la multiplication par ces taux,
    # contrairement à ce qui se passe sous SAS

    def use_tx(type, per):   # À remplacer par les bonnes localisation:
        if type == 'EM':
            if per == 'PPM':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                        '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hpm.txt')
                                        , sep = '\t')
                # Kiko - C'est quoi la différence entre tx_desagr_em1 et tx_desagr_em2 ?
            if per == 'PCJ':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hc.txt')
                                            , sep='\t')
            if per == 'PPS':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hps.txt')
                                        , sep='\t')

        if type == 'ATT':
            if per == 'PPM':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                        '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hpm.txt')
                                        , sep = '\t')
            if per == 'PCJ':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hc.txt')
                                        , sep='\t')
            if per == 'PPS':
                tx_desagr = pd.read_csv(os.path.join(dir_resultCalibrage,
                                                     '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hps.txt')
                                        , sep='\t')
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



    '''#Kiko - Ce n'est pas vraiment ce qui se passe avec le code on MODUS. 
    TX_EM = TX_EM.T
    TX_ATT = TX_ATT.T'''
    
    # 1. Réalisation de l'étape de génération

    # - a. Module d'équilibrage des émissions et attractions par moyennage
    def equilib(A,B):
        A_tot = A.sum(axis=0)
        B_tot = B.sum(axis=0)
        MOY = (A_tot + B_tot) / 2
        A *= (MOY/A_tot)
        B *= (MOY / B_tot)
        return A, B

    # b. Calcul des émissions et des attractions
    EM_base = np.maximum((Pop_Emp @ EM_PAR.T), 1)
    ATT_base = np.maximum((Pop_Emp @ ATT_PAR.T), 1)
    EM_base, ATT_base = equilib(EM_base, ATT_base)

    # - c. Calcul des effets des hypothèses de télétravail sur les émissions et attractions équilibrées
    
    if idTTV == 1:
        TTV = teletravail(n)
        if per == 'PPM':
            EM_base.iloc[:, 0] = EM_base.iloc[:, 0] * TTV.iloc[:, 3]
            EM_base.iloc[:, 4] = EM_base.iloc[:, 4] * TTV.iloc[:, 0]
            EM_base.iloc[:, 5] = EM_base.iloc[:, 5] * TTV.iloc[:, 0]
            EM_base.iloc[:, 6] = EM_base.iloc[:, 6] * TTV.iloc[:, 1]
            EM_base.iloc[:, 7] = EM_base.iloc[:, 7] * TTV.iloc[:, 2]
            EM_base.iloc[:, 8] = EM_base.iloc[:, 8] * TTV.iloc[:, 0]
            EM_base.iloc[:, 9] = EM_base.iloc[:, 9] * TTV.iloc[:, 0]
            EM_base.iloc[:, 10] = EM_base.iloc[:, 10] * TTV.iloc[:, 1]
            EM_base.iloc[:, 11] = EM_base.iloc[:, 11] * TTV.iloc[:, 2]
            EM_base.iloc[:, 18] = EM_base.iloc[:, 18] * TTV.iloc[:, 5]
            EM_base.iloc[:, 19] = EM_base.iloc[:, 19] * TTV.iloc[:, 5]
            ATT_base.iloc[:, 1] = ATT_base.iloc[:, 1] * TTV.iloc[:, 4]
            ATT_base.iloc[:, 4] = ATT_base.iloc[:, 4] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 5] = ATT_base.iloc[:, 5] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 6] = ATT_base.iloc[:, 6] * TTV.iloc[:, 2]
            ATT_base.iloc[:, 7] = ATT_base.iloc[:, 7] * TTV.iloc[:, 1]
            ATT_base.iloc[:, 8] = ATT_base.iloc[:, 8] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 9] = ATT_base.iloc[:, 9] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 10] = ATT_base.iloc[:, 10] * TTV.iloc[:, 2]
            ATT_base.iloc[:, 11] = ATT_base.iloc[:, 11] * TTV.iloc[:, 1]
            ATT_base.iloc[:, 18] = ATT_base.iloc[:, 18] * TTV.iloc[:, 5]
            ATT_base.iloc[:, 19] = ATT_base.iloc[:, 19] * TTV.iloc[:, 5]
            
        if per == 'PPS':
            EM_base.iloc[:, 0] = EM_base.iloc[:, 0] * TTV.iloc[:, 4]
            EM_base.iloc[:, 4] = EM_base.iloc[:, 4] * TTV.iloc[:, 0]
            EM_base.iloc[:, 5] = EM_base.iloc[:, 5] * TTV.iloc[:, 0]
            EM_base.iloc[:, 6] = EM_base.iloc[:, 6] * TTV.iloc[:, 1]
            EM_base.iloc[:, 7] = EM_base.iloc[:, 7] * TTV.iloc[:, 2]
            EM_base.iloc[:, 8] = EM_base.iloc[:, 8] * TTV.iloc[:, 0]
            EM_base.iloc[:, 9] = EM_base.iloc[:, 9] * TTV.iloc[:, 0]
            EM_base.iloc[:, 10] = EM_base.iloc[:, 10] * TTV.iloc[:, 1]
            EM_base.iloc[:, 11] = EM_base.iloc[:, 11] * TTV.iloc[:, 2]
            EM_base.iloc[:, 18] = EM_base.iloc[:, 18] * TTV.iloc[:, 5]
            EM_base.iloc[:, 19] = EM_base.iloc[:, 19] * TTV.iloc[:, 5]
            ATT_base.iloc[:, 1] = ATT_base.iloc[:, 1] * TTV.iloc[:, 3]
            ATT_base.iloc[:, 4] = ATT_base.iloc[:, 4] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 5] = ATT_base.iloc[:, 5] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 6] = ATT_base.iloc[:, 6] * TTV.iloc[:, 2]
            ATT_base.iloc[:, 7] = ATT_base.iloc[:, 7] * TTV.iloc[:, 1]
            ATT_base.iloc[:, 8] = ATT_base.iloc[:, 8] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 9] = ATT_base.iloc[:, 9] * TTV.iloc[:, 0]
            ATT_base.iloc[:, 10] = ATT_base.iloc[:, 10] * TTV.iloc[:, 2]
            ATT_base.iloc[:, 11] = ATT_base.iloc[:, 11] * TTV.iloc[:, 1]
            ATT_base.iloc[:, 18] = ATT_base.iloc[:, 18] * TTV.iloc[:, 5]
            ATT_base.iloc[:, 19] = ATT_base.iloc[:, 19] * TTV.iloc[:, 5]
            
        EM_base, ATT_base = equilib(EM_base, ATT_base)

    # 2. Désagrégation des émissions et attractions entre catégories

    EM = np.ones((cNbZone,(cNbCat-1)*cNbMotif + cNbMotif))
    ATT = np.ones((cNbZone, (cNbCat - 1) * cNbMotif + cNbMotif))

    TX_EM = use_tx('EM', per)
    TX_ATT = use_tx('ATT', per)

    # Kiko -> Une seule matrice de TX_EM. Check avec timeit
    for iCat in cNbCat:
        for iMotif in range(cNbMotif):
            ident = iMotif + iCat
            EM[:, ident] = EM_base.iloc[:, iMotif] * TX_EM[:, ident]
            ATT[:, ident] = ATT_base.iloc[:, iMotif] * TX_ATT[:, ident]


    EM, ATT = equilib(EM, ATT)
    # Matrice diagonales avec les 1 additionnels là ou il y a
    # Kiko -> refait avec fonction de matrice diagonale.
    Motifs_Gen_Dist = defaultdict(list)     # C'est une nouvelle étape qu'on vient de créer après le rendez-vous de 22-06-21, dans
    # laquelle on va décrire les combinaisons de motifs et à partir de ça la matrice de fusion.
    # Les clés du dictionnaire corréspondent aux motifs - distribution, et les élements aux motifs génération (selon
    # diapo 6 de la documentation de Modus)


    Motifs_Gen_Dist[1].extend((1, ))
    Motifs_Gen_Dist[2].extend((2, ))
    Motifs_Gen_Dist[3].extend((3, 4))
    Motifs_Gen_Dist[4].extend((5, 6))
    Motifs_Gen_Dist[5].extend((7, 8))
    Motifs_Gen_Dist[6].extend((9, 10))
    Motifs_Gen_Dist[7].extend((11, 12))
    Motifs_Gen_Dist[8].extend((13, 14))
    Motifs_Gen_Dist[9].extend((15, 16))
    Motifs_Gen_Dist[10].extend((17, 18))
    Motifs_Gen_Dist[11].extend((19, ))
    Motifs_Gen_Dist[12].extend((20,))
    Motifs_Gen_Dist[13].extend((21,))
    Motifs_Gen_Dist[14].extend((22,))

    Fusion = np.zeros((44, 28))
    for colonne, value in Motifs_Gen_Dist.items():
        for ligne in value:
            Fusion[ligne-1, colonne-1] = 1
            Fusion[ligne -1 + 22, colonne - 1 + 14] = 1



    EM_final = EM @ Fusion
    ATT_final = ATT @ Fusion

    return EM_final, ATT_final




