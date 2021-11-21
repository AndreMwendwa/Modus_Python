import pandas as pd
import numpy as np
from dataclasses import dataclass
from Data.A_CstesModus import *
from Data.teletravail_dist import modif_dist_par
from Quatre_Etapes.dossiers_simul import *


@dataclass
class dist_data:
    per: str = ''
    n: str = ''

    def DIST_PAR_FUNC(self):
        if idTTVdist == 1 and self.n == 'scen':
            return modif_dist_par(pd.read_sas(DIST_PAR_DICT[self.per]), self.per)
        else:
            return pd.read_sas(DIST_PAR_DICT[self.per])


