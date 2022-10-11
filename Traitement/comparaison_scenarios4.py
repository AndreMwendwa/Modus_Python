import pandas as pd
import matplotlib.pyplot as plt
import dotmap
import os
import seaborn as sns
import sys
from textwrap import wrap
import PySimpleGUI as sg
from ESE import visum_data, user_veh, externalites, user_md_cy_tc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Data.A_CstesModus import *
from pandas.plotting import parallel_coordinates
import datapane as dp

yaml_file = open(f'{dir_modus_py}\\Data\\config_yml.yml', 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
from pathlib import Path


def GetFilesToCompare():
    '''Pour séléctionner les dossiers avec les résultats'''
    form_rows = [[sg.Text('Veuillez choisir les dossiers qui contiennent des résultats que vous aimeriez comparer')],
                 [sg.Text('Dossier de résultats', size=(20, 1)),
                  sg.InputText(key='-file1-'), sg.FolderBrowse()],
                 [sg.Text('Scénario de référence', size=(20, 1)), sg.InputText(key='-file2-'),
                  sg.FolderBrowse(target='-file2-')],
                 [sg.Text('Dossiers de résultats', size=(20, 1)), sg.InputText(key='-file3-'),
                  sg.FolderBrowse(target='-file3-')],
                 [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Choix de scénarios', form_rows)
    event, values = window.read()
    window.close()
    return event, values

def call_dashboard():
    button, values = GetFilesToCompare()
    f1, f2, f3 = values['-file1-'], Path(values['-file2-']), Path(values['-file3-'])


    if any((button != 'Submit', f1 == '', f2 == '')):
        sg.popup_error('Operation cancelled')
        return

    subdirs = [Path(os.path.join(f1, x)) for x in os.listdir(f1)]
    results_dict_ESE = {}   # Dictionnaire où je vais mettre les résultats de l'ESE
    results_dict_VKT_VHT = {}   # Dictionnaire où je vais mettre les résultats VKT, VHT

    for folder in subdirs:
        if folder != f2:
            name, *files, vkt_vht = dashboard_datapane_comparaison(f2, folder, f3)
            results_dict_ESE[name] = files    # sauvegarde des résultats de l'ESE
            results_dict_VKT_VHT[name] = vkt_vht

    # Sauvegarde des résultats ESE
    with open(f'{f3}/result_dfs', 'wb') as dbfile:
        pkl.dump(results_dict_ESE, dbfile)

    # Sauvegarde des résultats VKT, VHT
    with open(f'{f3}/result_vkt_vht', 'wb') as dbfile:
        pkl.dump(results_dict_VKT_VHT, dbfile)








def dashboard_datapane_comparaison(f1, f2, f3):
    '''Cette fonction créé le Tableau de bord des indicateurs
    L'utilisateur séléctionne  les deux dossiers contenant les résultats de MODUS qu'il veut comparer.
    Le programme navigue automatiquement à la localisation de différents résultats, et alors construit un tableau de
    bord de comparaison entre ces résultats.
    '''
    name1, name2 = f1.parts[-1], f2.parts[-1]

    # Ici on prend les deux fichiers sur lesquels on se basera pour calculer les indicateurs de la mobilité
    dbfile = open(os.path.join(f1, '1_Fichiers_intermediares', 'tous_mobs'), 'rb')
    # dbfile = open(Path(f1 + '/1_Fichiers_intermediares/tous_mobs'), 'rb')
    tous_mobs1 = pkl.load(dbfile)

    dbfile = open(os.path.join(f2, '1_Fichiers_intermediares', 'tous_mobs'), 'rb')
    # dbfile = open(Path(f2 + '/1_Fichiers_intermediares/tous_mobs'), 'rb')
    tous_mobs2 = pkl.load(dbfile)

    tous_mobs = dotmap.DotMap()
    mob_keys = list(tous_mobs1.keys())
    for key in mob_keys:
        tous_mobs[key] = tous_mobs1[key].copy()
        if isinstance(tous_mobs[key], pd.DataFrame):
            for col in tous_mobs1[key].columns:
                if tous_mobs[key][col].dtypes != 'object':
                    tous_mobs[key][col] = tous_mobs1[key][col] - tous_mobs2[key][col]
        elif isinstance(tous_mobs[key], list):
            for i in range(len(tous_mobs[key])):
                for col in tous_mobs1[key][i].columns:
                    if tous_mobs[key][i][col].dtypes != 'object':
                        tous_mobs[key][i][col] = tous_mobs1[key][i][col] - tous_mobs2[key][i][col]

    # vkm2, vhr2, *autres2 = vkm_vhr_fn(f2)
    # vkm1, vhr1, *autres1 = vkm_vhr_fn(f1)

    class socio_eco:
        def __init__(self, f1, f2, f3, hor):
            self.hor = hor
            self.name = f1.parts[-1] + '-' + f2.parts[-1]
            self.f3 = f3
            self.visum_data1 = visum_data.visum_data(f1, hor)
            self.visum_data2 = visum_data.visum_data(f2, hor)
            self.user_md_cy_tc1 = user_md_cy_tc.user_md_cy_tc(f1, hor)
            self.user_md_cy_tc2 = user_md_cy_tc.user_md_cy_tc(f2, hor)
            self.dictionnaire_user_costs1 = {}  # Pour en faire un dataframe après
            self.dictionnaire_externalites1 = {}  # Pour en faire un dataframe après
            self.dictionnaire_user_costs2 = {}  # Pour en faire un dataframe après
            self.dictionnaire_externalites2 = {}  # Pour en faire un dataframe après
            self.all_outputs_ROTH1 = user_veh.all_outputs_ROTH(self.visum_data1)
            self.all_outputs_ROTH2 = user_veh.all_outputs_ROTH(self.visum_data2)
            self.externalites1 = externalites.externalites(self.visum_data1)
            self.externalites2 = externalites.externalites(self.visum_data2)
            self.user_df, self.totals_df = self.comparaison_df()
            self.dictionnaire_vkt_vht = {}  # Pour en faire un dataframe après


        def user_dict(self, all_outputs_ROTH, user_md_cy_tc_object):
            user_dict = {}  # Pour en faire un dataframe après
            user_dict[f'Road user generalised cost - time component, {self.hor}'] = \
                all_outputs_ROTH.avg_cost_time()
            user_dict[f'Road user generalised cost - money component, {self.hor}'] = \
                all_outputs_ROTH.avg_cost_money()
            user_dict[f'PT user generalised cost - time component, {self.hor}'] = \
                user_md_cy_tc_object.avg_cost_time_tc()
            user_dict[f'PT user generalised cost - money component, {self.hor}'] = \
                user_md_cy_tc_object.avg_cost_money_tc()
            user_dict[f'Walkers generalised cost - time component, {self.hor}'] = \
                user_md_cy_tc_object.avg_cost_time_md()
            user_dict[f'Cyclists generalised cost - money component, {self.hor}'] = \
                user_md_cy_tc_object.avg_cost_time_cy()
            return user_dict

        def totals_dict(self, externalites_object, user_md_cy_tc_object):
            totals_dict = {}  # Pour en faire un dataframe après
            totals_dict[f'Cost of local pollution, {self.hor}'] = externalites_object.polln_local()
            ghg, ghg_LCA = externalites_object.ghg_LCA_fn()
            totals_dict[f'Cost of climate change, {self.hor}'] = ghg
            totals_dict[f'Cost of climate change - life cycle effects, {self.hor}'] = ghg_LCA
            totals_dict[f'Cost of infrastructure usage, {self.hor}'] = externalites_object.usage_infras()
            totals_dict[f'Cost of noise, {self.hor}'] = externalites_object.noise()
            totals_dict[f'Cost of accidents, {self.hor}'] = externalites_object.accidentologie()
            totals_dict[f'Cyclists consumer surplus, {self.hor}'] = user_md_cy_tc_object.vot_cy()
            totals_dict[f'Walkers consumer surplus, {self.hor}'] = user_md_cy_tc_object.vot_md()
            return totals_dict

        def comparaison_df(self):
            user_df1 = pd.DataFrame(self.user_dict(self.all_outputs_ROTH1, self.user_md_cy_tc1),
                                      index=['Cost per user per hour (€) - scénario 1']).T
            user_df2 = pd.DataFrame(self.user_dict(self.all_outputs_ROTH2, self.user_md_cy_tc2),
                                      index=['Cost per user per hour (€) - scénario 2']).T
            totals_df1 = pd.DataFrame(self.totals_dict(self.externalites1, self.user_md_cy_tc1),
                                      index=['Total Cost per hour (€) - scénario 1']).T
            totals_df2 = pd.DataFrame(self.totals_dict(self.externalites2, self.user_md_cy_tc2),
                                      index=['Total Cost per hour (€) - scénario 2']).T
            user_df = pd.concat([user_df1, user_df2], axis=1)
            totals_df = pd.concat([totals_df1, totals_df2], axis=1)
            return user_df, totals_df

        def somme_df(self):
            totals_df = self.totals_df
            consumer_surplus_temps, consumer_surplus_money = user_veh.rule_of_half_vp_sep_time_money(self.visum_data1, self.visum_data2)
            totals_df['Total Cost per hour (€) - différence between scénarios'] = (
                    totals_df['Total Cost per hour (€) - scénario 1'] -
                    totals_df['Total Cost per hour (€) - scénario 2']
            )
            totals_df.loc[f'Road users consumer surplus (time), {self.hor}'
                f'Road users consumer surplus (time) , {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                consumer_surplus_temps
            totals_df.loc[f'Road users consumer surplus (money), {self.hor}'
                          f'Road users consumer surplus (money), {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                consumer_surplus_money
            totals_df.loc[
                f'PT users consumer surplus, , {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                user_md_cy_tc.rule_of_half_tc_function(self.user_md_cy_tc1, self.user_md_cy_tc2)
            totals_df.loc[
                f'Total change in surplus, {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                totals_df['Total Cost per hour (€) - différence between scénarios'].sum()
            totals_df.fillna('-', inplace=True)
            return totals_df

        def vkt_vht(self):
            self.dictionnaire_vkt_vht['VKT Scen 1'] = self.visum_data1.vkt_total_links
            self.dictionnaire_vkt_vht['VKT Scen 2'] = self.visum_data2.vkt_total_links
            self.dictionnaire_vkt_vht['VHT Scen 1'] = self.visum_data1.vht_total_links
            self.dictionnaire_vkt_vht['VHT Scen 2'] = self.visum_data2.vht_total_links
            vkt_vht_df = pd.DataFrame(self.dictionnaire_vkt_vht, index=[self.name])
            return vkt_vht_df
            

    # Créer les variables pour les utiliser après dans le graphe à venir
    if PPM:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PPM')
        comparaison_df_PPM = socio_eco_obj.user_df
        totals_PPM = socio_eco_obj.somme_df()
        vkt_vht_df_PPM = socio_eco_obj.vkt_vht()
    else:
        totals_PPM, comparaison_df_PPM, vkt_vht_df_PPM = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    if PCJ:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PCJ')
        comparaison_df_PCJ = socio_eco_obj.user_df
        totals_PCJ = socio_eco_obj.somme_df()
        vkt_vht_df_PCJ = socio_eco_obj.vkt_vht()
    else:
        totals_PCJ, comparaison_df_PCJ, vkt_vht_df_PCJ = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    if PPS:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PPS')
        comparaison_df_PPS = socio_eco_obj.user_df
        totals_PPS = socio_eco_obj.somme_df()
        vkt_vht_df_PPS = socio_eco_obj.vkt_vht()
    else:
        totals_PPS, comparaison_df_PPS, vkt_vht_df_PPS = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Début du code qui lance le dashboard.
    report = dp.Report(



            '# Indicateurs au niveau des individus',
            dp.Table(comparaison_df_PPM), dp.Table(comparaison_df_PCJ), dp.Table(comparaison_df_PPS),

            '# Indicateurs des totaux',
            dp.Table(totals_PPM), dp.Table(totals_PCJ), dp.Table(totals_PPS),

            '# Indicateurs des VKT, VHT',
            dp.Table(vkt_vht_df_PPM), dp.Table(vkt_vht_df_PCJ), dp.Table(vkt_vht_df_PPS),

            dp.Text('base originale MODUS (DRIEAT-IDF/SCDD/DMEM), modifié par le Laboratoire Ville Mobilité Transport'),
    )
    name_file = name2
    report.save(os.path.join(f3, f"{name_file}.html"), open=False)

    ## On créet un dictionnaire des dataframe de VKT, VHT
    # vkt_vht_dictionnaire = {}
    # vkt_vht_dictionnaire[name_file] = vkt_vht_df_PPM, vkt_vht_df_PCJ, vkt_vht_df_PPS
    vkt_vht = pd.concat([vkt_vht_df_PPM, vkt_vht_df_PCJ, vkt_vht_df_PPS])
    return name_file, totals_PPM, totals_PCJ, totals_PPS, vkt_vht



if __name__ == '__main__':
    print('Bienvenue au programme de comparaison des résultats de simulations avec Modus_Python')
    call_dashboard()
