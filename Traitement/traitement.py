from Data.fonctions_gen import *
import pickle as pkl
from pathlib import Path

from Data.fonctions_gen import ODvide_func
from Quatre_Etapes.dossiers_simul import *
# from vecteurs_spec import Vecteurs_SpecTC, Vecteurs_SpecVP  # Pas actif, puisque la méthode prise en compte des
# vecteurs spécifiques dans Modus-Python est basé sur le calage.

# Liste des fichiers intérmediaires crées ici et la où ils sont utilisés (important pour modifier quoi que ce soit
# dans Modus_Python):
# 1. bdinter - BDD interzonale créé dans prepare data, modifié dans bouclage
# 2. Modus_TC_motcat - résultat de choix modal pour l'horaire (H) et l'horizon(n).
# 3. ModusTCcarre - résultat du traitementTC, le résultat de 2 ci-dessus divisé par 4 (PPM et PPS) ou 6 (PCJ)
# (format matrice de cNbZone * cNbZone)
#     ModusTC_df - le même, mais sous forme de dataframe avec colonnes = ZONEO, ZONED, FLUX
# 4. Modus_VP_motcat - résultat de choix modal pour l'horaire (H) et l'horizon(n).
# 5. ModusUVPcarre - résultat de traitementVP, le résultat de 4 ci-dessus divisé par 4 (PPM et PPS) ou 6 (PCJ)
#     ModusUVP_df - le même, mais sous forme de dataframe avec colonnes = ZONEO, ZONED, FLUX
# 6. ModusTC - résultat du rajoute des VS et des vecteurs gares pour les TC.
# 7. MODUSUVP_cord - résultat du rajoute des VS et des vecteurs gares pour les UVP.


# Cette fonction crée à la fois les classes de portée pour le dessin des cartes et pour l'attribution des taux de
# conducteurs et d'autosolismes. Les résultats sont ensuite picklés.
def classe_gen(n):
    dbfile = open(f'{dir_dataTemp}bdinter_{n}', 'rb')
    bdinter = pkl.load(dbfile)
    bdinter['Classe_carte'] = 0
    bdinter.loc[(bdinter['DVOL'] > 0) & (bdinter['DVOL'] < classe1), 'Classe_carte'] = 'Classe1'
    bdinter.loc[(bdinter['DVOL'] > classe1) & (bdinter['DVOL'] < classe2), 'Classe_carte'] = 'Classe2'
    bdinter.loc[(bdinter['DVOL'] > classe2) & (bdinter['DVOL'] < classe3), 'Classe_carte'] = 'Classe3'
    bdinter.loc[(bdinter['DVOL'] > classe3) & (bdinter['DVOL'] < classe4), 'Classe_carte'] = 'Classe4'
    bdinter.loc[(bdinter['DVOL'] > classe4) & (bdinter['DVOL'] < classe5), 'Classe_carte'] = 'Classe5'
    bdinter.loc[(bdinter['DVOL'] > classe5) & (bdinter['DVOL'] < classe6), 'Classe_carte'] = 'Classe6'
    bdinter.loc[(bdinter['DVOL'] > classe6) & (bdinter['DVOL'] < classe7), 'Classe_carte'] = 'Classe7'
    bdinter.loc[bdinter['DVOL'] > classe7, 'Classe_carte'] = 'Classe8'

    bdinter['Classe_convvp'] = 0
    bdinter.loc[(bdinter['DVOL'] > 0) & (bdinter['DVOL'] < classe_convvp1), 'Classe_convvp'] = 'Classe1'
    bdinter.loc[(bdinter['DVOL'] > classe_convvp1) & (bdinter['DVOL'] < classe_convvp2), 'Classe_convvp'] = 'Classe2'
    bdinter.loc[bdinter['DVOL'] > classe_convvp2, 'Classe_convvp'] = 'Classe3'

    dbfile = open(f'{dir_dataTemp}Classe', 'wb')
    pkl.dump(bdinter[['Classe_carte', 'Classe_convvp']], dbfile)
    dbfile.close()
    return bdinter[['Classe_carte', 'Classe_convvp']]


#  I. FINALISATION DES MATRICES MODUS

