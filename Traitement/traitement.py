import pandas as pd
from Data import A_CstesModus, CstesStruct
from Data.A_CstesModus import *
from Data.fonctions_gen import *
import pickle as pkl




def ODvide_func(n):
    ODvide = np.ones((n**2, 2))
    for i in range(n):
        for j in range(n):
            k = (i) * n + j
            ODvide[k, 0] = i + 1
            ODvide[k, 1] = j + 1
    return ODvide

# Cette fonction crée à la fois les classes de portée pour le dessin des cartes et pour l'attribution des taux de
# conducteurs et d'autosolismes. Les résultats sont ensuite picklés.
def classe_gen():
    dbfile = open(f'{dir_dataTemp}bdinter', 'rb')
    bdinter = pkl.load(dbfile)
    bdinter['Classe_carte'] = 0
    bdinter.loc[(bdinter['DVOL'] > 0)&(bdinter['DVOL'] < classe1), 'Classe_carte'] = 'Classe1'
    bdinter.loc[(bdinter['DVOL'] > classe1) & (bdinter['DVOL'] < classe2), 'Classe_carte'] = 'Classe2'
    bdinter.loc[(bdinter['DVOL'] > classe2) & (bdinter['DVOL'] < classe3), 'Classe_carte'] = 'Classe3'
    bdinter.loc[(bdinter['DVOL'] > classe3) & (bdinter['DVOL'] < classe4), 'Classe_carte'] = 'Classe4'
    bdinter.loc[(bdinter['DVOL'] > classe4) & (bdinter['DVOL'] < classe5), 'Classe_carte'] = 'Classe5'
    bdinter.loc[(bdinter['DVOL'] > classe5) & (bdinter['DVOL'] < classe6), 'Classe_carte'] = 'Classe5'
    bdinter.loc[(bdinter['DVOL'] > classe6) & (bdinter['DVOL'] < classe7), 'Classe_carte'] = 'Classe6'
    bdinter.loc[bdinter['DVOL'] > classe7, 'Classe_carte'] = 'Classe8'

    bdinter['Classe_convvp'] = 0
    bdinter.loc[(bdinter['DVOL'] > 0)&(bdinter['DVOL'] < classe_convvp1), 'Classe_convvp'] = 'Classe1'
    bdinter.loc[(bdinter['DVOL'] > classe_convvp1) & (bdinter['DVOL'] < classe_convvp2), 'Classe_convvp'] = 'Classe2'
    bdinter.loc[bdinter['DVOL'] > classe_convvp2, 'Classe_convvp'] = 'Classe3'

    dbfile = open(f'{dir_dataTemp}Classe', 'wb')
    pkl.dump(bdinter[['Classe_carte', 'Classe_convvp']], dbfile)
    dbfile.close()
    return bdinter[['Classe_carte', 'Classe_convvp']]




def traitementTC(H, n, hor):
    # Kiko - temporary source of the files that will be used for this step;
    ModusTC_motcat = pd.read_sas(dir_root + '\\M3_Chaine\Modus_Python\Other_files\Confirmation distribution\\motcattc.sas7bdat')

    if H == 'PPM' or H == 'PPS':
        ModusTC_motcatH = ModusTC_motcat / 4
    if H == 'PCJ':
        ModusTC_motcatH = ModusTC_motcat / 6

    ModusTC_motcatH_Parmod = ModusTC_motcatH.sum(1)

    ModusTCH = ModusTC_motcatH.sum(1).to_numpy().reshape((cNbZone, cNbZone))

    # Pickling ModusTCH parce qu'il est utilisé ailleurs que dans la fonction principal où traitementTC est appelé
    dbfile = open(f'{dir_dataTemp}ModusTCH', 'wb')
    pkl.dump(ModusTCH, dbfile)
    dbfile.close()

    return ModusTCH, ModusTC_motcatH_Parmod

