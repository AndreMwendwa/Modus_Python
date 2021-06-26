# Ce modèle contient les tests des différents aspects de MODUS

# Importation des modules nécessaires à la réalisation des tests
import pandas as pd
import numpy as np
import unittest

from C_Modus import generation

class Test_Generation(unittest.TestCase):
    def test_Generation_PPS(self):
        EM_test_PPS, ATT_test_PPS = generation('actuel', 'PPS')
        EM_test_PPS = pd.DataFrame(EM_test_PPS)
        EM_validation_PPS = pd.read_sas('em_hps_2012.sas7bdat')
        EM_validation_PPS.columns = range(28)
        diff = np.abs((EM_test_PPS - EM_validation_PPS)) / EM_validation_PPS
        sommediff = diff.sum().sum()
        self.assertLess(sommediff, 0.001)

    def test_Generation_PPM(self):
        EM_test_PPM, ATT_test_PPM = generation('actuel', 'PPM')
        EM_test_PPM = pd.DataFrame(EM_test_PPM)
        EM_validation_PPM = pd.read_sas('em_hpm_2012.sas7bdat')
        EM_validation_PPM.columns = range(28)
        diff = np.abs((EM_test_PPM - EM_validation_PPM)) / EM_validation_PPM
        sommediff = diff.sum().sum()
        self.assertLess(sommediff, 0.001)


if __name__ == '__main__':
    unittest.main()