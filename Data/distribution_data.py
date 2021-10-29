import pandas as pd
import numpy as np
from dataclasses import dataclass
from Data import A_CstesModus, CstesStruct
from Data.A_CstesModus import *
from Data.teletravail_dist import modif_dist_par

# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from importlib import reload
reload(A_CstesModus)
reload(CstesStruct)


@dataclass
class dist_data:
    per: str = ''
    n: str = ''

    def DIST_PAR_FUNC(self):
        if idTTVdist == 0:
            return pd.read_sas(DIST_PAR_DICT[self.per])
        else:
            return modif_dist_par(pd.read_sas(DIST_PAR_DICT[self.per]))