def traitementVP(H, n, hor):
    def prepconvvp(H):
        Classe = classe_gen().Classe_convvp.to_numpy()
        convvp_modus313 = pd.read_sas(f'{dir_zonage}\\convvp_modus313.sas7bdat')
        convvp_modus313['Periode'].replace({b'M':'PPM', b'C':'PCJ', b'S':'PPS'}, inplace=True)
        convvp_modus313['Classe'] = 0
        convvp_modus313['Classe'] = convvp_modus313['Classe'].astype('float64')
        for key, value in Classe_dict.items():
            convvp_modus313['Classe'] = np.where(((convvp_modus313['Portee_min'] >= value[0]) & (convvp_modus313['Portee_max'] <= value[1])), key, convvp_modus313['Classe'])
        convvp_modus313 = convvp_modus313[convvp_modus313['Periode'] == H]
        convvp_modus313['MOTIF_C'] = convvp_modus313['MOTIF_C'].astype('int64')
        # Array numpy parce qu'un dataframe était trop lent.
        motif_classe_part = convvp_modus313[['Classe', 'MOTIF_C', 'Part_conducteur']].T.to_numpy()
        Part_conducteur = convvp_modus313['Part_conducteur'].to_numpy()
        Part_autosoliste = convvp_modus313['Part_autosoliste'].to_numpy()

        # Kiko - Une fonction pour faire le calcul plus rapidement, mais ne marche pas pour l'instant
        # @jit(nopython=True)
        # def tx_conv_fonc():
        #     TXCONV = np.zeros((cNbZone ** 2, cNbMotifC))
        #     for i in range(cNbZone ** 2):
        #         for j in range(cNbMotifC):
        #             TXCONV[i, j] = Part_conducteur[(motif_classe_part[1] == j + 1)&
        #                                                (motif_classe_part[0] == Classe[i])]
        #     return TXCONV
        #
        # TXCONV = tx_conv_fonc()


        # Kiko - Correcte mais trop lent.
        TXSOLO = np.zeros((cNbZone ** 2, cNbMotifC))
        TXCONV = np.zeros((cNbZone ** 2, cNbMotifC))
        for i in range(cNbZone ** 2):
            for j in range(cNbMotifC):
                TXCONV[i, j] = Part_conducteur[(motif_classe_part[1] == j + 1)&
                                                   (motif_classe_part[0] == Classe[i])]
                TXSOLO[i, j] = Part_autosoliste[(motif_classe_part[1] == j + 1) &
                                                (motif_classe_part[0] == Classe[i])]
        TXCONV = np.concatenate([TXCONV, TXCONV], axis=1)
        TXSOLO = np.concatenate([TXSOLO, TXSOLO], axis=1)
        return TXCONV, TXSOLO

        # TXCONV = np.zeros((cNbZone ** 2, cNbMotifC))
        # for i in range(cNbZone ** 2):
        #     for j in range(cNbMotifC):
        #         TXCONV[i, j] = convvp_modus313.loc[(motif_classe_part['MOTIF_C'] == j + 1)&
        #                                            (motif_classe_part['Classe'] == Classe.loc[i]), 'Part_conducteur']
        #     TXCONV[:, i + 1] = colonne

        # convvp = convvp_modus313[['Part_conducteur', 'Part_autosoliste', 'MOTIF_C', 'Classe']].groupby(by=['Classe', 'MOTIF_C']).sum()
        # convvp = convvp.unstack()

        # Kiko - consider using a dictionary for the TXCONV
        # TXCONV1 = np.zeros((cNbZone**2, cNbMotifC))
        # TXCONV2 = np.zeros((cNbZone**2, cNbMotifC))
        # TXCONV3 = np.zeros((cNbZone**2, cNbMotifC))
        # CONVOSOLO = np.zeros((cNbZone ** 2, cNbMotifC))
        # for j in range(1, cNbMotifC+1):
        #     TXCONV1[:, j-1] = convvp_modus313.loc[(convvp_modus313['Classe'] == 'Classe1')&(convvp_modus313['MOTIF_C'] == j), 'Part_conducteur']
        #     TXCONV2[:, j-1] = convvp_modus313.loc[(convvp_modus313['Classe'] == 'Classe2')&(convvp_modus313['MOTIF_C'] == j), 'Part_conducteur']
        #     TXCONV3[:, j-1] = convvp_modus313.loc[(convvp_modus313['Classe'] == 'Classe3')&(convvp_modus313['MOTIF_C'] == j), 'Part_conducteur']
        #     CONVOSOLO[:, j-1] = convvp_modus313.loc[(convvp_modus313['Classe'] == 'Classe3')&(convvp_modus313['MOTIF_C'] == j), 'Part_autosoliste']
        # TXCONV1 = np.concatenate([TXCONV1, TXCONV1], axis=1)
        # TXCONV2 = np.concatenate([TXCONV2, TXCONV2], axis=1)
        # TXCONV3 = np.concatenate([TXCONV3, TXCONV3], axis=1)
        # TXSOLO = np.concatenate([CONVOSOLO, CONVOSOLO], axis=1)
        # return TXCONV1, TXCONV2, TXCONV3, TXSOLO
        # Kiko - temporary source of the files that will be used for this step;
    ModusVP_motcat = pd.read_sas(
        dir_root + '\\M3_Chaine\Modus_Python\Other_files\Confirmation distribution\\motcatvp.sas7bdat')

    if H == 'PPM' or H == 'PPS':
        ModusVP_motcatH = ModusVP_motcat / 4
    if H == 'PCJ':
        ModusVP_motcatH = ModusVP_motcat / 6

    TXCONV, TXSOLO = prepconvvp(H)
    ModusVP_motcatH_Parmod = ModusVP_motcatH.sum(1)

    ModusUVP_motcatH = ModusVP_motcatH * TXCONV
    ModusUVP = ModusUVP_motcatH.sum(1)
    ModusUVPSOLO = (ModusUVP_motcatH * TXSOLO).sum(1)
    ModusUVPSOLO = np.where(ModusUVP > 0, ModusUVPSOLO/ModusUVP, ModusUVPSOLO)
    ModusUVPSOLO = ModusUVPSOLO.reshape(cNbZone**2, 1)

    ODvide = ODvide_func(cNbZone)

    ModusUVPSOLO = np.concatenate([ODvide, ModusUVPSOLO], axis=1)
    ModusUVPcarre = ModusUVP.to_numpy().reshape(cNbZone, cNbZone)

    # Pickling ModusUVPcarre parce qu'il est utilisé ailleurs que dans la fonction principal où traitementTC est appelé
    dbfile = open(f'{dir_dataTemp}ModusUVPcarre', 'wb')
    pkl.dump(ModusUVPcarre, dbfile)
    dbfile.close()

    ModusUVP = np.concatenate([ODvide, ModusUVP.to_numpy().reshape(cNbZone**2, 1)], axis=1)
    ModusUVP = pd.DataFrame(ModusUVP, columns=['ZONEO', 'ZONED', 'FLUX'])
    dbfile = open(f'{dir_dataTemp}ModusUVP', 'wb')
    pkl.dump(ModusUVP, dbfile)
    dbfile.close()

    return ModusUVP, ModusUVPcarre, ModusUVPSOLO

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
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        else:
            cibleATT = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Att'].sum()
            cibleEM = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
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
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        else:
            cibleATT = VS_Emp_CDG.loc[
                ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Att'].sum()
            cibleEM = VS_Emp_CDG.loc[
                ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Em'].sum()
            SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
                'FLUX'].sum().sum()
            SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
                'FLUX'].sum().sum()
        M_sans_VS_cordon[M_sans_VS_cordon['ZONED'] == i] = SelAtt
        M_sans_VS_cordon[M_sans_VS_cordon['ZONEO'] == i] = SelEm
    return M_sans_VS_cordon

