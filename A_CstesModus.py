'''
FICHIER DE CONSTANTES DE MODUS 3
Auteur: Guillaume Tremblin
Transcription en python: Mwendwa Kiko.
Date: 30 septembre 2021
'''

# Modules de Python nécessaires à ce projet.
from collections import namedtuple
import os

import CstesStruct

# Variables qui sous SAS étaient dans le module 0_CstesCalibr, séction II, III

# MACROVARIABLES GÉNÉRALES
# 1. Caractéristiques géographique

cNbZone = 1289      # nombre de zones interne Idf
cNbDpt = 8          # nombre de départements : DPRT
cNbCour = 3         # nombre de couronnes : COUR
cNbClacc = 6        # nombre de classes d'accessibilité TC : CLACC


# 2. Désagrégation
cNbMotif = 22       # nombre de motifs à la génération
cNbMotifD = 14      # nombre de motifs à la distribution
cNbMotifC = 11      # nombre de motifs au choix modal
cNbCat = 2          # nombre de catégories dans la désagrégation
cNbTot = cNbMotif*cNbCat        # nombre total de types de déplacements
cNbTot_D = cNbMotifD*cNbCat     # nombre total de types de déplacements
cNbTot_C = cNbMotifC*cNbCat     # nombre total de types de déplacements

#Niv = DPRT      # niveau géographique (avec le nom utilisé dans la table calibr.zone) pour la désagrégation
#NivO = ORDPRT   # niveau géographique de l'EGT pour la désagrégation à l'origine
#NivD = DESTDPRT     # niveau géographique de l'EGT pour la désagrégation à la destination
cNbNiv = cNbDpt     # nombre d'éléments dans le niveau géographique de l'EGT pour la désagrégation





# CARACTÉRISTIQUES DU CALIBRAGE
# 0. Variables diverses
cNbClasse = 8   # nombre de classes de portée
Classe1 = 0.75  # seuil max de la classe 1 en km
Classe2 = 1.25  # seuil max de la classe 2 en km
Classe3 = 2.0   # seuil max de la classe 3 en km
Classe4 = 3.5   # seuil max de la classe 4 en km
Classe5 = 6.0   # seuil max de la classe 5 en km
Classe6 = 9.0   # seuil max de la classe 6 en km
Classe7 = 15.0  # seuil max de la classe 7 en km


VARGEN = ['PTOT', 'PACT', 'PACTHQ', 'PACTAQ', 'RETR', 'SCOLSUP','SCOLSEC', 'SCOLPRIM','PSCOL', 'CHOM', 'PNACTA', 'PNACTACHO',
          'PINACT', 'ETOT', 'EMPHQ', 'EMPAQ', 'EMPCOM', 'EMPLOI', 'EMPACH', 'SUP_LE', 'SEC_LE', 'PRIM_LE', 'SCOL_LE']



# !. Macrovariables de MODUS 3

# 0. Caractéristiques du zonage
# hors zones internes, cNbZones défini dans le fichier de constantes du calibrage

cNbZgare = 12   # nombre de zones gares
cNbZext = 34    # nombre de zones du cordon
cNbZspec = 4    # nombre de zones spécifiques externes
cNbZtot = cNbZspec+cNbZext      # nombre total de zones affectation VP
# Kiko cNbZtot = %eval(&cNbZone+&cNbZspec+&cNbZext) Problème: version originelle, mais c'est quoi cNbZone?

# 1. Horizons considérés
actuel = 2012   # année de la situation de calage du modèle
scen = 2022     # année de la situation de scénario > actuel
caleVP = 2012
caleTC = 2012

# 2. Périodes horaires simulées
PPM = 1     # exécution ou non de la simulation en PPM
PCJ = 0     # exécution ou non de la simulation en PCJ
PPS = 1     # exécution ou non de la simulation en PPS

# 3. Méthode demande PL
# a. choix de la méthode
idPL = 2    # =0, 1, 2 ou 3 selon la méthode choisie parmi les quatre ci-dessous

# b. Méthodes
# -- méthode 0 : pas de prise en compte des PL dans l'affectation
# -- méthode 1 : projection des matrices de flux PL calées par période horaire selon la croissance du PIB
CroisPIB = 1.5      # % de croissance annuelle du PIB : 1.5%

# -- méthode 2 : utilisation d'une matrice flux PL journalière interne IdF et de cordons PL actuelle et projetée pour
# déterminer les évolutions par OD à appliquer aux matrices PL calées par période horaire définies dans la méthode 1

