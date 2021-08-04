# Ce modèle contient les tests des différents aspects de MODUS

# Importation des modules nécessaires à la réalisation des tests
import pandas as pd
import numpy as np
import unittest
# import Prepare_Data
from Data.A_CstesModus import *
import Data.generation_data

from Quatre_Etapes import generation
from Quatre_Etapes import distribution
from Data.util_data import OD

class Test_Generation(unittest.TestCase):
    def test_Generation_PPS(self):
        EM_test_PPS, ATT_test_PPS = generation.generation('actuel', 'PPS')
        EM_test_PPS = pd.DataFrame(EM_test_PPS)
        EM_validation_PPS = pd.read_sas('..\\em_hps_2012.sas7bdat')
        EM_validation_PPS.columns = range(28)
        diff = np.abs((EM_test_PPS - EM_validation_PPS)) / EM_validation_PPS
        sommediff = diff.sum().sum()
        self.assertLess(sommediff, 0.001)

    def test_Generation_PPM(self):
        EM_test_PPM, ATT_test_PPM = generation.generation('actuel', 'PPM')
        EM_test_PPM = pd.DataFrame(EM_test_PPM)
        EM_validation_PPM = pd.read_sas('..\\em_hpm_2012.sas7bdat')
        EM_validation_PPM.columns = range(28)
        diff = np.abs((EM_test_PPM - EM_validation_PPM)) / EM_validation_PPM
        sommediff = diff.sum().sum()
        self.assertLess(sommediff, 0.001)

    # def test_teletravail(self):
    #     generation.idTTV = 1
    #     # Data.generation_data.jourTTV = 0.3
    #     # Data.generation_data.partTTV = 0.75
    #     # generation_data.tauxTTVHQ = 0.85
    #     # generation_data.tauxTTVAQact = 0.228
    #     # generation_data.tauxTTVAQemp = 0.228
    #     # generation_data.varJTTVpro = 0.07
    #     # generation_data.varJLTHpro = 1.00
    #     # generation_data.varJTTVacc = 1.00
    #     # generation_data.varJLTHacc = 1.00
    #     # generation_data.varJTTVaut = 1.00
    #     # generation_data.varJLTHaut = 1.00
    #     EM_test_PPM, ATT_test_PPM = generation.generation('scen', 'PPM')
    #     self.assertEqual(np.round((EM_test_PPM.sum().sum() - 3631287), 0), 3311030)



    # def test_util_data(self):
    #     OD_test = OD('actuel')
    #     bdinter = pd.read_sas('..\\bdinter2012.sas7bdat')
    #     bdinter.rename(
    #         columns={'TMAR_HC': 'TMAR_PCJ', 'TACC_HC': 'TACC_PCJ', 'TMAR_HPS': 'TMAR_PPS', 'TVEH_HC': 'TVEH_PCJ',
    #                  'TACC_HPS': 'TACC_PPS', 'TRAB_HPM': 'TRAB_PPM', 'TATT_HPS': 'TATT_PPS', 'TRAB_HPS': 'TRAB_PPS',
    #                  'TMAR_HPM': 'TMAR_PPM', 'TVEH_HPS': 'TVEH_PPS', 'TRAB_HC': 'TRAB_PCJ', 'TVEH_HPM': 'TVEH_PPM',
    #                  'TACC_HPM': 'TACC_PPM', 'TATT_HC': 'TATT_PCJ', 'TATT_HPM': 'TATT_PPM', 'CTKKM': 'CTTKKM'},
    #         inplace=True)
    #     for i in range(1, 19):
    #         bdinter.drop(columns=f'CO{i}', inplace=True)
    #
    #     diff = np.abs(OD_test - bdinter) / bdinter
    #     diff = diff.replace(np.inf, 0)
    #     sommediff = diff.mean(0).sum()
    #     self.assertLess(sommediff, 0.1)

    # def test_distribution(self):
    #     dist_test = distribution.distribution('actuel', 'PPM')
    #     dist_valid = pd.read_sas('Other_files\\modus_motcat_2012_hpm.sas7bdat')
    #     dist_valid.columns = range(28)
    #     diff = np.abs(dist_test - dist_valid) / dist_valid
    #     diff = diff.replace(np.inf, 0)
    #     sommediff = diff.mean(0).mean()
    #     self.assertLess(sommediff, 0.1)

if __name__ == '__main__':
    unittest.main()