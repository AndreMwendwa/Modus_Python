import pandas as pd
import matplotlib.pyplot as plt
import dotmap
import os
import seaborn as sns
import sys
from textwrap import wrap
import PySimpleGUI as sg
from ESE import visum_data, user_veh, user_pt, externalites, user_md_cy_tc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Data.A_CstesModus import *
from pandas.plotting import parallel_coordinates
import datapane as dp

yaml_file = open(f'{dir_modus_py}\\Data\\config_yml.yml', 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)


def dashboard_datapane_comparaison():
    '''Cette fonction créé le Tableau de bord des indicateurs
    L'utilisateur séléctionne  les deux dossiers contenant les résultats de MODUS qu'il veut comparer.
    Le programme navigue automatiquement à la localisation de différents résultats, et alors construit un tableau de
    bord de comparaison entre ces résultats.
    '''
    def GetFilesToCompare():
        '''Pour séléctionner les dossiers avec les résultats'''
        form_rows = [[sg.Text('Veuillez choisir les dossiers qui contiennent des résultats que vous aimeriez comparer')],
                     [sg.Text('Scénario de référence', size=(20, 1)),
                      sg.InputText(key='-file1-'), sg.FolderBrowse()],
                     [sg.Text('Scénario de projet', size=(20, 1)), sg.InputText(key='-file2-'),
                      sg.FolderBrowse(target='-file2-')],
                     [sg.Text('Dossiers de résultats', size=(20, 1)), sg.InputText(key='-file3-'),
                      sg.FolderBrowse(target='-file3-')],
                     [sg.Submit(), sg.Cancel()]]

        window = sg.Window('Choix de scénarios', form_rows)
        event, values = window.read()
        window.close()
        return event, values

    button, values = GetFilesToCompare()
    f1, f2, f3 = values['-file1-'], values['-file2-'], values['-file3-']
    name1, name2 = f1.split('/')[-1], f2.split('/')[-1]

    if any((button != 'Submit', f1 == '', f2 == '')):
        sg.popup_error('Operation cancelled')
        return

    # Ici on prend les deux fichiers sur lesquels on se basera pour calculer les indicateurs de la mobilité
    dbfile = open(Path(f1 + '/1_Fichiers_intermediares/tous_mobs'), 'rb')
    tous_mobs1 = pkl.load(dbfile)

    dbfile = open(Path(f2 + '/1_Fichiers_intermediares/tous_mobs'), 'rb')
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

    # Calcul des indicateurs socio-économiques
    # Scénario 1
    dbfile = open(f'{Path(f1)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    bdinter = pkl.load(dbfile)
    dvol = bdinter['DVOL']
    tvpm, tpmc, tvps = bdinter['TVPM'], bdinter['TVPC'], bdinter['TVPS']    # Temps VP pour les trois périodes

    couts_df_scen1 = pd.DataFrame()    # Le dataframe où seront enregistrés des résultats du calcul une fois terminée.

    if PPM:
        dbfile = open(Path(f1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPM_scen'), 'rb')
        VP1_PPM = pkl.load(dbfile)
        VP1_PPM_VKM = VP1_PPM.FLUX * dvol
        VP1_PPM_VKM_total = VP1_PPM_VKM.sum()
        VP1_PPM_Vhr = VP1_PPM.FLUX * tvpm
        VP1_PPM_Vhr_total = VP1_PPM_Vhr.sum()
        couts_df_scen1 = pd.concat([couts_df_scen1, pd.DataFrame.from_dict({'PPM': [VP1_PPM_VKM_total, VP1_PPM_Vhr_total]})], axis=1)

    if PCJ:
        dbfile = open(Path(f1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PCJ_scen'), 'rb')
        VP1_PCJ = pkl.load(dbfile)
        VP1_PCJ_VKM = VP1_PCJ.FLUX * dvol
        VP1_PCJ_VKM_total = VP1_PCJ_VKM.sum()
        VP1_PCJ_Vhr = VP1_PCJ.FLUX * tvpm
        VP1_PCJ_Vhr_total = VP1_PCJ_Vhr.sum()
        couts_df_scen1 = pd.concat([couts_df_scen1, pd.DataFrame.from_dict({'PCJ': [VP1_PCJ_VKM_total, VP1_PCJ_Vhr_total]})], axis=1)

    if PPS:
        dbfile = open(Path(f1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPS_scen'), 'rb')
        VP1_PPS = pkl.load(dbfile)
        VP1_PPS_VKM = VP1_PPS.FLUX * dvol
        VP1_PPS_VKM_total = VP1_PPS_VKM.sum()
        VP1_PPS_Vhr = VP1_PPS.FLUX * tvpm
        VP1_PPS_Vhr_total = VP1_PPS_Vhr.sum()
        couts_df_scen1 = pd.concat([couts_df_scen1, pd.DataFrame.from_dict({'PPS': [VP1_PPS_VKM_total, VP1_PPS_Vhr_total]})], axis=1)
    couts_df_scen1.index = ['VKM', 'Veh-hr']
    #
    # # Scénario 2
    # dbfile = open(f'{Path(f2)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    # bdinter = pkl.load(dbfile)
    # dvol = bdinter['DVOL']
    # tvpm, tpmc, tvps = bdinter['TVPM'], bdinter['TVPC'], bdinter['TVPS']  # Temps VP pour les trois périodes
    #
    # couts_df_scen2 = pd.DataFrame()  # Le dataframe où seront enregistrés des résultats du calcul une fois terminée.
    #
    # if PPM:
    #     dbfile = open(Path(f2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPM_scen'), 'rb')
    #     VP2_PPM = pkl.load(dbfile)
    #     VP2_PPM_VKM = VP2_PPM.FLUX * dvol
    #     VP2_PPM_VKM_total = VP2_PPM_VKM.sum()
    #     VP2_PPM_Vhr = VP2_PPM.FLUX * tvpm
    #     VP2_PPM_Vhr_total = VP2_PPM_Vhr.sum()
    #     couts_df_scen2 = pd.concat(
    #         [couts_df_scen2, pd.DataFrame.from_dict({'PPM': [VP2_PPM_VKM_total, VP2_PPM_Vhr_total]})], axis=1)
    #
    # if PCJ:
    #     dbfile = open(Path(f2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PCJ_scen'), 'rb')
    #     VP2_PCJ = pkl.load(dbfile)
    #     VP2_PCJ_VKM = VP2_PCJ.FLUX * dvol
    #     VP2_PCJ_VKM_total = VP2_PCJ_VKM.sum()
    #     VP2_PCJ_Vhr = VP2_PCJ.FLUX * tvpm
    #     VP2_PCJ_Vhr_total = VP2_PCJ_Vhr.sum()
    #     couts_df_scen2 = pd.concat(
    #         [couts_df_scen2, pd.DataFrame.from_dict({'PCJ': [VP2_PCJ_VKM_total, VP2_PCJ_Vhr_total]})], axis=1)
    #
    # if PPS:
    #     dbfile = open(Path(f2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPS_scen'), 'rb')
    #     VP2_PPS = pkl.load(dbfile)
    #     VP2_PPS_VKM = VP2_PPS.FLUX * dvol
    #     VP2_PPS_VKM_total = VP2_PPS_VKM.sum()
    #     VP2_PPS_Vhr = VP2_PPS.FLUX * tvpm
    #     VP2_PPS_Vhr_total = VP2_PPS_Vhr.sum()
    #     couts_df_scen2 = pd.concat(
    #         [couts_df_scen2, pd.DataFrame.from_dict({'PPS': [VP2_PPS_VKM_total, VP2_PPS_Vhr_total]})], axis=1)
    # couts_df_scen2.index = ['VKM', 'Veh-hr']
    #
    #
    # # Différence de VKM, Veh-hr
    # couts_df_diff = couts_df_scen1 - couts_df_scen2     # Difference entre les dataframes pour trouver le dataframe
    # # de comparaison
    # cout_df_diff_total = couts_df_diff.sum(axis=1)
    # cout_diff_comparative = cout_df_diff_total/couts_df_scen1.sum(axis=1) * 100
    # cout_df_diff_total.name = f'Difference en valeur absolu entre les scénarios (unités)'
    # cout_diff_comparative.name = f'Différence relative entre les scénarios (%)'
    # valeurs_tutelaires = pd.DataFrame.from_dict({'Valeurs_tutelaires (€/unité)': [yaml_content['CO2_VP'],
    #                                                                     yaml_content['Valeur_temp']]})
    # valeurs_tutelaires.index = ['VKM', 'Veh-hr']
    # cout_df_diff_total = pd.concat([cout_df_diff_total, cout_diff_comparative], axis=1)
    # cout_df_diff_total = pd.concat([cout_df_diff_total, valeurs_tutelaires], axis=1)
    # cout_df_diff_total['Valeurs économiques (€)'] = cout_df_diff_total[f'Difference en valeur absolu entre les scénarios (unités)'] * \
    #                                             cout_df_diff_total['Valeurs_tutelaires (€/unité)']
    # decimales = pd.Series([2, 2, 4, 2], index=cout_df_diff_total.columns)    # A utiliser pour arrondir chaque colonne
    # # différemment
    # cout_df_diff_total = cout_df_diff_total.round(decimales)   # On doit arrondir deux fois, puisque on va vréer une ligne qui
    # # contient un mélange de string et de float, alors il faut arrondir toute la dataframe avant de la rajouter.
    # somme = pd.DataFrame({f'Difference en valeur absolu entre les scénarios (unités)': '-', 'Valeurs_tutelaires (€/unité)': '-',
    #                                'Valeurs économiques (€)': cout_df_diff_total['Valeurs économiques (€)'].sum()},
    #                                index=['Total'])
    # cout_df_diff_total = pd.concat([cout_df_diff_total, somme])
    # cout_df_diff_total.fillna(inplace=True, value='-')
    # cout_df_diff_total = cout_df_diff_total.round(2)

    # # Utilisant les chiffres des tronçons
    # couts_df_scen1 = pd.DataFrame({'PPM': [autres1[0], autres1[2]], 'PPS': [autres1[1], autres1[3]]},
    #                               index=['VKM', 'Veh-hr'])
    # couts_df_scen2 = pd.DataFrame({'PPM': [autres2[0], autres2[2]], 'PPS': [autres2[1], autres2[3]]},
    #                               index=['VKM', 'Veh-hr'])
    # couts_df_diff = couts_df_scen1 - couts_df_scen2
    #
    # cout_df_diff_total = pd.DataFrame({'VKM': vkm2 - vkm1, 'Vhr': vhr2 - vhr1},
    #                              index=['Difference en valeur absolu entre les scénarios (unités)'])
    # cout_df_diff_total = cout_df_diff_total.T
    # cout_df_diff_total['Différence relative entre les scénarios (%)'] = \
    #     cout_df_diff_total['Difference en valeur absolu entre les scénarios (unités)']/pd.Series([vkm1, vhr1], index=['VKM', 'Vhr']) * 100
    # cout_df_diff_total['Valeurs_tutelaires (€/unité)'] = pd.DataFrame({'Valeurs_tutelaires (€/unité)':[yaml_content['CO2_VP']
    #     , yaml_content['Valeur_temp']]}, index=['VKM', 'Vhr'])
    # cout_df_diff_total['Valeurs économiques (€)'] = cout_df_diff_total['Difference en valeur absolu entre les scénarios (unités)'] * \
    #                                                 cout_df_diff_total['Valeurs_tutelaires (€/unité)']
    # decimales = pd.Series([2, 2, 4, 2], index=cout_df_diff_total.columns)  # A utiliser pour arrondir chaque colonne
    # # # différemment
    # cout_df_diff_total = cout_df_diff_total.round(decimales)
    # somme = pd.DataFrame(
    #     {f'Difference en valeur absolu entre les scénarios (unités)': '-', 'Valeurs_tutelaires (€/unité)': '-',
    #                                 'Valeurs économiques (€)': cout_df_diff_total['Valeurs économiques (€)'].sum()},
    #                                 index=['Total'])
    # cout_df_diff_total = pd.concat([cout_df_diff_total, somme])
    # cout_df_diff_total.fillna(inplace=True, value='-')
    # cout_df_diff_total = cout_df_diff_total.round(2)

    # couts_df_diff, cout_df_diff_total, couts_df_scen1, couts_df_scen2 = calcul_socio_eco(f1, f2)

    # # Les graphes des indicateurs socio-éco
    # fig30, ax30 = plt.subplots()
    # sns.barplot(x=couts_df_diff.columns, y=couts_df_diff.loc['VKM', :])
    # plt.title(f'Différence de VKM parcourus entre les deux scénarios ')
    # plt.tight_layout(pad=2)
    #
    # fig31, ax31 = plt.subplots()
    # sns.barplot(x=couts_df_diff.columns, y=couts_df_diff.loc['Veh-hr', :])
    # plt.title(f'Différence de véhicule-hrs parcourus entre les deux scénarios ')
    # plt.tight_layout(pad=2)
    #
    # #Les graphes des valeurs relatives des indicateurs socio-éco
    # fig32, ax32 = plt.subplots()
    # sns.barplot(x=couts_df_diff.columns, y=couts_df_diff.loc['VKM', :]/couts_df_scen1.loc['VKM', :] * 100)
    # plt.title(f'Différence relative de VKM parcourus entre les deux scénarios ')
    # plt.ylabel('Différence en %')
    # plt.tight_layout(pad=2)
    #
    # fig33, ax33 = plt.subplots()
    # sns.barplot(x=couts_df_diff.columns, y=couts_df_diff.loc['Veh-hr', :]/couts_df_scen1.loc['VKM', :] * 100)
    # plt.title(f'Différence relative de véhicule-hrs parcourus entre les deux scénarios ')
    # plt.ylabel('Différence en %')
    # plt.tight_layout(pad=2)

    class socio_eco:
        def __init__(self, f1, f2, f3, hor):
            self.hor = hor
            self.name = (f1.split('/')[-1]) + '-' + f2.split('/')[-1]
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
            totals_df['Total Cost per hour (€) - différence between scénarios'] = (
                    totals_df['Total Cost per hour (€) - scénario 1'] -
                    totals_df['Total Cost per hour (€) - scénario 2']
            )
            totals_df.loc[
                f'Road users consumer surplus , {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                user_veh.rule_of_half_vp_function(self.visum_data1, self.visum_data2)
            totals_df.loc[
                f'PT users consumer surplus, , {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                user_md_cy_tc.rule_of_half_tc_function(self.user_md_cy_tc1, self.user_md_cy_tc2)
            totals_df.loc[
                f'Total change in surplus, {self.hor}', 'Total Cost per hour (€) - différence between scénarios'] = \
                totals_df['Total Cost per hour (€) - différence between scénarios'].sum()
            totals_df.fillna('-', inplace=True)
            totals_df.to_excel(f'{self.f3}/{self.name}_{self.hor}.xlsx')
            return totals_df


    #     def outputs_socio_eco(self, dictionnaire_user_costs, dictionnaire_externalites, dossier_projet):
    #         ''' This function actually does two things: filling the user costs, and externalities dictionnaries,
    #         and creating the visum_data object which is the input for the RoTH road user calculation'''
    #         visum_data_object = visum_data.visum_data(dossier_projet, self.hor)
    #         all_outputs_ROTH = user_veh.all_outputs_ROTH(visum_data_object)
    #         user_md_cy_tc_object = user_md_cy_tc.user_md_cy_tc(dossier_projet, self.hor)
    #         externalites_object = externalites.externalites(visum_data_object)
    #         dictionnaire_user_costs[f'Road user generalised cost - time component, {self.hor}'] = \
    #             all_outputs_ROTH.generalised_cost_time()
    #         dictionnaire_user_costs[f'Road user generalised cost - money component, {self.hor}'] = \
    #             all_outputs_ROTH.generalised_cost_money()
    #         dictionnaire_user_costs[f'PT user generalised cost - time component, {self.hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_tc()
    #         dictionnaire_user_costs[f'PT user generalised cost - money component, {self.hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_money_tc()
    #         dictionnaire_user_costs[f'Walkers generalised cost - time component, {self.hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_md()
    #         dictionnaire_user_costs[f'Cyclists generalised cost - money component, {self.hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_cy()
    #         dictionnaire_externalites['Cost of local pollution'] = externalites_object.polln_local()
    #         ghg, ghg_LCA = externalites_object.ghg_LCA_fn()
    #         dictionnaire_externalites['Cost of climate change'] = ghg
    #         dictionnaire_externalites['Cost of climate change - life cycle effects'] = ghg_LCA
    #         dictionnaire_externalites['Cost of infrastructure usage'] = externalites_object.usage_infras()
    #         dictionnaire_externalites['Cost of noise'] = externalites_object.noise()
    #
    #     def dataframe_comparaison(self):
    #
    #
    #
    # def indicateurs_socio_eco():
    #     dictionnaire_user_costs1 = {}  # Pour en faire un dataframe après
    #     dictionnaire_externalites1 = {}  # Pour en faire un dataframe après
    #     dictionnaire_user_costs2 = {}  # Pour en faire un dataframe après
    #     dictionnaire_externalites2 = {}  # Pour en faire un dataframe après
    #     dossier_projet1 = os.path.abspath(os.path.join(f1, '..'))
    #     dossier_projet2 = os.path.abspath(os.path.join(f2, '..'))
    #
    #     def outputs_socio_eco(hor, dictionnaire_user_costs, dictionnaire_externalites, dossier_projet):
    #         ''' This function actually does two things: filling the user costs, and externalities dictionnaries,
    #         and creating the visum_data object which is the input for the RoTH road user calculation'''
    #         visum_data_object = visum_data.visum_data(dossier_projet, hor)
    #         all_outputs_ROTH = user_veh.all_outputs_ROTH(visum_data_object)
    #         user_md_cy_tc_object = user_md_cy_tc.user_md_cy_tc(dossier_projet, hor)
    #         externalites_object = externalites.externalites(visum_data_object)
    #         dictionnaire_user_costs[f'Road user generalised cost - time component, {hor}'] = \
    #             all_outputs_ROTH.generalised_cost_time()
    #         dictionnaire_user_costs[f'Road user generalised cost - money component, {hor}'] = \
    #             all_outputs_ROTH.generalised_cost_money()
    #         dictionnaire_user_costs[f'PT user generalised cost - time component, {hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_tc()
    #         dictionnaire_user_costs[f'PT user generalised cost - money component, {hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_money_tc()
    #         dictionnaire_user_costs[f'Walkers generalised cost - time component, {hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_md()
    #         dictionnaire_user_costs[f'Cyclists generalised cost - money component, {hor}'] = \
    #             user_md_cy_tc_object.generalised_cost_time_cy()
    #         dictionnaire_externalites['Cost of local pollution'] = externalites_object.polln_local()
    #         ghg, ghg_LCA = externalites_object.ghg_LCA_fn()
    #         dictionnaire_externalites['Cost of climate change'] = ghg
    #         dictionnaire_externalites['Cost of climate change - life cycle effects'] = ghg_LCA
    #         dictionnaire_externalites['Cost of infrastructure usage'] = externalites_object.usage_infras()
    #         dictionnaire_externalites['Cost of noise'] = externalites_object.noise()
    #         return visum_data_object, user_md_cy_tc_object
    #
    #     if PPM:
    #         visum_data1, user_md_cy_tc_object1 = outputs_socio_eco('PPM', dictionnaire_user_costs1, dictionnaire_externalites1, dossier_projet1)
    #         visum_data2 = outputs_socio_eco('PPM', dictionnaire_user_costs2, dictionnaire_externalites2, dossier_projet2)
    #
    #     if PCJ:
    #         outputs_socio_eco('PCJ', dictionnaire_user_costs1, dictionnaire_externalites1)
    #         outputs_socio_eco('PCJ', dictionnaire_user_costs2, dictionnaire_externalites2)
    #     if PPS:
    #         outputs_socio_eco('PPS', dictionnaire_user_costs1, dictionnaire_externalites1)
    #         outputs_socio_eco('PPS', dictionnaire_user_costs2, dictionnaire_externalites2)
    #
    #     indic_socio_eco1 = pd.DataFrame(dictionnaire_user_costs1, index=['Cost per user per hour (€) - scénario 1'])
    #     indic_socio_eco2 = pd.DataFrame(dictionnaire_user_costs1, index=['Cost per user per hour (€) - scénario 2'])
    #     indic_socio_eco = pd.concat([indic_socio_eco1, indic_socio_eco2])
    #     indic_socio_eco = indic_socio_eco.T
    #
    #     externalites_df1 = pd.DataFrame(dictionnaire_externalites1, index=['Total Cost per hour (€) - scénario 1'])
    #     externalites_df2 = pd.DataFrame(dictionnaire_externalites2, index=['Total Cost per hour (€) - scénario 2'])
    #     externalites_df = pd.concat([externalites_df1, externalites_df2])
    #     externalites_df = indic_socio_eco.T
    #     return indic_socio_eco, externalites_df

    # Créer les variables pour les utiliser après dans le graphe à venir
    if PPM:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PPM')
        comparaison_df_PPM = socio_eco_obj.user_df
        totals_PPM = socio_eco_obj.somme_df()
    else:
        totals_PPM, comparaison_df_PPM = pd.DataFrame(), pd.DataFrame()
    if PCJ:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PCJ')
        comparaison_df_PCJ = socio_eco_obj.user_df
        totals_PCJ = socio_eco_obj.somme_df()
    else:
        totals_PCJ, comparaison_df_PCJ = pd.DataFrame(), pd.DataFrame()
    if PPS:
        socio_eco_obj = socio_eco(f1, f2, f3, 'PPS')
        comparaison_df_PPS = socio_eco_obj.user_df
        totals_PPS = socio_eco_obj.somme_df()
    else:
        totals_PPS, comparaison_df_PPS = pd.DataFrame(), pd.DataFrame()

    # Début du code qui lance le dashboard.
    report = dp.Report(
        dp.Page(


            '# Indicateurs au niveau des individus',
            dp.Table(comparaison_df_PPM), dp.Table(comparaison_df_PCJ), dp.Table(comparaison_df_PPS),

            '# Indicateurs des totaux',
            dp.Table(totals_PPM), dp.Table(totals_PCJ), dp.Table(totals_PPS),

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
    name_file = name1 + '-' + name2
    report.save(f"{f3}/{name_file}.html", open=True)


if __name__ == '__main__':
    print('Bienvenue au programme de comparaison des résultats de simulations avec Modus_Python')
    dashboard_datapane_comparaison()
