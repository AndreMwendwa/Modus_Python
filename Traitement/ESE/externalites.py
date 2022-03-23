import pickle as pkl
import pandas as pd
from pathlib import Path
from Data.A_CstesModus import *
import win32com.client as win32


def polln_local_fn2(fichier1, fichier2):
    # VKm PPM
    # Coût de la pollution locale pour la première scénario
    visum_path1 = os.path.join(fichier1, '2_Bouclage')
    for i in range(cNbBcl, 0, -1):
        path_iter = os.path.join(visum_path1, f'Iter{i}')
        isExist = os.path.exists(path_iter)
        if isExist:
            break
    myvisum = win32.Dispatch("Visum.Visum")
    # PPM
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    longueurs1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    temps1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('TCur_PrTSys(V)'))
    vkm_ppm1 = (longueurs1[1] * flux1[1])
    
    # PPS
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPS_scen_iter{i}.ver'))
    longueurs1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_pps1 = (longueurs1[1] * flux1[1])

    vkm_1 = vkm_ppm1 + vkm_pps1  # La somme des vkm/route pour le scénario projet

    polln_local_somme1 = 0    # Le résultat finale

    # Liste de la moyenne des densité pous des zones traversées
    intersect_file = r'C:\Users\mwendwa.kiko\Documents\Personal Kiko\Intersect_test.ver'
    myvisum = win32.Dispatch("Visum.Visum")
    myvisum.LoadVersion(intersect_file)
    zones_traversed = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('Zones_traversed'))
    zones_traversed['densh_moy'] = 0
    links_avec_problemes = []     # Des links qui ne traversent aucune zone
    Pop_Emp_data = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))
    i = 0      # Counter of links
    for zone_trav in zones_traversed[1].to_list():
        densh_avg = 0
        total = 0
        try:
            for zone in zone_trav.split(','):
                densh = Pop_Emp_data.loc[int(zone) - 1, 'DENSH']
                total += densh
            densh_avg = total / len(zone_trav)
            zones_traversed.loc[i, 'densh_moy'] = densh_avg
        except ValueError:          # Parce que certains links ne traversent aucune zone, alors le calcul ci-dessus ne 
            # marchera pas. On mes une densité de 0 sur ceux-ci
            zones_traversed.loc[i, 'densh_moy'] = 0
            links_avec_problemes.append(i)
            pass
        i += 1

    # Le calcul par tranche de densité
    somme_intermediare1 = np.where(zones_traversed['densh_moy'] > yaml_content['bornes'][0], (vkm_1 *
                                                                                   yaml_content['valeurs_vp'][0]),
                                   0).sum()  # Zones les plus denses
    somme_intermediare2 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][0]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][1]), (vkm_1 *
                                                                                     yaml_content['valeurs_vp'][
                                                                                         1]), 0).sum()
    somme_intermediare3 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][1]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][2]), (vkm_1 *
                                                                                     yaml_content['valeurs_vp'][
                                                                                         2]), 0).sum()
    somme_intermediare4 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][2]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][3]), (vkm_1 *
                                                                                     yaml_content['valeurs_vp'][
                                                                                         3]), 0).sum()
    somme_intermediare5 = np.where(zones_traversed['densh_moy'] < yaml_content['bornes'][3], (vkm_1 *
                                                                                   yaml_content['valeurs_vp'][4]),
                                   0).sum()  # Zones les moins denses
    somme_intermediare_PPM = somme_intermediare1 + somme_intermediare2 + somme_intermediare3 + somme_intermediare4 \
                             + somme_intermediare5
    polln_local_somme1 += somme_intermediare_PPM

    # Coût de la pollution locale pour la deuxième scénario
    visum_path2 = os.path.join(fichier2, '2_Bouclage')
    for i in range(cNbBcl, 0, -1):
        path_iter = os.path.join(visum_path2, f'Iter{i}')
        isExist = os.path.exists(path_iter)
        if isExist:
            break
    myvisum = win32.Dispatch("Visum.Visum")
    # PPM
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    longueurs2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_ppm2 = (longueurs2[1] * flux2[1])

    # PPS
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPS_scen_iter{i}.ver'))
    longueurs2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_pps2 = (longueurs2[1] * flux2[1])
    
    vkm_2 = vkm_ppm2 + vkm_pps2     # La somme des vkm/route pour le scénario projet

    polln_local_somme2 = 0  # Le résultat finale

    # Le calcul par tranche de densité
    somme_intermediare1 = np.where(zones_traversed['densh_moy'] > yaml_content['bornes'][0], (vkm_2 *
                                                                                              yaml_content[
                                                                                                  'valeurs_vp'][0]),
                                   0).sum()  # Zones les plus denses
    somme_intermediare2 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][0]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][1]), (vkm_2 *
                                                                                                yaml_content[
                                                                                                    'valeurs_vp'][
                                                                                                    1]), 0).sum()
    somme_intermediare3 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][1]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][2]), (vkm_2 *
                                                                                                yaml_content[
                                                                                                    'valeurs_vp'][
                                                                                                    2]), 0).sum()
    somme_intermediare4 = np.where((zones_traversed['densh_moy'] < yaml_content['bornes'][2]) |
                                   (zones_traversed['densh_moy'] > yaml_content['bornes'][3]), (vkm_2 *
                                                                                                yaml_content[
                                                                                                    'valeurs_vp'][
                                                                                                    3]), 0).sum()
    somme_intermediare5 = np.where(zones_traversed['densh_moy'] < yaml_content['bornes'][3], (vkm_2 *
                                                                                              yaml_content[
                                                                                                  'valeurs_vp'][4]),
                                   0).sum()  # Zones les moins denses
    somme_intermediare_PPM = somme_intermediare1 + somme_intermediare2 + somme_intermediare3 + somme_intermediare4 \
                             + somme_intermediare5
    polln_local_somme2 += somme_intermediare_PPM
    
    polln_local_somme = polln_local_somme2 - polln_local_somme1

    polln_locale = {}  # Coût de la pollution causé pour les usagers des VP
    polln_locale[list_cols_ESE.Item] = 'Health costs - local pollution (VP)'
    polln_locale[list_cols_ESE.Diff_scenarios] = '-'
    polln_locale[list_cols_ESE.Val_tutelaires] = '-'
    polln_locale = pd.Series(polln_locale)
    polln_locale[list_cols_ESE.Val_econ] = polln_local_somme
    return pd.DataFrame(polln_locale)

    # for i in range(cNbBcl, 0, -1):
    #     path_iter = os.path.join(visum_path1, f'Iter{i}')
    #     isExist = os.path.exists(path_iter)
    #     if isExist:
    #         break
    # myvisum = win32.Dispatch("Visum.Visum")
    # # PPM
    # myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    # longueurs1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    # flux1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    # temps1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('TCur_PrTSys(V)'))
    # vkm_ppm1 = (longueurs1[1] * flux1[1])