def Vecteurs_SpecVP(H, n):
    dbfile = open(f'{dir_dataTemp}ModusUVP', 'rb')
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

    if IdVsVp == 1:
        ModusUVP_sans_VS_cordon = retranche_VS_cordon(n, H, ModusUVP)
        MODUSUVP_cord = pd.merge(MODUSUVP_cord, ModusUVP_sans_VS_cordon, on=['ZONEO', 'ZONED'], how='outer')
        MODUSUVP_cord['FLUX'] = np.where((MODUSUVP_cord['ZONEO'] <= cNbZone)|(MODUSUVP_cord['ZONED'] <= cNbZone),
                                         MODUSUVP_cord['FLUX_y'], MODUSUVP_cord['FLUX_x']
                                         )
        MODUSUVP_cord = MODUSUVP_cord.loc[:, ('ZONEO', 'ZONED', 'FLUX')]
    return MODUSUVP_cord





# # This was broken up into separate functions
# def Vecteurs_SpecVP(H, n):
#
#     # CORDVP = pd.read_csv(Mat_Calees[f'CORDVP_{H}_{n}'].path, sep=Mat_Calees[f'CORDVP_{H}_{n}'].sep,
#     #                      skiprows=Mat_Calees[f'CORDVP_{H}_{n}'].skip, encoding='Latin1', names=['ZONEO', 'ZONED', 'FLUX'])
#     from Data.traitment_data import read_mat
#     read_mat = read_mat()
#     read_mat.n = n
#     read_mat.per = H
#     PoidsVS, VS, VS_Emp_CDG, VS_Emp_ORLY, VS_Voy_CDG, VS_Voy_ORLY = read_mat.vect_spec()
#
#     CORDVP = read_mat.CORDVP_func()
#
#     PoidsVS.index = PoidsVS['ZONE']
#     # Kiko - 16/09/21 taux conversion déplacements - UVP ont changé, alors ne peut pas utiliser mes calculs précedents
# #     dbfile = open(f'{dir_dataTemp}ModusUVP', 'rb')
# #     ModusUVP = pkl.load(dbfile)
#     ModusUVP = pd.read_sas('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\'
# 								   'Modus_Python\\Copie de work\\modusuvpm2012_tmp2.sas7bdat')
#     ModusUVP.rename(columns={'ZoneO':'ZONEO', 'ZoneD':'ZONED'}, inplace=True)
#     # ModusUVP_tmp = pd.concat([ModusUVP, CORDVP], ignore_index=True)
#     #
#     # MODUSUVP_cord = complete(ModusUVP_tmp, cNbZone, cNbZone + 1, cNbZspec, cNbZone + cNbZspec + 1, cNbZext, 1)
#     #
#     # MODUSUVP_cord = MODUSUVP_cord['FLUX'].to_numpy().reshape((cNbZone + cNbZspec + cNbZext, cNbZone + cNbZspec + cNbZext))
#
#
#     ModusUVP_sans_VS = ModusUVP.copy()
#
#
#     for i in ZoneADP:
#         SelAtt = ModusUVP_sans_VS[ModusUVP_sans_VS['ZONED'] == i].copy()
#         SelEm = ModusUVP_sans_VS[ModusUVP_sans_VS['ZONEO'] == i].copy()
#         if i in ZoneOrly:
#             cibleATT = VS_Emp_ORLY.loc[~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)), 'Flux_Att'].sum()
#             cibleEM = VS_Emp_ORLY.loc[~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)), 'Flux_Em'].sum()
#             SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt['FLUX'].sum().sum()
#             SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm['FLUX'].sum().sum()
#         else:
#             cibleATT = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Att'].sum()
#             cibleEM = VS_Emp_CDG.loc[~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)), 'Flux_Em'].sum()
#             SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
#                 'FLUX'].sum().sum()
#             SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
#                 'FLUX'].sum().sum()
#         ModusUVP_sans_VS[ModusUVP_sans_VS['ZONED'] == i] = SelAtt
#         ModusUVP_sans_VS[ModusUVP_sans_VS['ZONEO'] == i] = SelEm
#
#     ModusUVP_sans_VS_cordon = ModusUVP_sans_VS.copy()
#
#         for i in ZoneADP:
#             SelAtt = ModusUVP_sans_VS_cordon[ModusUVP_sans_VS_cordon['ZONED'] == i].copy()
#             SelEm = ModusUVP_sans_VS_cordon[ModusUVP_sans_VS_cordon['ZONEO'] == i].copy()
#             if i in ZoneOrly:
#                 cibleATT = VS_Emp_ORLY.loc[
#                     ~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Att'].sum()
#                 cibleEM = VS_Emp_ORLY.loc[
#                     ~(VS_Emp_ORLY['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Em'].sum()
#                 SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
#                     'FLUX'].sum().sum()
#                 SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
#                     'FLUX'].sum().sum()
#             else:
#                 cibleATT = VS_Emp_CDG.loc[
#                     ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Att'].sum()
#                 cibleEM = VS_Emp_CDG.loc[
#                     ~(VS_Emp_CDG['Zone'].isin(ZoneEmpADP)) & (VS_Emp_ORLY['Zone'] <= cNbZone + cNbZspec), 'Flux_Em'].sum()
#                 SelAtt['FLUX'] *= (SelAtt['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Att_PPM'] * cibleATT)) / SelAtt[
#                     'FLUX'].sum().sum()
#                 SelEm['FLUX'] *= (SelEm['FLUX'].sum().sum() - (PoidsVS.loc[i, 'Em_PPM'] * cibleEM)) / SelEm[
#                     'FLUX'].sum().sum()
#             ModusUVP_sans_VS_cordon[ModusUVP_sans_VS_cordon['ZONED'] == i] = SelAtt
#             ModusUVP_sans_VS_cordon[ModusUVP_sans_VS_cordon['ZONEO'] == i] = SelEm
#
#     ModusUVP = pd.merge(ModusUVP_sans_VS_cordon, VS, on=['ZONEO', 'ZONED'], how='outer')
#     ModusUVP['FLUX'] = np.where(~(ModusUVP['ZONEO'].isin(ZoneADP))|~(ModusUVP['ZONED'].isin(ZoneADP)), ModusUVP['FLUX_x'],
#                                                ModusUVP['FLUX_y']
#     ModusUVP = ModusUVP.loc[:, ('ZONEO', 'ZONED', 'FLUX')]
#     dbfile = open(f'{dir_dataTemp}ModusUVP', 'wb')
#     pkl.dump(ModusUVP, dbfile)
#     dbfile.close()


    # Change code to make sure its output isn't negative.

    # Poids = pd.read_csv(Vect_spec[f'Poids_VS_{n}'].path, sep=Vect_spec[f'Poids_VS_{n}'].sep)
    # Poids.rename(columns={'Em_HPS':'Em_PPS', 'Em_HPM':'Em_PPM', 'Em_HPC':'Em_PCJ',
    #                       'Att_HPS': 'Att_PPS', 'Att_HPM': 'Att_PPM', 'Att_HPC': 'Em_PCJ',
    #                       }, inplace=True)
    # Poids_H = Poids[['ZONE', f'Em_{H}', f'Att_{H}']]


    # def retranche_VS(M,VS1,VS2,Zones1,Zones2,Zemp1,Zemp2,Poids):
    #     nr = M.shape[0]
    #     nz_CDG = len(ZoneCDG)
    #     nz_ORLY = len(ZoneOrly)
    #     Poids = np.zeros((max(nz_CDG, nz_ORLY), 2))
    #
    #
    #
    # if IdVsVp == 1:
    #     M_ssCordon = ModusUVP




    # II. IMPLEMENTATION DES VECTEURS SPECIFIQUES (ET CORDON POUR LE CAS VP)