# 1. Macro de Traitement des matrices TC à l'heure
#  pas de passage à l'horaire, hormis la division par 4 ou 6 selon la période étudiée

def traitementTC(H, n, hor):
    # -- TC : chargement de la matrice de la période concernée

    dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'rb')
    ModusTC_motcat = pkl.load(dbfile)

    # -- TC : passage horaire
    if H == 'PPM' or H == 'PPS':
        ModusTC_motcatH = ModusTC_motcat / 4
    elif H == 'PCJ':
        ModusTC_motcatH = ModusTC_motcat / 6

    # -- Storage de la matrice HPM pour calcul des parts modales
    ModusTC_motcatH_Parmod = ModusTC_motcatH.sum(1)

    # -- TC HPX : matrice "carrée" somme et stockage
    ModusTCcarre = ModusTC_motcatH.sum(1).to_numpy().reshape((cNbZone, cNbZone))
    dbfile = open(f'{dir_dataTemp}ModusTCcarre_{H}_{n}', 'wb')
    pkl.dump(ModusTCcarre, dbfile)
    dbfile.close()

    #  Créant la dataframe de format ZONEO, ZONED, FLUX
    ModusTC_df = ModusTC_motcatH.sum(1)
    ODvide = pd.DataFrame(ODvide_func(cNbZone))
    ModusTC_df = pd.concat([ODvide, ModusTC_df], axis=1)
    ModusTC_df.columns = ['ZONEO', 'ZONED', 'FLUX']
    dbfile = open(f'{dir_dataTemp}ModusTC_df{H}_{n}', 'wb')
    pkl.dump(ModusTC_df, dbfile)
    dbfile.close()

    return ModusTCcarre, ModusTC_motcatH_Parmod