def polln_local_fn(fichier1, fichier2):
    polln_local_somme = 0    # On initialize la somme des coûts des polluants locaux

    dbfile = open(f'{Path(fichier1)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    bdinter1 = pkl.load(dbfile)
    bdinter1['DENSH'] = (bdinter1['DENSHO'] + bdinter1['DENSHO'])/2     # On va faire ça une seule fois seulement.
    dbfile = open(f'{Path(fichier2)}/1_Fichiers_intermediares/bdinter_scen', 'rb')
    bdinter2 = pkl.load(dbfile)

    # Le calcul est faite séparément pour chaque classe de densité, et puis la somme est faite à la fin.
    if PPM:
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPM_scen'), 'rb')
        VP2_PPM = pkl.load(dbfile)
        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPM_scen'), 'rb')
        VP1_PPM = pkl.load(dbfile)
        VP_PPM = VP2_PPM['FLUX'] - VP1_PPM['FLUX']

        somme_intermediare1 = np.where(bdinter1['DENSH'] > yaml_content['bornes'][0], (VP_PPM *
                                        yaml_content['valeurs_vp'][0]), 0).sum()       # Zones les plus denses
        somme_intermediare2 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][0]) |
                                        (bdinter1['DENSH'] > yaml_content['bornes'][1]), (VP_PPM *
                                                                                        yaml_content['valeurs_vp'][
                                                                                            1]), 0).sum()
        somme_intermediare3 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][1]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][2]), (VP_PPM *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             2]), 0).sum()
        somme_intermediare4 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][2]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][3]), (VP_PPM *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             3]), 0).sum()
        somme_intermediare5 = np.where(bdinter1['DENSH'] < yaml_content['bornes'][3], (VP_PPM *
                                                                                       yaml_content['valeurs_vp'][4]),
                                       0).sum()         # Zones les moins denses
        somme_intermediare_PPM = somme_intermediare1 + somme_intermediare2 + somme_intermediare3 + somme_intermediare4 \
                                    + somme_intermediare5
        polln_local_somme += somme_intermediare_PPM
    if PCJ:
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PCJ_scen'), 'rb')
        VP2_PCJ = pkl.load(dbfile)
        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PCJ_scen'), 'rb')
        VP1_PCJ = pkl.load(dbfile)
        VP_PCJ = VP2_PCJ['FLUX'] - VP1_PCJ['FLUX']

        somme_intermediare1 = np.where(bdinter1['DENSH'] > yaml_content['bornes'][0], (VP_PCJ *
                                        yaml_content['valeurs_vp'][0]), 0).sum()       # Zones les plus denses
        somme_intermediare2 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][0]) |
                                        (bdinter1['DENSH'] > yaml_content['bornes'][1]), (VP_PCJ *
                                                                                        yaml_content['valeurs_vp'][
                                                                                            1]), 0).sum()
        somme_intermediare3 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][1]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][2]), (VP_PCJ *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             2]), 0).sum()
        somme_intermediare4 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][2]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][3]), (VP_PCJ *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             3]), 0).sum()
        somme_intermediare5 = np.where(bdinter1['DENSH'] < yaml_content['bornes'][3], (VP_PCJ *
                                                                                       yaml_content['valeurs_vp'][4]),
                                       0).sum()         # Zones les moins denses
        somme_intermediare_PCJ = somme_intermediare1 + somme_intermediare2 + somme_intermediare3 + somme_intermediare4 \
                                    + somme_intermediare5
        polln_local_somme += somme_intermediare_PCJ
    if PPS:
        dbfile = open(Path(fichier2 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPS_scen'), 'rb')
        VP2_PPS = pkl.load(dbfile)
        dbfile = open(Path(fichier1 + '/1_Fichiers_intermediares/MODUSCaleUVP_df_PPS_scen'), 'rb')
        VP1_PPS = pkl.load(dbfile)
        VP_PPS = VP2_PPS['FLUX'] - VP1_PPS['FLUX']

        somme_intermediare1 = np.where(bdinter1['DENSH'] > yaml_content['bornes'][0], (VP_PPS *
                                        yaml_content['valeurs_vp'][0]), 0).sum()       # Zones les plus denses
        somme_intermediare2 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][0]) |
                                        (bdinter1['DENSH'] > yaml_content['bornes'][1]), (VP_PPS *
                                                                                        yaml_content['valeurs_vp'][
                                                                                            1]), 0).sum()
        somme_intermediare3 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][1]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][2]), (VP_PPS *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             2]), 0).sum()
        somme_intermediare4 = np.where((bdinter1['DENSH'] < yaml_content['bornes'][2]) |
                                       (bdinter1['DENSH'] > yaml_content['bornes'][3]), (VP_PPS *
                                                                                         yaml_content['valeurs_vp'][
                                                                                             3]), 0).sum()
        somme_intermediare5 = np.where(bdinter1['DENSH'] < yaml_content['bornes'][3], (VP_PPS *
                                                                                       yaml_content['valeurs_vp'][4]),
                                       0).sum()         # Zones les moins denses
        somme_intermediare_PPS = somme_intermediare1 + somme_intermediare2 + somme_intermediare3 + somme_intermediare4 \
                                    + somme_intermediare5
        polln_local_somme += somme_intermediare_PPS

    polln_locale = {}  # Valeur du temps pour les usagers des VP
    polln_locale[list_cols_ESE.Item] = 'Health costs - local pollution (VP)'
    polln_locale[list_cols_ESE.Diff_scenarios] = '-'
    polln_locale[list_cols_ESE.Val_tutelaires] = '-'
    polln_locale = pd.Series(polln_locale)
    polln_locale[list_cols_ESE.Val_econ] = polln_local_somme
    return pd.DataFrame(polln_locale)