#-- méthode 3 : utilisation de matrices de flux PL projetées par période horaire

# 4. Paramètre du report de calage

idVP = 1    # identifiant d'exécution (=1) ou pas (=0) du report de calage VP
idTC = 1    # identifiant d'exécution (=1) ou pas (=0) du report de calage TC
k0 = 1.77   # seuil de croissance extreme avant prise en compte du taux de croissance annuel de la méthode de report de
# calage n°2
cSeuilh = 2 # borne de l'amplification multiplicative de la méthode de report de calage n°1
cSeuilb = 0.25  # borne de la réduction multiplicative de la méthode de report de calage n°1
# calzonage = Zone  C'est quoi zone?


# 5. Bouclage
idBcl = 1       # identifiant d'exécution du bouclage sur la distribution (=1), le choix modal (=2), le choix modal
# restreint aux modes motorisés (=3), le choix modal restreint aux modes véhiculés (=4) ou pas du tout (=0)
cConv_M = 50    # critère de convergence du bouclage en HPM (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cConv_C = 50    # critère de convergence du bouclage en HC (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cConv_S = 50    # critère de convergence du bouclage en HPS (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cNbBcl = 10     # nombre maximum d'itérations lors du bouclage - doit être >1
cParTpsBcl = 0.5  # paramètre du bouclage pour la pondération des temps des itérations n-1 et n
cParMatBcl = 0.5    # paramètre du bouclage pour la pondération des matrices des itérations n-1 et n

# 6. Vecteurs Spécifiques
# a. identifiant d'éxécution de l'implémentation des vecteurs spécifiques
IdVsVp = 1      # identifiant d'implémentation (=1) ou pas (=0) des vecteurs spécifiques VP
IdVsTc = 1      # identifiant d'implémentation (=1) ou pas (=0) des vecteurs spécifiques TC
IdcorADP = 1    # identifiant d'implémentation (=1) ou pas (=0) des corrections de volume UVP sur base des études
# d'impact d'ADP sur T4
IdmethodeVSTC = 2   # méthode de calcul des VS TC : basée sur le choix modal de Modus (=1) ou basée sur la
# génération/distribution de Modus (=2)

# b. Numérotation des zones spécifiques
cZEmpCDG = 1290     # Zone spécifique associée aux emplois de la plateforme de Roissy-CDG
cZVoyCDG = 1291     # Zone spécifique associée aux voyageurs de la plateforme de Roissy-CDG
cZEmpOrly = 1292    # Zone spécifique associée aux emplois de la plateforme d'Orly
cZVoyOrly = 1293    # Zone spécifique associée aux voyageurs de la plateforme d'Orly
ZoneCDG = (245, 995, 1249)      # Liste des zones CDG
ZoneOrly = (679, 1078)      # Liste des zones Orly

# 7. Vecteurs Gares
idVGTC = 1  # Implémentation ou non des vecteurs voyageurs TC émis et attiré par les gares
idVGVP = 0  # Implémentation ou non des vecteurs voyageurs VP émis et attiré par les gares

# 8. Lecture fichiers VISUM TempsM.csv, TempsC.csv et TempsS.csv
deb = 32    # ligne de début= 32 si Temps seul sans péage; =33 si Temps et Peage
fin = deb + cNbZtot * cNbZtot - 1   # ligne de fin= deb+dimension de la matrice MODUS-1

Path_sep = namedtuple('Path_sep', 'path sep')  # Un namedtuple de la localisation et le type de séparateur à employer
# pour la lecture des fichiers .txt et .csv
dir_dataScen = CstesStruct.dir_dataScen
dir_dataAct = CstesStruct.dir_dataAct
dir_dataRef = CstesStruct.dir_dataRef

