from Quatre_Etapes import utility, distribution, choix_modal, bouclage
from Traitement import traitement
# import streamlit as st
from Traitement.gui3 import *
import time
from Traitement.indicateurs import indicateurs_func, print_typo
import shutil
import logging
from Quatre_Etapes.dossiers_simul import *
from Data.fonctions_gen import *
from Data.A_CstesModus import *
# from Traitement.dashboard_streamlit import dashboard_streamlit
# from Traitement.dashboard_datapane import dashboard_datapane
# from dossiers_simul import *

# def run_GUI():
#     modus_mode, bdinter, gen_results, dist_results, choix_results = None, None, None, None, None
#
#     submit = GUI()
#     print(submit)
#
#
#     if submit['-Bdinter_res-']:
#         modus_mode = 1
#         bdinter = submit['-bdinter-']
#     elif submit['-Gen_res-']:
#         modus_mode = 2
#         gen_results = submit['-gen_results-']
#     elif submit['-dist_results-']:
#         modus_mode = 3
#         dist_results = submit['-dist_results-']
#     elif submit['-choix_results-']:
#         modus_mode = 4
#         choix_results = submit['-choix_results-']
#
#
#     params_user = {'modus_mode': modus_mode, 'bdinter': bdinter, 'gen_results': gen_results,
#                                  'dist_results': dist_results, 'choix_results': choix_results}
#
#     dbfile = open(f'{dir_dataTemp}params_user', 'wb')
#     pkl.dump(params_user, dbfile)
#     dbfile.close()
#
#     n = submit[2]
#     per = submit[3]


def demande(n, itern):
    if PPM == 1:
        print("Calcul de la demande pour l'année de calage  \n")
        distribution.distribution(n, 'PPM')
        choix_modal.choix_modal(n, 'PPM', itern)
    if PCJ == 1:
        distribution.distribution(n, 'PCJ')
        choix_modal.choix_modal(n, 'PCJ', itern)
    if PPS == 1:
        distribution.distribution(n, 'PPS')
        choix_modal.choix_modal(n, 'PPS', itern)
    traitement.finalise(n)


def bouclage_func(idBcl, MaxIter):
    if idBcl == 0:
        itern = 1
        print("Calcul de la demande pour l'année de scénario  \n")
        dir_iter = os.path.join(out_bcl, 'Iter1')
        try:
            os.mkdir(dir_iter)
        except OSError:
            pass
        if PPM == 1:
            distribution.distribution('scen', 'PPM')
            choix_modal.choix_modal('scen', 'PPM', itern)
        if PCJ == 1:
            distribution.distribution('scen', 'PCJ')
            choix_modal.choix_modal('scen', 'PCJ', itern)
        if PPS == 1:
            distribution.distribution('scen', 'PPS')
            choix_modal.choix_modal('scen', 'PPS', itern)
        traitement.finalise('scen')
        traitement.report_calage(idTC, idVP)
    else:
        dir_iter = os.path.join(out_bcl, 'Iter1')
        try:
            os.mkdir(dir_iter)
        except OSError:
            pass
        itern = 1
        print("Calcul de la demande pour l'année de scénario  \n")
        print('Iteration = 1 \n')
        done_affect = 0
        dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'wb')
        pkl.dump(done_affect, dbfile)
        dbfile.close()  # done_affect est un sentinel qu'on va utiliser pour s'assurer que multiprocessing (biblithéque utilisé pour
        # lancer les deux instances de Visum simultanément) ne créet pas les 'child process' à l'infini.
        if PPM == 1:
            distribution.distribution('scen', 'PPM')
            choix_modal.choix_modal('scen', 'PPM', itern)
            # AFFECT_iter_PPM = bouclage.mat_iter('PPM', cParMatBcl)
        if PCJ == 1:
            distribution.distribution('scen', 'PCJ')
            choix_modal.choix_modal('scen', 'PCJ', itern)
            # AFFECT_iter_PCJ = bouclage.mat_iter('PCJ', cParMatBcl)
        if PPS == 1:
            distribution.distribution('scen', 'PPS')
            choix_modal.choix_modal('scen', 'PPS', itern)
            # AFFECT_iter_PPS = bouclage.mat_iter('PPS', cParMatBcl)
        traitement.finalise('scen')
        traitement.report_calage(idTC, idVP)
        bouclage.boucle(cParMatBcl, 1, dir_iter)
        while done_affect < PPM + PCJ + PPS:
            dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'rb')
            done_affect = pkl.load(dbfile)
            # print(done_affect)
            time.sleep(60)      # Tant que la fonction d'affectation de VISUM défini dans Quatre_Etapes.affect n'a pas fini
            # de tourner, on s'arrête ici et on regarde tous les 60 secs pour voir s'il a terminé ou non.
        RMSE_PPM, RMSE_PCJ, RMSE_PPS = 0, 0, 0
        if PPM == 1:
            RMSE_PPM = bouclage.RMSE('PPM', 1)
        if PCJ == 1:
            RMSE_PCJ = bouclage.RMSE('PCJ', 1)
        if PPS == 1:
            RMSE_PPS = bouclage.RMSE('PPS', 1)
        bouclage.data_update(cParTpsBcl, 'scen')
        while (RMSE_PPM > cConv_M or RMSE_PCJ > cConv_C or RMSE_PPS > cConv_S) and itern <= MaxIter:
            itern += 1
            print(f'Iteration = {itern} \n\n')
            dir_iter = os.path.join(out_bcl, f'Iter{itern}')
            try:
                os.mkdir(dir_iter)
            except OSError:
                pass
            done_affect = 0
            dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'wb')
            pkl.dump(done_affect, dbfile)
            if idBcl == 1:
                if PPM == 1:
                    distribution.distribution('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPM', itern)

                if PCJ == 1:
                    distribution.distribution('scen', 'PCJ')
                    choix_modal.choix_modal('scen', 'PCJ', itern)

                if PPS == 1:
                    distribution.distribution('scen', 'PPS')
                    choix_modal.choix_modal('scen', 'PPS', itern)
                traitement.finalise('scen')
                traitement.report_calage(idTC, idVP)
                bouclage.boucle(cParMatBcl, itern, dir_iter)
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
                bouclage.data_update(cParTpsBcl, 'scen')
            elif idBcl == 2 or idBcl == 3:
                if PPM == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPM', itern)
                if PCJ == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PCJ', itern)
                if PPS == 1:
                    utility.utilite('scen', 'PPM')
                    choix_modal.choix_modal('scen', 'PPS', itern)
                traitement.finalise('scen')
                traitement.report_calage(idTC, idVP)
                bouclage.boucle(cParMatBcl, itern, dir_iter)
                while done_affect < PPM + PCJ + PPS:
                    dbfile = open(f'{dir_dataTemp}done_affect{itern}', 'rb')
                    done_affect = pkl.load(dbfile)
                    # print(done_affect)
                    time.sleep(60)
                if PPM == 1:
                    RMSE_PPM = bouclage.RMSE('PPM', itern)
                if PCJ == 1:
                    RMSE_PCJ = bouclage.RMSE('PCJ', itern)
                if PPS == 1:
                    RMSE_PPS = bouclage.RMSE('PPS', itern)
                bouclage.data_update(cParTpsBcl, 'scen')
        # Dernière itération, avec paramètres à 0
        dir_iter = os.path.join(out_bcl, f'Iter{itern}')
        try:
            os.mkdir(dir_iter)
        except OSError:
            pass
        bouclage.data_update(0, 'scen')
        bouclage.boucle(0, itern, dir_iter)