# 2. Macro de traitement des matrices VP à une heure de pointe
def traitementVP(H, n, hor):

    # Préparation des taux de conversion
    def prepconvvp(H, n):
        # La première partie de cette fonction donne une classe de portée à chaque pair OD à partir de la fonction classe_gen
        # définie ci-dessus.
        Classe = classe_gen(n).Classe_convvp.to_numpy()     # Array numpy des classes pour chaque zone
        convvp_modus313 = pd.read_sas(f'{dir_zonage}\\convvp_modus313.sas7bdat')
        convvp_modus313['Periode'].replace({b'M' : 'PPM', b'C' : 'PCJ', b'S' : 'PPS'}, inplace=True)   # Dans MODUS-Python,
        # PPM n'est jamais appelé 'M'
        convvp_modus313['Classe'] = 0
        convvp_modus313['Classe'] = convvp_modus313['Classe'].astype('float64')

        # Ici on créet le dataframe avec les taux de conversation et taux d'autosolisme corréspondant aux différents
        # motifs et différents classes de portée.
        for key, value in Classe_dict.items():
            convvp_modus313['Classe'] = np.where(((convvp_modus313['Portee_min'] >= value[0]) &
                                        (convvp_modus313['Portee_max'] <= value[1])), key, convvp_modus313['Classe'])
        convvp_modus313 = convvp_modus313[convvp_modus313['Periode'] == H]
        convvp_modus313['MOTIF_C'] = convvp_modus313['MOTIF_C'].astype('int64')

        # Array numpy parce qu'un dataframe était trop lent.
        motif_classe_part = convvp_modus313[['Classe', 'MOTIF_C', 'Part_conducteur']].T.to_numpy()
        Part_conducteur = convvp_modus313['Part_conducteur'].to_numpy()
        Part_autosoliste = convvp_modus313['Part_autosoliste'].to_numpy()

        # Création des taux de conversion et taux d'autosolisme corréspondant aux 11 motifs pour tous les pairs OD selon
        # leurs classes de portée
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

        TX_CONV_SOLO = [TXCONV, TXSOLO]
        dbfile = open(f'{dir_dataTemp}TX_CONV_SOLO', 'wb')
        pkl.dump(TX_CONV_SOLO, dbfile)
        dbfile.close()

        return TXCONV, TXSOLO

    dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'rb')
    ModusVP_motcat = pkl.load(dbfile)

    if H == 'PPM' or H == 'PPS':
        ModusVP_motcatH = ModusVP_motcat / 4
    if H == 'PCJ':
        ModusVP_motcatH = ModusVP_motcat / 6

    # Puisque le processus de création des classes de portée est assez lent, on le fait seulement la première fois,
    # après on lit les résultats déjà crées.
    if not Path(f'{dir_dataTemp}TX_CONV_SOLO').is_file():
        TXCONV, TXSOLO = prepconvvp(H, n)
    else:
        dbfile = open(f'{dir_dataTemp}TX_CONV_SOLO', 'rb')
        TX_CONV_SOLO = pkl.load(dbfile)
        TXCONV, TXSOLO = TX_CONV_SOLO[0], TX_CONV_SOLO[1]

    # -- Storage de la matrice HPM pour calcul des parts modales
    ModusVP_motcatH_Parmod = ModusVP_motcatH.sum(1)

    ModusUVP_motcatH = ModusVP_motcatH * TXCONV     # -- passage en UVP
    ModusUVP_df = ModusUVP_motcatH.sum(1)
    ModusUVPSOLO = (ModusUVP_motcatH * TXSOLO).sum(1)   # calcul de la matrice d'autosolistes
    ModusUVPSOLO = np.where(ModusUVP_df > 0, ModusUVPSOLO/ModusUVP_df, ModusUVPSOLO)   # calcul de la part d'autosoliste
    # par OD
    ModusUVPSOLO = ModusUVPSOLO.reshape(cNbZone**2, 1)

    ODvide = ODvide_func(cNbZone)

    # ajout de Modus 3.1.3 : calcul de coefficient de séparation des matrices VP solistes et covoitureurs
    ModusUVPSOLO = np.concatenate([ODvide, ModusUVPSOLO], axis=1)

    # passage au format carré
    ModusUVPcarre = ModusUVP_df.to_numpy().reshape(cNbZone, cNbZone)   # -- UVP HPX : pas d'ajout des PL car affectation
    # sous VISUM est multiclasse, mais transformation en matrice carrée

    # Pickling ModusUVPcarre parce qu'il est utilisé ailleurs que dans la fonction principal où traitementTC est appelé
    dbfile = open(f'{dir_dataTemp}ModusUVPcarre_{H}_{n}', 'wb')
    pkl.dump(ModusUVPcarre, dbfile)
    dbfile.close()

    ModusUVP_df = np.concatenate([ODvide, ModusUVP_df.to_numpy().reshape(cNbZone**2, 1)], axis=1)
    ModusUVP_df = pd.DataFrame(ModusUVP_df, columns=['ZONEO', 'ZONED', 'FLUX'])
    ModusUVP_df = complete_b(ModusUVP_df, cNbZtot)
    dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_{n}', 'wb')
    pkl.dump(ModusUVP_df, dbfile)
    dbfile.close()

    return ModusUVP_df, ModusUVPcarre, ModusUVPSOLO

# 3. Ajout des flux voyageurs émis et attirés par les gares