# 9. Télétravail
idTTV = 0   # 1 = activation du module télétravail en scénario, 0 sinon
jourTTV = 0.3    # part moyenne du temps de travail réalisée en télétravail (nb jour télétravaillé / nb jour travaillé)
partTTV = 0.75   # part des emplois télétravaillables occupées par des télétravailleurs
tauxTTVHQ = 0.85     # part des emplois HQ télétravaillables : 0.85 selon DADDT 2020
tauxTTVAQact = 0.228    # part des actifs AQ occupant un emploi télétravaillable : 0.228 selon DADDT 2020
tauxTTVAQemp = 0.228     # part des emplois AQ télétravaillables : 0.228 selon DADDT 2020
varJTTVpro = 0.07       # ratio de mobilité professionnelle un jour télétravaillé : 0.07 selon ADEME 2020
varJLTHpro = 1.00       # ratio de mobilité professionnelle un jour en lieu de travail habituel : 1.00 selon ADEME 2020
varJTTVacc = 1.00      # ratio de mobilité accompagnement un jour télétravaillé : 0.55 selon ADEME 2020, 1.00 si inactif
varJLTHacc = 1.00      # ratio de mobilité accompagnement un jour en lieu de travail habituel : 1.13 selon ADEME 2020,
# 1.00 si inactif
varJTTVaut = 1.00   # ratio de mobilité autres un jour télétravaillé : 0.43 selon ADEME 2020, 1.00 si inactif
varJLTHaut = 1.00  # ratio de mobilité autres un jour en lieu de travail habituel :
# 1.16 selon ADEME 2020, 1.00 si inactif
tauxTTVAQ = Path_sep(os.path.join(dir_dataScen, 'tauxTTVAQ.txt'), '\t')


#  Kiko do I import tauxTTVAQ here or in the file where it's used.

# 10. Vélo

idvelo = 0
intcy = 0.7
capvelib = 1

# 11. Croissance du coût d'usage de la voiture

idcoutvp = 1    # 1 = activation de l'augmentation du coût vp, 0 sinon
croiscarb = 2   # pourcentage de croissance annuelle du coût des carburants en € constant = 2%/an entre 2015 et 2030
croisentr = 1   # pourcentage de croissance annuelle du coût d'entretien des VP en € constant = 1%/an entre 2015 et 2030
croispeag = 0   # pourcentage de croissance annuelle du coût des péages des VP en € constant
croiscoutVP = (1 + (scen-actuel)*(croiscarb*0.38+croisentr*0.53+croispeag*0.09)/100)    # facteur de croissance du coût
# km des VP entre l'horizon de calage et le scénario en € constant

# II. FICHIERS D'INPUT

# Ici il y a des fichiers .ver, mais je ne savais pas comment les lire sous python.

Donnees_Res = {}    # Un dictionnaire pour contenir les données de réseau (fichiers .ver)

Donnees_Res[f'VersionM{scen}'] = os.path.join(dir_dataScen, '2019', '210219_ReseauVPv4.6_GV_GT_lambert93_PPM2020.ver')
# Version du scénario étudié
Donnees_Res[f'VersionC{scen}'] = os.path.join(dir_dataScen, '2019', '210219_ReseauVPv4.6_GV_GT_lambert93_PPS2020.ver')
# Version du scénario étudié
Donnees_Res[f'VersionS{scen}'] = os.path.join(dir_dataScen, '2019', '210219_ReseauVPv4.6_GV_GT_lambert93_PPS2020.ver')
# Version du scénario étudié





# Kiko Il manque ce fichier.
Par_affect = os.path.join(dir_dataScen, 'Par_affect_Modus3.1.xml')


Donnees_Zonales = {} # Dictionnaire de données zonales. Un dictionnaire a été choisi pour repliquer plus facileent
# le comportement des macro-variables de SAS, qui n'existe pas en python. 


