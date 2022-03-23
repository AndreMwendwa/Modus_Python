import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import dotmap
import os
import sys
import seaborn as sns
import sys
from textwrap import wrap
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Quatre_Etapes.dossiers_simul import dir_dataTemp
from Data.A_CstesModus import *
from pandas.plotting import parallel_coordinates
import datapane as dp


def dashboard_datapane():
    '''Cette fonction créé le Tableau de bord des indicateurs'''

    # On lit d'abord la localisation actuelle de MODUS
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    dbfile = open(f'{dir_dataTemp}tous_mobs', 'rb')
    tous_mobs = pkl.load(dbfile)

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
    df_total = pd.DataFrame()   # Dataframe de tous les modes pour le calcul des parts modaux
    modes = ['TC', 'VP', 'CY', 'MD']    # Pour le dataframe montrant tous les modes

    # Parts modaux modes motorisés
    df_moto = pd.DataFrame()    # Dataframe des modes motorisés pour le calcul des parts modaux
    modes_moto = ['TC', 'VP']  # Pour le dataframe montrant tous les modes motorisés

    def parts_modaux_calc_df(hor, df_ttl, modes_choisis, numero_df):
        tous_mobs[f'part_actuel_{hor}'][numero_df].columns = modes_choisis
        tous_mobs[f'part_actuel_{hor}'][numero_df].index = [f'{actuel} PPM']
        # dp.Table(tous_mobs.part_scen_PPM[0])
        tous_mobs[f'part_scen_{hor}'][numero_df].columns = modes_choisis
        tous_mobs[f'part_scen_{hor}'][numero_df].index = [f'{scen} PPM']
        df_ttl = pd.concat([df_ttl, tous_mobs[f'part_actuel_{hor}'][numero_df], tous_mobs[f'part_scen_{hor}'][numero_df]])
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
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :4].sum(1), color='grey', label='MD')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :3].sum(1), color='brown', label='CY')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax7.legend(loc="best", frameon=True)


    fig8, ax8 = plt.subplots()
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax8.legend(loc="best", frameon=True)

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

    # Début du code qui lance le dashboard.
    report = dp.Report(
    '# Dashboard simple de MODUS',
    '## Le type de simulation',
    dp.Table(tous_mobs.simul),


    '## Les indicateurs de mobilité',
    dp.Table(tous_mobs.mob_PPM), '### Sous forme de graph', dp.Plot(fig26),

    dp.Table(tous_mobs.mob_PCJ), '### Sous forme de graph', dp.Plot(fig27),

    dp.Table(tous_mobs.mob_PPS), '### Sous forme de graph', dp.Plot(fig28),

    '## Les indicateurs de portée',
    dp.Table(tous_mobs.port_PPM), '### Sous forme de graphe', dp.Group(blocks=[dp.Plot(fig9), dp.Plot(fig10)], columns=2),

    dp.Table(tous_mobs.port_PCJ), '### Sous forme de graphe', dp.Group(blocks=[dp.Plot(fig11), dp.Plot(fig29)], columns=2),

    dp.Table(tous_mobs.port_PPS), '### Sous forme de graphe', dp.Group(blocks=[dp.Plot(fig12), dp.Plot(fig13)], columns=2),

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
                                                                                   dp.Table(tous_mobs.affect_PPM[3]),

    dp.Table(tous_mobs.affect_PCJ[0]), dp.Table(tous_mobs.affect_PCJ[1]), dp.Table(tous_mobs.affect_PCJ[2]), 
                                                                                   dp.Table(tous_mobs.affect_PCJ[3]),

    dp.Table(tous_mobs.affect_PPS[0]), dp.Table(tous_mobs.affect_PPS[1]), dp.Table(tous_mobs.affect_PPS[2]), 
                                                                                   dp.Table(tous_mobs.affect_PPS[3]),

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
    dp.Text('base originale MODUS (DRIEAT-IDF/SCDD/DMEM), modifié par le Laboratoire Ville Mobilité Transport')
    )
    name_file = dir_dataTemp.split('\\')[-3]
    # report.save(f"{name_file}.html", open=True)
    report.save(f"{dir_dataTemp}\\{name_file}.html", open=True)

if __name__ == '__main__':
    dashboard_datapane()
