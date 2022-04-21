import numpy as np
from Data.A_CstesModus import *
import pandas as pd
from pathlib import Path

class user_md_cy_tc:
    def __init__(self, dossier, hor):
        self.hor = hor  # Time being considered: PPM, PCJ, PPS
        if self.hor == 'PPM' or 'PPS':
            no_hours = 4        # A factor that we'll divide the flows by to give their hourly equivalents
        else:
            no_hours = 6

        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', 'bdinter_scen'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/bdinter_scen'), 'rb')
        self.bdinter = pkl.load(dbfile)
        self.travel_time()      # A fonction that adds the overall travel time columns for TC, with appropriate coeffs

        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'Modus_CY_motcat_scen_{hor}'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_CY_motcat_scen_{hor}'), 'rb')
        self.flux_cy = pkl.load(dbfile) / no_hours        # To give the values per hour
        self.flux_cy_business, self.flux_cy_commute_school_childcare, self.flux_cy_others = self.flux_division(self.flux_cy)

        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'Modus_MD_motcat_scen_{hor}'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_MD_motcat_scen_{hor}'), 'rb')
        self.flux_md = pkl.load(dbfile) / no_hours      # To give the values per hour
        self.flux_md_business, self.flux_md_commute_school_childcare, self.flux_md_others = self.flux_division(
            self.flux_md)

        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'Modus_TC_motcat_scen_{hor}'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_TC_motcat_scen_{hor}'), 'rb')
        self.flux_tc = pkl.load(dbfile) / no_hours        # To give the values per hour
        self.flux_tc_business, self.flux_tc_commute_school_childcare, self.flux_tc_others = self.flux_division(
            self.flux_tc)
        
        self.VTTS_business = yaml_content['VTTS_business']  # Valeur du temps pour les usagers des VP motif =
        # business
        self.VTTS_commute_school_childcare = yaml_content['VTTS_commute_school_childcare']  # motif =
        # commute/school/childcare
        self.VTTS_others = yaml_content['VTTS_others']  # motif = 'others'
        


    def flux_division(self, flux_input):
        flux_business = flux_input[[2, 3, 13, 14]].sum(1)
        flux_commute_school_childcare = flux_input[[0, 1, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19]].sum(1)
        flux_others = flux_input[[9, 10, 20, 21]].sum(1)
        return flux_business, flux_commute_school_childcare, flux_others
    
    def vot_cy(self):
        vot_business = self.flux_cy_business * self.bdinter['DVOL']/VCY * self.VTTS_business
        vot_commute_school_childcare = (self.flux_cy_commute_school_childcare * self.bdinter['DVOL'] / VCY / 60 * 
                                        self.VTTS_commute_school_childcare)
        vot_others = self.flux_cy_others * self.bdinter['DVOL'] / VCY * self.VTTS_others
        vot_cy = (vot_others + vot_business + vot_commute_school_childcare).sum()
        return vot_cy

    def vot_md(self):
        vot_business = self.flux_md_business * self.bdinter['DVOL'] / VMD * self.VTTS_business
        vot_commute_school_childcare = (self.flux_md_commute_school_childcare * self.bdinter['DVOL'] / VMD / 60 *
                                        self.VTTS_commute_school_childcare)
        vot_others = self.flux_md_others * self.bdinter['DVOL'] / VMD * self.VTTS_others
        vot_md = (vot_others + vot_business + vot_commute_school_childcare).sum()
        return vot_md

    # def travel_time(self):
    #     for hor in ['PPM', 'PCJ', 'PPS']:
    #         self.bdinter[f'travel_time_{hor}'] = (
    #                 self.bdinter[f'TVEH_{hor}'] + self.bdinter[f'TATT_{hor}'] * yaml_content['multiplier_wait'] +
    #                 self.bdinter[f'TACC_{hor}'] * yaml_content['multiplier_access'] +
    #                 self.bdinter[f'TMAR_{hor}'] * yaml_content['multiplier_transfer']
    #         )

    def travel_time(self):
        self.bdinter['travel_time'] = (
                self.bdinter[f'TVEH_{self.hor}'] + self.bdinter[f'TATT_{self.hor}'] * yaml_content['multiplier_wait'] +
                self.bdinter[f'TACC_{self.hor}'] * yaml_content['multiplier_access'] +
                self.bdinter[f'TMAR_{self.hor}'] * yaml_content['multiplier_transfer']
        ) / 60      # Divide by 60 to convert to minutes

    def avg_cost_time_md(self):
        vot_md = self.vot_md()
        return vot_md/self.flux_md.sum().sum()
    
    def avg_cost_time_cy(self):
        vot_cy = self.vot_cy()
        return vot_cy/self.flux_cy.sum().sum()

    def avg_cost_time_tc(self):
        '''
        Inputs: currently works with bdinter as inputs, but eventually will work with skim matrix results from TC visum
        network (once that been received from the DRIEAT).
        :return: generalised_cost_time component
        '''
        total_time_business = (self.flux_tc_business * self.bdinter[f'travel_time']).sum()
               #TODO: Replace bdinter reference with skim matrix reference from VISUM TC network.
        total_time_commute_school_childcare = (
                (self.flux_tc_commute_school_childcare * self.bdinter[f'travel_time']).sum()
        )       # We divide by 60 because Modus gives outputs in minutes
        total_time_others = (self.flux_tc_others * self.bdinter[f'travel_time']).sum()
        generalised_cost_time = (
                total_time_business * self.VTTS_business +
                total_time_commute_school_childcare * self.VTTS_commute_school_childcare +
                total_time_others * self.VTTS_others
        ) / self.flux_tc.sum().sum()
        return generalised_cost_time

    def avg_cost_money_tc(self):
        generalised_cost_money = (self.flux_tc.sum(1) * self.bdinter['CTTKKM']).mean()
        return generalised_cost_money
