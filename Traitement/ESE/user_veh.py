import numpy as np

from Data.A_CstesModus import *
import pandas as pd
import Data.VisumPy.helpers2 as helpers
import win32com.client as win32


def user_veh_fn(vkm_in):
    carburant_vp = {}       # Vehicle fuel costs
    carburant_vp[list_cols_ESE.Item] = 'Vehicle fuel costs'
    carburant_vp[list_cols_ESE.Diff_scenarios] = vkm_in
    carburant_vp[list_cols_ESE.Val_tutelaires] = yaml_content['VP_moy_fuel_basic']
    carburant_vp = pd.Series(carburant_vp)

    operating_vp = {}   # Vehicle operating  costs - non fuel
    operating_vp[list_cols_ESE.Item] = 'Vehicle operating  costs - non fuel'
    operating_vp[list_cols_ESE.Diff_scenarios] = vkm_in
    operating_vp[list_cols_ESE.Val_tutelaires] = yaml_content['VP_non_fuel_basic']
    operating_vp = pd.Series(operating_vp)

    capital_vp = {}     # Vehicle capital  costs
    capital_vp[list_cols_ESE.Item] = 'Vehicle capital  costs - non fuel'
    capital_vp[list_cols_ESE.Diff_scenarios] = vkm_in
    capital_vp[list_cols_ESE.Val_tutelaires] = yaml_content['VP_capital_marginal_basic']
    capital_vp = pd.Series(capital_vp)

    user_veh = pd.concat([carburant_vp, operating_vp, capital_vp], axis=1).T
    user_veh[list_cols_ESE.Val_econ] = user_veh[list_cols_ESE.Val_tutelaires] * user_veh[list_cols_ESE.Diff_scenarios]
    return user_veh

def user_time_vp(vhr_in):
    time_vp ={}         # Valeur du temps pour les usagers des VP
    time_vp[list_cols_ESE.Item] = 'VTTS - passenger trips (VP)'
    time_vp[list_cols_ESE.Diff_scenarios] = vhr_in * yaml_content['taux_occupation']
    time_vp[list_cols_ESE.Val_tutelaires] = yaml_content['VTTS']
    time_vp = pd.Series(time_vp)
    time_vp[list_cols_ESE.Val_econ] = time_vp[list_cols_ESE.Val_tutelaires] * time_vp[list_cols_ESE.Diff_scenarios]
    return pd.DataFrame(time_vp)

def rule_of_half_vp(f1, f2):
    # Constantes qu'on va utiliser
    carburant_vp = yaml_content['VP_moy_fuel_basic']        # Vehicle fuel costs
    operating_vp = yaml_content['VP_non_fuel_basic']        # Vehicle operating  costs - non fuel
    capital_vp = yaml_content['VP_capital_marginal_basic']  # Vehicle capital  costs
    VTTS_business = yaml_content['VTTS_business']      # Valeur du temps pour les usagers des VP motif = business
    VTTS_commute_school_childcare = yaml_content['VTTS_commute_school_childcare']   # motif = commute/school/childcare
    VTTS_others = yaml_content['VTTS_others']      # motif = 'others'
    #TODO: Différenciation entre motifs.


    def load_skims(dossier, hor):
        visum_path = os.path.join(dossier, '2_Bouclage')
        for i in range(cNbBcl, 0, -1):
            path_iter = os.path.join(visum_path, f'Iter{i}')
            isExist = os.path.exists(path_iter)
            if isExist:
                break
        myvisum = win32.Dispatch("Visum.Visum")
        # PPM
        myvisum.LoadVersion(os.path.join(path_iter, f'Vers{hor}_scen_iter{i}.ver'))
        temps = helpers.GetSkimMatrix(myvisum, 'TpsCh', 'V')
        distance = helpers.GetSkimMatrix(myvisum, 'Dist', 'V')
        return temps, distance

    # def flux_to_vehhr(flux, temps):
    #     veh_hr = flux *
    #     return

    def read_flux(dossier, hor):
        dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/MODUSCaleUVP_df_{hor}_scen'), 'rb')
        flux_uvp = pkl.load(dbfile)
        dbfile = open(Path(dossier + f'/1_Fichiers_intermediares/Modus_VP_motcat_scen_{hor}'), 'rb')
        flux_apres_cm = pkl.load(dbfile)

        flux_motifs_drieat = pd.DataFrame(np.zeros(flux_apres_cm.shape))
        for col in flux_motifs_drieat.columns:
            flux_motifs_drieat[col] = flux_apres_cm[col]/flux_apres_cm.sum(1) * flux_uvp['FLUX']

            # Pour chacun des motifs, on va créet une série, et le transformer en array numpy pour ensuite faire un
            # reshape pour créer les matrices qui sont les outputs de cette étape
        flux_business = flux_motifs_drieat[[2, 3, 13, 14]].sum(1).to_numpy().reshape(cNbZone, cNbZone)
        flux_commute_school_childcare = flux_motifs_drieat[[0, 1, 4, 5, 6, 7, 8,
                                                            11, 12, 15, 16, 17, 18, 19]].to_numpy()\
                                                            .sum(1).reshape(cNbZone, cNbZone)
        flux_others = flux_motifs_drieat[[9, 10, 20, 21]].to_numpy().sum(1).reshape(cNbZone, cNbZone)
        flux_uvp = flux_uvp['FLUX'].to_numpy().reshape(cNbZone, cNbZone)
        return flux_uvp, flux_business, flux_commute_school_childcare, flux_others




    if PPM:
        t1, d1 = load_skims(f1, 'PPM')
        t2, d2 = load_skims(f2, 'PPM')
        flux_uvp1, flux_business1, flux_commute_school_childcare1, flux_others1 = read_flux(f1, 'PPM')
        flux_uvp2, flux_business2, flux_commute_school_childcare2, flux_others2 = read_flux(f2, 'PPM')
        # delta_cs_ppm = 0.5 * (flux_PPM1 + flux_PPM2) * \
        #                (time_vp * t2 +

    t1



if __name__ == '__main__':
    # user_veh_fn(1e5)
    # user_time_vp(5e5)
    f1 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_avec_gratuite'
    f2 = r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite'
    rule_of_half_vp(f1, f2)


