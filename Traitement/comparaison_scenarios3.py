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


    ## Arrondir les valeurs du dataframe de générations
    # différemment
    if PPM:
        decimales = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3],
                                  index=tous_mobs.mob_PPM.columns)  # A utiliser pour arrondir chaque colonne
        tous_mobs.mob_PPM = tous_mobs.mob_PPM.round(decimales)

    if PCJ:
        decimales = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3],
                                  index=tous_mobs.mob_PCJ.columns)  # A utiliser pour arrondir chaque colonne
        tous_mobs.mob_PCJ = tous_mobs.mob_PCJ.round(decimales)
    if PPS:
        decimales = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3],
                                  index=tous_mobs.mob_PPS.columns)  # A utiliser pour arrondir chaque colonne
        tous_mobs.mob_PPS = tous_mobs.mob_PPS.round(decimales)

    # Le nombre de générations par motif pour les périodes étudiées
    def mobs(hor):
        tous_mobs_hor = tous_mobs[f'mob_{hor}']
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[0, 1:3], color='grey',
                    label='Accompagnement')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[2:, 1:3].sum(), color='blue',
                    label='Accompagnement')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[3:, 1:3].sum(), color='brown',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[4:, 1:3].sum(), color='green',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[5:, 1:3].sum(), color='yellow',
                    label='Maternelle et primaire')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[6:, 1:3].sum(), color='purple',
                    label='Enseignement secondaire')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[7:, 1:3].sum(), color='aqua',
                    label='Etudes supérieures')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[8:, 1:3].sum(), color='bisque',
                    label='Achats-loisirs')
        sns.barplot(x=tous_mobs_hor.columns[1:3], y=tous_mobs_hor.iloc[9, 1:3], color='black',
                    label='Achats-loisirs')
        ax.legend(loc="right", frameon=True)
        return fig

    if PPM:
        fig26 = mobs('PPM')
    else:
        fig26 = plt.figure(figsize=(0, 0))
    if PCJ:
        fig27 = mobs('PCJ')
    else:
        fig27 = plt.figure(figsize=(0, 0))
    if PPS:
        fig28 = mobs('PPS')
    else:
        fig28 = plt.figure(figsize=(0, 0))



    # Les indicateurs de portée, sous forme de table et de graphe
    def portees(hor):
        tous_mobs.port_hor = tous_mobs[f'port_{hor}'].round(2)  # On arrondit le dataframe des portées ici
        tous_mobs.port_hor.reset_index(inplace=True)
        fig1, ax1 = plt.subplots(figsize=(20, 12))  # Pour faire des graphes
        list_cols = list(tous_mobs.port_hor.columns)
        valeurs_abs = list_cols[:7]
        labels1 = ['\n'.join(wrap(l, 10)) for l in valeurs_abs[1:]]
        # valeurs_abs = [x[:16].join('\n').join(x[16:]) for x in valeurs_abs]
        valeurs_evol = list_cols[7:]
        labels2 = ['\n'.join(wrap(l, 10)) for l in valeurs_evol]
        valeurs_evol.append(list_cols[0])  # La colonne 'index' doit être présente
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_hor.loc[:, valeurs_abs], 'index', colormap=plt.get_cmap("tab20"),
                             linewidth=6)
        # plt.xticks(rotation=10, fontsize=20, ticks=range(1, 7), labels=labels1)
        plt.xticks(rotation=10, fontsize=20)
        plt.tight_layout()
        ax1.legend(fontsize=20)

        fig2, ax2 = plt.subplots(figsize=(20, 12))
        plt.xticks(rotation=10, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_hor.loc[:, valeurs_evol], 'index', colormap=plt.get_cmap("tab20"),
                             linewidth=6)
        plt.tight_layout()
        ax2.legend(fontsize=20)
        return fig1, fig2

    if PPM:
        fig9, fig10 = portees('PPM')
    else:
        fig9, fig10 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    if PCJ:
        fig11, fig29 = portees('PCJ')
    else:
        fig11, fig29 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    if PPS:
        fig12, fig13 = portees('PPS')
    else:
        fig12, fig13 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    # Parts modaux tous modes
    df_total = pd.DataFrame()  # Dataframe de tous les modes pour le calcul des parts modaux
    modes = ['TC', 'VP', 'CY', 'MD']  # Pour le dataframe montrant tous les modes

    # Parts modaux modes motorisés
    df_moto = pd.DataFrame()  # Dataframe des modes motorisés pour le calcul des parts modaux
    modes_moto = ['TC', 'VP']  # Pour le dataframe montrant tous les modes motorisés

    def parts_modaux_calc_df(hor, df_ttl, modes_choisis, numero_df):
        tous_mobs[f'part_actuel_{hor}'][numero_df].columns = modes_choisis
        tous_mobs[f'part_actuel_{hor}'][numero_df].index = [f'{actuel} PPM']
        # dp.Table(tous_mobs.part_scen_PPM[0])
        tous_mobs[f'part_scen_{hor}'][numero_df].columns = modes_choisis
        tous_mobs[f'part_scen_{hor}'][numero_df].index = [f'{scen} PPM']
        df_ttl = pd.concat(
            [df_ttl, tous_mobs[f'part_actuel_{hor}'][numero_df], tous_mobs[f'part_scen_{hor}'][numero_df]])
        return df_ttl

    if PPM:
        df_total = parts_modaux_calc_df('PPM', df_total, modes, 0)
        df_moto = parts_modaux_calc_df('PPM', df_moto, modes_moto, 1)
    if PCJ:
        df_total = parts_modaux_calc_df('PCJ', df_total, modes, 0)
        df_moto = parts_modaux_calc_df('PPM', df_moto, modes_moto, 1)
    if PPS:
        df_total = parts_modaux_calc_df('PPS', df_total, modes, 0)
        df_moto = parts_modaux_calc_df('PPM', df_moto, modes_moto, 1)
    df_total = df_total.round(4)  # On arrondit le dataframe des parts modaux
    df_moto = df_moto.round(4)  # On arrondit le dataframe des parts modaux

    fig7, ax7 = plt.subplots()
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :4].sum(1), color='grey', label='CY')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :3].sum(1), color='brown', label='MD')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax7.legend(loc="best", frameon=True)

    fig8, ax8 = plt.subplots()
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax8.legend(loc="best", frameon=True)

    # Le nombre de déplacements par classe de distance
    # Arrondir les indicateurs de l'affectation
    def arrondir_affect(tous_mobs_par, hor):
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs_par.affect_PPM[0].columns)
        tous_mobs_par.affect_PPM[0] = tous_mobs_par[f'affect_{hor}'][0].round(decimales)
        tous_mobs_par.affect_PPM[1] = tous_mobs_par[f'affect_{hor}'][1].round(decimales)
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs_par.affect_PPM[2].columns)
        tous_mobs_par.affect_PPM[2] = tous_mobs_par[f'affect_{hor}'][2].round(decimales)
        tous_mobs_par.affect_PPM[3] = tous_mobs_par[f'affect_{hor}'][3].round(decimales)
        return tous_mobs_par

    if PPM:
        tous_mobs = arrondir_affect(tous_mobs, 'PPM')
    if PCJ:
        tous_mobs = arrondir_affect(tous_mobs, 'PCJ')
    if PPS:
        tous_mobs = arrondir_affect(tous_mobs, 'PPS')

    def deplacements_distance(hor):
        fig, ax = plt.subplots()
        ax = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs[f'graph_TC_{hor}'])
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = TC")
        plt.ylabel('Nombre de déplacements')

        fig2, ax2 = plt.subplots()
        ax2 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs[f'graph_UVP_{hor}'])
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = VP")
        plt.ylabel('Nombre de déplacements')

        fig3, ax3 = plt.subplots()
        ax3 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs[f'graph_MD_{hor}'])
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = MD")
        plt.ylabel('Nombre de déplacements')

        fig4, ax4 = plt.subplots()
        ax4 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs[f'graph_CY_{hor}'])
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = CY")
        plt.ylabel('Nombre de déplacements')

        fig5, ax5 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs[f'graph_parts_actuel_{hor}'], color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs[f'graph_parts_actuel_{hor}'], color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs[f'graph_parts_actuel_{hor}'], color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs[f'graph_parts_actuel_{hor}'], color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax5.legend(ncol=2, loc="best", frameon=True)

        fig6, ax6 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs[f'graph_parts_scen_{hor}'], color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs[f'graph_parts_scen_{hor}'], color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs[f'graph_parts_scen_{hor}'], color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs[f'graph_parts_scen_{hor}'], color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax6.legend(ncol=2, loc="best", frameon=True)
        return fig, fig2, fig3, fig4, fig5, fig6

    if PPM:
        fig, fig2, fig3, fig4, fig5, fig6 = deplacements_distance('PPM')
    else:
        fig, fig2, fig3, fig4, fig5, fig6 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                            plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                                plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))


    if PCJ:
        fig14, fig15, fig16, fig17, fig18, fig19 = deplacements_distance('PCJ')
    else:
        fig14, fig15, fig16, fig17, fig18, fig19 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                            plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                                plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    if PPS:
        fig20, fig21, fig22, fig23, fig24, fig25 = deplacements_distance('PPS')
    else:
        fig20, fig21, fig22, fig23, fig24, fig25 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                            plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                                plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))


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
        dp.Page(


            '# Indicateurs au niveau des individus',
            dp.Table(comparaison_df_PPM), dp.Table(comparaison_df_PCJ), dp.Table(comparaison_df_PPS),

            '# Indicateurs des totaux',
            dp.Table(totals_PPM), dp.Table(totals_PCJ), dp.Table(totals_PPS),

            '# Indicateurs des VKT, VHT',
            dp.Table(vkt_vht_df_PPM), dp.Table(vkt_vht_df_PCJ), dp.Table(vkt_vht_df_PPS),

            dp.Text('base originale MODUS (DRIEAT-IDF/SCDD/DMEM), modifié par le Laboratoire Ville Mobilité Transport'),
            title='Résumé',
        ),
        dp.Page(
        '# Comparaison des résultats de deux simulations de MODUS',
        f'## Scénario de projet = {name1}',
        f'## Scénario de réference = {name2}',
        '## Le type de simulation',
        dp.Table(tous_mobs.simul),

        '## Les indicateurs de mobilité',
        dp.Table(tous_mobs.mob_PPM), '### Sous forme de graph', dp.Plot(fig26),

        dp.Table(tous_mobs.mob_PCJ), '### Sous forme de graph', dp.Plot(fig27),

        dp.Table(tous_mobs.mob_PPS), '### Sous forme de graph', dp.Plot(fig28),

        '## Les indicateurs de portée',
        dp.Table(tous_mobs.port_PPM), '### Sous forme de graphe',
        dp.Group(blocks=[dp.Plot(fig9), dp.Plot(fig10)], columns=2),

        dp.Table(tous_mobs.port_PCJ), '### Sous forme de graphe',
        dp.Group(blocks=[dp.Plot(fig11), dp.Plot(fig29)], columns=2),

        dp.Table(tous_mobs.port_PPS), '### Sous forme de graphe',
        dp.Group(blocks=[dp.Plot(fig12), dp.Plot(fig13)], columns=2),

        '## Les parts modaux : tous les modes',

        '### Sous forme de tableau',
        dp.Table(df_total),

        '### Sous forme de tableau',
        dp.Table(df_moto),
        '### Sous forme de graph',
        dp.Group(
            blocks=[dp.Plot(fig7), dp.Plot(fig8)], columns=2),

        '## Les parts modaux : les modes motorisés',

        "## Les indicateurs de l'affectation",
        dp.Table(tous_mobs.affect_PPM[0]), dp.Table(tous_mobs.affect_PPM[1]), dp.Table(tous_mobs.affect_PPM[2]),

        dp.Table(tous_mobs.affect_PCJ[0]), dp.Table(tous_mobs.affect_PCJ[1]), dp.Table(tous_mobs.affect_PCJ[2]),

        dp.Table(tous_mobs.affect_PPS[0]), dp.Table(tous_mobs.affect_PPS[1]), dp.Table(tous_mobs.affect_PPS[2]),

        "## Indicateurs graphiques des matrices MODUS",

        "### Periode = PPM",
        dp.Group(blocks=[dp.Plot(fig), dp.Plot(fig2)], columns=2),
        dp.Group(blocks=[dp.Plot(fig3), dp.Plot(fig4)], columns=2),
        dp.Group(blocks=[dp.Plot(fig5), dp.Plot(fig6)], columns=2),

        "### Periode = PCJ",
        dp.Group(blocks=[dp.Plot(fig14), dp.Plot(fig15)], columns=2),
        dp.Group(blocks=[dp.Plot(fig16), dp.Plot(fig17)], columns=2),
        dp.Group(blocks=[dp.Plot(fig18), dp.Plot(fig19)], columns=2),

        "### Periode = PPS",
        dp.Group(blocks=[dp.Plot(fig20), dp.Plot(fig21)], columns=2),
        dp.Group(blocks=[dp.Plot(fig22), dp.Plot(fig23)], columns=2),
        dp.Group(blocks=[dp.Plot(fig24), dp.Plot(fig25)], columns=2),

        dp.Text('base originale MODUS (DRIEAT-IDF/SCDD/DMEM), modifié par le Laboratoire Ville Mobilité Transport'),
            title='Détaillé'
    ))
    name_file = name2
    report.save(os.path.join(f3, f"{name_file}.html"), open=True)

    ## On créet un dictionnaire des dataframe de VKT, VHT
    # vkt_vht_dictionnaire = {}
    # vkt_vht_dictionnaire[name_file] = vkt_vht_df_PPM, vkt_vht_df_PCJ, vkt_vht_df_PPS
    vkt_vht = pd.concat([vkt_vht_df_PPM, vkt_vht_df_PCJ, vkt_vht_df_PPS])
    return name_file, totals_PPM, totals_PCJ, totals_PPS, vkt_vht



if __name__ == '__main__':
    print('Bienvenue au programme de comparaison des résultats de simulations avec Modus_Python')
    call_dashboard()
