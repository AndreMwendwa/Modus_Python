import Quatre_Etapes.main
from Data.fonctions_gen import *
from Quatre_Etapes import affect
import multiprocessing
import os
import pickle as pkl
from Data.fonctions_gen import ODvide_func
from Quatre_Etapes.dossiers_simul import *



# I. PRÉPARATION ET ANALYSE DES MATRICES VP

# 1. Calcul des matrices d'affectation de l'itération
from Quatre_Etapes.dossiers_simul import dir_dataTemp


def mat_iter(H, par, itern):

    # dbfile = open(f'{dir_dataTemp}MODUSUVPCale', 'rb')


    # - a. Cas particulier de la 1ère itération
    if itern == 1:
        # # -- matrice d'affectation de l'itération précédente : nulle pour la 1ère itération
        # AFFECT_prec = MODUSUVPCale.copy()
        # AFFECT_prec = 0
        from Data.traitment_data import read_mat
        read_mat = read_mat()
        read_mat.n = 'actuel'
        read_mat.per = H
        MODUSUVPCale_prec = read_mat.CALEUVP()
        AFFECT_prec = MODUSUVPCale_prec['FLUX'].to_numpy().reshape((cNbZtot, cNbZtot))

        # -- matrice d'affectation de l'itération actuelle : matrice du report de calage
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen', 'rb')
        AFFECT_iter = pkl.load(dbfile)


    else:
        # - b. Cas générique
        # -- matrice d'affectation de l'itération précédente
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen_prec', 'rb')
        AFFECT_prec = pkl.load(dbfile)

        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen', 'rb')
        AFFECT_iter = pkl.load(dbfile)
        # AFFECT_iter = AFFECT_prec.copy()
        # AFFECT_iter = pd.merge(AFFECT_iter, MODUSUVPCale, on=['ZONEO', 'ZONED'])
        # -- calcul de la matrice d'affectation de l'itération n à partir de :
        # 		- la matrice calculée par report de calage à l'itération n
        # 		- la matrice d'affectation de l'itérations n-1 :
        # 		Maff(n) = par * Maff(n-1) + (1-par)* Mcalc(n)
        AFFECT_iter = par * AFFECT_iter + (1 - par) * AFFECT_prec
    return AFFECT_iter
    # c. Ecriture de la matrice VP sous format fma
    # ecriredavisum(AFFECT_iter, Exec_Modus.dir_iter, f'UVP_{H}_scen_iter{iter}', 'VP', 0, 24)



# 2. Analyse des matrices utilisées pour l'itération
def analyse_iter(itern):
    if itern == 1:
        MODUSUVP_scen_prec = np.zeros((cNbZone, cNbZone)),
    else:
        dbfile = open(f'{dir_dataTemp}MODUSUVP_{H}_scen_prec', 'rb')
        MODUSUVP_scen_prec = pkl.load(dbfile)

    VAL = np.zeros((1, (PPM + PCJ + PPS)*4 + 1))
    VAL[0, 0] = itern

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
        dbfile = open(f'{dir_dataTemp}AFFECT{H}_{itern}', 'rb')
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

def RMSE(H, itern):
    if itern == 1:
        # MODUSUVP_scen_prec = np.zeros((cNbZtot, cNbZtot)),
        from Data.traitment_data import read_mat
        read_mat = read_mat()
        read_mat.n = 'actuel'
        read_mat.per = H
        MODUSUVPCale_prec = read_mat.CALEUVP()
        MODUSUVP_scen_prec = MODUSUVPCale_prec['FLUX'].to_numpy().reshape((cNbZtot, cNbZtot))
    else:
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen_prec', 'rb')
        MODUSUVP_scen_prec = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen', 'rb')
    MODUSUVP = pkl.load(dbfile)

    print(f'RMSE_{H} =',  np.sqrt(((MODUSUVP - MODUSUVP_scen_prec)**2).sum()))  # Kiko ligne temporaire
    return np.sqrt(((MODUSUVP - MODUSUVP_scen_prec)**2).sum())

# III. REALISATION D'UNE BOUCLE

def boucle(par1, itern, dir_itern):
    #     1. Création du dossier de l'itération
    #     Ce try block existe au cas où les dossiers ont déjà été créés pour une raison ou une autre.

    # 3. Exécution de la boucle
    Result = {}
    if PPM == 1:

        mat1_M = multiprocessing.Process(name='mat1PPM', target=affect.affect, args=(Donnees_Res[f'Version_PPM_scen'],
                                                                                     mat_iter('PPM', par1, itern), itern, 'PPM', dir_itern))
        mat1_M.start()

    if PCJ == 1:

        mat1_C = multiprocessing.Process(name='mat1PCJ', target=affect.affect, args=(Donnees_Res[f'Version_PCJ_scen'],
                                                                                     mat_iter('PCJ', par1, itern), itern, 'PCJ', dir_itern))
        mat1_C.start()
    if PPS == 1:

        mat1_S = multiprocessing.Process(name='mat1PPS', target=affect.affect, args=(Donnees_Res[f'Version_PPS_scen'],
                                                                                     mat_iter('PPS', par1, itern), itern, 'PPS', dir_itern))
        mat1_S.start()