def Calcul_VSTC(ADP, H, n, ModusUVPcarre, ModusTCH):
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
            SelRow = (ModusUVPcarre[ZoneCDG_list, :cNbZone + 1].sum(0) > 0)
            SelCol = (ModusUVPcarre[:cNbZone + 1, ZoneCDG_list].sum(1) > 0)

            RVpRow[0, SelRow] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneCDG_list, :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1)

            VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneCDG_list].sum(1) * RVpRow[0, :]
            VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneCDG_list, :cNbZone].sum(0) * RVpCol[:, 0].T

            # Même calcul, mais pour les voyageurs.
            RVpRow[0, SelRow] = VS_Voy_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneCDG_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Voy_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneCDG_list].sum(1)

            VSTcVoy[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneCDG_list].sum(1) * RVpRow[0, :]
            VSTcVoy[:cNbZone, 1] = ModusTCH[ZoneCDG_list, :cNbZone].sum(0) * RVpCol[:, 0].T
            if ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() > 0:
                VSTcEmp[cZEmpCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() * \
                                            VS_Emp_CDG.loc[cZEmpCDG - 1, 'Flux_Em'] / ModusTCH[ZoneCDG_list, ZoneCDG_list].sum()
                VSTcVoy[cZVoyCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() * \
                                            VS_Voy_CDG.loc[cZVoyCDG - 1, 'Flux_Em'] / ModusTCH[ZoneCDG_list, ZoneCDG_list].sum()
        else:
            SelRow = (ModusUVPcarre[ZoneOrly_list, :cNbZone + 1].sum(0) > 0)
            SelCol = (ModusUVPcarre[:cNbZone + 1, ZoneOrly_list].sum(1) > 0)

            RVpRow[0, SelRow] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneOrly_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneOrly_list].sum(1)
            VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
            VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T

            RVpRow[0, SelRow] = VS_Voy_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneOrly_list,
                                                                                          :cNbZone].sum(0)
            RVpCol[SelCol, 0] = VS_Voy_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                         ZoneOrly_list].sum(1)
            VSTcVoy[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
            VSTcVoy[:cNbZone, 1] = ModusTCH[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T
            if ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() > 0:
                VSTcEmp[cZEmpOrly - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() * \
                                            VS_Emp_ORLY.loc[cZEmpOrly - 1, 'Flux_Em'] / ModusTCH[ZoneOrly_list, ZoneOrly_list].sum()
                VSTcVoy[cZVoyOrly - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() * \
                                            VS_Voy_ORLY.loc[cZVoyOrly - 1, 'Flux_Em'] / ModusTCH[ZoneOrly_list, ZoneOrly_list].sum()

    else:
            if ADP == 'CDG':
                SelRow = (ModusUVPcarre[ZoneCDG_list, :cNbZone + 1].sum(0) > 0)
                SelCol = (ModusUVPcarre[:cNbZone + 1, ZoneCDG_list].sum(1) > 0)

                RVpRow[0, SelRow] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] - ModusUVPcarre[ZoneCDG_list,:cNbZone].sum(0)[SelRow]


                RVpCol[SelCol, 0] = VS_Emp_CDG.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] - ModusUVPcarre[:cNbZone, ZoneCDG_list].sum(1)[SelCol]


                VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneCDG_list].sum(1) + RVpRow[0, :]
                VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneCDG_list, :cNbZone].sum(0) + RVpCol[:, 0].T


                if ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() > 0:
                    VSTcEmp[cZEmpCDG - 1, 1] = ModusUVPcarre[ZoneCDG_list, ZoneCDG_list].sum() + ModusTCH[
                                                    ZoneCDG_list, ZoneCDG_list].sum() - \
                                                VS_Emp_CDG.loc[cZEmpCDG - 1, 'Flux_Em']

                VSTcVoyATT = VSTCCDG.loc[VSTCCDG['ZONED'] == cZVoyCDG]
                VSTcVoyATT.reset_index(inplace=True)
                VSTcVoyEM = VSTCCDG.loc[VSTCCDG['ZONEO'] == cZVoyCDG]
                VSTcVoyEM.reset_index(inplace=True)
                VSTcVoy = pd.concat([VSTcVoyATT['FLUX'], VSTcVoyEM['FLUX']], axis=1).to_numpy()
                
            else:
                SelRow = (ModusUVPcarre[ZoneOrly_list, :cNbZone + 1].sum(0) > 0)
                SelCol = (ModusUVPcarre[:cNbZone + 1, ZoneOrly_list].sum(1) > 0)

                RVpRow[0, SelRow] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelRow, 'Flux_Att'] / ModusUVPcarre[
                                                                                               ZoneOrly_list,
                                                                                               :cNbZone].sum(0)
                RVpCol[SelCol, 0] = VS_Emp_ORLY.loc[:cNbZone - 1, :].loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone,
                                                                                              ZoneOrly_list].sum(1)
                VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneOrly_list].sum(1) * RVpRow[0, :]
                VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneOrly_list, :cNbZone].sum(0) * RVpCol[:, 0].T

                
                if ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() > 0:
                    VSTcEmp[cZEmpOrly - 1, 1] = ModusUVPcarre[ZoneOrly_list, ZoneOrly_list].sum() + ModusTCH[
                                                    ZoneOrly_list, ZoneOrly_list].sum() - \
                                                VS_Emp_ORLY.loc[cZEmpOrly - 1, 'Flux_Em']
                VSTcVoyATT = VSTCORLY.loc[VSTCORLY['ZONED'] == cZVoyOrly]
                VSTcVoyATT.reset_index(inplace=True)
                VSTcVoyEM = VSTCORLY.loc[VSTCORLY['ZONEO'] == cZVoyOrly]
                VSTcVoyEM.reset_index(inplace=True)
                VSTcVoy = pd.concat([VSTcVoyATT['FLUX'], VSTcVoyEM['FLUX']], axis=1).to_numpy()
    VSTcEmp = np.where(VSTcEmp<0, 0, VSTcEmp)
    VSTcVoy = np.where(VSTcVoy < 0, 0, VSTcVoy)
    ADP_res[ADP] = ADP_tuple(VSTcEmp, VSTcVoy)

