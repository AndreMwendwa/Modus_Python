from Data.CstesStruct import *
from Data.A_CstesModus import *
from Quatre_Etapes import generation, utility, distribution, choix_modal, bouclage
from Traitement import traitement
import pickle as pkl
from Traitement.gui3 import *
import time

def GUI():
    from Quatre_Etapes import choix_modal
    modus_mode, bdinter, gen_results, dist_results, choix_results = None, None, None, None, None

    submit = GUI()

    if submit['-Bdinter_res-']:
        modus_mode = 1
        bdinter = submit['-bdinter-']
    elif submit['-Gen_res-']:
        modus_mode = 2
        gen_results = submit['-gen_results-']
    elif submit['-dist_results-']:
        modus_mode = 3
        dist_results = submit['-dist_results-']
    elif submit['-choix_results-']:
        modus_mode = 4
        choix_results = submit['-choix_results-']


    params_user = {'modus_mode': modus_mode, 'bdinter': bdinter, 'gen_results': gen_results,
                                 'dist_results': dist_results, 'choix_results': choix_results}

    dbfile = open(f'{dir_dataTemp}params_user', 'wb')
    pkl.dump(params_user, dbfile)
    dbfile.close()

    n = submit[2]
    per = submit[3]



def demande(n, itern):
    if PPM == 1:
        distribution.distribution(n, 'PPM')
        choix_modal.choix_modal(n, 'PPM', itern)
    if PCJ == 1:
        distribution.distribution(n, 'PCJ')
        choix_modal.choix_modal(n, 'PCJ', itern)
    if PPS == 1:
        distribution.distribution(n, 'PPS')
        choix_modal.choix_modal(n, 'PPS', itern)

def croissancecoutvp(bdinter):
    if idcoutvp == 1:
        dbfile = open(f'{dir_dataTemp}bdinter_scen', 'rb')
        bdinter_scen = pkl.load(dbfile)
        bdinter_scen['CTVP'] *= croiscoutVP


def bouclage_func(idBcl, MaxIter, idTC, idVP):
    if idBcl == 0:
        itern = 1
        if PPM == 1:
            distribution.distribution('scen', 'PPM')
            choix_modal.choix_modal('scen', 'PPM', itern)
        if PCJ == 1:
            distribution.distribution('scen', 'PCJ')
            choix_modal.choix_modal('scen', 'PCJ', itern)
        if PPS == 1:
            distribution.distribution('scen', 'PPS')
            choix_modal.choix_modal('scen', 'PPS', itern)
    else:
        itern = 1
        done_affect = 0
        dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'wb')
        pkl.dump(done_affect, dbfile)
        dbfile.close()  # done_affect est un sentinel qu'on va utiliser pour s'assurer que multiprocessing (biblithéque utilisé pour
        # lancer les deux instances de Visum simultanément) ne créet pas les 'child process' à l'infini.
        if PPM == 1:
            distribution.distribution('scen', 'PPM')
            choix_modal.choix_modal('scen', 'PPM', itern)
            traitement.traitementVP('PPM', 'scen', 'PPM')
            # AFFECT_iter_PPM = bouclage.mat_iter('PPM', cParMatBcl)
        if PCJ == 1:
            distribution.distribution('scen', 'PCJ')
            choix_modal.choix_modal('scen', 'PCJ', itern)
            traitement.traitementVP('PCJ', 'scen', 'PCJ')
            # AFFECT_iter_PCJ = bouclage.mat_iter('PCJ', cParMatBcl)
        if PPS == 1:
            distribution.distribution('scen', 'PPS')
            choix_modal.choix_modal('scen', 'PPS', itern)
            traitement.traitementVP('PPS', 'scen', 'PPS')
            # AFFECT_iter_PPS = bouclage.mat_iter('PPS', cParMatBcl)
        bouclage.boucle(cParMatBcl, 1)
        while done_affect < PPM + PCJ + PPS:
            dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'rb')
            done_affect = pkl.load(dbfile)
            print(done_affect)
            time.sleep(60)      # Tant que la fonction d'affectation de VISUM défini dans Quatre_Etapes.affect n'a pas fini
            # de tourner, on s'arrête ici et on regarde tous les 60 secs pour voir s'il a terminé ou non.
        RMSE_PPM, RMSE_PCJ, RMSE_PPS = 0, 0, 0
        if PPM == 1:
            RMSE_PPM = bouclage.RMSE('PPM', 1)
        if PCJ == 1:
            RMSE_PCJ = bouclage.RMSE('PCJ', 1)
        if PPS == 1:
            RMSE_PPS = bouclage.RMSE('PPS', 1)

        while (RMSE_PPM > cConv_M or RMSE_PCJ > cConv_C or RMSE_PPS > cConv_S) and itern <= MaxIter:
            itern += 1
            done_affect = 0
            dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'wb')
            pkl.dump(done_affect, dbfile)
            if idBcl == 1:
                if PPM == 1:
                    distribution.distribution('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPM', itern)
                    traitement.traitementVP('PPM', 'scen', 'PPM')
                if PCJ == 1:
                    distribution.distribution('scen', 'PCJ')
                    choix_modal.choix_modal('scen', 'PCJ', itern)
                    traitement.traitementVP('PCJ', 'scen', 'PCJ')
                if PPS == 1:
                    distribution.distribution('scen', 'PPS')
                    choix_modal.choix_modal('scen', 'PPS', itern)
                    traitement.traitementVP('PPS', 'scen', 'PPS')

                bouclage.boucle(cParMatBcl, itern)
                while done_affect < PPM + PCJ + PPS:
                    dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'rb')
                    done_affect = pkl.load(dbfile)
                    time.sleep(60)
                if PPM == 1:
                    RMSE_PPM = bouclage.RMSE('PPM', itern)
                if PCJ == 1:
                    RMSE_PCJ = bouclage.RMSE('PCJ', itern)
                if PPS == 1:
                    RMSE_PPS = bouclage.RMSE('PPS', itern)
                bouclage.data_update(cParTpsBcl)
            elif idBcl == 2 or idBcl == 3:
                if PPM == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPM', itern)
                    traitement.traitementVP('PPM', 'scen', 'PPM')
                if PCJ == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PCJ', itern)
                    traitement.traitementVP('PCJ', 'scen', 'PCJ')
                if PPS == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPS', itern)
                    traitement.traitementVP('PPS', 'scen', 'PPS')
                bouclage.boucle(cParMatBcl, itern)
                while done_affect < PPM + PCJ + PPS:
                    dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'rb')
                    done_affect = pkl.load(dbfile)
                    print(done_affect)
                    time.sleep(60)
                if PPM == 1:
                    RMSE_PPM = bouclage.RMSE('PPM', itern)
                if PCJ == 1:
                    RMSE_PCJ = bouclage.RMSE('PCJ', itern)
                if PPS == 1:
                    RMSE_PPS = bouclage.RMSE('PPS', itern)
                bouclage.data_update(cParTpsBcl)

if __name__ == '__main__':
    # demande('scen', 1)
    # demande('actuel', 0)
    bouclage_func(1, cNbBcl, None, None)

