import numpy as np

from Data.A_CstesModus import *
import pandas as pd

import Data.VisumPy.helpers2 as helpers
import win32com.client as win32
from dataclasses import dataclass
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from visum_data import visum_data


class all_outputs_ROTH:
    def __init__(self, visum_data):
        self.visum_data = visum_data
        self.flux_business, self.flux_commute_school_childcare, self.flux_others = \
            self.flux_division(self.visum_data.flux_motifs_drieat)
        self.travel_time = pd.DataFrame(self.visum_data.temps[:cNbZone, :cNbZone].reshape((cNbZone**2)))
        self.travel_distance = pd.DataFrame(self.visum_data.distance[:cNbZone, :cNbZone].reshape((cNbZone**2)))
    # def __init__(self, dossier, hor):
        # self.carburant_vp = yaml_content['VP_moy_fuel_basic']        # Vehicle fuel costs
        # self.operating_vp = yaml_content['VP_non_fuel_basic']        # Vehicle operating  costs - non fuel
        # self.capital_vp = yaml_content['VP_capital_marginal_basic']  # Vehicle capital  costs
        # self.user_veh_unit_cost = self.carburant_vp + self.operating_vp + self.capital_vp
        # self.VTTS_business = yaml_content['VTTS_business']      # Valeur du temps pour les usagers des VP motif =
        # # business
        # self.VTTS_commute_school_childcare = yaml_content['VTTS_commute_school_childcare']   # motif =
        # # commute/school/childcare
        # self.VTTS_others = yaml_content['VTTS_others']      # motif = 'others'
        # self.taux_occpation = yaml_content['taux_occupation']
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/MODUSCaleUVP_df_{hor}_scen'), 'rb')
        # self.flux_uvp = pkl.load(dbfile)
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_VP_motcat_scen_{hor}'), 'rb')
        #
        # # Pour chacun des motifs, on va créet une série, et le transformer en array numpy pour ensuite faire un
        # # reshape pour créer les matrices qui sont les inputs de l'étape de calculation des temps moyens
        # self.flux_apres_cm = pkl.load(dbfile)
        # self.flux_motifs_drieat = pd.DataFrame(np.zeros(self.flux_apres_cm.shape))
        # for col in self.flux_motifs_drieat.columns:
        #     self.flux_motifs_drieat[col] = self.flux_apres_cm[col] / self.flux_apres_cm.sum(1) * self.flux_uvp['FLUX']
        # self.flux_uvp_square = self.flux_uvp['FLUX'].to_numpy().reshape(cNbZone, cNbZone)
        # self.flux_uvp_sum = self.flux_uvp_square.sum()
        # self.dossier = dossier
        # self.hor = hor
        #
        # # Les temps et les distances pour notre scenario
        # self.temps, self.distance = self.load_skims()
        # self.temps_sum = self.temps[:cNbZone, :cNbZone].sum()    # Car dans VISUM il y a plus que les
        # # cNbZone nombre de zones qui sont des zones ordinaires de MODUS


    # def load_skims(self):
    #     visum_path = os.path.join(self.dossier, '2_Bouclage')
    #     for i in range(cNbBcl, 0, -1):
    #         path_iter = os.path.join(visum_path, f'Iter{i}')
    #         isExist = os.path.exists(path_iter)
    #         if isExist:
    #             break
    #     myvisum = win32.Dispatch("Visum.Visum")
    #     # PPM
    #     myvisum.LoadVersion(os.path.join(path_iter, f'Vers{self.hor}_scen_iter{i}.ver'))
    #     temps = helpers.GetSkimMatrix(myvisum, 'TpsCh', 'V')
    #     distance = helpers.GetSkimMatrix(myvisum, 'Dist', 'V')
    #     return temps, distance
    #
    # def read_flux(self):
    #     flux_different_types = DotMap()
    #     flux_motifs_drieat = pd.DataFrame(np.zeros(self.flux_apres_cm.shape))
    #     for col in flux_motifs_drieat.columns:
    #         flux_motifs_drieat[col] = self.flux_apres_cm[col]/self.flux_apres_cm.sum(1) * self.flux_uvp['FLUX']
    #
    #         # Pour chacun des motifs, on va créet une série, et le transformer en array numpy pour ensuite faire un
    #         # reshape pour créer les matrices qui sont les outputs de cette étape
    #     flux_different_types.flux_business = flux_motifs_drieat[[2, 3, 13, 14]].sum(1).to_numpy().reshape(cNbZone, cNbZone)
    #     flux_different_types.flux_commute_school_childcare = flux_motifs_drieat[[0, 1, 4, 5, 6, 7, 8,
    #                                                         11, 12, 15, 16, 17, 18, 19]].to_numpy()\
    #                                                         .sum(1).reshape(cNbZone, cNbZone)
    #     flux_different_types.flux_others = flux_motifs_drieat[[9, 10, 20, 21]].to_numpy().sum(1).reshape(cNbZone, cNbZone)
    #     return flux_different_types


    def flux_division(self, flux_input):
        flux_business = flux_input[[2, 3, 13, 14]].sum(1)
        flux_commute_school_childcare = flux_input[[0, 1, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19]].sum(1)
        flux_others = flux_input[[9, 10, 20, 21]].sum(1)
        return flux_business, flux_commute_school_childcare, flux_others

    def flux_to_person_hr(self, flux, tmps, taux_occupation):
        psn_hr = ((flux * tmps[:cNbZone, :cNbZone]).sum()/60) * taux_occupation
        return psn_hr

    def flux_to_vkm(self, flux, dist):
        vkm = (flux * dist[:cNbZone, :cNbZone]).sum()
        return vkm

    def total_time_business(self):
        '''
        In: flux_business: flows corresponding to motive business, travel times from visum skim matrices
        :return: average travel time for the 'business' trip motive
        '''
        flux_business = self.visum_data.flux_motifs_drieat[[2, 3, 13, 14]].sum(1).to_numpy().reshape(cNbZone, cNbZone)
        temps_business = self.visum_data.temps
        psn_hr_business = self.flux_to_person_hr(flux_business, temps_business, self.visum_data.taux_occpation)
        return psn_hr_business

    def total_time_commute_school_childcare(self):
        '''
        Input: flows corresponding to motive commute_school_childcare, travel times from visum skim matrices
        :return: average travel time for the 'commute_school_childcare' trip motive
        '''
        flux_commute_school_childcare = (
                                            self.visum_data.flux_motifs_drieat[[0, 1, 4, 5, 6, 7, 8,
                                                            11, 12, 15, 16, 17, 18, 19]].to_numpy()
                                                            .sum(1).reshape(cNbZone, cNbZone)
                                         )
        temps_commute_school_childcare = self.visum_data.temps
        psn_hr_commute_school_childcare = self.flux_to_person_hr(flux_commute_school_childcare,
                                                                 temps_commute_school_childcare, self.visum_data.taux_occpation)
        return psn_hr_commute_school_childcare

    def total_time_others(self):
        '''
        Input: flows corresponding to motive other, travel times from visum skim matrices
        :return: average travel time for the 'other' trip motive
        '''
        flux_others = self.visum_data.flux_motifs_drieat[[9, 10, 20, 21]].to_numpy().sum(1).reshape(cNbZone, cNbZone)
        temps_others = self.visum_data.temps
        psn_hr_others = self.flux_to_person_hr(flux_others, temps_others, self.visum_data.taux_occpation)
        return psn_hr_others

    def vkm(self):
        vkm = self.flux_to_vkm(self.visum_data.flux_uvp_square, self.visum_data.distance)
        return vkm

    def generalised_cost_time(self):
        '''Donne le composant du cout généralisé dû au temps pour la scénario en question'''
        generalised_cost_time = (
                self.visum_data.VTTS_business * self.total_time_business() +
                self.visum_data.VTTS_commute_school_childcare * self.total_time_commute_school_childcare() +
                self.visum_data.VTTS_others * self.total_time_others()
               ) / (self.visum_data.flux_uvp_sum * self.visum_data.taux_occpation)
        return generalised_cost_time

    def generalised_cost_money(self):
        '''Donne le composant du cout généralisé dû au cout d'utilisation du véhicule en termes monétaires
          pour la scénario en question'''
        generalised_cost_money = self.visum_data.user_veh_unit_cost * self.vkm()/self.visum_data.flux_uvp_sum
        return generalised_cost_money

