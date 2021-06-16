import pandas as pd
import numpy as np
import CstesModus_0



def teletravail(hor):   # Kiko - Il me semble que scen et n parlent finalement de la même chose. À confirmer. 

    TTVAQ = pd.read_csv(CstesModus_0.tauxTTVAQ.path, sep = CstesModus_0.tauxTTVAQ.sep)
    VARGEN = pd.DataFrame()
    if hor == 'actuel':
        VARGEN_Temp = pd.read_sas('..\\..\\Donnees\\Input\\1_Actuel\\bdzone2012.sas7bdat')
    elif hor == 'scen':
        VARGEN_Temp = pd.read_sas('..\\..\\Donnees\\Input\\2_Scenario\\bdzone2022.sas7bdat')

    for var in ['ZONE', 'PACT', 'PACTHQ', 'PACTAQ', 'ETOT', 'EMPHQ', 'EMPAQ']:
        VARGEN[var] = VARGEN_Temp[var]

    #VARGEN.index = (VARGEN['ZONE']).astype('int64')
    #TTVAQ.index = TTVAQ['ZONE']



    VARGEN = pd.merge(TTVAQ, VARGEN, on = 'ZONE')     # Equivalent du merge sur la ligne 22 de
    # 2_Modus entre TTVAQ et Modus.BDzone&scen

    #tauxTTVact = 1
    #tauxTTVemp = 1     # Kiko Je crois que ça c'était juste pour donner les valeurs défaut, mais je fais ça
    # maintenant avec np.where.
    jourTTV = CstesModus_0.jourTTV
    partTTV = CstesModus_0.partTTV
    tauxTTVHQ = CstesModus_0.tauxTTVHQ
    tauxTTVAQact = CstesModus_0.tauxTTVAQact
    tauxTTVAQemp = CstesModus_0.tauxTTVAQemp
    varJTTVpro = CstesModus_0.varJTTVpro
    varJLTHpro = CstesModus_0.varJLTHpro
    varJTTVacc = CstesModus_0.varJTTVacc
    varJLTHacc = CstesModus_0.varJLTHacc
    varJTTVaut = CstesModus_0.varJTTVaut
    varJLTHaut = CstesModus_0.varJLTHaut


    VARGEN['tauxTTVact'] = np.where(VARGEN.PACT > 0,
                                    (VARGEN.PACTHQ * tauxTTVHQ + VARGEN.PACTAQ * tauxTTVAQact)/VARGEN.PACT,
                                    1)
    VARGEN['tauxTTVemp'] = np.where(VARGEN.PACT > 0,
                                    (VARGEN.EMPHQ * tauxTTVHQ + VARGEN.EMPAQ * tauxTTVAQact) / VARGEN.PACT,
                                    1)
    Result = pd.DataFrame()     # Nouveau variable, pas dans les fichier sas

    Result['ZONE'] = VARGEN['ZONE']
    Result['HQpro'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVHQ
    Result['AQproact'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQact
    Result['AQproemp'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQemp
    Result['ACTacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * VARGEN['tauxTTVact']
    Result['EMPacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * VARGEN['tauxTTVemp']
    Result['ACTaut'] = 1 + ((jourTTV * varJTTVaut + (1 - jourTTV) * varJLTHaut) * partTTV + (1 - partTTV) - 1) * VARGEN['tauxTTVact']
    Result.index = Result['ZONE']
    del Result['ZONE']

    return Result

def generation(n, hor,per):

    # 0. Lecture des données de base

    # - a. Lecture des OS utilisées pour la génération
    # Au lieu du variable VARGEN, on a utilisé ici les variables em et att pour contenir les variables de génération.
    if per == 'hpm':
        EM_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hpm_par.sas7bdat')
        ATT_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hpm_par.sas7bdat')
    elif per == 'hc':
        EM_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hc_par.sas7bdat')
        ATT_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hc_par.sas7bdat')
    elif per =='hps':
        EM_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                         '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\em_hps_par.sas7bdat')
        ATT_PAR = pd.read_sas('..\\..\\M3_Calibrage\\2_Resultats\\'
                          '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\att_hps_par.sas7bdat')
    # On fait en sorte que les indices soit les motifs des déplacements
    EM_PAR.index = EM_PAR['MOTIF'].astype('int64')
    ATT_PAR.index = ATT_PAR['MOTIF'].astype('int64')
    del EM_PAR['MOTIF'], ATT_PAR['MOTIF']  # Supprimer les anciens indices

    # - b. Lecture des paramètres de génération

    #Kiko - Je n'étais pas trop sur s'il fallait prendre VARGEN comme le fichier P + E qu'on va eventuellement multiplié ou non?
    if hor == 'actuel':
        VARGEN_Temp = pd.read_sas('..\\..\\Donnees\\Input\\1_Actuel\\bdzone2012.sas7bdat')
    elif hor == 'scen':
        VARGEN_Temp = pd.read_sas('..\\..\\Donnees\\Input\\2_Scenario\\bdzone2022.sas7bdat')

    VARGEN = pd.DataFrame()
    for attr_c in list(ATT_PAR.columns):
        VARGEN[attr_c] = VARGEN_Temp[attr_c]
        
    VARGEN.index = range(1, 1290) # Pour donner les mêmes indices que SAS.

    # - c. Lecture des taux de désagrégation en différentes catégories d'usagers
    # Kiko - C'est dans cette étape qu'il y a un souci
    if per == 'hpm':
        TX_EM = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hpm.txt'
                            , sep = '\t')
        TX_ATT = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hpm.txt'
                            , sep = '\t')
    elif per == 'hc':
        TX_EM = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hc.txt'
                            , sep = '\t')
        TX_ATT = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hc.txt'
                            , sep = '\t')
    elif per == 'hps':
        TX_EM = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_em1_hps.txt'
                            , sep = '\t')
        TX_ATT = pd.read_csv('..\\..\\M3_Calibrage\\2_Resultats\\'
                            '200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\5_Export\\tx_desagr_att1_hps.txt'
                            , sep = '\t')
    #Kiko - Ce n'est pas vraiment ce qui se passe avec le code on MODUS. 
    TX_EM = TX_EM.T
    TX_ATT = TX_ATT.T
    
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
    EM_base = np.maximum((VARGEN @ EM_PAR.T), 1)
    ATT_base = np.maximum((VARGEN @ ATT_PAR.T), 1)
    EM_base, ATT_base = equilib(EM_base, ATT_base)

    # - c. Calcul des effets des hypothèses de télétravail sur les émissions et attractions équilibrées
    
    if n == 'scen' and idTTV == 1:
        TTV = teletravail('scen')
        if per == 'S':
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
            
        if per == 'M':
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
        #Kiko c'est la dernière chose pour l'instant qui est correcte. 
        
        # 2. Désagrégation des émissions et attractions entre catégories
        
        cNbCat, cNbZone, cNbMotif= 2, 1289, 22   
        # Kiko -> C'est pas du tout ce qui est fait dans le code de Modus. 
        
        EM = np.ones((cNbZone,(cNbCat-1)*cNbMotif + cNbMotif))
        ATTR = np.ones((cNbZone,(cNbCat-1)*cNbMotif + cNbMotif))
        
        for iCat in range(cNbCat):
            for iMotif in range(cNbMotif):
                ident = (iCat-1)*cNbMotif + iMotif
                EM[:,ident] = EM_base[:,iMotif] * TX_EM.iloc[:,ident]
                ATTR[:,ident] = ATT_base[:,iMotif] * TX_ATT.iloc[:,ident]
    return EM_base, ATT_base