def AjoutMode_Gare(H, n, mode):
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = n
    read_mat.per = H

    # a. Chargement des matrices mode
    dbfile = open(f'{dir_dataTemp}ModusTCcarre_{H}_{n}', 'rb')
    ModusTC_df = pkl.load(dbfile)
    ModusTC_df = pd.DataFrame(ModusTC_df.reshape(cNbZone ** 2))
    ODvide = pd.DataFrame(ODvide_func(cNbZone))
    ModusTC_df = pd.concat([ODvide, ModusTC_df], axis=1)
    ModusTC_df.columns = ['ZONEO', 'ZONED', 'FLUX']

    dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_{n}', 'rb')
    ModusUVP_df = pkl.load(dbfile)

    # b. Ajout du vecteur Flux voyageurs émis et attirés par les gares
    if mode == 'VP':
        if idVGVP == 1:
            VGVP = read_mat.read_VGVP()
            # Ajout du vecteur Flux voyageurs émis et attirés par les gares en deux étapes
            # D'abord, on combine les deux dataframes. Ensuite, on fait une seule colonne pour contenir les deux flux
            # flux_x, flux_y
            ModusUVP_df = pd.merge(ModusUVP_df, VGVP, on=['ZONEO', 'ZONED'], how='outer')
            ModusUVP_df['FLUX'] = np.where((ModusUVP_df['ZONEO'] <= cNbZone + cNbZspec + cNbZext)&
                                             (ModusUVP_df['ZONED'] <= cNbZone + cNbZspec + cNbZext), ModusUVP_df['FLUX_x'],
                                            ModusUVP_df['FLUX_y'])
            ModusUVP_df = ModusUVP_df.loc[:, ('ZONEO', 'ZONED', 'FLUX')]
            ModusUVP_df.sort_values(by=['ZONEO', 'ZONED'], inplace=True)

            # Stockage de la matrice crée
            dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_{n}', 'wb')
            pkl.dump(ModusUVP_df, dbfile)
            dbfile.close()

    elif mode == 'TC':
        if idVGTC == 1:
            VGTC = read_mat.read_VGTC()
            # Ajout du vecteur Flux voyageurs émis et attirés par les gares en deux étapes
            # D'abord, on combine les deux dataframes. Ensuite, on fait une seule colonne pour contenir les deux flux
            # flux_x, flux_y
            ModusTC_df = pd.merge(ModusTC_df, VGTC, on=['ZONEO', 'ZONED'], how='outer')
            ModusTC_df['FLUX'] = np.where((ModusTC_df['ZONEO'] <= cNbZone + cNbZspec + cNbZext) &
                                             (ModusTC_df['ZONED'] <= cNbZone + cNbZspec + cNbZext),
                                             ModusTC_df['FLUX_x'],
                                             ModusTC_df['FLUX_y'])
            ModusTC_df = ModusTC_df.loc[:, ('ZONEO', 'ZONED', 'FLUX')]
            ModusTC_df.sort_values(by=['ZONEO', 'ZONED'], inplace=True)
            ModusTC_df = complete_b(ModusTC_df, cNbZtot + 9)   # Le +9 est pour ajouter les 9 zones de plus à cNbZtot

            # Stockage de la matrice crée
            dbfile = open(f'{dir_dataTemp}ModusTC_{H}_{n}', 'wb')
            pkl.dump(ModusTC_df, dbfile)
            dbfile.close()


# Regroupement

def finalise(n):
    if PPM == 1:
        traitementTC('PPM', n, 'PPM')
        traitementVP('PPM', n, 'PPM')
        # Vecteurs_SpecVP('PPM', n)   # Pas actif, puisque la méthode prise en compte des vecteurs spécifiques dans
        # Modus-Python est basé sur le calage.
        # Vecteurs_SpecTC('PPM', n)
        if idVGTC == 1:
            AjoutMode_Gare('PPM', n, 'TC')
        if idVGVP == 1:
            AjoutMode_Gare('PPM', n, 'VP')
    
    if PCJ == 1:
        traitementTC('PCJ', n, 'PCJ')
        traitementVP('PCJ', n, 'PCJ')
        # Vecteurs_SpecVP('PCJ', n)
        # Vecteurs_SpecTC('PCJ', n)
        if idVGTC == 1:
            AjoutMode_Gare('PCJ', n, 'TC')
        if idVGVP == 1:
            AjoutMode_Gare('PCJ', n, 'VP')
    
    if PPS == 1:
        traitementTC('PPS', n, 'PPS')
        traitementVP('PPS', n, 'PPS')
        # Vecteurs_SpecVP('PPS', n)
        # Vecteurs_SpecTC('PPS', n)
        if idVGTC == 1:
            AjoutMode_Gare('PPS', n, 'TC')
        if idVGVP == 1:
            AjoutMode_Gare('PPS', n, 'VP')


    # REPORT DE CALAGE