Donnees_Zonales[f'OS{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191220_PE_RP2012_corRoissy.txt'), '\t')
Donnees_Zonales[f'Surf{actuel}'] = Path_sep(os.path.join(dir_dataRef, '080827_SURFACES.txt'), '\t')
Donnees_Zonales[f'CTSTAT{actuel}'] = Path_sep(os.path.join(dir_dataAct, '180406_CSTAT_2012.txt'), '\t')
Donnees_Zonales[f'VELIB{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'Calcul_CapaVelib_ZoneModus.csv'), ';')
Donnees_Zonales[f'AccessTC{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'AccessTC.txt'), '\t')


# b. horizon scénario

Donnees_Zonales[f'OS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2022', '210427_OS2022h.txt'), sep ='\t')
# Kiko The file above could not be found.
Donnees_Zonales[f'Surf{scen}'] = Path_sep(os.path.join(dir_dataRef, '080827_SURFACES.txt'), sep ='\t')
# Kiko The file above could not be found.
Donnees_Zonales[f'Surf{scen}'] = Path_sep(os.path.join(dir_dataScen, '080827_SURFACES.txt'), '\t')
Donnees_Zonales[f'CTSTAT{scen}'] = Path_sep(os.path.join(dir_dataScen, '180406_CSTAT_2012.txt'), '\t')
Donnees_Zonales[f'VELIB{scen}'] = Path_sep(os.path.join(dir_dataScen, 'Calcul_CapaVelib_ZoneModus.csv'), ';')
Donnees_Zonales[f'AccessTC{scen}'] = Path_sep(os.path.join(dir_dataScen, 'AccessTC.txt'), '\t')


# 3. Données interzonales

# a. horizon actuel
Donnees_Interz = {}

Donnees_Interz[f'tps_TC_M{actuel}'] = Path_sep(os.path.join(dir_dataAct, '20191218_TTC2012_HPM_reseau2012v14.txt'), '\t')
# temps TC actuel en PPM
Donnees_Interz[f'tps_TC_C{actuel}'] = Path_sep(os.path.join(dir_dataAct, '20191219_TTC2012_HC_reseau2012v14.txt'), '\t')
# temps TC actuel en PCJ
Donnees_Interz[f'tps_TC_S{actuel}'] = Path_sep(os.path.join(dir_dataAct, '20191218_TTC2012_HPS_reseau2012v14.txt'), '\t')
# temps TC actuel en PPS

Donnees_Interz[f'tps_VP_M{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPM_2012.txt'), '\t')
# temps VP actuel PPM
Donnees_Interz[f'tps_VP_C{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPM_2012.txt'), '\t')
# temps VP actuel PCJ
Donnees_Interz[f'tps_VP_S{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPS_2012.txt'), '\t')
# temps VP actuel PPS
Donnees_Interz[f'dist_vol{actuel}'] = Path_sep(os.path.join(dir_dataRef, '090721_DVOL_km.txt'), '\t')
# distance à vol d'oiseau actuelle
# Kiko - Lequel des trois fichiers portant ce nom est-ce que je suis censé utilisé
Donnees_Interz[f'carte_o{actuel}'] = Path_sep(os.path.join(dir_dataRef, '06JAN2020_CoutTC_MOTIF_Distancetotale.txt'), '\t')
# coût TC moyen par Motif et OD en actuel
Donnees_Interz[f'couttc{actuel}'] = Path_sep(os.path.join(dir_dataRef, '06JAN2020_CoutTC_ABO_TK_2012.txt'), '\t')

# - b. horizon scenario
Donnees_Interz[f'tps_TC_M{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                                          '20201216_GTFS_prospectif_v4_SC2019_HPM.txt'), '\t')
# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PPM
# Kiko - Il manque ce fichier.
Donnees_Interz[f'tps_TC_C{scen}'] = Path_sep(os.path.join(dir_dataScen,
                                       'GTFS_20170111_aff_v7_9_coeff2tiers_v2_importG_aff20190424HC1016_TTC.txt'), '\t')
# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PCJ
Donnees_Interz[f'tps_TC_S{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                        '20201216_GTFS_prospectif_v4_SC2019_HPS.txt'), '\t')
# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PPS
Donnees_Interz[f'tps_TC_MBclCM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                                                '20201216_GTFS_prospectif_v4_SC2019_HPM.txt'), '\t')
# temps TC scénario étudié utilisé pour le bouclage sur le choix modal, à partir de la distribution obtenue à partir
# du temps TC scénario tendanciel en PPM
Donnees_Interz[f'tps_TC_SBclCM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                                               '20201216_GTFS_prospectif_v4_SC2019_HPS.txt') , '\t')
# temps TC scénario étudié utilisé pour le bouclage sur le choix modal, à partir de la distribution obtenue à partir
# du temps TC scénario tendanciel en PPS
Donnees_Interz[f'tps_VP_M{scen}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPM_2012.txt'), '\t')
# temps VP scénario tendanciel PPM
Donnees_Interz[f'tps_VP_C{scen}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PCJ_2012.txt'), '\t')
# temps VP scénario tendanciel PCJ
Donnees_Interz[f'tps_VP_S{scen}'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPS_2012.txt'), '\t')
# temps VP scénario tendanciel PPS

Donnees_Interz[f'dist_vol{scen}'] = Path_sep(os.path.join(dir_dataRef, '090721_DVOL_km.txt'), '\t')
# distance à vol d'oiseau scénario

Donnees_Interz[f'carte_o{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                                         '10FEB2021_CoutTC2019_MOTIF_Distancetotale.txt'), '\t')
# coût TC moyen par Motif et OD en scénario

Donnees_Interz[f'couttc{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019',
                                                         '10FEB2021_CoutTC_ABO_TK_2019.txt'), '\t')
# coût TC par OD en scénario


# 4. Données de flux

# a. Matrices calées

Path_sep_skip = namedtuple('Path_sep', 'path sep skip')  # Un namedtuple de la localisation et le type de
# séparateur à employer et le nombre de lignes à sauter

Mat_Calees = {}     # Un dictionnaire des matrices calées

Mat_Calees[f'CALETCM{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'Matrice_TC_PPM_calée_19-11-18.fma'), '\t', 8)
Mat_Calees[f'CALETCC{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'TC_PCJ_VG2012.fma'), '\t', 8)
Mat_Calees[f'CALETCS{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'Matrice_TC_PPS_calée_19-11-18.fma'), '\t', 8)

Mat_Calees[f'CALEUVPM{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, '132_VL_PPM_calée_2012.fma'), '\t', 8)
Mat_Calees[f'CALEUVPC{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, 'UVP_PCJ2012_cordons_corriges.fma'), '\t', 13)
Mat_Calees[f'CALEUVPS{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, '133_VL_PPS_calée_2012.fma'), '\t', 8)


# - b. Matrices PL

# -- horizon actuel

Mat_Calees[f'CALEPLJ{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_JOUR_2009_FRETURB.fma'), '\t', 8)
# Matrice PL FretUrb journalière actuel
Mat_Calees[f'CALEPLM{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '121_Mat_PL_PPM_t-flow.fma'), '\t', 8)
# Matrice PL calée actuelle PPM
Mat_Calees[f'CALEPLC{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_PCJ2012_cordons_corriges.fma'), '\t', 8)
# Matrice PL calée actuelle PCJ à modifier une fois l'HC calée
Mat_Calees[f'CALEPLS{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '122_Mat_PL_PPS_t-flow.fma'), '\t', 8)
# Matrice PL calée actuelle PPS


# -- horizon scénario

Mat_Calees[f'CALEPLJ{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, '2019', 'PL_JOUR_2009_FRETURB.fma'), '\t', 13)
# Matrice PL FretUrb journalière scénario
Mat_Calees[f'CALEPLM{scen}'] = Path_sep_skip(os.path.join(dir_dataAct, '121_Mat_PL_PPM_t-flow.fma'), '\t', 13)
# Matrice PL scénario PPM
Mat_Calees[f'CALEPLC{scen}'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_PCJ2012_cordons_corriges.fma'), '\t', 13)
# Matrice PL scénario PCJ à modifier une fois l'HC calée
Mat_Calees[f'CALEPLS{scen}'] = Path_sep_skip(os.path.join(dir_dataAct, '122_Mat_PL_PPS_t-flow.fma'), '\t', 13)
# Matrice PL scénario PPS


# - c. cordons routiers

# -- horizon actuel

Mat_Calees[f'CORDVPM{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPM.fma'), '\t', 8)
Mat_Calees[f'CORDVPC{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HC.fma'), '\t', 8)
Mat_Calees[f'CORDVPS{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPS.fma'), '\t', 8)

Mat_Calees[f'CORDPLM{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HPM.fma'), '\t', 8)
Mat_Calees[f'CORDPLC{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HC.fma'), '\t', 8)
Mat_Calees[f'CORDPLS{actuel}'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HPS.fma'), '\t', 8)


# -- horizon scénario

Mat_Calees[f'CORDVPM{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, '2019', '15.02.2021_cordon_VP_HPM_2017.fma'),
                                               '\t', 8)
# Cordon VP scénario PPM en veh/h
Mat_Calees[f'CORDVPC{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, 'cordon_VP_HC_2030.fma'), '\t', 8)
# Cordon VP scénario PCJ en veh/h
Mat_Calees[f'CORDVPS{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, '2019', '15.02.2021_cordon_VP_HPS_2017.fma'),
                                             '\t', 8)
# Cordon VP scénario PPS en veh/h

Mat_Calees[f'CORDPLM{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, '2019', '15.02.2021_cordon_PL_HPM_2017.fma'),
                                             '\t', 8)
# Cordon PL scénario PPM en veh/h
Mat_Calees[f'CORDPLC{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, 'cordon_PL_HC_2030.fma'), '\t', 8)
# Cordon PL scénario PCJ en veh/h
Mat_Calees[f'CORDPLS{scen}'] = Path_sep_skip(os.path.join(dir_dataScen, '2019', '15.02.2021_cordon_PL_HPS_2017.fma'),
                                             '\t', 8)
# Cordon PL scénario PPS en veh/h


# - d. vecteurs spécifiques

Vect_spec = {}  # Un dictionnaire des flux des vecteurs spécifiques

# -- horizon actuel

Vect_spec[f'VSM{actuel}'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hpm.txt'), '\t')
# Vecteur spécifique VP actuel PPM en veh/h
Vect_spec[f'VSC{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191008_VectSpec2010_hc.txt'), '\t')
# Vecteur spécifique VP actuel PCJ en veh/h
Vect_spec[f'VSS{actuel}'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hps.txt'), '\t')
# Vecteur spécifique VP actuel PPS en veh/h

Vect_spec[f'PoidsVS{actuel}'] = Path_sep(os.path.join(dir_dataAct, '191008_Poids_2010.txt'), '\t')
# Poids de chaque zones Specifiques

EmpCDGactuel = 85.0     # Nombre de milliers d'emplois sur la plateforme CDG en actuel
PaxCDGactuel = 61.6     # Nombre de millions de passagers annuels transportés à CDG en actuel

Vect_spec[f'VSTCCDGM{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PPM en voy/h
Vect_spec[f'VSTCCDGC{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HC.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PCJ en voy/h
Vect_spec[f'VSTCCDGS{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PPS en voy/h

EmpORLactuel = 26.2
PaxORLactuel = 27.2

Vect_spec[f'VSTCORLYM{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTCORLYC{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HC.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PCJ en voy/h
Vect_spec[f'VSTCORLYS{actuel}'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h


# -- horizon scénario

Vect_spec[f'VSM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019', '140117_VectSpec2020_hpm.txt'), '\t')
Vect_spec[f'VSC{scen}'] = Path_sep(os.path.join(dir_dataScen, '191023_VectSpec2030_hc.txt'), '\t')
Vect_spec[f'VSS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019', '140117_VectSpec2020_hps.txt'), '\t')

Vect_spec[f'PoidsVS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2025', '210216_Poids_2025.txt'), '\t')

EmpCDGscen = 92.7   # Nombre de milliers d'emplois sur la plateforme CDG en scénario
# 2012=85.0 ; 2018=92.7 ; 2024=107.3 ; 2028sansT4=110.8 ; 2028avecT4=128.3 ; 2037sansT4=112.9 ; 2037avecT4=165.0
PaxCDGscen = 76.2   # Nombre de millions de passagers annuels transportés à CDG en scénario
# 2012=61.6 ; 2018=70.8 ; 2019=76.2 ; 2024=85.4 ; 2028sansT4=88.9 ; 2028avecT4=95.7 ; 2037sansT4=91.0 ; 2037avecT4=128.8

Vect_spec[f'VSTCCDGM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTCCDGC{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HC.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PCJ en voy/h
Vect_spec[f'VSTCCDGS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h

EmpORLscen = 29.0   # Nombre de milliers d'emplois sur la plateforme ORLY en scénario
# 2012=26.2 ; 2019=29.0? ; 2028=33.0
PaxORLscen = 31.9   # Nombre de millions de passagers annuels transportés à ORLY en scénario
# 2012=27.2 ; 2018=33.1 ; 2019=31.9 ; 2028=40.0

Vect_spec[f'VSTCORLYM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTCORLYC{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HC.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PCJ en voy/h
Vect_spec[f'VSTCORLYS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h


# - e. vecteurs emission et attraction voyageurs TC des gares

Vect_gare = {}  # Un dictionnaire des flux des gares.

# -- horizon actuel
Vect_gare[f'VGTCM{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPM.txt'), '\t')
Vect_spec[f'VGTCC{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PCJ.txt'), '\t')
Vect_spec[f'VGTCS{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPS.txt'), '\t')

# -- horizon scénario

Vect_spec[f'VGTCM{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PPM.txt'), '\t')
Vect_spec[f'VGTCC{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PCJ.txt'), '\t')
Vect_spec[f'VGTCS{scen}'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PPS.txt'), '\t')


# - f. vecteurs emission et attraction voyageurs VP des gares

# -- horizon actuel
Vect_spec[f'VGVPM{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPM.txt'), '\t')    # non activé
Vect_spec[f'VGVPC{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPM.txt'), '\t')    # non activé
Vect_spec[f'VGVPS{actuel}'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPS.txt'), '\t')    # non activé

# -- horizon scénario
Vect_spec[f'VGVPM{scen}'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPM.txt'), '\t')    # non activé
Vect_spec[f'VGVPC{scen}'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPM.txt'), '\t')    # non activé
Vect_spec[f'VGVPS{scen}'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPS.txt'), '\t')    # non activé








































































