from os.path import exists
import os
from Data.A_CstesModus import *
import win32com.client as win32
import pandas as pd


def vkm_vhr_fn(dossier):
    # file_exists = exists(path_to_file)
    visum_path = os.path.join(dossier, '2_Bouclage')
    for i in range(cNbBcl, 0, -1):
        path_iter = os.path.join(visum_path, f'Iter{i}')
        isExist = os.path.exists(path_iter)
        if isExist:
            break
    myvisum = win32.Dispatch("Visum.Visum")
    # PPM
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPM_scen_iter{i}.ver'))
    longueurs = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    temps = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('TCur_PrTSys(V)'))
    vkm_ppm = (longueurs[1] * flux[1]).sum()
    vhr_ppm = (temps[1] * flux[1]).sum()/3600
    # PPS
    myvisum.LoadVersion(os.path.join(path_iter, f'VersPPS_scen_iter{i}.ver'))
    longueurs = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('length'))
    flux = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('VolVehPrT (AP)'))
    temps = pd.DataFrame(myvisum.Net.Links.GetMultiAttValues('TCur_PrTSys(V)'))
    vkm_pps = (longueurs[1] * flux[1]).sum()
    vhr_pps = (temps[1] * flux[1]).sum()/3600
    # TODO: Ca n'a aucun sens. Avec ces valeurs divisés par 3600
    #  on obtient des effets tellement minimes pour la valeur du temps.
    # Totaux
    vkm = vkm_ppm + vkm_pps
    vhr = (vhr_ppm + vhr_pps)
    return vkm, vhr, vkm_ppm, vkm_pps, vhr_ppm, vhr_pps



if __name__ == '__main__':
    vkm_vhr_fn(r'C:\Users\mwendwa.kiko\Documents\Stage\MODUSv3.1.3\M3_Chaine\Modus_Python\Other_files\Econtrans_sans_gratuite')