# def rule_of_half_vp_function(visum_data1, visum_data2):
#     '''
#     :param f1: Path to reference scenario
#     :param f2:  Path to project scenario
#     :param hor: PPM/PCJ/PPS
#     :return: Consumer surplus for a single scenario
#     '''
#     ROTH1 = all_outputs_ROTH(visum_data1)
#     ROTH2 = all_outputs_ROTH(visum_data2)
#     delta_consumer_surp = (
#         0.5 * (ROTH1.visum_data.flux_uvp_sum + ROTH2.visum_data.flux_uvp_sum) *
#         (
#                 ROTH1.generalised_cost_time() + ROTH1.generalised_cost_money()
#               - ROTH2.generalised_cost_time() - ROTH2.generalised_cost_money()
#         )
#     )
#     return delta_consumer_surp

def rule_of_half_vp_function(visum_data1, visum_data2):
    '''
    :param f1: Path to reference scenario
    :param f2:  Path to project scenario
    :param hor: PPM/PCJ/PPS
    :return: Consumer surplus for a single scenario
    '''
    ROTH1 = all_outputs_ROTH(visum_data1)
    ROTH2 = all_outputs_ROTH(visum_data2)
    delta_consumer_surp_business = (
        0.5 * (ROTH1.visum_data.flux_ + ROTH2.visum_data.flux_uvp_sum) *
        (
                ROTH1.generalised_cost_time() + ROTH1.generalised_cost_money()
              - ROTH2.generalised_cost_time() - ROTH2.generalised_cost_money()
        )
    )
    return delta_consumer_surp

def calc_rule_of_the_half(f1, f2):
    '''
    :return: The total consumer surplus for all the scenarios considered (PPM, PCJ and PPS)
    '''

    delta_consumer_surplus = 0  # We initialize the consumer surplus

    if PPM:
        delta_consumer_surplus += rule_of_half_vp_function(visum_data(f1, 'PPM'), visum_data(f2, 'PPM'))
    if PCJ:
        delta_consumer_surplus += rule_of_half_vp_function(visum_data(f1, 'PCJ'), visum_data(f2, 'PCJ'))
    if PPS:
        delta_consumer_surplus += rule_of_half_vp_function(visum_data(f1, 'PPS'), visum_data(f2, 'PPS'))
    return delta_consumer_surplus







if __name__ == '__main__':
    # user_veh_fn(1e5)
    # user_time_vp(5e5)
    f1 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite')
    f2 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite')

    calc_rule_of_the_half(f1, f2)