ADP_res = {}  # Dictionnaire pour sauvegarder les résultats des calculs ADP

def Vecteurs_SpecTC (H, n):
    dbfile = open(f'{dir_dataTemp}ModusUVPcarre', 'rb')
    ModusUVPcarre = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}ModusTCH', 'rb')
    ModusTCH = pkl.load(dbfile)

    Calcul_VSTC('CDG', H, n, ModusUVPcarre, ModusTCH)
    Calcul_VSTC('Orly', H, n, ModusUVPcarre, ModusTCH)


    return ADP_res


def AjoutMode_Gare(H, n ,mode):
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H
    if mode == 'VP':
        if idVGVP == 1:
            VGVP = read_mat.read_VGVP()



    #     # SelRow = (ModusUVPcarre[ZoneCDG - 1, :cNbZone + 1].sum(0) > 0)|(ModusUVPcarre[ZoneOrly - 1, :cNbZone + 1].sum(0) > 0)
    #     # SelCol = (ModusUVPcarre[:cNbZone + 1, ZoneCDG - 1].sum(1) > 0) | (ModusUVPcarre[:cNbZone + 1, ZoneOrly].sum(1) > 0)
    #
    #     # Vect_specdf = pd.read_csv(Vect_spec[f'VS_{H}{actuel}'].path, sep=Vect_spec[f'VS_{H}{actuel}'].sep)
    #     # # Vect_specdf = Vect_specdf[Vect_specdf['Zone'] <= cNbZone]
    #     # CDGEMP = Vect_specdf[(Vect_specdf['ZONEADP'] == 1290) & (Vect_specdf['Zone'] <= cNbZone)]
    #     # CDGVOY = Vect_specdf[(Vect_specdf['ZONEADP'] == 1291) & (Vect_specdf['Zone'] <= cNbZone)]
    #     # ORLYEMP = Vect_specdf[(Vect_specdf['ZONEADP'] == 1292) & (Vect_specdf['Zone'] <= cNbZone)]
    #     # ORLYVOY = Vect_specdf[(Vect_specdf['ZONEADP'] == 1293) & (Vect_specdf['Zone'] <= cNbZone)]
    #
    #     # Kiko - what to do about the length of that array VSEmp?
    #     # if max(len(SelCol), len(SelRow)) > 0:
    #     #     RVpRowCDG[0, SelRow] = CDGEMP.loc[SelRow, 'Flux_Att']/ModusUVPcarre[ZoneCDG, :cNbZone].sum(0)
    #     #     RVpColCDG[SelCol, 0] = CDGEMP.loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone, ZoneCDG].sum(1)
    #     #
    #     #     RVpRowORLY[0, SelRow] = ORLYEMP.loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneOrly, :cNbZone].sum(0)
    #     #     RVpColORLY[SelCol, 0] = ORLYEMP.loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone, ZoneOrly].sum(1)
    #     #     # RVpRow[0, SelRow] = Vect_specdf.loc[SelRow, 'Flux_Att'] / ModusUVPcarre[ZoneADP, :cNbZone].sum(0)
    #     #     # RVpCol[SelCol, 0] = Vect_specdf.loc[SelCol, 'Flux_Em'] / ModusUVPcarre[:cNbZone, ZoneADP].sum(1)
    #     #
    #     # VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneCDG].sum(1) * RVpRow[0, :]
    #     # VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneCDG, :cNbZone].sum(0) * RVpCol[:, 0].T
    #     # Pickling ModusTCH, ModusUVPcarre  parce qu'il est utilisé ailleurs que dans la fonction principal où traitementTC est appelé
    #
    #
    #
    #     VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneCDG].sum(1) * RVpRowCDG[0, :]
    #     VSTcEmp[:cNbZone, 0] += ModusTCH[:cNbZone, ZoneOrly].sum(1) * RVpRowORLY[0, :]
    #
    #     VSTcEmp[:cNbZone, 1] = ModusTCH[ZoneCDG, :cNbZone].sum(0) * RVpColCDG[:, 0].T
    #     VSTcEmp[:cNbZone, 1] += ModusTCH[ZoneOrly, :cNbZone].sum(0) * RVpColORLY[:, 0].T
    #     # VSTcEmp[:cNbZone, 0] = ModusTCH[:cNbZone, ZoneADP].sum(1) * RVpRow[0, :]
    #
    #     if ModusUVPcarre[ZoneADP, ZoneADP].sum() > 0:
    #         VSTcEmp[ZoneEmpADP, 0] = ModusTCH[ZoneADP, ZoneADP].sum() * \
    #                                  Vect_specdf.loc[(Vect_specdf['Zone'].isin(ZoneEmpADP)) &
    #                                                  (Vect_specdf['Zone'] == Vect_specdf['ZONEADP']),
    #                                                  'Flux_Att']/ModusUVPcarre[ZoneADP, ZoneADP].sum()
    #         VSTcEmp[ZoneEmpADP, 1] = VSTcEmp[ZoneEmpADP, 0]
    #
    #
    #     # Kiko - J'ai sauté directement aux calculs de VSTcVoy
    #     RVpRowCDG, RVpRowORLY = np.zeros((1, cNbZone)), np.zeros(
    #         (1, cNbZone))  # rapport calulés OD par OD pour chaque ligne
    #     RVpColCDG, RVpColORLY = np.zeros((cNbZone, 1)), np.zeros(
    #         (cNbZone, 1))  # rapport calulés OD par OD pour chaque colonne
    #
    #     # VSVoy_CDG = pd.read_csv(Vect_spec[f'VSTC_CDG_{H}{actuel}'].path, sep=Vect_spec[f'VSTC_CDG_{H}{actuel}'].sep)
    #     # VSVoy_ORLY = pd.read_csv(Vect_spec[f'VSTC_ORLY_{H}{actuel}'].path, sep=Vect_spec[f'VSTC_ORLY_{H}{actuel}'].sep)
    #
    #     if max(len(SelCol), len(SelRow)) > 0:
    #         RVpRowCDG[0, SelRow] = CDGVOY.loc[SelRow, 'Flux_Att']/ModusUVPcarre[1291, :cNbZone]
    #
    # ModusTCH = ModusTC_motcatH.sum(1).to_numpy().reshape((cNbZone, cNbZone))
    #
    #
    #     # TXCONV1 = np.zeros((cNbZone**2, cNbMotifC))
    #     # TXCONV2 = TXCONV1.copy()
    #     # TXCONV3 = TXCONV1.copy()
    #     # for i in range(cNbZone**2):
    #     #     for j in range(1, cNbMotifC+1):
    #     #         TXCONV1[i, j] = convvp_modus313.loc[(['Classe'] == 'Classe1'), ('Part_conducteur', j)]
    #     #         TXCONV2[i, j] = convvp_modus313.loc[(['Classe'] == 'Classe2'), ('Part_conducteur', j)]
    #     #         TXCONV3[i, j] = convvp_modus313.loc['Classe3', ('Part_conducteur', j)]
    #
    #
    #     # convvp = pd.pivot_table(convvp_modus313, values=['Part_conducteur', 'Part_autosoliste'], index=['Classe', 'Periode'], columns=['MOTIF_C', 'Part_conducteur', 'Part_autosoliste'])
    #     # convvp = convvp.T
    #     # convvp.to_csv(dir_dataTemp + 'convvp.csv')
    #     # convvp = pd.crosstab(convvp_modus313['Classe'], rownames = convvp_modus313['Classe'],
    #     #                      colnames=convvp_modus313['Part_conducteur', 'Part_autosoliste'],
    #     #                      )
    #     #
    #     #
    #     #
    #     # for motif in range(1, cNbMotifC + 1):
    #     #     for Classe in range(cNbClasse):
    #     #         np.where((Classe>convvp_modus313['Portee_min'])|(Classe<convvp_modus313['Portee_max']), )


