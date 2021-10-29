import numpy as np
import pandas as pd
import pickle as pkl
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes import distribution

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
from Data.A_CstesModus import *

# dbfile = open(f'{dir_dataTemp}params_user', 'rb')
# params_user = pkl.load(dbfile)


def choix_modal(n, hor, itern):
    dbfile = open(f'{dir_dataTemp}UTIL_DB', 'rb')
    db = pkl.load(dbfile)

    euTC = db['util_TC']
    euVP = db['util_VP']
    euCY = db['util_CY']
    euMD = db['util_MD']
    # Modus_motcat = distribution.distribution(n, hor)
    dbfile = open(f'{dir_dataTemp}Modus_motcat_{n}_{hor}', 'rb')
    Modus_motcat = pkl.load(dbfile)

    Modus_motcat = Modus_motcat @ Duplication.T

    seU = euTC + euVP + euCY + euMD



    if n == 'actuel':

        BASE = Modus_motcat/seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_MD_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl < 3 or itern == 1:
        BASE = Modus_motcat / seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_MD_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl == 3 and itern > 1:
        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'rb')
        Modus_MD_motcat = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'rb')
        Modus_CY_motcat = pkl.load(dbfile)

        BASE = (Modus_motcat - Modus_MD_motcat - Modus_CY_motcat)/seU
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl == 4 and itern > 1:
        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'rb')
        Modus_MD_motcat = pkl.load(dbfile)

        BASE = (Modus_motcat - Modus_MD_motcat) / seU
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    # return Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat










