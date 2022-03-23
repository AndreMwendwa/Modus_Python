from Traitement.ESE.vkm_vhr_gen import vkm_vhr_fn
from Data.A_CstesModus import *
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from user_veh import *
from user_pt import *
from externalites import *

def calcul_socio_eco(fichier1, fichier2):
    vkm2, vhr2, *autres2 = vkm_vhr_fn(fichier2)
    vkm1, vhr1, *autres1 = vkm_vhr_fn(fichier1)
    vkm_diff = vkm2 - vkm1
    vhr_diff = vhr2 - vhr1
    autres_diff = [i - j for i, j in zip(autres2, autres1)]

    user_veh = user_veh_fn(vkm_diff)
    time_vp = user_time_vp(vhr_diff)
    user_pt_time = user_pt_fn(fichier1, fichier2)
    polln_locale = polln_local_fn2(fichier1, fichier2)
    usage_infras_df = usage_infras(fichier1, fichier2)
    ghg_LCA_vp = ghg_LCA_fn(vkm_diff)

    cout_df_diff_total = pd.concat([user_veh, time_vp.T, user_pt_time.T, polln_locale.T, ghg_LCA_vp.T,
                                    usage_infras_df.T], axis=0)
    decimales = pd.Series([0, 2, 2, 2], index=cout_df_diff_total.columns)  # A utiliser pour arrondir chaque colonne
    # différemment
    cout_df_diff_total = cout_df_diff_total.round(decimales)
    ligne_de_somme = pd.DataFrame(
            {list_cols_ESE.Item: 'Total', list_cols_ESE.Diff_scenarios: '-', list_cols_ESE.Val_tutelaires: '-',
                                        list_cols_ESE.Val_econ: cout_df_diff_total['Valeurs économiques (€)'].sum()},
                                        index=[0])
    cout_df_diff_total = pd.concat([cout_df_diff_total, ligne_de_somme])
    cout_df_diff_total = cout_df_diff_total.round(2)

    # Celles-ci sont juste pour tracer les graphes
    couts_df_scen1 = pd.DataFrame({'PPM': [autres1[0], autres1[2]], 'PPS': [autres1[1], autres1[3]]},
                                  index=['VKM', 'Veh-hr'])
    couts_df_scen2 = pd.DataFrame({'PPM': [autres2[0], autres2[2]], 'PPS': [autres2[1], autres2[3]]},
                                  index=['VKM', 'Veh-hr'])
    couts_df_diff = couts_df_scen1 - couts_df_scen2

    return couts_df_diff, cout_df_diff_total, couts_df_scen1, couts_df_scen2
    # Utilisant les chiffres des tronçons
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
    # return couts_df_diff, cout_df_diff_total, couts_df_scen1, couts_df_scen2

if __name__ == '__main__':
    f1 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite'
    f2 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite'
    calcul_socio_eco(f1, f2)