# Fonction d'ajout des évolutions pour le report de calage
def ajout_evol(type: 'UVP ou TC', H: 'PPM, PCJ, PPS', id: 'idTC, idVP', seuilh, seuilb):
    from Data.traitment_data import read_mat
    read_mat = read_mat()
    read_mat.n = 'actuel'
    read_mat.per = H

    # Fichiers avec VS
    dbfile = open(f'{dir_dataTemp}ModusTC_{H}_actuel', 'rb')
    MODUSTC_actuel = pkl.load(dbfile)
    MODUSTC_actuel = MODUSTC_actuel.loc[(MODUSTC_actuel['ZONEO'] <= cNbcalzonage)&
                    (MODUSTC_actuel['ZONED'] <= cNbcalzonage), 'FLUX'].to_numpy()
    dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_actuel', 'rb')
    MODUSUVP_actuel = pkl.load(dbfile)
    MODUSUVP_actuel = MODUSUVP_actuel.loc[(MODUSUVP_actuel['ZONEO'] <= cNbcalzonage) &
                    (MODUSUVP_actuel['ZONED'] <= cNbcalzonage), 'FLUX'].to_numpy()
    dbfile = open(f'{dir_dataTemp}ModusTC_{H}_scen', 'rb')
    MODUSTC_scen = pkl.load(dbfile)
    MODUSTC_scen = MODUSTC_scen.loc[(MODUSTC_scen['ZONEO'] <= cNbcalzonage)&
                    (MODUSTC_scen['ZONED'] <= cNbcalzonage), 'FLUX'].to_numpy()
    dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_scen', 'rb')
    MODUSUVP_scen = pkl.load(dbfile)
    MODUSUVP_scen = MODUSUVP_scen.loc[(MODUSUVP_scen['ZONEO'] <= cNbcalzonage) &
                    (MODUSUVP_scen['ZONED'] <= cNbcalzonage), 'FLUX'].to_numpy()

    # Fichiers avec VS et cordon
    # Depuis qu'on a mis à arrêter d'appliquer la méthode de la DRIEAT, on fait juste une copie des fichiers crées
    # ci-dessous
    dbfile = open(f'{dir_dataTemp}ModusUVP_df{H}_scen', 'rb')
    MODUSUVP_cord_scen = pkl.load(dbfile)
    dbfile = open(f'{dir_dataTemp}ModusTC_{H}_scen', 'rb')
    ModusTC_VS_scen = pkl.load(dbfile)

    # Réduction aux nombres de zones qu'on va considérer
    ModusTC_VS_scen = ModusTC_VS_scen.loc[(ModusTC_VS_scen['ZONEO'] <= cNbZone + cNbZspec)
                                          & (ModusTC_VS_scen['ZONED'] <= cNbZone + cNbZspec), 'FLUX']
    ModusTC_VS_scen = ModusTC_VS_scen.to_numpy().reshape(cNbZone + cNbZspec, cNbZone + cNbZspec)

    MODUSUVP_cord_scen = MODUSUVP_cord_scen.loc[:, 'FLUX'].to_numpy().reshape((cNbZtot, cNbZtot))

    MODUSCaleUVP_actuel = read_mat.CALEUVP()
    MODUSCaleTC_actuel = read_mat.CALETC()

    # - a. Définition des paramètres du report de calage: CALE(actuel) = K.MODUS(actuel) + D
    # -- cas où on effectue le report de calage avec analyse des évolutions
    if type == 'VP':
        if id == 2:
            MODUSUVP_actuel = pd.Series(MODUSUVP_actuel)
            MODUSUVP_scen = pd.Series(MODUSUVP_scen)

            MODUSCaleUVP_actuel = MODUSCaleUVP_actuel.loc[
                (MODUSCaleUVP_actuel['ZONEO'] <= cNbcalzonage) & (MODUSCaleUVP_actuel['ZONED'] <= cNbcalzonage), 'FLUX']
            MODUSCaleUVP_actuel.reset_index(inplace=True, drop=True)

            # -- calcul du taux de croissance moyen entre les matrices MODUS
            TCM_UVP = MODUSUVP_scen.sum() / MODUSUVP_actuel.sum()

            C3_UVP = MODUSUVP_scen - TCM_UVP * k0 * MODUSUVP_actuel

            POS1_UVP = MODUSUVP_actuel == 0

            POS2_UVP = C3_UVP < 0

            POS3_UVP = C3_UVP >= 0

            CALEscen_UVP = pd.Series(np.zeros((cNbcalzonage ** 2)))
            CALEscen_UVP[POS1_UVP] = MODUSUVP_scen.loc[POS1_UVP] + MODUSUVP_actuel.loc[POS1_UVP]
            CALEscen_UVP[POS2_UVP] = MODUSUVP_scen.loc[POS2_UVP] * MODUSCaleUVP_actuel.loc[POS2_UVP] / MODUSUVP_actuel
            CALEscen_UVP[POS3_UVP] = MODUSUVP_scen.loc[POS3_UVP] + TCM_UVP * k0 * (
                        MODUSCaleUVP_actuel[POS3_UVP] - MODUSUVP_actuel[POS3_UVP])

            CALEscen_UVP = CALEscen_UVP.to_numpy().reshape((cNbcalzonage, cNbcalzonage))

            MODUSCaleUVP_scen = np.zeros((cNbZtot, cNbZtot))
            MODUSCaleUVP_scen[:cNbcalzonage, :cNbcalzonage] = CALEscen_UVP
            MODUSCaleUVP_scen[cNbcalzonage:cNbZtot, :] = MODUSUVP_cord_scen[cNbcalzonage:cNbZtot, :]
            MODUSCaleUVP_scen[:, cNbcalzonage:cNbZtot] = MODUSUVP_cord_scen[:, cNbcalzonage:cNbZtot]

        # -- cas où on effectue le report de calage sans analyse des évolutions
        elif id == 1:
            MODUSUVP_actuel = pd.Series(MODUSUVP_actuel)

            MODUSCaleUVP_actuel = MODUSCaleUVP_actuel.loc[
                (MODUSCaleUVP_actuel['ZONEO'] <= cNbcalzonage) & (MODUSCaleUVP_actuel['ZONED'] <= cNbcalzonage), 'FLUX']
            MODUSCaleUVP_actuel.reset_index(inplace=True, drop=True)

            # -- paramètre K de "dilatation" de la matrice MODUS
            R1_UVP = np.ones(cNbcalzonage ** 2)
            POS_UVP = MODUSUVP_actuel >= 0.001

            R1_UVP[POS_UVP] = MODUSCaleUVP_actuel[POS_UVP] / MODUSUVP_actuel[POS_UVP]
            K_UVP = np.minimum(R1_UVP, seuilh)  # on contraint la dilatation à être inférieure ou
            # égale à la valeur de "cSeuilh"
            K_UVP = np.maximum(K_UVP, seuilb)  # on contraint la dilatation à être supérieure ou
            # égale à la valeur de "cSeuilb"

            #   -- paramètre D d'ajout des flux manquants,
            #   On prend le maximum de D_TC et 0 pour garantir que D ne fait qu'ajouter des flux, sans en retirer
            D_UVP = np.maximum(MODUSCaleUVP_actuel - K_UVP * MODUSUVP_actuel, 0)

            #   -- ajustement pour recréer à la bonne dimension et conserver les flux intrazonaux : diag(K) = 1 et diag(D) = 0
            K_UVP = K_UVP.reshape((cNbcalzonage, cNbcalzonage))

            D_UVP = D_UVP.to_numpy().reshape((cNbcalzonage, cNbcalzonage))

            K_UVP = np.concatenate([K_UVP, np.ones((cNbcalzonage, cNbZtot - cNbcalzonage))], axis=1)
            K_UVP = np.concatenate([K_UVP, np.ones((cNbZtot - cNbcalzonage, cNbZtot))], axis=0)

            D_UVP = np.concatenate([D_UVP, np.zeros((cNbcalzonage, cNbZtot - cNbcalzonage))], axis=1)
            D_UVP = np.concatenate([D_UVP, np.zeros((cNbZtot - cNbcalzonage, cNbZtot))], axis=0)

        # * -- cas où on n'effectue pas le report de calage *
        else:
            K_UVP = np.ones((cNbZtot, cNbZtot))
            D_UVP = np.zeros((cNbZtot, cNbZtot))
        #   - b. Report de calage : CALE(scen) = K.MODUS(scen) + D
        if id < 2:
            MODUSCaleUVP_scen = K_UVP * MODUSUVP_cord_scen + D_UVP
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_{H}_scen', 'wb')
        pkl.dump(MODUSCaleUVP_scen, dbfile)
        dbfile.close()

        #  Résultats du calage sous forme d'un DataFrame pour le traitement.
        MODUSCaleUVP_df = pd.concat([pd.DataFrame(ODvide_func(cNbZone)),
                                     pd.DataFrame(MODUSCaleUVP_scen[:cNbZone, :cNbZone].reshape(cNbZone ** 2))], axis=1)
        MODUSCaleUVP_df.columns = ['ZONEO', 'ZONED', 'FLUX']
        dbfile = open(f'{dir_dataTemp}MODUSCaleUVP_df_{H}_scen', 'wb')
        pkl.dump(MODUSCaleUVP_df, dbfile)
        dbfile.close()

    elif type == 'TC':
        if id == 2:
            MODUSTC_actuel = pd.Series(MODUSTC_actuel)
            MODUSTC_scen = pd.Series(MODUSTC_scen)

            MODUSCaleTC_actuel = MODUSCaleTC_actuel.loc[
                (MODUSCaleTC_actuel['ZONEO'] <= cNbcalzonage) & (MODUSCaleTC_actuel['ZONED'] <= cNbcalzonage), 'FLUX']
            MODUSCaleTC_actuel.reset_index(inplace=True, drop=True)
            # MODUSCalePL = MODUSCalePL.loc[
            #     (MODUSCalePL['ZONEO'] <= cNbcalzonage) & (MODUSCalePL['ZONED'] <= cNbcalzonage), 'FLUX']
            # MODUSCalePL.reset_index(inplace=True, drop=True)

            #         -- calcul du taux de croissance moyen entre les matrices MODUS
            TCM_TC = MODUSTC_scen.sum() / MODUSTC_actuel.sum()

            C3_TC = MODUSTC_scen - TCM_TC * k0 * MODUSTC_actuel

            POS1_TC = MODUSTC_actuel == 0

            POS2_TC = C3_TC < 0

            POS3_TC = C3_TC >= 0

            CALEscen_TC = pd.Series(np.zeros((cNbcalzonage ** 2)))
            CALEscen_TC[POS1_TC] = MODUSTC_scen.loc[POS1_TC] + MODUSTC_actuel.loc[POS1_TC]
            CALEscen_TC[POS2_TC] = MODUSTC_scen.loc[POS2_TC] * MODUSCaleTC_actuel.loc[POS2_TC] / MODUSTC_actuel
            CALEscen_TC[POS3_TC] = MODUSTC_scen.loc[POS3_TC] + TCM_TC * k0 * (
                    MODUSCaleTC_actuel[POS3_TC] - MODUSTC_actuel[POS3_TC])

            CALEscen_TC = CALEscen_TC.to_numpy().reshape((cNbcalzonage, cNbcalzonage))

            MODUSCaleTC_scen = np.zeros((cNbZone + cNbZspec, cNbZone + cNbZspec))
            MODUSCaleTC_scen[:cNbcalzonage, :cNbcalzonage] = CALEscen_TC
            MODUSCaleTC_scen[cNbcalzonage:cNbZone + cNbZspec, :] = ModusTC_VS_scen[cNbcalzonage:cNbZone + cNbZspec, :]
            MODUSCaleTC_scen[:, cNbcalzonage:cNbZone + cNbZspec] = ModusTC_VS_scen[:, cNbcalzonage:cNbZone + cNbZspec]

        elif id == 1:
            # -- cas où on effectue le report de calage sans analyse des évolutions
            MODUSTC_actuel = pd.Series(MODUSTC_actuel)

            MODUSCaleTC_actuel = MODUSCaleTC_actuel.loc[
                (MODUSCaleTC_actuel['ZONEO'] <= cNbcalzonage) & (MODUSCaleTC_actuel['ZONED'] <= cNbcalzonage), 'FLUX']
            MODUSCaleTC_actuel.reset_index(inplace=True, drop=True)

            # -- paramètre K de "dilatation" de la matrice MODUS
            R1_TC = np.ones(cNbcalzonage ** 2)
            POS_TC = MODUSTC_actuel >= 0.001

            R1_TC[POS_TC] = MODUSCaleTC_actuel[POS_TC]/MODUSTC_actuel[POS_TC]
            K_TC = np.minimum(R1_TC, seuilh)
            # égale à la valeur de "cSeuilh"
            K_TC = np.maximum(K_TC, seuilb)
            # égale à la valeur de "cSeuilb"

            #   -- paramètre D d'ajout des flux manquants,
            #   On prend le maximum de D_TC et 0 pour garantir que D ne fait qu'ajouter des flux, sans en retirer
            D_TC = np.maximum(MODUSCaleTC_actuel - K_TC * MODUSTC_actuel, 0)

            #   -- ajustement pour recréer à la bonne dimension et conserver les flux intrazonaux : diag(K) = 1 et diag(D) = 0
            K_TC = K_TC.reshape((cNbcalzonage, cNbcalzonage))

            D_TC = D_TC.to_numpy().reshape((cNbcalzonage, cNbcalzonage))

            if cNbcalzonage == cNbZone:
                K_TC = np.concatenate([K_TC, np.ones((cNbZone, cNbZspec))], axis=1)
                K_TC = np.concatenate([K_TC, np.ones((cNbZspec, cNbZone + cNbZspec))], axis=0)

                D_TC = np.concatenate([D_TC, np.zeros((cNbZone, cNbZspec))], axis=1)
                D_TC = np.concatenate([D_TC, np.zeros((cNbZspec, cNbZone + cNbZspec))], axis=0)

        else:    # * -- cas où on n'effectue pas le report de calage *
            K_TC = np.ones((cNbZone + cNbZspec, cNbZone + cNbZspec))
            D_TC = np.zeros((cNbZone + cNbZspec, cNbZone + cNbZspec))

        #   - b. Report de calage : CALE(scen) = K.MODUS(scen) + D
        if id < 2:
            MODUSCaleTC_scen = K_TC * ModusTC_VS_scen + D_TC
        dbfile = open(f'{dir_dataTemp}MODUSCaleTC_{H}_scen', 'wb')
        pkl.dump(MODUSCaleTC_scen, dbfile)
        dbfile.close()
        
        #  Reécris les résultats de calage sous forme d'un DataFrame de pandas
        MODUSCaleTC_df = pd.concat([pd.DataFrame(ODvide_func(cNbZone)),
                                    pd.DataFrame(MODUSCaleTC_scen[:cNbZone, :cNbZone].reshape(cNbZone ** 2))], axis=1)
        MODUSCaleTC_df.columns = ['ZONEO', 'ZONED', 'FLUX']
        dbfile = open(f'{dir_dataTemp}MODUSCaleTC_df_{H}_scen', 'wb')
        pkl.dump(MODUSCaleTC_df, dbfile)
        dbfile.close()

