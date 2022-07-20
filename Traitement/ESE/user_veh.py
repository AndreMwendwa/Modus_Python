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
            self.flux_division(self.visum_data.flux_motifs_drieat)          # Ce sont des flux de personnes, puisqu'on a
        # multiplié par le taux d'occupation dans la fonction flux_division.
        self.travel_time = pd.DataFrame(self.visum_data.temps[:cNbZone, :cNbZone].reshape((cNbZone**2))) / 60
        # Divide by 60 to convert to hours
        self.travel_distance = pd.DataFrame(self.visum_data.distance[:cNbZone, :cNbZone].reshape((cNbZone**2)))
        self.generalised_cost_money = self.travel_distance * self.visum_data.user_veh_unit_cost

    def flux_division(self, flux_input):
        flux_input = flux_input.copy() * self.visum_data.taux_occpation
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

    def avg_cost_time(self):
        '''Donne le composant du cout généralisé dû au temps pour la scénario en question'''
        generalised_cost_time = (
                self.visum_data.VTTS_business * self.total_time_business() +
                self.visum_data.VTTS_commute_school_childcare * self.total_time_commute_school_childcare() +
                self.visum_data.VTTS_others * self.total_time_others()
               ) / (self.visum_data.flux_uvp_sum * self.visum_data.taux_occpation)
        return generalised_cost_time

    def avg_cost_money(self):
        '''Donne le composant du cout généralisé dû au cout d'utilisation du véhicule en termes monétaires
          pour la scénario en question'''
        generalised_cost_money = self.visum_data.user_veh_unit_cost * self.vkm()/self.visum_data.flux_uvp_sum
        return generalised_cost_money

    
    

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
        pd.DataFrame(0.5 * (ROTH1.flux_business + ROTH2.flux_business)) *
        pd.DataFrame((
                ROTH1.travel_time * ROTH1.visum_data.VTTS_business + ROTH1.generalised_cost_money
              - (ROTH2.travel_time * ROTH2.visum_data.VTTS_business + ROTH2.generalised_cost_money)
        ))
    )       # Because when it's not a dataframe, it tries to multiply the two series like one is a row vector and the
    # other a column vector
    delta_consumer_surp_commute_school_childcare = (
            pd.DataFrame(0.5 * (ROTH1.flux_commute_school_childcare + ROTH2.flux_commute_school_childcare)) *
            pd.DataFrame((
                    ROTH1.travel_time * ROTH1.visum_data.VTTS_commute_school_childcare + ROTH1.generalised_cost_money
                    - (ROTH2.travel_time * ROTH2.visum_data.VTTS_commute_school_childcare + ROTH2.generalised_cost_money)
            ))
    )
    delta_consumer_surp_others = (
            pd.DataFrame(0.5 * (ROTH1.flux_others + ROTH2.flux_others)) *
            pd.DataFrame((
                    ROTH1.travel_time * ROTH1.visum_data.VTTS_others + ROTH1.generalised_cost_money
                    - (ROTH2.travel_time * ROTH2.visum_data.VTTS_others + ROTH2.generalised_cost_money)
            ))
    )
    return (delta_consumer_surp_business + delta_consumer_surp_commute_school_childcare + delta_consumer_surp_others).sum().sum()

def rule_of_half_vp_sep_time_money(visum_data1, visum_data2):
    '''
    :param f1: Path to reference scenario
    :param f2:  Path to project scenario
    :param hor: PPM/PCJ/PPS
    :return: Consumer surplus for a single scenario
    '''
    ROTH1 = all_outputs_ROTH(visum_data1)
    ROTH2 = all_outputs_ROTH(visum_data2)
    delta_consumer_surp_business = (
        pd.DataFrame(0.5 * (ROTH1.flux_business + ROTH2.flux_business)) *
        pd.DataFrame((
                ROTH1.travel_time * ROTH1.visum_data.VTTS_business
              - (ROTH2.travel_time * ROTH2.visum_data.VTTS_business)
        ))
    )       # Because when it's not a dataframe, it tries to multiply the two series like one is a row vector and the
    # other a column vector
    delta_consumer_surp_commute_school_childcare = (
            pd.DataFrame(0.5 * (ROTH1.flux_commute_school_childcare + ROTH2.flux_commute_school_childcare)) *
            pd.DataFrame((
                    ROTH1.travel_time * ROTH1.visum_data.VTTS_commute_school_childcare
                    - (ROTH2.travel_time * ROTH2.visum_data.VTTS_commute_school_childcare)
            ))
    )
    delta_consumer_surp_others = (
            pd.DataFrame(0.5 * (ROTH1.flux_others + ROTH2.flux_others)) *
            pd.DataFrame((
                    ROTH1.travel_time * ROTH1.visum_data.VTTS_others
                    - (ROTH2.travel_time * ROTH2.visum_data.VTTS_others)
            ))
    )
    delta_consumer_surp_money = (
            pd.DataFrame(0.5 * (ROTH1.flux_others + ROTH1.flux_commute_school_childcare + ROTH1.flux_business +
                                ROTH2.flux_others + ROTH2.flux_commute_school_childcare + ROTH2.flux_business)) *
            pd.DataFrame(ROTH1.generalised_cost_money - ROTH2.generalised_cost_money)
    )
    return (delta_consumer_surp_business + delta_consumer_surp_commute_school_childcare + delta_consumer_surp_others).sum().sum()\
        , delta_consumer_surp_money.sum().sum()


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
    # f1 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite')
    # f2 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite')
    f1 = Path(
        r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\teletravail_resultats\without_TTV_recalibré_factech2')
    f2 = Path(
        r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\teletravail_resultats\with_TTV_gen_nodist_recalibré_factech')
    print(calc_rule_of_the_half(f1, f2))


