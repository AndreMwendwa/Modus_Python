import numpy as np
import pandas as pd
from Data.fonctions_gen import *
from Quatre_Etapes import Exec_Modus
from Quatre_Etapes import Affect
import multiprocessing
import os
import pickle as pkl

# I. PRÉPARATION ET ANALYSE DES MATRICES VP

# 1. Calcul des matrices d'affectation de l'itération
def mat_iter(H, scen, par):

    dbfile = open(f'{dir_dataTemp}MODUSUVPCale', 'rb')
    MODUSUVPCale = pkl.load(dbfile)

    # - a. Cas particulier de la 1ère itération
    if iter == 1:
        # -- matrice d'affectation de l'itération précédente : nulle pour la 1ère itération
        AFFECT_prec = MODUSUVPCale.copy()
        AFFECT_prec['FLUX'] = 0

        # -- matrice d'affectation de l'itération actuelle : matrice du report de calage
        AFFECT_iter = MODUSUVPCale.copy()


    else:
        # - b. Cas générique
        # -- matrice d'affectation de l'itération précédente
        dbfile = open(f'{dir_dataTemp}AFFECT_iter', 'rb')
        AFFECT_prec = pkl.load(dbfile)

        AFFECT_iter = AFFECT_prec.copy()
        AFFECT_iter = pd.merge(AFFECT_iter, MODUSUVPCale, on=['ZONEO', 'ZONED'])
        # -- calcul de la matrice d'affectation de l'itération n à partir de :
        # 		- la matrice calculée par report de calage à l'itération n
        # 		- la matrice d'affectation de l'itérations n-1 :
        # 		Maff(n) = par * Maff(n-1) + (1-par)* Mcalc(n)
        AFFECT_iter['FLUX'] = par * AFFECT_iter['FLUX_x'] + (1 - par) * AFFECT_iter['FLUX_y']

    # c. Ecriture de la matrice VP sous format fma
    ecriredavisum(AFFECT_iter, Exec_Modus.dir_iter, f'UVP_{H}_scen_iter{iter}', 'VP', 0, 24)


# 2. Analyse des matrices utilisées pour l'itération
def analyse_iter(Iter):
    if Iter == 1:
        MODUSUVP_scen_prec = np.zeros((cNbZone, cNbZone)),
    else:
        dbfile = open(f'{dir_dataTemp}MODUSUVP_{H}_scen_prec', 'rb')
        MODUSUVP_scen_prec = pkl.load(dbfile)

    VAL = np.zeros((1, (PPM + PCJ + PPS)*4 + 1))
    VAL[0, 0] = Iter

    # - b. Calcul des volumes des matrices
    def val_fill(H, ini):
        # -- matrice UVP modus finalisée
        dbfile = open(f'{dir_dataTemp}MODUSUVP_{H}_scen', 'rb')
        MODUSUVP = pkl.load(dbfile)
        VAL[0, ini - 1] = MODUSUVP['FLUX'].sum()

        # -- matrice UVP après report de calage
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen', 'rb')
        MODUSCaleUVP = pkl.load(dbfile)
        VAL[0, ini] = MODUSCaleUVP['FLUX'].sum()

        # -- matrice UVP affectée lors de l'itération
        dbfile = open(f'{dir_dataTemp}AFFECT{H}_{Iter}', 'rb')
        AFFECT = pkl.load(dbfile)
        VAL[0, ini + 1] = AFFECT['FLUX'].sum()

#         -- comparaison des flux par RMSE
# 		 --- calcul du RMSE
        VAL[0, ini + 2] = np.sqrt((MODUSUVP - MODUSUVP_scen_prec).sum())

        # --- mise à jour de la matrice MODUS "mémoire" en vue de l'itération suivante
        dbfile = open(f'{dir_dataTemp}MODUSUVP_{H}_scen_prec', 'wb')
        pkl.dump(MODUSUVP, dbfile)
        dbfile.close()

    if PPM == 1:
        val_fill('PPM', 2)
    if PCJ == 1:
        val_fill('PCJ', (PPM * 4 + 2))
    if PPS == 1:
        val_fill('PCJ', ((PPM + PCJ) * 4 + 2))

    # - c. Sortie des résultats
#     Kiko - Pas terminé du coup.


# III. REALISATION D'UNE BOUCLE

def boucle(par1):
    #     1. Création du dossier de l'itération
    #     Ce try block existe au cas où les dossiers ont déjà été créés pour une raison ou une autre.
    try:
        os.mkdir(Exec_Modus.dir_iter)
    except OSError:
        pass

    #     2. Calcul et analyse des matrices de l'itération
    # Trois 'if'  puisque tous les trois variables peuvent être simultanément egale à 1
    # # Peut-être pas nécessaire avec Visum helpers.
    # if PPM == 1:
    #     mat_iter('PPM', 'scen', par1)
    # if PCJ == 1:
    #     mat_iter('PPM', 'scen', par1)
    # if PPS == 1:
    #     mat_iter('PPM', 'scen', par1)
    # analyse_iter(Iter)

    # 3. Exécution de la boucle
    if PPM == 1:
        dbfile = open(f'{dir_dataTemp}MODUSUVPcarre_PPM_scen', 'rb')
        MODUSUVP = pkl.load(dbfile)

        mat1_M = multiprocessing.Process(name='mat1PPM', target=Affect.affect,  args=(Donnees_Res[f'Version_PPM_scen'], MODUSUVP, 1))

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PPM_scen', 'wb')
        pkl.dump(mat1_M, dbfile)
        dbfile.close()

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PPM_scen_prec', 'wb')
        pkl.dump(MODUSUVP, dbfile)
        dbfile.close()

    if PCJ == 1:
        dbfile = open(f'{dir_dataTemp}MODUSUVPcarre_PCJ_scen', 'rb')
        MODUSUVP = pkl.load(dbfile)
        mat1_C = multiprocessing.Process(name='mat1PCJ', target=Affect.affect, args=(Donnees_Res[f'Version_PCJ_scen'], MODUSUVP, 1))

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PCJ_scen', 'wb')
        pkl.dump(mat1_C, dbfile)
        dbfile.close()

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PCJ_scen_prec', 'wb')
        pkl.dump(MODUSUVP, dbfile)
        dbfile.close()
    if PCJ == 1:
        dbfile = open(f'{dir_dataTemp}MODUSUVPcarre_PPS_scen', 'rb')
        MODUSUVP = pkl.load(dbfile)
        mat1_S = multiprocessing.Process(name='mat1PPS', target=Affect.affect, args=(Donnees_Res[f'Version_PPS_scen'], MODUSUVP, Iter))

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PPS_scen', 'wb')
        pkl.dump(mat1_S, dbfile)
        dbfile.close()

        dbfile = open(f'{dir_dataTemp}ModusUVPcarre_PCJ_scen_prec', 'wb')
        pkl.dump(MODUSUVP, dbfile)
        dbfile.close()


if __name__ == '__main__':
    Iter = 1
    boucle(0.5)