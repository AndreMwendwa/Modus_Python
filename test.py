# Ce modèle contient les tests des différents aspects de MODUS

# Importation des modules nécessaires à la réalisation des tests
import pandas as pd
import numpy as np
from CstesModus_0 import *
from CstesStruct import *

from Modus_2 import generation

EM_test_PPM, ATT_test_PPM = generation('actuel', 'PPM')
EM_test_PPM = pd.DataFrame(EM_test_PPM)
EM_validation_PPM = pd.read_sas('em_hpm_2012.sas7bdat')
EM_validation_PPM.columns = range(28)
diff = (EM_test_PPM - EM_validation_PPM)/EM_validation_PPM
sommediff = diff.sum().sum()
assert sommediff < 0.001

EM_test_PPS, ATT_test_PPS = generation('actuel', 'PPS')
EM_test_PPS = pd.DataFrame(EM_test_PPS)
EM_validation_PPS = pd.read_sas('em_hps_2012.sas7bdat')
EM_validation_PPS.columns = range(28)
diff = (EM_test_PPS - EM_validation_PPS)/EM_validation_PPS
sommediff = diff.sum().sum()
assert sommediff < 0.001