# Brouillons
convvp_modus313['Classe'].sum()
value = (0,2)
key = 'Classe1'
convvp_modus313['Classe'] = np.where(((convvp_modus313['Portee_min'] >= value[0]) & (convvp_modus313['Portee_max'] <= value[1])), key, 0)
((convvp_modus313['Portee_min']>=value[0]) & (convvp_modus313['Portee_max'] <= value[1])).sum()
convvp_modus313['Classe'].sum()

convvp_modus313[['Portee_min', 'Portee_max']].groupby(by = ['Portee_min', 'Portee_max']).count()
ODvide = pd.DataFrame(ODvide)
ODvide.to_csv(dir_dataTemp+'ODvide.csv')

ModusUVPcarre[ZoneCDG, 1:cNbZone].shape
Vect_specdf['ZONEADP'].plot()
Vect_specdf['Zone'].plot()

CDGEMP = Vect_specdf[Vect_specdf['ZONEADP'] == 1290]
CDGVOY = Vect_specdf[Vect_specdf['ZONEADP'] == 1291]
ORLYEMP = Vect_specdf[Vect_specdf['ZONEADP'] == 1292]
ORLYVOY = Vect_specdf[Vect_specdf['ZONEADP'] == 1293]


Vect_specdf.groupby(by='ZONEADP').values()