# Une fonction pour copier les fichiers Python comme SAS fait actuellement avec les fichiers SAS.
def copy_files():
    Data_orig = os.path.join(dir_modus, 'Data')
    Data_new = os.path.join(programmes, 'Data')
    try:
        destination = shutil.copytree(Data_orig, Data_new)
    except FileExistsError:
        pass

    Quatre_Etapes_orig = os.path.join(dir_modus, 'Quatre_Etapes')
    Quatre_Etapes_new = os.path.join(programmes, 'Quatre_Etapes')
    try:
        destination = shutil.copytree(Quatre_Etapes_orig, Quatre_Etapes_new)
    except FileExistsError:
        pass

    Traitement_orig = os.path.join(dir_modus, 'Traitement')
    Traitement_new = os.path.join(programmes, 'Traitement')
    try:
        destination = shutil.copytree(Traitement_orig, Traitement_new)
    except FileExistsError:
        pass

def main_func():
    # copy_files()
    print("Bienvenue à Modus_Python. \n Vous avez choisi d'utiliser le modèle en mode ")
    if idBcl == 0:
        print("sans bouclage")
    else:
        print("avec bouclage")
    print(f"pour l'année de calage {actuel} et l'année de scénario {scen}")

    logging.basicConfig(filename=f'{dir_dataTemp}{nom_simul}_log.log', level=logging.INFO)
    logging.info('Début')
    demande('actuel', 0)
    bouclage_func(idBcl, cNbBcl)
    indicateurs_func()
    print_typo()
    logging.info('Fin')
    print('Quatre étapes de MODUS terminées')
    input("Appuyer sur 'Enter' pour fermer")
    # dashboard_streamlit()
    # dashboard_datapane()

if __name__ == '__main__':
    # demande('scen', 1)
    # copy_files()
    print("Bienvenue à Modus_Python. \n Vous avez choisi d'utiliser le modèle en mode ")
    if idBcl == 0:
        print("sans bouclage")
    else:
        print("avec bouclage")
    print(f"pour l'année de calage {actuel} et l'année de scénario {scen}")

    logging.basicConfig(filename=f'{dir_dataTemp}{nom_simul}_log.log', level=logging.INFO)
    logging.info('Début')
    demande('actuel', 0)
    bouclage_func(idBcl, cNbBcl)
    indicateurs_func()
    print_typo()
    logging.info('Fin')
    print('Quatre étapes de MODUS terminées')
    input("Appuyer sur 'Enter' pour fermer")
    # dashboard_streamlit()
    # run_GUI()
    # dashboard_datapane()