#agrège ou non?

# def rule_of_half_tc_function(user_md_cy_tc1, user_md_cy_tc2):
#     '''
#     :param user_md_cy_tc1:
#     :param user_md_cy_tc2:
#     :return: change in consumer surplus for TC users
#     '''
#     delta_consumer_surp = (
#             0.5 * (user_md_cy_tc1.flux_tc.sum().sum() + user_md_cy_tc2.flux_tc.sum().sum()) *
#             (
#                     user_md_cy_tc1.generalised_cost_time_tc() + user_md_cy_tc1.generalised_cost_money_tc()
#                     - user_md_cy_tc2.generalised_cost_time_tc() - user_md_cy_tc2.generalised_cost_money_tc()
#             )
#     )
#     return delta_consumer_surp

def rule_of_half_tc_function(user_md_cy_tc1, user_md_cy_tc2):
    '''
    :param user_md_cy_tc1: 
    :param user_md_cy_tc2: 
    :return: change in consumer surplus for TC users
    '''
    delta_consumer_surp_business = (
            0.5 * (user_md_cy_tc1.flux_tc_business + user_md_cy_tc2.flux_tc_business) *
            (
                    user_md_cy_tc1.bdinter['travel_time'] * user_md_cy_tc1.VTTS_business + 
                    user_md_cy_tc1.bdinter['CTTKKM']
                    - (user_md_cy_tc2.bdinter['travel_time'] * user_md_cy_tc2.VTTS_business + 
                    user_md_cy_tc2.bdinter['CTTKKM'])
            )
    )
    delta_consumer_surp_commute_school_childcare = (
            0.5 * (user_md_cy_tc1.flux_tc_commute_school_childcare + user_md_cy_tc2.flux_tc_commute_school_childcare) *
            (
                    user_md_cy_tc1.bdinter['travel_time'] * user_md_cy_tc1.VTTS_commute_school_childcare +
                    user_md_cy_tc1.bdinter['CTTKKM']
                    - (user_md_cy_tc2.bdinter['travel_time'] * user_md_cy_tc2.VTTS_commute_school_childcare +
                       user_md_cy_tc2.bdinter['CTTKKM'])
            )
    )
    delta_consumer_surp_others = (
            0.5 * (user_md_cy_tc1.flux_tc_others + user_md_cy_tc2.flux_tc_others) *
            (
                    user_md_cy_tc1.bdinter['travel_time'] * user_md_cy_tc1.VTTS_others +
                    user_md_cy_tc1.bdinter['CTTKKM']
                    - (user_md_cy_tc2.bdinter['travel_time'] * user_md_cy_tc2.VTTS_others +
                       user_md_cy_tc2.bdinter['CTTKKM'])
            )
    )
    return (delta_consumer_surp_business + delta_consumer_surp_commute_school_childcare + delta_consumer_surp_others).sum().sum()

    # def avg_time_business(self):
    #     '''
    #     In: flux_business: flows corresponding to motive business, travel times from visum skim matrices
    #     :return: average travel time for the 'business' trip motive
    #     '''
    #     avg_time_business = self.flux_tc_business * self.bdinter
    #     return psn_hr_business/flux_business.sum()
    #
    # def avg_time_commute_school_childcare(self):
    #     '''
    #     Input: flows corresponding to motive commute_school_childcare, travel times from visum skim matrices
    #     :return: average travel time for the 'commute_school_childcare' trip motive
    #     '''
    #     flux_commute_school_childcare = (
    #                                         self.visum_data.flux_motifs_drieat[[0, 1, 4, 5, 6, 7, 8,
    #                                                         11, 12, 15, 16, 17, 18, 19]].to_numpy()
    #                                                         .sum(1).reshape(cNbZone, cNbZone)
    #                                      )
    #     temps_commute_school_childcare = self.visum_data.temps
    #     psn_hr_commute_school_childcare = self.flux_to_person_hr(flux_commute_school_childcare,
    #                                                              temps_commute_school_childcare, self.visum_data.taux_occpation)
    #     return psn_hr_commute_school_childcare / flux_commute_school_childcare.sum()
    #
    # def avg_time_others(self):
    #     '''
    #     Input: flows corresponding to motive other, travel times from visum skim matrices
    #     :return: average travel time for the 'other' trip motive
    #     '''
    #     flux_others = self.visum_data.flux_motifs_drieat[[9, 10, 20, 21]].to_numpy().sum(1).reshape(cNbZone, cNbZone)
    #     temps_others = self.visum_data.temps
    #     psn_hr_others = self.flux_to_person_hr(flux_others,
    #                                                              temps_others, self.visum_data.taux_occpation)
    #     return psn_hr_others / flux_others.sum()
    
    
    

    


if __name__ == '__main__':
    f1 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite')
    f2 = Path(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite')
    user_md_cy_tc1 = user_md_cy_tc(f1, 'PPM')
    user_md_cy_tc2 = user_md_cy_tc(f2, 'PPM')
    print(rule_of_half_tc_function(user_md_cy_tc1, user_md_cy_tc2))