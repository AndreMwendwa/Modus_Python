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
    plots26 = []
    if PPM:
        tous_mobsPPM = tous_mobs.mob_PPM
        fig26, ax26 = plt.subplots(figsize=(15, 8))
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[0, 1:3], color='grey',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[2:, 1:3].sum(), color='blue',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[3:, 1:3].sum(), color='brown',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[4:, 1:3].sum(), color='green',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[5:, 1:3].sum(), color='yellow',
                    label='Maternelle et primaire')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[6:, 1:3].sum(), color='purple',
                    label='Enseignement secondaire')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[7:, 1:3].sum(), color='aqua',
                    label='Etudes supérieures')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[8:, 1:3].sum(), color='bisque',
                    label='Achats-loisirs')
        sns.barplot(x=tous_mobsPPM.columns[1:3], y=tous_mobsPPM.iloc[9, 1:3], color='black',
                    label='Achats-loisirs')
        ax26.legend(loc="right", frameon=True)
        plots26.append(fig26)
    if PCJ:
        tous_mobsPCJ = tous_mobs.mob_PCJ
        fig27, ax27 = plt.subplots(figsize=(15, 8))
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[0, 1:3], color='grey',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[2:, 1:3].sum(), color='blue',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[3:, 1:3].sum(), color='brown',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[4:, 1:3].sum(), color='green',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[5:, 1:3].sum(), color='yellow',
                    label='Maternelle et primaire')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[6:, 1:3].sum(), color='purple',
                    label='Enseignement secondaire')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[7:, 1:3].sum(), color='aqua',
                    label='Etudes supérieures')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[8:, 1:3].sum(), color='bisque',
                    label='Achats-loisirs')
        sns.barplot(x=tous_mobsPCJ.columns[1:3], y=tous_mobsPCJ.iloc[9, 1:3], color='black',
                    label='Achats-loisirs')
        ax27.legend(loc="right", frameon=True)
        plots26.append(fig27)
    else:
        fig27 = plt.figure(figsize=(0, 0))
        plots26.append(fig27)
    if PPS:
        tous_mobsPPS = tous_mobs.mob_PPS
        fig28, ax28 = plt.subplots(figsize=(15, 8))
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[0, 1:3], color='grey',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[2:, 1:3].sum(), color='blue',
                    label='Accompagnement')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[3:, 1:3].sum(), color='brown',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[4:, 1:3].sum(), color='green',
                    label='Professionnel et Travail')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[5:, 1:3].sum(), color='yellow',
                    label='Maternelle et primaire')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[6:, 1:3].sum(), color='purple',
                    label='Enseignement secondaire')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[7:, 1:3].sum(), color='aqua',
                    label='Etudes supérieures')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[8:, 1:3].sum(), color='bisque',
                    label='Achats-loisirs')
        sns.barplot(x=tous_mobsPPS.columns[1:3], y=tous_mobsPPS.iloc[9, 1:3], color='black',
                    label='Achats-loisirs')
        ax28.legend(loc="right", frameon=True)
        plots26.append(fig28)
    else:
        fig28 = plt.figure(figsize=(0, 0))
        plots26.append(fig28)



    # Les indicateurs de portée, sous forme de table et de graphe
    plots9 = []
    if PPM:
        tous_mobs.port_PPM = tous_mobs.port_PPM.round(2)   # On arrondit le dataframe des portées ici
        tous_mobs.port_PPM.reset_index(inplace=True)
        fig9, ax9 = plt.subplots(figsize=(20, 12))  # Pour faire des graphes
        list_cols = list(tous_mobs.port_PPM.columns)
        valeurs_abs = list_cols[:7]
        labels9 = ['\n'.join(wrap(l, 10)) for l in valeurs_abs[1:]]
        # valeurs_abs = [x[:16].join('\n').join(x[16:]) for x in valeurs_abs]
        valeurs_evol = list_cols[7:]
        labels10 = ['\n'.join(wrap(l, 10)) for l in valeurs_evol]
        valeurs_evol.append(list_cols[0])  # La colonne 'index' doit être présente
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PPM.loc[:, valeurs_abs], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        # plt.xticks(rotation=90, fontsize=20, ticks=range(1, 7), labels=labels9)
        plt.xticks(rotation=90, fontsize=20)
        plt.tight_layout()
        ax9.legend(fontsize=20)
    
        fig10, ax10 = plt.subplots(figsize=(20, 12))
        plt.xticks(rotation=90, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PPM.loc[:, valeurs_evol], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        plt.tight_layout()
        ax10.legend(fontsize=20)
    else:
        fig9, fig10 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))
    
    if PCJ:
        tous_mobs.port_PCJ.reset_index(inplace=True)
        tous_mobs.port_PCJ = tous_mobs.port_PCJ.round(2)  # On arrondit le dataframe des portées ici
        fig29, ax29 = plt.subplots(figsize=(20, 12))   # Pour faire des graphes
        list_cols = list(tous_mobs.port_PCJ.columns)
        valeurs_abs = list_cols[:7]
        valeurs_evol = list_cols[7:]
        valeurs_evol.append(list_cols[0])  # La colonne 'index' doit être présente
        # ticks = plt.xticks(ticks=[], labels=valeurs_abs,  rotation='vertical')
        plt.xticks(rotation=90, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PCJ.loc[:, valeurs_abs], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        plt.tight_layout()
        ax29.legend(fontsize=20)

        fig11, ax11 = plt.subplots(figsize=(20, 12))
        plt.xticks(rotation=90, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PCJ.loc[:, valeurs_evol], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        plt.tight_layout()
        ax11.legend(fontsize=20)
    else:
        fig11 = plt.figure(figsize=(0, 0))
        fig29 = plt.figure(figsize=(0, 0))

    if PPS:
        tous_mobs.port_PPS.reset_index(inplace=True)
        tous_mobs.port_PPS = tous_mobs.port_PPS.round(2)  # On arrondit le dataframe des portées ici
        fig12, ax12 = plt.subplots(figsize=(20, 12))   # Pour faire des graphes
        list_cols = list(tous_mobs.port_PPS.columns)
        valeurs_abs = list_cols[:7]
        valeurs_evol = list_cols[7:]
        valeurs_evol.append(list_cols[0])  # La colonne 'index' doit être présente
        # ticks = plt.xticks(ticks=[], labels=valeurs_abs,  rotation='vertical')
        plt.xticks(rotation=90, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PPS.loc[:, valeurs_abs], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        plt.tight_layout()
        ax12.legend(fontsize=20)

        #Le deuxième graphe
        fig13, ax13 = plt.subplots(figsize=(20, 12))
        plt.xticks(rotation=90, fontsize=20)
        plt.yticks(fontsize=20)
        plt.title('Les indicateurs de portée', fontsize=24)
        parallel_coordinates(tous_mobs.port_PPS.loc[:, valeurs_evol], 'index', colormap=plt.get_cmap("tab20"), linewidth=6)
        plt.tight_layout()
        ax13.legend(fontsize=20)
    else:
        fig12, fig12  = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    # Parts modaux tous modes
    df_total = pd.DataFrame()   # Dataframe de tous les modes pour le calcul des parts modaux
    modes = ['TC', 'VP', 'CY', 'MD']    # Pour le dataframe montrant tous les modes
    if PPM:
        # dp.Table(tous_mobs.part_actuel_PPM[0])
        tous_mobs.part_actuel_PPM[0].columns = modes
        tous_mobs.part_actuel_PPM[0].index = [f'{actuel} PPM']
        # dp.Table(tous_mobs.part_scen_PPM[0])
        tous_mobs.part_scen_PPM[0].columns = modes
        tous_mobs.part_scen_PPM[0].index = [f'{scen} PPM']
        df_total = pd.concat([df_total, tous_mobs.part_actuel_PPM[0], tous_mobs.part_scen_PPM[0]])

    if PCJ:
        # dp.Table(tous_mobs.part_actuel_PCJ[0])
        tous_mobs.part_actuel_PCJ[0].columns = modes
        tous_mobs.part_actuel_PCJ[0].index = [f'{actuel} PCJ']
        # dp.Table(tous_mobs.part_scen_PCJ[0])
        tous_mobs.part_scen_PCJ[0].columns = modes
        tous_mobs.part_scen_PCJ[0].index = [f'{scen} PCJ']
        df_total = pd.concat([df_total, tous_mobs.part_actuel_PCJ[0], tous_mobs.part_scen_PCJ[0]])
    
    if PPS:
        # dp.Table(tous_mobs.part_actuel_PPS[0])
        tous_mobs.part_actuel_PPS[0].columns = modes
        tous_mobs.part_actuel_PPS[0].index = [f'{actuel} PPS']
        # dp.Table(tous_mobs.part_scen_PPS[0])
        tous_mobs.part_scen_PPS[0].columns = modes
        tous_mobs.part_scen_PPS[0].index = [f'{scen} PPS']
        df_total = pd.concat([df_total, tous_mobs.part_actuel_PPS[0], tous_mobs.part_scen_PPS[0]])
    df_total = df_total.round(4)    # On arrondit le dataframe des parts modaux

    fig7, ax7 = plt.subplots()
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :4].sum(1), color='grey', label='MD')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :3].sum(1), color='brown', label='CY')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax7.legend(loc="best", frameon=True)

    # Parts modaux modes motorisés
    df_moto = pd.DataFrame()    # Dataframe des modes motorisés pour le calcul des parts modaux
    modes_moto = ['TC', 'VP']  # Pour le dataframe montrant tous les modes motorisés
    if PPM:
        # dp.Table(tous_mobs.part_actuel_PPM[1])
        tous_mobs.part_actuel_PPM[1].columns = modes_moto
        tous_mobs.part_actuel_PPM[1].index = [f'{actuel} PPM']
        # dp.Table(tous_mobs.part_scen_PPM[1])
        tous_mobs.part_scen_PPM[1].columns = modes_moto
        tous_mobs.part_scen_PPM[1].index = [f'{scen} PPM']
        df_moto = pd.concat([df_moto, tous_mobs.part_actuel_PPM[1], tous_mobs.part_scen_PPM[1]])


    if PCJ:
        # dp.Table(tous_mobs.part_actuel_PCJ[1])
        tous_mobs.part_actuel_PCJ[1].columns = modes_moto
        tous_mobs.part_actuel_PCJ[1].index = [f'{actuel} PCJ']
        # dp.Table(tous_mobs.part_scen_PCJ[1])
        tous_mobs.part_scen_PCJ[1].columns = modes_moto
        tous_mobs.part_scen_PCJ[1].index = [f'{scen} PCJ']
        df_moto = pd.concat([df_moto, tous_mobs.part_actuel_PPM[1], tous_mobs.part_scen_PPM[1]])

    if PPS:
        # dp.Table(tous_mobs.part_actuel_PPS[1])
        tous_mobs.part_actuel_PPS[1].columns = modes_moto
        tous_mobs.part_actuel_PPS[1].index = [f'{actuel} PPS']
        # dp.Table(tous_mobs.part_scen_PPS[1])
        tous_mobs.part_scen_PPS[1].columns = modes_moto
        tous_mobs.part_scen_PPS[1].index = [f'{scen} PPS']
        df_moto = pd.concat([df_moto, tous_mobs.part_actuel_PPS[1], tous_mobs.part_scen_PPS[1]])
    df_moto = df_moto.round(4)     # On arrondit le dataframe des parts modaux motorisés.

    fig8, ax8 = plt.subplots()
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :2].sum(1), color='lightblue', label='VP')
    sns.barplot(x=df_total.index, y=df_total.iloc[:, :1].sum(1), color='darkblue', label='TC')
    ax8.legend(loc="best", frameon=True)

    # Arrondir les indicateurs de l'affectation
    if PPM:
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PPM[0].columns)
        tous_mobs.affect_PPM[0] = tous_mobs.affect_PPM[0].round(decimales)
        tous_mobs.affect_PPM[1] = tous_mobs.affect_PPM[1].round(decimales)
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PPM[2].columns)
        tous_mobs.affect_PPM[2] = tous_mobs.affect_PPM[2].round(decimales)
        tous_mobs.affect_PPM[3] = tous_mobs.affect_PPM[3].round(decimales)
    if PCJ:
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PCJ[0].columns)
        tous_mobs.affect_PCJ[0] = tous_mobs.affect_PCJ[0].round(decimales)
        tous_mobs.affect_PCJ[1] = tous_mobs.affect_PCJ[1].round(decimales)
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PCJ[2].columns)
        tous_mobs.affect_PCJ[2] = tous_mobs.affect_PCJ[2].round(decimales)
        tous_mobs.affect_PCJ[3] = tous_mobs.affect_PCJ[3].round(decimales)
    if PPS:
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PPS[0].columns)
        tous_mobs.affect_PPS[0] = tous_mobs.affect_PPS[0].round(decimales)
        tous_mobs.affect_PPS[1] = tous_mobs.affect_PPS[1].round(decimales)
        decimales = pd.Series([0, 0, 0, 2, 4], index=tous_mobs.affect_PPS[2].columns)
        tous_mobs.affect_PPS[2] = tous_mobs.affect_PPS[2].round(decimales)
        tous_mobs.affect_PPS[3] = tous_mobs.affect_PPS[3].round(decimales)

    # Le nombre de déplacements par classe de distance
    if PPM:
        fig, ax = plt.subplots()
        ax = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_TC_PPM)
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = TC")
        plt.ylabel('Nombre de déplacements')

        fig2, ax2 = plt.subplots()
        ax2 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_UVP_PPM)
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = VP")
        plt.ylabel('Nombre de déplacements')

        fig3, ax3 = plt.subplots()
        ax3 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_MD_PPM)
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = MD")
        plt.ylabel('Nombre de déplacements')

        fig4, ax4 = plt.subplots()
        ax4 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_CY_PPM)
        plt.title("Volume PPM observé et simulé pour les observations de l'EGT: mode = CY")
        plt.ylabel('Nombre de déplacements')

        fig5, ax5 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_actuel_PPM, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_actuel_PPM, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_actuel_PPM, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_actuel_PPM, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax5.legend(ncol=2, loc="best", frameon=True)

        fig6, ax6 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_scen_PPM, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_scen_PPM, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_scen_PPM, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_scen_PPM, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax6.legend(ncol=2, loc="best", frameon=True)
    else:
        fig, fig2, fig3, fig4, fig5, fig6 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                            plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                                plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))


    if PCJ:
        fig14, ax14 = plt.subplots()
        ax14 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_TC_PCJ)
        plt.title("Volume PCJ observé et simulé pour les observations de l'EGT: mode = TC")
        plt.ylabel('Nombre de déplacements')

        fig15, ax15 = plt.subplots()
        ax15 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_UVP_PCJ)
        plt.title("Volume PCJ observé et simulé pour les observations de l'EGT: mode = VP")
        plt.ylabel('Nombre de déplacements')

        fig16, ax16 = plt.subplots()
        ax16 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_MD_PCJ)
        plt.title("Volume PCJ observé et simulé pour les observations de l'EGT: mode = MD")
        plt.ylabel('Nombre de déplacements')

        fig17, ax17 = plt.subplots()
        ax17 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_CY_PCJ)
        plt.title("Volume PCJ observé et simulé pour les observations de l'EGT: mode = CY")
        plt.ylabel('Nombre de déplacements', fontsize=17)

        fig18, ax18 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_actuel_PCJ, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_actuel_PCJ, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_actuel_PCJ, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_actuel_PCJ, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax18.legend(ncol=2, loc="best", frameon=True)

        fig19, ax19 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_scen_PCJ, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_scen_PCJ, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_scen_PCJ, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_scen_PCJ, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax19.legend(ncol=2, loc="best", frameon=True)

    else:
        fig14, fig15, fig16, fig17, fig18, fig19 = plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                            plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0)), \
                                                plt.figure(figsize=(0, 0)), plt.figure(figsize=(0, 0))

    if PPS:
        fig20, ax20 = plt.subplots()
        ax20 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_TC_PPS)
        plt.title("Volume PPS observé et simulé pour les observations de l'EGT: mode = TC")
        plt.ylabel('Nombre de déplacements')

        fig21, ax21 = plt.subplots()
        ax21 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_UVP_PPS)
        plt.title("Volume PPS observé et simulé pour les observations de l'EGT: mode = VP")
        plt.ylabel('Nombre de déplacements')

        fig22, ax22 = plt.subplots()
        ax22 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_MD_PPS)
        plt.title("Volume PPS observé et simulé pour les observations de l'EGT: mode = MD")
        plt.ylabel('Nombre de déplacements')

        fig23, ax23 = plt.subplots()
        ax23 = sns.barplot(x='Portee', y='Value', hue='Variable', data=tous_mobs.graph_CY_PPS)
        plt.title("Volume PPS observé et simulé pour les observations de l'EGT: mode = CY")
        plt.ylabel('Nombre de déplacements')

        fig24, ax24 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_actuel_PPS, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_actuel_PPS, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_actuel_PPS, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_actuel_PPS, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax24.legend(ncol=2, loc="best", frameon=True)

        fig25, ax25 = plt.subplots(figsize=(11.7, 8.27))
        sns.barplot(x='Portee', y='TC', data=tous_mobs.graph_parts_scen_PPS, color='r', label='TC')
        sns.barplot(x='Portee', y='CY', data=tous_mobs.graph_parts_scen_PPS, color='b', label='CY')
        sns.barplot(x='Portee', y='VP', data=tous_mobs.graph_parts_scen_PPS, color='y', label='VP')
        sns.barplot(x='Portee', y='MD', data=tous_mobs.graph_parts_scen_PPS, color='g', label='MD')
        plt.ylabel('Part modal')
        plt.title('Part modal pour chaque classe de portée')
        ax25.legend(ncol=2, loc="best", frameon=True)
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