# Fonction de regroupement des étapes

def report_calage(idTC, idVP):
    if PPM == 1:
        ajout_evol('TC', 'PPM', idTC, cSeuilh, cSeuilb)
        ajout_evol('VP', 'PPM', idVP, cSeuilh, cSeuilb)
    if PCJ == 1:
        ajout_evol('TC', 'PCJ', idTC, cSeuilh, cSeuilb)
        ajout_evol('VP', 'PCJ', idVP, cSeuilh, cSeuilb)
    if PPS == 1:
        ajout_evol('TC', 'PPS', idTC, cSeuilh, cSeuilb)
        ajout_evol('VP', 'PPS', idVP, cSeuilh, cSeuilb)

if __name__ == '__main__':
    # traitementVP('PPM', 'scen', 'PPM')
    # AjoutMode_Gare('PPM', 'scen', 'VP')
    # traitementTC('PPS', 'scen', 'PPS')
    # finalise('actuel')
    # finalise('scen')
    from Data.A_CstesModus import cSeuilh, cSeuilb
    ajout_evol('TC', 'PPM', idTC, cSeuilh, cSeuilb)
    ajout_evol('VP', 'PPM', idVP, cSeuilh, cSeuilb)
    # traitementVP('PPS', 'scen', 'PPS')
    dbfile = open('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python'
                              '\\Other_files\\with_TTV_gen_no_dist\\test_calage\\MODUSCaleUVP_PPM_scen', 'rb')
    test_calUVP = pkl.load(dbfile)
    dbfile = open('C:\\Users\\mwendwa.kiko\\Documents\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python'
                  '\\Other_files\\with_TTV_gen_no_dist\\MODUSCaleUVP_PPM_scen', 'rb')
    real_calUVP = pkl.load(dbfile)
    diff = (test_calUVP - real_calUVP).sum().sum()
    assert diff == 0