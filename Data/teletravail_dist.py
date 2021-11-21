# Fonction pour modifier la matrice de paramètres de distribution
from Data.A_CstesModus import *


def modif_dist_par(dist_par, per):
    # dist_par.iloc[0, 2:3] *= ACTacc
    # dist_par.iloc[1, 2:3] *= EMPacc
    # dist_par.iloc[3, 2:3] *= HQPro
    # dist_par.iloc[4, 2:3] *= AQPro
    # dist_par.iloc[10, 2:3] *= ACTaut
    # dist_par.iloc[11, 2:3] *= ACTaut
    if per == 'PPM':
        dist_par.iloc[3:7, 2:3] *= factPPM
    elif per == 'PPS':
        dist_par.iloc[3:7, 2:3] *= factPPS
    return dist_par