def derniere_iteration(itern, dir_itern):
    from Traitement.pp_hp import pp_hp
    if PPM == 1:
        pp_hp_obj = pp_hp('PPM')   # On initialize la classe qu'on utilise pour redresser nos flux
        mat1_M = multiprocessing.Process(name='mat1PPM', target=affect.affect, args=(Donnees_Res[f'Version_PPM_scen'],
                                                                                     pp_hp_obj.redresse_matrice(), itern, 'PPM', dir_itern))
        mat1_M.start()
    if PPS == 1:
        pp_hp_obj = pp_hp('PPS')   # On initialize la classe qu'on utilise pour redresser nos flux
        mat1_S = multiprocessing.Process(name='mat1PPS', target=affect.affect, args=(Donnees_Res[f'Version_PPS_scen'],
                                                                                     pp_hp_obj.redresse_matrice(), itern, 'PPS', dir_itern))
        mat1_S.start()

def derniere_iteration_b(itern, dir_itern):
    from Traitement.pp_hp import pp_hp
    if PPM == 1:
        pp_hp('PPM', dir_itern).redresse_matrice()   # On initialize la classe qu'on utilise pour redresser nos flux
        dbfile = open(f'{dir_dataTemp}flux_derniere_iteration_PPM', 'rb')
        matVP = pkl.load(dbfile)
        mat1_M = multiprocessing.Process(name='mat1PPM', target=affect.affect, args=(Donnees_Res[f'Version_PPM_scen'],
                                                                                     matVP, itern, 'PPM', dir_itern))
        mat1_M.start()
    if PPS == 1:
        pp_hp('PPS', dir_itern).redresse_matrice()    # On initialize la classe qu'on utilise pour redresser nos flux
        dbfile = open(f'{dir_dataTemp}flux_derniere_iteration_PPS', 'rb')
        matVP = pkl.load(dbfile)
        mat1_S = multiprocessing.Process(name='mat1PPS', target=affect.affect, args=(Donnees_Res[f'Version_PPS_scen'],
                                                                                     matVP, itern, 'PPS', dir_itern))
        mat1_S.start()

def derniere_iteration_c(itern, dir_itern):
    from Traitement.pp_hp import pp_hp
    if PPM == 1:
        # On initialize la classe qu'on utilise pour redresser nos flux
        mat1_M = multiprocessing.Process(name='mat1PPM', target=pp_hp('PPM', dir_itern, itern).affect())
        mat1_M.start()
    if PPS == 1:
        mat1_S = multiprocessing.Process(name='mat1PPS', target=pp_hp('PPS', dir_itern, itern).affect())
        mat1_S.start()

def data_update(par2, n):
    dbfile = open(f'{dir_dataTemp}bdinter_{n}', 'rb')
    bdinter = pkl.load(dbfile)

    if PPM == 1:
        dbfile = open(f'{dir_dataTemp}TV_PPM_scen', 'rb')
        TVP_PPM = pkl.load(dbfile)
        TVP_PPM = pd.DataFrame(TVP_PPM.reshape((cNbZtot ** 2)), columns=['TVPM'])
        ODvide = pd.DataFrame(ODvide_func(cNbZtot), columns=['ZONEO', 'ZONED'])
        TVP_PPM = pd.concat([ODvide, TVP_PPM], axis=1)
        TVP_PPM = TVP_PPM.loc[(TVP_PPM['ZONEO'] <= cNbZone) & (TVP_PPM['ZONED'] <= cNbZone)]
        TVP_PPM.reset_index(inplace=True)
        bdinter['TVPM'] = np.where(bdinter['ZONEO'] != bdinter['ZONED'], (par2 * TVP_PPM['TVPM'] + (1 - par2) * bdinter['TVPM']), bdinter['TVPM'])
    if PCJ == 1:
        dbfile = open(f'{dir_dataTemp}TV_PCJ_scen', 'rb')
        TVP_PCJ = pkl.load(dbfile)
        TVP_PCJ = pd.DataFrame(TVP_PCJ.reshape((cNbZtot ** 2)), columns=['TVPC'])
        ODvide = pd.DataFrame(ODvide_func(cNbZtot), columns=['ZONEO', 'ZONED'])
        TVP_PCJ = pd.concat([ODvide, TVP_PCJ], axis=1)
        TVP_PCJ = TVP_PCJ.loc[(TVP_PCJ['ZONEO'] <= cNbZone) & (TVP_PCJ['ZONED'] <= cNbZone)]
        TVP_PCJ.reset_index(inplace=True)
        bdinter['TVPC'] = np.where(bdinter['ZONEO'] != bdinter['ZONED'], (par2 * TVP_PCJ['TVPC'] + (1 - par2) * bdinter['TVPC']), bdinter['TVPC'])
    if PPS == 1:
        dbfile = open(f'{dir_dataTemp}TV_PPS_scen', 'rb')
        TVP_PPS = pkl.load(dbfile)
        TVP_PPS = pd.DataFrame(TVP_PPS.reshape((cNbZtot ** 2)), columns=['TVPS'])
        ODvide = pd.DataFrame(ODvide_func(cNbZtot), columns=['ZONEO', 'ZONED'])
        TVP_PPS = pd.concat([ODvide, TVP_PPS], axis=1)
        TVP_PPS = TVP_PPS.loc[(TVP_PPS['ZONEO'] <= cNbZone) & (TVP_PPS['ZONED'] <= cNbZone)]
        TVP_PPS.reset_index(inplace=True)
        bdinter['TVPS'] = np.where(bdinter['ZONEO'] != bdinter['ZONED'], (par2 * TVP_PPS['TVPS'] + (1 - par2) * bdinter['TVPS']), bdinter['TVPS'])

    dbfile = open(f'{dir_dataTemp}bdinter_{n}', 'wb')
    pkl.dump(bdinter, dbfile)
    dbfile.close()



if __name__ == '__main__':
    # itern = 1
    # data_update(0.5, 'actuel')
    derniere_iteration_c(2, dir_iter)