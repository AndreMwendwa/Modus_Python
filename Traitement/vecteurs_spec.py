# Le calcul des vecteurs specifiques selon la méthode donné dans 3_Traitement_Modus3.1.3)

import pickle as pkl
from collections import namedtuple

import numpy
import pandas

from Data.A_CstesModus import ZoneADP, ZoneOrly, ZoneEmpADP, cNbZone, cNbZspec, cNbZext, idVSVP, ZoneCDG, IdmethodeVSTC, \
    cZEmpCDG, cZVoyCDG, cZEmpORLY, cZVoyORLY
from Data.fonctions_gen import complete, ODvide_func
from Quatre_Etapes.dossiers_simul import dir_dataTemp


def retranche_VS(n, H, M):
    M_sans_VS = M.copy()

    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H
    PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = read_mat.vect_spec()

    CORDVP = read_mat.CORDVP_func()

    PoidsVS.index = PoidsVS['ZONE']

    for i in ZoneADP:
        SelAtt = M_sans_VS[M_sans_VS['ZONED'] == i].copy()
        SelEm = M_sans_VS[M_sans_VS['ZONEO'] == i].copy()
        if i in ZoneOrly:
            cibleATT = VS_Emp_ORLY.loc[~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)), 'Flux_Att'].sum()
            cibleEM = VS_Emp_ORLY.loc[~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Att_{H}'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Em_{H}'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        else:
            cibleATT = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Att'].sum()
            cibleEM = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Att_{H}'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Em_{H}'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        M_sans_VS[M_sans_VS['ZONED'] == i] = SelAtt
        M_sans_VS[M_sans_VS['ZONEO'] == i] = SelEm
    return M_sans_VS


def retranche_VS_cordon(n, H, M_sans_VS):
    M_sans_VS_cordon = M_sans_VS.copy()

    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H
    PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = read_mat.vect_spec()

    PoidsVS.index = PoidsVS['ZONE']
    for i in ZoneADP:
        SelAtt = M_sans_VS_cordon[M_sans_VS_cordon['ZONED'] == i].copy()
        SelEm = M_sans_VS_cordon[M_sans_VS_cordon['ZONEO'] == i].copy()
        if i in ZoneOrly:
            cibleATT = VS_Emp_ORLY.loc[
                ~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Att'].sum()
            cibleEM = VS_Emp_ORLY.loc[
                ~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Att_{H}'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Em_{H}'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        else:
            cibleATT = VS_Emp_CDG.loc[
                ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Att'].sum()
            cibleEM = VS_Emp_CDG.loc[
                ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Att_{H}'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, f'Em_{H}'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        M_sans_VS_cordon[M_sans_VS_cordon['ZONED'] == i] = SelAtt
        M_sans_VS_cordon[M_sans_VS_cordon['ZONEO'] == i] = SelEm
    return M_sans_VS_cordon


def Vecteurs_SpecVP(H, n):
    dbfile = open(f'{dir_dataTemp}ModusUVP_{H}_{n}', 'rb')
    ModusUVP = pkl.load(dbfile)
    # ModusUVP = pd.read_sas('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\'
    #                        'Modus_Python\\Copie de work\\modusuvpm2012_tmp2.sas7bdat')
    # ModusUVP.rename(columns={'ZoneO': 'ZONEO', 'ZoneD': 'ZONED'}, inplace=True)
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H

    CORDVP = read_mat.CORDVP_func()
    ModusUVP_tmp = pd.concat([ModusUVP, CORDVP], ignore_index=True)

    MODUSUVP_cord = complete(ModusUVP_tmp, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)

    if idVSVP == 1:
        ModusUVP_sans_VS_cordon = retranche_VS_cordon(n, H, ModusUVP)
        MODUSUVP_cord = pd.merge(MODUSUVP_cord, ModusUVP_sans_VS_cordon, on=['ZONEO', 'ZONED'], how='outer')
        MODUSUVP_cord['FLUX'] = np.where((MODUSUVP_cord['ZONEO'] <= cNbZone) & (MODUSUVP_cord['ZONED'] <= cNbZone),
                                         MODUSUVP_cord['FLUX_y'], MODUSUVP_cord['FLUX_x']
                                         )
        MODUSUVP_cord = MODUSUVP_cord.loc[:, ('ZONEO', 'ZONED', 'FLUX')]

    # Pickling temporaire
    dbfile = open(f'{dir_dataTemp}MODUSUVP_cord_{H}_{n}', 'wb')
    pkl.dump(MODUSUVP_cord, dbfile)
    dbfile.close()
    return MODUSUVP_cord


    # II. IMPLEMENTATION DES VECTEURS SPECIFIQUES (ET CORDON POUR LE CAS VP)


def Calcul_VSTC(ADP, H, n, ModusUVPcarre, ModusTCcarre):
    global ADP_res
    ADP_tuple = namedtuple('ADP_tuple', 'EMP VOY')
    # Un namedtuple pour stocker les résultats ADP
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H

    VSTcEmp, VSTcVoy = np.zeros((cNbZone + cNbZspec, 2)), np.zeros((cNbZone + cNbZspec, 2))
    VSTCCDG, VSTCORLY = read_mat.VSTC()

    ZoneCDG_list = [x - 1 for x in ZoneCDG]
    ZoneOrly_list = [x - 1 for x in ZoneOrly]

    RVpRow = np.zeros((1, cNbZone))  # rapport calulés OD par OD pour chaque ligne
    RVpCol = np.zeros((cNbZone, 1))  # rapport calulés OD par OD pour chaque colonne

    PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = read_mat.vect_spec()
    if IdmethodeVSTC == 1:

        if ADP == 'CDG':
            SelRow = (ModusUVPcarre[ZoneCDG_list, :cNbZone].sum(0) > 0)
            SelCol = (ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1) > 0)

            RVpRow[0, SelRow] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneCDG_list, :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1)

            VSTcEmp[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneCDG_list].sum(1) * RVpRow[0, :]
            VSTcEmp[:cNbZone, 1] = ModusTCcarre[ZoneCDG_list, :cNbZone].sum(0) * RVpCol[:, 0].T

            # Même calcul, mais pour les voyageurs.
            RVpRow[0, SelRow] = VS_Voy_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneCDG_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Voy_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneCDG_list].sum(1)

            VSTcVoy[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneCDG_list].sum(1) * RVpRow[0, :]
            VSTcVoy[:cNbZone, 1] = ModusTCcarre[ZoneCDG_list, :cNbZone].sum(0) * RVpCol[:, 0].T
            if ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() > 0:
                VSTcEmp[cZEmpCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() * \
                                           VS_Emp_CDG.loc[cZEmpCDG - 1, 'Flux_Em'] / ModusTCcarre[ZoneCDG_list, ZoneCDG_list].sum()
                VSTcVoy[cZVoyCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() * \
                                           VS_Voy_CDG.loc[cZVoyCDG - 1, 'Flux_Em'] / ModusTCcarre[ZoneCDG_list, ZoneCDG_list].sum()
        else:
            SelRow = (ModusUVPcarre[ZoneOrly_list, :cNbZone].sum(0) > 0)
            SelCol = (ModusUVPcarre[:cNbZone, ZoneOrly_list].sum(1) > 0)

            RVpRow[0, SelRow] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneOrly_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneOrly_list].sum(1)
            VSTcEmp[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
            VSTcEmp[:cNbZone, 1] = ModusTCcarre[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T

            RVpRow[0, SelRow] = VS_Voy_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneOrly_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Voy_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneOrly_list].sum(1)
            VSTcVoy[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
            VSTcVoy[:cNbZone, 1] = ModusTCcarre[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T
            if ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() > 0:
                VSTcEmp[cZEmpORLY - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() * \
                                            VS_Emp_ORLY.loc[cZEmpORLY - 1, 'Flux_Em'] / ModusTCcarre[ZoneOrly_list, ZoneOrly_list].sum()
                VSTcVoy[cZVoyORLY - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() * \
                                            VS_Voy_ORLY.loc[cZVoyORLY - 1, 'Flux_Em'] / ModusTCcarre[ZoneOrly_list, ZoneOrly_list].sum()

    else:
            if ADP == 'CDG':
                SelRow = (ModusUVPcarre[ZoneCDG_list, :cNbZone].sum(0) > 0)
                SelCol = (ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1) > 0)

                RVpRow[0, SelRow] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] - ModusUVPcarre[ZoneCDG_list,:cNbZone].sum(0)[SelRow]


                RVpCol[SelCol, 0] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] - ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1)[SelCol]


                VSTcEmp[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneCDG_list].sum(1) + RVpRow[0, :]
                VSTcEmp[:cNbZone, 1] = ModusTCcarre[ZoneCDG_list, :cNbZone].sum(0) + RVpCol[:, 0].T


                if ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() > 0:
                    VSTcEmp[cZEmpCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() + ModusTCcarre[
                                                    ZoneCDG_list, ZoneCDG_list].sum() - \
                                               VS_Emp_CDG.loc[cZEmpCDG - 1, 'Flux_Em']

                VSTcVoy = np.zeros((cNbZone + cNbZspec, 2))
                VSTcVoyATT = VSTCCDG.loc[VSTCCDG['ZONED'] == cZVoyCDG]
                VSTcVoyATT.reset_index(inplace=True)
                VSTcVoyEM = VSTCCDG.loc[VSTCCDG['ZONEO'] == cZVoyCDG]
                VSTcVoyEM.reset_index(inplace=True)
                VSTcVoy[:cNbZone, :] = pd.concat([VSTcVoyATT['FLUX'], VSTcVoyEM['FLUX']], axis=1).to_numpy()
            else:
                SelRow = (ModusUVPcarre[ZoneOrly_list, :cNbZone].sum(0) > 0)
                SelCol = (ModusUVPcarre[:cNbZone, ZoneOrly_list].sum(1) > 0)

                RVpRow[0, SelRow] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[
                                                                                               ZoneOrly_list,
                                                                                               :cNbZone].sum(0)
                RVpCol[SelCol, 0] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                              ZoneOrly_list].sum(1)
                VSTcEmp[:cNbZone, 0] = ModusTCcarre[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
                VSTcEmp[:cNbZone, 1] = ModusTCcarre[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T


                if ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() > 0:
                    VSTcEmp[cZEmpORLY - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() + ModusTCcarre[
                                                    ZoneOrly_list, ZoneOrly_list].sum() - \
                                                VS_Emp_ORLY.loc[cZEmpORLY - 1, 'Flux_Em']
                VSTcVoy = np.zeros((cNbZone + cNbZspec, 2))
                VSTcVoyATT = VSTCORLY.loc[VSTCORLY['ZONED'] == cZVoyORLY]
                VSTcVoyATT.reset_index(inplace=True)
                VSTcVoyEM = VSTCORLY.loc[VSTCORLY['ZONEO'] == cZVoyORLY]
                VSTcVoyEM.reset_index(inplace=True)
                VSTcVoy[:cNbZone, :] = pd.concat([VSTcVoyATT['FLUX'], VSTcVoyEM['FLUX']], axis=1).to_numpy()
    VSTcEmp = np.where(VSTcEmp<0, 0, VSTcEmp)
    VSTcVoy = np.where(VSTcVoy < 0, 0, VSTcVoy)
    ADP_res[ADP] = ADP_tuple(VSTcEmp, VSTcVoy)


ADP_res = {}  # Dictionnaire pour sauvegarder les résultats des calculs ADP


def Vecteurs_SpecTC (H, n):
    dbfile = open(f'{dir_dataTemp}ModusUVPcarre_{H}_{n}', 'rb')
    ModusUVPcarre = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}ModusTCcarre_{H}_{n}', 'rb')
    ModusTCcarre = pkl.load(dbfile)


    # * 2-b. Calcul des vecteurs spécifiques TC */
    # /* 2-b-i. Utilisation de la macro VSTC pour le calcul des VS correspondant à chacun des aéroports */
    Calcul_VSTC('CDG', H, n, ModusUVPcarre, ModusTCcarre)
    Calcul_VSTC('ORLY', H, n, ModusUVPcarre, ModusTCcarre)

    # 2-c. Soustraction des VS de la matrice */
    # 			/*--- On soustrait les VS de la matrice de travail
    ODvide = pd.DataFrame(ODvide_func(cNbZone))
    ModusTCcarre = pd.DataFrame(ModusTCcarre.reshape(cNbZone ** 2))
    ModusTCcarre = pd.concat([ODvide, ModusTCcarre], axis=1)
    ModusTCcarre.columns = ['ZONEO', 'ZONED', 'FLUX']
    ModusTCcarre = retranche_VS(n, H, ModusTCcarre)
    ModusTCcarre = ModusTCcarre['FLUX'].to_numpy().reshape((cNbZone, cNbZone))
    # --- On crée la matrice finale en ajoutant les VS TC
    ModusTC = np.zeros((cNbZone + cNbZspec, cNbZone + cNbZspec))
    ModusTC[:cNbZone, :cNbZone] = ModusTCcarre
    ModusTC[cZEmpCDG - 1, :] = ADP_res['CDG'].EMP[:, 1]
    ModusTC[:, cZEmpCDG - 1] = ADP_res['CDG'].EMP[:, 0]
    ModusTC[cZEmpORLY - 1, :] = ADP_res['ORLY'].EMP[:, 1]
    ModusTC[:, cZEmpORLY - 1] = ADP_res['ORLY'].EMP[:, 0]

    ModusTC[cZVoyCDG - 1, :] = ADP_res['CDG'].VOY[:, 1]
    ModusTC[:, cZVoyCDG - 1] = ADP_res['CDG'].VOY[:, 0]
    ModusTC[cZVoyORLY - 1, :] = ADP_res['ORLY'].VOY[:, 1]
    ModusTC[:, cZVoyORLY - 1] = ADP_res['ORLY'].VOY[:, 0]

    ODvide = pd.DataFrame(ODvide_func(cNbZone + cNbZspec))
    ModusTC = pd.DataFrame(ModusTC.reshape((cNbZone + cNbZspec) ** 2, 1))
    ModusTC = pd.concat([ODvide, ModusTC], axis=1)
    ModusTC.columns = ['ZONEO', 'ZONED', 'FLUX']

    # Pickling temporaire
    dbfile = open(f'{dir_dataTemp}ModusTC_{H}_{n}', 'wb')
    pkl.dump(ModusTC, dbfile)
    dbfile.close()
    return ModusTC