def ghg_LCA_fn(vkm):
    ghg_vp = {}  # Valeur des emissions des GES
    ghg_vp[list_cols_ESE.Item] = 'GHG emissions (VP)'
    ghg_vp[list_cols_ESE.Diff_scenarios] = vkm * yaml_content['VP_CO2_gkm']/1e6
    ghg_vp[list_cols_ESE.Val_tutelaires] = yaml_content['CO2_prix_tonne']
    ghg_vp = pd.Series(ghg_vp)
    ghg_vp[list_cols_ESE.Val_econ] = ghg_vp[list_cols_ESE.Val_tutelaires] * ghg_vp[list_cols_ESE.Diff_scenarios]
    
    lca_vp = {}  # Valeur des emissions des GES
    lca_vp[list_cols_ESE.Item] = 'Health costs of air pollutant for upstream effects (VP)'
    lca_vp[list_cols_ESE.Diff_scenarios] = vkm
    lca_vp[list_cols_ESE.Val_tutelaires] = yaml_content['VP_LCA']
    lca_vp = pd.Series(lca_vp)
    lca_vp[list_cols_ESE.Val_econ] = lca_vp[list_cols_ESE.Val_tutelaires] * lca_vp[list_cols_ESE.Diff_scenarios]
    ghg_LCA_vp = pd.DataFrame({0: ghg_vp, 1: lca_vp})

    return pd.DataFrame(ghg_vp)

def usage_infras(fichier1, fichier2):
    # Scénario 1
    visum_path1 = os.path.join(fichier1, '2_Bouclage')
    for i in range(cNbBcl, 0, -1):
        path_iter = os.path.join(visum_path1, f'Iter{i}')
        isExist = os.path.exists(path_iter)
        if isExist:
            break
    myvisum = win32.Dispatch("Visum.Visum")

    # Scénario 1 PPM 
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    longueurs1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    temps1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('TCur_PrTSys(V)'))
    vkm_ppm1 = (longueurs1[1] * flux1[1])
    vkm_ppm1.name = 'vkm_ppm1'

    # Préparation du tableau de la classification des routes entre nationales, départementales, communales, autoroutes 
    # et inconnus (les routes qui tombent dans aucun catégorie, auxquelles on va appliquer le coût moyen d'usage des 
    # infras)
    # Parsing le nom de la route 
    nomroutes = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('NomRoute'))
    a = nomroutes[1].str.split(expand=True)
    mask = a[0].notna()
    # a = nomroutes.apply(lambda x: x[1] if x is not None else 0)

    def split(word):
        return [char for char in word]
    b = a.loc[mask, 0].apply(split)
    # b.apply(lambda x: x[0])
    # b.apply(lambda x: x[1] if len(x) > 1 else 0)
    route_class = pd.concat([b.apply(lambda x: x[0]), b.apply(lambda x: x[1] if len(x) > 1 else 0)], axis=1)
    route_class.columns = [0, 1]
    route_class['Nat'] = 0      # Colonne des routes nationales
    route_class['Nat'] = np.where((route_class[0] == 'N') | ((route_class[0] == 'R') & (route_class[1] == 'N')), 1, 0)
    route_class['Dep'] = 0      # Colonne des routes départmentales
    route_class['Dep'] = np.where((route_class[0] == 'D') | ((route_class[0] == 'R') & (route_class[1] == 'D')), 1, 0)
    route_class['Comm'] = 0     # Colonne des routes communales
    route_class['Comm'] = np.where((route_class[0] == 'C') | ((route_class[0] == 'R') & (route_class[1] == 'C')), 1, 0)
    route_class['Autoroute'] = 0  # Colonne des autoroutes et des bretelles d'autoroutes
    route_class['Autoroute'] = np.where((route_class[0] == 'A') | ((route_class[0] == 'B') & (route_class[1] == 'r')), 1, 0)

    # Calcul du coût d'usage des infras
    vkm_ppm1_route = pd.merge(vkm_ppm1, route_class, left_index=True, right_index=True, how='outer')
    vkm_ppm1_route['usage_infra'] = 0
    vkm_ppm1_route['usage_infra'] = \
        np.where(vkm_ppm1_route['Autoroute'] == 1, vkm_ppm1_route['vkm_ppm1'] * yaml_content['usage_infra_vp'][0],
            np.where(vkm_ppm1_route['Nat'] == 1, vkm_ppm1_route['vkm_ppm1'] * yaml_content['usage_infra_vp'][1],
                 np.where(vkm_ppm1_route['Dep'] == 1, vkm_ppm1_route['vkm_ppm1'] * yaml_content['usage_infra_vp'][2],
                    np.where(vkm_ppm1_route['Comm'] == 1, vkm_ppm1_route['vkm_ppm1'] * yaml_content['usage_infra_vp'][3],
                             vkm_ppm1_route['vkm_ppm1'] * yaml_content['usage_infra_vp'][4],
                 ))))
    # Scénario 1 PPS
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPS_scen_iter{i}.ver'))
    longueurs1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux1 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_pps1 = (longueurs1[1] * flux1[1])
    vkm_pps1.name = 'vkm_pps1'
    
    vkm_pps1_route = pd.merge(vkm_pps1, route_class, left_index=True, right_index=True, how='outer')
    vkm_pps1_route['usage_infra'] = 0
    vkm_pps1_route['usage_infra'] = \
        np.where(vkm_pps1_route['Autoroute'] == 1, vkm_pps1_route['vkm_pps1'] * yaml_content['usage_infra_vp'][0],
                 np.where(vkm_pps1_route['Nat'] == 1, vkm_pps1_route['vkm_pps1'] * yaml_content['usage_infra_vp'][1],
                          np.where(vkm_pps1_route['Dep'] == 1,
                                   vkm_pps1_route['vkm_pps1'] * yaml_content['usage_infra_vp'][2],
                                   np.where(vkm_pps1_route['Comm'] == 1,
                                            vkm_pps1_route['vkm_pps1'] * yaml_content['usage_infra_vp'][3],
                                            vkm_pps1_route['vkm_pps1'] * yaml_content['usage_infra_vp'][4],
                                            ))))
    usage_infras_somme1 = vkm_ppm1_route['usage_infra'].sum() + vkm_pps1_route['usage_infra'].sum()

    # Scénario 2
    visum_path2 = os.path.join(fichier2, '2_Bouclage')
    for i in range(cNbBcl, 0, -1):
        path_iter = os.path.join(visum_path2, f'Iter{i}')
        isExist = os.path.exists(path_iter)
        if isExist:
            break
    myvisum = win32.Dispatch("Visum.Visum")

    # Scénario 2 PPM
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    longueurs2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_ppm2 = (longueurs2[1] * flux2[1])
    vkm_ppm2.name = 'vkm_ppm2'

    # Calcul du coût d'usage des infras
    vkm_ppm2_route = pd.merge(vkm_ppm2, route_class, left_index=True, right_index=True, how='outer')
    vkm_ppm2_route['usage_infra'] = 0
    vkm_ppm2_route['usage_infra'] = \
        np.where(vkm_ppm2_route['Autoroute'] == 1, vkm_ppm2_route['vkm_ppm2'] * yaml_content['usage_infra_vp'][0],
                 np.where(vkm_ppm2_route['Nat'] == 1, vkm_ppm2_route['vkm_ppm2'] * yaml_content['usage_infra_vp'][1],
                          np.where(vkm_ppm2_route['Dep'] == 1,
                                   vkm_ppm2_route['vkm_ppm2'] * yaml_content['usage_infra_vp'][2],
                                   np.where(vkm_ppm2_route['Comm'] == 1,
                                            vkm_ppm2_route['vkm_ppm2'] * yaml_content['usage_infra_vp'][3],
                                            vkm_ppm2_route['vkm_ppm2'] * yaml_content['usage_infra_vp'][4],
                                            ))))
    # Scénario 2 PPS
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPS_scen_iter{i}.ver'))
    longueurs2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux2 = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    vkm_pps2 = (longueurs2[1] * flux2[1])
    vkm_pps2.name = 'vkm_pps2'

    vkm_pps2_route = pd.merge(vkm_pps2, route_class, left_index=True, right_index=True, how='outer')
    vkm_pps2_route['usage_infra'] = 0
    vkm_pps2_route['usage_infra'] = \
        np.where(vkm_pps2_route['Autoroute'] == 1, vkm_pps2_route['vkm_pps2'] * yaml_content['usage_infra_vp'][0],
                 np.where(vkm_pps2_route['Nat'] == 1, vkm_pps2_route['vkm_pps2'] * yaml_content['usage_infra_vp'][1],
                          np.where(vkm_pps2_route['Dep'] == 1,
                                   vkm_pps2_route['vkm_pps2'] * yaml_content['usage_infra_vp'][2],
                                   np.where(vkm_pps2_route['Comm'] == 1,
                                            vkm_pps2_route['vkm_pps2'] * yaml_content['usage_infra_vp'][3],
                                            vkm_pps2_route['vkm_pps2'] * yaml_content['usage_infra_vp'][4],
                                            ))))
    usage_infras_somme2 = vkm_ppm2_route['usage_infra'].sum() + vkm_pps2_route['usage_infra'].sum()

    # Différence entre les scénarios
    usage_infras_somme = usage_infras_somme2 - usage_infras_somme1

    usage_infras_df = {}  # Coût de la pollution causé pour les usagers des VP
    usage_infras_df[list_cols_ESE.Item] = 'Road external costs'
    usage_infras_df[list_cols_ESE.Diff_scenarios] = '-'
    usage_infras_df[list_cols_ESE.Val_tutelaires] = '-'
    usage_infras_df = pd.Series(usage_infras_df)
    usage_infras_df[list_cols_ESE.Val_econ] = usage_infras_somme
    return pd.DataFrame(usage_infras_df)

if __name__ == '__main__':
    f1 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite'
    f2 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite'
    usage_infras(f1, f2)
    # polln_local_fn(f1, f2)
    polln_local_fn2(f1, f2)
    ghg_LCA_fn(1e5)