ModusTCH_valid = pd.read_sas(f'{dir_dataTemp}\\Confirmation distribution\\modustcm2012.sas7bdat')
ModusTCH_valid = ModusTCH_valid.to_numpy()

diffModusTCH = pd.DataFrame((ModusTCH - ModusTCH_valid)/ModusTCH)
diffModusTCH.mean(1).plot()
diffModusTCH.sum().sum()
pd.DataFrame(ModusTCH_valid)
pd.DataFrame(ModusTCH)


ModusUVPSOLO_valid = pd.read_sas(f'{dir_dataTemp}\\Confirmation distribution\\modusuvpsolom2012.sas7bdat')
ModusUVPSOLO_valid.columns = range(3)
ModusUVPSOLO = pd.DataFrame(ModusUVPSOLO)
diffModusUVPSOLO = np.abs(ModusUVPSOLO - ModusUVPSOLO_valid)/ModusUVPSOLO_valid
diffModusUVPSOLO[2].mean()
diffModusUVPSOLO[2].plot()


ModusUVP_valid = pd.read_sas(f'{dir_dataTemp}\\Confirmation distribution\\modusuvpm2012_tmp.sas7bdat')
ModusUVP_valid.columns = range(3)
ModusUVP = pd.DataFrame(ModusUVP)
diffModusUVP = np.abs(ModusUVP - ModusUVP_valid)/ModusUVP
diffModusUVP[2].mean()
diffModusUVP[2].plot()

