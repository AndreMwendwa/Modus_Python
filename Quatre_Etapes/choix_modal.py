import numpy as np
import pandas as pd
import pickle as pkl
from Data import util_data, A_CstesModus, CstesStruct
from Quatre_Etapes import distribution

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
from Data.A_CstesModus import *

dbfile = open(f'{dir_dataTemp}params_user', 'rb')
params_user = pkl.load(dbfile)
dbfile = open(f'{dir_dataTemp}UTIL_DB', 'rb')
db = pkl.load(dbfile)

euTC = db['util_TC']
euVP = db['util_VP']
euCY = db['util_CY']
euMD = db['util_MD']

def choix_modal(n, hor):

    Modus_motcat = distribution.distribution(n, hor)
    Modus_motcat = Modus_motcat @ Duplication.T

    seU = euTC + euVP + euCY + euMD

    itern = 0   # Kiko: Sentinel temporaire, à supprimer

    if n == 'actuel':

        BASE = Modus_motcat/seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl < 3 and itern > 1:
        BASE = Modus_motcat / seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl == 3 and itern > 1:
        BASE = (Modus_motcat - Modus_MD_motcat - Modus_CY_motcat)/seU
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    elif idBcl == 4 and itern > 1:
        BASE = (Modus_motcat - Modus_MD_motcat) / seU
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

    return Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat










