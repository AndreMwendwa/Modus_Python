import numpy as np
from Data.A_CstesModus import *
import pandas as pd
import Data.VisumPy.helpers2 as helpers
import win32com.client as win32
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotmap import DotMap

class visum_data:
    def __init__(self, dossier, hor):
        self.carburant_vp = yaml_content['VP_moy_fuel_basic']        # Vehicle fuel costs
        self.operating_vp = yaml_content['VP_non_fuel_basic']        # Vehicle operating  costs - non fuel
        self.capital_vp = yaml_content['VP_capital_marginal_basic']  # Vehicle capital  costs
        self.user_veh_unit_cost = self.carburant_vp + self.operating_vp + self.capital_vp
        self.VTTS_business = yaml_content['VTTS_business']      # Valeur du temps pour les usagers des VP motif =
        # business
        self.VTTS_commute_school_childcare = yaml_content['VTTS_commute_school_childcare']   # motif =
        # commute/school/childcare
        self.VTTS_others = yaml_content['VTTS_others']      # motif = 'others'
        self.taux_occpation = yaml_content['taux_occupation']
        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'MODUSCaleUVP_df_{hor}_scen'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/MODUSCaleUVP_df_{hor}_scen'), 'rb')
        self.flux_uvp = pkl.load(dbfile)

        # Pour chacun des motifs, on va créet une série, et le transformer en array numpy pour ensuite faire un
        # reshape pour créer les matrices qui sont les inputs de l'étape de calculation des temps moyens
        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'Modus_VP_motcat_scen_{hor}'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_VP_motcat_scen_{hor}'), 'rb')
        self.flux_apres_cm = pkl.load(dbfile)
        self.flux_motifs_drieat = pd.DataFrame(np.zeros(self.flux_apres_cm.shape))
        for col in self.flux_motifs_drieat.columns:
            self.flux_motifs_drieat[col] = self.flux_apres_cm[col] / self.flux_apres_cm.sum(1) * self.flux_uvp['FLUX']
        self.flux_uvp_square = self.flux_uvp['FLUX'].to_numpy().reshape(cNbZone, cNbZone)
        self.flux_uvp_sum = self.flux_uvp_square.sum()
        self.dossier = dossier
        self.hor = hor

        # Les temps et les distances pour notre scenario
        # The first two are matricial
        # The last two are for the links
        self.temps, self.distance, self.lengths_links, self.flux_links, self.nom_routes, self.temps_vide_links, \
            self.temps_chg_links = self.load_skims()

        # Indicateur de congestion
        self.excess_delay, self.travel_time_index = self.congestion_indicators()

        self.vkm_links = self.flux_links * self.lengths_links       # The vkm flows along the links
        self.vht_links = self.flux_links * self.temps_chg_links     # The vht flows along the links

        # VHT, VKT totals that will be outputted by the dashboard, and saved in the comparaison_scenarios file
        self.vkt_total_links = self.vkm_links.sum()
        self.vht_total_links = self.vht_links.sum()

        self.temps_sum = self.temps[:cNbZone, :cNbZone].sum()    # Car dans VISUM il y a plus que les
        # cNbZone nombre de zones qui sont des zones ordinaires de MODUS
        if yaml_content['calc_zones_traversed'] == 1:
            self.zones_traversed = self.zones_traversed_fn()       # List des zones traversées par des tronçons.
        else:
            self.zones_traversed = pd.read_excel(yaml_content['zones_traversed_file'])

        if yaml_content['calc_avg_density_along_links'] == 1:
            self.avg_density_along_links = self.avg_density_along_links_fn()       # List des zones traversées par des tronçons.
        else:
            self.avg_density_along_links = pd.read_excel(yaml_content['avg_density_along_links_file'])['densh_moy']

        # self.avg_density_along_links = self.avg_density_along_links_fn()
        # self.routes_class_df = self.routes_classes()        # Hierarchy of routes within the Visum network

        if yaml_content['calc_routes_class'] == 1:
            self.routes_class_df = self.routes_classes()
        else:
            self.routes_class_df = pd.read_excel(yaml_content['routes_class_df_fle'])

        ## Les UVP en année de calage
        dbfile = open(os.path.join(dossier, '1_Fichiers_intermediares', f'ModusUVP_df{hor}_actuel'), 'rb')
        # dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/ModusUVP_df{hor}_actuel'), 'rb')
        self.flux_uvp_actuel = pkl.load(dbfile)
        self.flux_uvp_actuel_sum = self.flux_uvp_actuel['FLUX'].sum()


    def load_skims(self):
        visum_path = os.path.join(self.dossier, '2_Bouclage')
        for i in range(cNbBcl, 0, -1):
            path_iter = os.path.join(visum_path, f'Iter{i}')
            isExist = os.path.exists(path_iter)
            if isExist:
                break
        myvisum = win32.Dispatch("Visum.Visum")
        # PPM
        myvisum.LoadVersion(os.path.join(path_iter, f'Vers{self.hor}_scen_iter{i}.ver'))
        temps = helpers.GetSkimMatrix(myvisum, 'TpsCh', 'V')
        distance = helpers.GetSkimMatrix(myvisum, 'Dist', 'V')
        lengths_links = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
        temps_vide_links = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('t0_PrTSys (V)'))
        temps_chg_links = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('tCur_PrTSys (V)'))
        flux_links = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
        nomroutes = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('NomRoute'))
        return temps, distance, lengths_links[1], flux_links[1], nomroutes, temps_vide_links[1], temps_chg_links[1]

    def zones_traversed_fn(self):
        # Liste de la moyenne des densité pous des zones traversées
        intersect_file = yaml_content['intersect_file']
        myvisum = win32.Dispatch("Visum.Visum")
        myvisum.LoadVersion(intersect_file)
        zones_traversed = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('Zones_traversed'))
        return zones_traversed

    def zones_traversed_fn_new(self):
        zones_traversed = pd.read_csv(r'C:\Users\mwendwa.kiko\Documents\VA Saclay\zones_traversed.csv')
        return zones_traversed

    def avg_density_along_links_fn(self):
        zones_traversed = self.zones_traversed.copy()      # On copie le paramètre puisqu'on va le changer au sein de cette
        # fonction
        zones_traversed['densh_moy'] = 0     # Initialization de la colonne des densités moyennes
        links_avec_problemes = []  # Des links qui ne traversent aucune zone
        Pop_Emp_data = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))
        i = 0  # Counter of links
        for zone_trav in zones_traversed[1].to_list():
            densh_avg = 0
            total = 0
            try:
                for zone in zone_trav.split(','):
                    densh = Pop_Emp_data.loc[int(zone) - 1, 'DENSH']
                    total += densh
                densh_avg = total / len(zone_trav)
                zones_traversed.loc[i, 'densh_moy'] = densh_avg
            except ValueError:  # Parce que certains links ne traversent aucune zone, alors le calcul ci-dessus ne
                # marchera pas. On mes une densité de 0 sur ceux-ci
                zones_traversed.loc[i, 'densh_moy'] = 0
                links_avec_problemes.append(i)
                pass
            i += 1
        return zones_traversed['densh_moy']

    def routes_classes(self):
        nomroutes = self.nom_routes.copy()
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
        route_class['Nat'] = 0  # Colonne des routes nationales
        route_class['Nat'] = np.where((route_class[0] == 'N') | ((route_class[0] == 'R') & (route_class[1] == 'N')), 1,
                                      0)
        route_class['Dep'] = 0  # Colonne des routes départmentales
        route_class['Dep'] = np.where((route_class[0] == 'D') | ((route_class[0] == 'R') & (route_class[1] == 'D')), 1,
                                      0)
        route_class['Comm'] = 0  # Colonne des routes communales
        route_class['Comm'] = np.where((route_class[0] == 'C') | ((route_class[0] == 'R') & (route_class[1] == 'C')), 1,
                                       0)
        route_class['Autoroute'] = 0  # Colonne des autoroutes et des bretelles d'autoroutes
        route_class['Autoroute'] = np.where(
            (route_class[0] == 'A') | ((route_class[0] == 'B') & (route_class[1] == 'r')), 1, 0)
        route_class.fillna(0, inplace=True)
        return route_class[['Nat', 'Dep', 'Comm', 'Autoroute']]

    def congestion_indicators(self):
        '''Indicateur de congestion, calculé selon
        Toledo, Carlos A. Moran. "Congestion indicators and congestion impacts: a study on the relevance of
        area-wide indicators." Procedia-Social and Behavioral Sciences 16 (2011): 781-791.'''
        # ExD
        self.temps_chg_links = np.where(self.temps_chg_links != 3.6e8, self.temps_chg_links, 0)    # Les liens non-
        # actifs sont montrés dans MODUS avec une vélocité = 0, temps à vide = 3.6e8
        self.temps_vide_links = np.where(self.temps_vide_links != 3.6e8, self.temps_vide_links, 0)
        travel_rate_observed = (self.flux_links * self.temps_chg_links).sum()/(self.flux_links * self.lengths_links).sum()
        travel_rate_ref = (self.flux_links * self.temps_vide_links).sum()/(self.flux_links * self.lengths_links).sum()
        excess_delay = travel_rate_observed - travel_rate_ref

        # TTI
        travel_time_index = (
            (self.flux_links * self.lengths_links * self.temps_chg_links/self.temps_vide_links).sum() /
            (self.flux_links * self.lengths_links).sum()
        )
        return excess_delay, travel_time_index