TXCONV_valid = pd.read_sas(f'{dir_dataTemp}\\Confirmation distribution\\txconv.sas7bdat')
TXCONV_valid.columns = range(22)

TXCONV = pd.DataFrame(TXCONV)
diffTXCONV = np.abs(TXCONV - TXCONV_valid)/TXCONV_valid
diffTXCONV.mean()


pd.DataFrame(TXCONV).mean(1).plot()

poids = pd.read_csv(Vect_spec[f'Poids_VS{actuel}'].path, sep=Vect_spec[f'Poids_VS{actuel}'].sep)

# Kiko - Plotting the impedance functions in Modus.

import matplotlib.pyplot as plt
from Data.distribution_data import dist_data
dist_data_instance = dist_data()
dist_data_instance.per = 'PPM'
DIST_PAR = dist_data_instance.DIST_PAR_FUNC()

vUTM = np.linspace(0, -5, 100)
vPAR = DIST_PAR.loc[20, :]
y = np.exp(vPAR[2] * vUTM) * (-vUTM) ** vPAR[3]
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.xlabel('Utility')
plt.ylabel('Impedance')


# plot the function
plt.plot(vUTM,y, 'r')

# show the plot
plt.show()


(UTM[1] < -1).sum()/1661521
(UTM[1] < -1).sum()
(UTM[1] < -1).sum() - (UTM.loc[(UTM.index)%1289 != 0, 1] < -1).sum()
1661521 - (UTM[1] < -1).sum()