

# Importation des modules nécessaires
from Data.A_CstesModus import *
from Quatre_Etapes.dossiers_simul import *
from Data.teletravail import teletravail
import pickle as pkl


# ------------
# I. GENERATION
# ------------

def generation(n, per):
    from Data.generation_data import generation
    generation = generation()
    generation.n = n
    generation.per = per

    # 0. Lecture des données de base
    # - a. Lecture des OS utilisées pour la génération
    Pop_Emp = generation.Pop_Emp()
    # if idTTV == 0:
    #     Pop_Emp = generation.Pop_Emp()
    #
    # else:
    #     Pop_Emp_temp = pd.read_csv(f'{dir_dataScen}\\210212_OS2025h.txt', sep = '\t')
    #     Pop_Emp = pd.DataFrame()
    #     for VAR in list(VARGEN):
    #         Pop_Emp[VAR] = Pop_Emp_temp[VAR]
    #     Pop_Emp.index = range(1, cNbZone + 1)

    # - b. Lecture des paramètres de génération

    EM_PAR = generation.EM_PAR()
    ATT_PAR = generation.ATT_PAR()

    # - c. Lecture des taux de désagrégation en différentes catégories d'usagers

    # Combinés dans une seule fonction avec l'étape de la multiplication par ces taux,
    # contrairement à ce qui se passe sous SAS

    # 1. Réalisation de l'étape de génération

    # - a. Module d'équilibrage des émissions et attractions par moyennage
    def equilib(A, B):
        A_tot = A.sum(axis=0)
        B_tot = B.sum(axis=0)
        MOY = (A_tot + B_tot) / 2
        A *= (MOY / A_tot)
        B *= (MOY / B_tot)
        return A, B

    # b. Calcul des émissions et des attractions
    EM_base = np.maximum((Pop_Emp @ EM_PAR.T), 1)
    ATT_base = np.maximum((Pop_Emp @ ATT_PAR.T), 1)
    EM_base, ATT_base = equilib(EM_base, ATT_base)

    # - c. Calcul des effets des hypothèses de télétravail sur les émissions et attractions équilibrées

    if idTTV == 1 and n == 'scen':
        TTV = teletravail('scen')
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

        elif per == 'PPS':
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

    EM = np.ones((cNbZone, (cNbCat - 1) * cNbMotif + cNbMotif))
    ATT = np.ones((cNbZone, (cNbCat - 1) * cNbMotif + cNbMotif))

    TX_EM = generation.use_tx('EM')
    TX_ATT = generation.use_tx('ATT')

    # Kiko -> Une seule matrice de TX_EM. Check avec timeit
    for iCat in range(cNbCat):
        for iMotif in range(cNbMotif):
            ident = iCat * cNbMotif + iMotif
            EM[:, ident] = EM_base.iloc[:, iMotif] * TX_EM[:, ident]
            ATT[:, ident] = ATT_base.iloc[:, iMotif] * TX_ATT[:, ident]

    EM, ATT = equilib(EM, ATT)
    # Matrice diagonales avec les 1 additionnels là ou il y a
    # Kiko -> refait avec fonction de matrice diagonale.
    Motifs_Gen_Dist = defaultdict(
        list)  # C'est une nouvelle étape qu'on vient de créer après le rendez-vous de 22-06-21, dans
    # laquelle on va décrire les combinaisons de motifs et à partir de ça la matrice de fusion.
    # Les clés du dictionnaire corréspondent aux motifs - distribution, et les élements aux motifs génération (selon
    # diapo 6 de la documentation de Modus)

    Motifs_Gen_Dist[1].extend((1,))
    Motifs_Gen_Dist[2].extend((2,))
    Motifs_Gen_Dist[3].extend((3, 4))
    Motifs_Gen_Dist[4].extend((5, 6))
    Motifs_Gen_Dist[5].extend((7, 8))
    Motifs_Gen_Dist[6].extend((9, 10))
    Motifs_Gen_Dist[7].extend((11, 12))
    Motifs_Gen_Dist[8].extend((13, 14))
    Motifs_Gen_Dist[9].extend((15, 16))
    Motifs_Gen_Dist[10].extend((17, 18))
    Motifs_Gen_Dist[11].extend((19,))
    Motifs_Gen_Dist[12].extend((20,))
    Motifs_Gen_Dist[13].extend((21,))
    Motifs_Gen_Dist[14].extend((22,))

    Fusion = np.zeros((44, 28))
    for colonne, value in Motifs_Gen_Dist.items():
        for ligne in value:
            Fusion[ligne - 1, colonne - 1] = 1
            Fusion[ligne - 1 + 22, colonne - 1 + 14] = 1

    EM_final = EM @ Fusion
    ATT_final = ATT @ Fusion

    # Pickling des résultats
    dbfile = open(f'{dir_dataTemp}gen_results_{n}_{per}', 'wb')
    tmp = {'EM': EM_final, 'ATT': ATT_final}
    pkl.dump(tmp, dbfile)
    dbfile.close()
    if n == 'actuel':
        if per == 'PPM':
            print(f"\t Génération terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Matin")
        elif per == 'PCJ':
            print(f"\t Génération terminé pour l'année de calage du modèle ({actuel}), pour la Période Creuse de la journée")
        else:
            print(f"\t Génération terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Soir")
    else:
        if per == 'PPM':
            print(f"\t Génération terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Matin")
        elif per == 'PCJ':
            print(f"\t Génération terminé pour l'année de scénario du modèle ({scen}), pour la Période Creuse de la journée")
        else:
            print(f"\t Génération terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Soir")

    return EM_final, ATT_final


if __name__ == '__main__':
    generation('actuel', 'PPM')
    generation('scen', 'PPM')
    generation('actuel', 'PPS')
    generation('scen', 'PPS')


