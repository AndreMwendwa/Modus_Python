'''
FICHIER DE CONSTANTES DE MODUS 3
Auteur: Guillaume Tremblin
Transcription en python: Mwendwa Kiko.
Date: 30 septembre 2021
'''

# Modules de Python nécessaires à ce projet².
from collections import namedtuple
from collections import defaultdict
import numpy as np
import pickle as pkl
import os

from Data import CstesStruct
from Data.CstesStruct import *
import yaml
import openpyxl
from pathlib import Path

yaml_file = open(f'{dir_modus_py}\\Data\\config_yml.yml', 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)


# Variables qui sous SAS étaient dans le module 0_CstesCalibr, séction II, III

# MACROVARIABLES GÉNÉRALES
# 1. Caractéristiques géographique

if yaml_content['cNbZone'] != -1:
    cNbZone = yaml_content['cNbZone']
else:
    cNbZone = 1289       # nombre de zones interne Idf
cNbDpt = 8          # nombre de départements : DPRT
cNbCour = 3         # nombre de couronnes : COUR
cNbClacc = 6        # nombre de classes d'accessibilité TC : CLACC
cNbClasse = 8       # nombre de classes de portée

# Les classes de portée pour le dessin des cartes dans le post-traitement.
classe1 = 0.75 #   seuil max de la classe 1 en km
classe2 = 1.25 #   seuil max de la classe 2 en km
classe3 = 2.0 #   seuil max de la classe 3 en km
classe4 = 3.5 #   seuil max de la classe 4 en km
classe5 = 6.0 #   seuil max de la classe 5 en km
classe6 = 9.0 #   seuil max de la classe 6 en km
classe7 = 15.0 #   seuil max de la classe 7 en km
tous_classes = [f'<{classe1}km', f'{classe1} - \n {classe2}km', f'{classe2} - \n {classe3}km',
                f'{classe3} - \n {classe4}km', f'{classe4} - \n {classe5}km', f'{classe5} - \n {classe6}km',
                f'{classe6} - \n {classe7}km', f'>{classe7}km']

# Les classes de portée pour l'attribution de taux d'autosolisme dans le fichier traitement.
classe_convvp1 = 2.0
classe_convvp2 = 9.0

Classe_dict = {}
# Classe_dict['Classe1'] = (0, 1.0)   # seuil max de la classe 1 en km
# Classe_dict['Classe2'] = (1.0, 2.0)  # seuil max de la classe 2 en km
# Classe_dict['Classe3'] = (2.0, 3.5)  # seuil max de la classe 3 en km
# Classe_dict['Classe4'] = (3.5, 6.0)  # seuil max de la classe 4 en km
# Classe_dict['Classe5'] = (6.0, 9.0)  # seuil max de la classe 5 en km
# Classe_dict['Classe6'] = (9.0, 1000)  # seuil max de la classe 6 en km
Classe_dict['Classe1'] = (0, 2.0)   # seuil max de la classe 1 en km
Classe_dict['Classe2'] = (2.0, 9.0)  # seuil max de la classe 2 en km
Classe_dict['Classe3'] = (9.0, 1000)  # seuil max de la classe 3 en km



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

cNbZext = yaml_content['cNbZext']       # nombre de zones du cordon
cNbZgare = yaml_content['cNbZgare']     # nombre de zones gares
cNbZspec = yaml_content['cNbZspec']     # nombre de zones spécifiques externes
# cNbZgare = 12   # nombre de zones gares
# cNbZext = 34    # nombre de zones du cordon
# cNbZspec = 4    # nombre de zones spécifiques externes
cNbZtot = cNbZone + cNbZspec + cNbZext      # nombre total de zones affectation VP
# Kiko cNbZtot = %eval(&cNbZone+&cNbZspec+&cNbZext) Problème: version originelle, mais c'est quoi cNbZone?
cNbZintsp = cNbZone + cNbZspec
# 1. Horizons considérés
actuel = yaml_content['actuel']     # année de la situation de calage du modèle
scen = yaml_content['scen']         # année de la situation de scénario > actuel
caleVP = yaml_content['caleVP']
caleTC = yaml_content['caleTC']
# actuel = 2012   # année de la situation de calage du modèle
# scen = 2030     # année de la situation de scénario > actuel
# caleVP = 2012
# caleTC = 2012

# 2. Périodes horaires simulées
PPM = yaml_content['PPM']       # exécution ou non de la simulation en PPM
PCJ = yaml_content['PCJ']       # exécution ou non de la simulation en PCJ
PPS = yaml_content['PPS']       # exécution ou non de la simulation en PPS
# PPM = 1     # exécution ou non de la simulation en PPM
# PCJ = 0     # exécution ou non de la simulation en PCJ
# PPS = 1     # exécution ou non de la simulation en PPS

# 3. Méthode demande PL
# a. choix de la méthode
idPL = yaml_content['idPL']     # =0, 1, 2 ou 3 selon la méthode choisie parmi les quatre ci-dessous
# idPL = 2    # =0, 1, 2 ou 3 selon la méthode choisie parmi les quatre ci-dessous

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
cNbcalzonage = cNbZone + cNbZspec  # zonage sur lequel appliqué le report de calage : cNbZone si zone interne IdF,
# cNbZtot si toutes les zones


# 5. Bouclage
# Maintenant dans le YML
if yaml_content['idBcl'] != -1:
    idBcl = yaml_content['idBcl']
else:
    idBcl = 0       # identifiant d'exécution du bouclage sur la distribution (=1), le choix modal (=2), le choix modal
# restreint aux modes motorisés (=3), le choix modal restreint aux modes véhiculés (=4) ou pas du tout (=0)
cConv_M = 50    # critère de convergence du bouclage en HPM (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cConv_C = 50    # critère de convergence du bouclage en HC (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cConv_S = 50    # critère de convergence du bouclage en HPS (ex : 100 pour le bouclage sur la dist, 30 pour le choix modal)
cNbBcl = 10     # nombre maximum d'itérations lors du bouclage - doit être >1
cParTpsBcl = 0.667  # paramètre du bouclage pour la pondération des temps des itérations n-1 et n
cParMatBcl = 0.667    # paramètre du bouclage pour la pondération des matrices des itérations n-1 et n

# 6. Vecteurs Spécifiques
# a. identifiant d'éxécution de l'implémentation des vecteurs spécifiques
idVSVP = 0      # identifiant d'implémentation (=1) ou pas (=0) des vecteurs spécifiques VP
idVSTC = 0      # identifiant d'implémentation (=1) ou pas (=0) des vecteurs spécifiques TC
idcorADP = 1    # identifiant d'implémentation (=1) ou pas (=0) des corrections de volume UVP sur base des études
# d'impact d'ADP sur T4


IdmethodeVSTC = 2   # méthode de calcul des VS TC : basée sur le choix modal de Modus (=1) ou basée sur la
# génération/distribution de Modus (=2)

# b. Numérotation des zones spécifiques
cZEmpCDG = 1290     # Zone spécifique associée aux emplois de la plateforme de Roissy-CDG
cZVoyCDG = 1291     # Zone spécifique associée aux voyageurs de la plateforme de Roissy-CDG
cZEmpORLY = 1292    # Zone spécifique associée aux emplois de la plateforme d'Orly
cZVoyORLY = 1293    # Zone spécifique associée aux voyageurs de la plateforme d'Orly
ZoneCDG = [245, 995, 1249]      # Liste des zones CDG
ZoneOrly = [679, 1078]      # Liste des zones Orly
ZoneADP = ZoneCDG + ZoneOrly
ZoneVoyADP = [cZVoyORLY, cZVoyCDG]
ZoneEmpADP = [cZEmpORLY, cZEmpCDG]

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
fact_reducn = 0.25   # A appliquer à la génération ainsi qu'à la distribution.
idTTV = 0   # 1 = activation du module télétravail en scénario, 0 sinon
jourTTV = 0.3 * fact_reducn    # part moyenne du temps de travail réalisée en télétravail (nb jour télétravaillé / nb jour travaillé)
partTTV = 0.75   # part des emplois télétravaillables occupées par des télétravailleurs
tauxTTVHQ = 0.85     # part des emplois HQ télétravaillables : 0.85 selon DADDT 2020
tauxTTVAQact = 0.228    # part des actifs AQ occupant un emploi télétravaillable : 0.228 selon DADDT 2020
tauxTTVAQemp = 0.228     # part des emplois AQ télétravaillables : 0.228 selon DADDT 2020
varJTTVpro = 0.07       # ratio de mobilité professionnelle un jour télétravaillé : 0.07 selon ADEME 2020
varJLTHpro = 1.00       # ratio de mobilité professionnelle un jour en lieu de travail habituel : 1.00 selon ADEME 2020
varJTTVacc = 1.00      # ratio de mobilité accompagnement un jour télétravaillé : 0.55 selon ADEME 2020, 1.00 si inactif
varJLTHacc = 1.3/3 * (jourTTV * fact_reducn) + 1      # ratio de mobilité accompagnement un jour en lieu de travail habituel : 1.13 selon ADEME 2020,
# # 1.00 si inactif
# varJLTHacc = 1.00
varJTTVaut = 1.00   # ratio de mobilité autres un jour télétravaillé : 0.43 selon ADEME 2020, 1.00 si inactif
varJLTHaut = 1.6/3 * (jourTTV * fact_reducn) + 1  # ratio de mobilité autres un jour en lieu de travail habituel :
# 1.16 selon ADEME 2020, 1.00 si inactif
# varJLTHaut = 1.00
tauxTTVAQ = Path_sep(os.path.join(dir_dataScen, 'tauxTTVAQ.txt'), '\t')

# 9b. Télétravail_distribution
# Module introduit pour prendre en compte le télétravail au niveau de la distribution.
idTTVdist = 0
# ACTacc = 1.2      # Paramètre de modification du paramètre de distribution pour le catégorie-motif actif-accompagnement
# EMPacc = 1      # Paramètre de modification du paramètre de distribution pour le catégorie-motif emploi-accompagnement
# HQPro = 1       # Paramètre de modification du paramètre de distribution pour le catégorie-motif emploi HQ-professionnel
# AQPro = 1       # Paramètre de modification du paramètre de distribution pour le catégorie-motif emploi AQ-professionnel
# ACTaut = 1       # Paramètre de modification du paramètre de distribution pour le catégorie-motif actifs-autres

aPPM = -0.33
aPPS = -0.285
# pctTTVscen = 1  #  Pour calibrer les alphas seulement
pctTTVscen = (partTTV * tauxTTVHQ * 0.289 + partTTV * tauxTTVAQemp * 0.711) * jourTTV * fact_reducn  # Pourcentage des HQ, AQ 0.289,
# 0.711 obtenus à partir
# du fichier des P + E en faisant EMHQ/ETOT et EMAQ/ETOT
pctTTVactuel = 0

factPPM = (1 + aPPM * (pctTTVscen - pctTTVactuel))
factPPS = (1 + aPPS * (pctTTVscen - pctTTVactuel))

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

# Donnees_Res[f'Version_PPM_scen'] = os.path.join(dir_dataScen, '2019', '210219_ReseauVPv4.6_GV_GT_lambert93_PPM2020.ver')
# Donnees_Res[f'Version_PPM_scen'] = os.path.join(dir_dataScen, '210219_ReseauVPv4.6_PPM2030.ver')
Donnees_Res[f'Version_PPM_scen'] = os.path.join(dir_dataScen, '210219_ReseauVPv4.6_PPM2030_edited.ver')

# Version du scénario étudié
Donnees_Res[f'Version_PCJ_scen'] = os.path.join(dir_dataScen, '2019', '210219_ReseauVPv4.6_GV_GT_lambert93_PPS2020.ver')
# Version du scénario étudié
# Donnees_Res[f'Version_PPS_scen'] = os.path.join(dir_dataScen, '210219_ReseauVPv4.6_PPS2030.ver')
Donnees_Res[f'Version_PPS_scen'] = os.path.join(dir_dataScen, '210219_ReseauVPv4.6_PPS2030_edited.ver')

# Version du scénario étudié





# Kiko Il manque ce fichier.
Par_affect = os.path.join(dir_dataScen, 'Par_affect_Modus3.1.xml')


Donnees_Zonales = {} # Dictionnaire de données zonales. Un dictionnaire a été choisi pour repliquer plus facileent
# le comportement des macro-variables de SAS, qui n'existe pas en python. 


Donnees_Zonales['OS_actuel'] = Path_sep(os.path.join(dir_dataAct, '191220_PE_RP2012_corRoissy.txt'), '\t')
Donnees_Zonales['Surf_actuel'] = Path_sep(os.path.join(dir_dataRef, '080827_SURFACES.txt'), '\t')
Donnees_Zonales['CTSTAT_actuel'] = Path_sep(os.path.join(dir_dataAct, '180406_CSTAT_2012.txt'), '\t')
Donnees_Zonales['VELIB_actuel'] = Path_sep(os.path.join(dir_dataAct, 'Calcul_CapaVelib_ZoneModus.csv'), ';')
Donnees_Zonales['AccessTC_actuel'] = Path_sep(os.path.join(dir_dataAct, 'AccessTC.txt'), '\t')


# b. horizon scénario

Donnees_Zonales['OS_scen'] = Path_sep(os.path.join(dir_dataScen, '210427_OS2022h.txt')
                                      , sep ='\t')
Donnees_Zonales['Surf_scen'] = Path_sep(os.path.join(dir_dataRef, '080827_SURFACES.txt'), sep ='\t')
Donnees_Zonales['CTSTAT_scen'] = Path_sep(os.path.join(dir_dataScen, '180406_CSTAT_2012.txt'), '\t')
Donnees_Zonales['VELIB_scen'] = Path_sep(os.path.join(dir_dataScen, 'Calcul_CapaVelib_ZoneModus.csv'), ';')
Donnees_Zonales['AccessTC_scen'] = Path_sep(os.path.join(dir_dataScen, 'AccessTC.txt'), '\t')


# 3. Données interzonales

# a. horizon actuel
Donnees_Interz = {}

Donnees_Interz['tps_TC_M_actuel'] = Path_sep(os.path.join(dir_dataAct, '20191218_TTC2012_HPM_reseau2012v14.txt'), '\t')
# temps TC actuel en PPM
Donnees_Interz['tps_TC_C_actuel'] = Path_sep(os.path.join(dir_dataAct, '20191219_TTC2012_HC_reseau2012v14.txt'), '\t')
# temps TC actuel en PCJ
Donnees_Interz['tps_TC_S_actuel'] = Path_sep(os.path.join(dir_dataAct, '20191218_TTC2012_HPS_reseau2012v14.txt'), '\t')
# temps TC actuel en PPS

Donnees_Interz['tps_VP_M_actuel'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPM_2012.txt'), '\t')
# temps VP actuel PPM
Donnees_Interz['tps_VP_C_actuel'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PCJ_2012.txt'), '\t')
# temps VP actuel PCJ
Donnees_Interz['tps_VP_S_actuel'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPS_2012.txt'), '\t')
# temps VP actuel PPS
Donnees_Interz['dist_vol_actuel'] = Path_sep(os.path.join(dir_dataRef, '090721_DVOL_km.txt'), '\t')
# distance à vol d'oiseau actuelle
# Kiko - Lequel des trois ichiers portant ce nom est-ce que je suis censé utilisé
Donnees_Interz['carte_o_actuel'] = Path_sep(os.path.join(dir_dataRef, '06JAN2020_CoutTC_MOTI_Distancetotale.txt'), '\t')
# coût TC moyen par Moti et OD en actuel
Donnees_Interz['couttc_actuel'] = Path_sep(os.path.join(dir_dataRef, '06JAN2020_CoutTC_ABO_TK_2012.txt'), '\t')

# - b. horizon scenario
Donnees_Interz['tps_TC_M_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
                                                          '210331_Test75_HPM_2030avecGPE_L17sansT4.txt'), '\t')
# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PPM
# Kiko - Remplacement temporaire
# Donnees_Interz['tps_TC_C_scen'] = Path_sep(os.path.join(dir_dataScen,
#                                        'GTS_20170111_a_v7_9_coe2tiers_v2_importG_a20190424HC1016_TTC.txt'), '\t')
Donnees_Interz['tps_TC_C_scen'] = Path_sep(os.path.join(dir_dataAct, '20191219_TTC2012_HC_reseau2012v14.txt'), '\t')

# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PCJ
Donnees_Interz['tps_TC_S_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
                                        '210331_Test75_HPS_2030avecGPE_L17sansT4.txt'), '\t')
# temps TC scénario (tendanciel si bouclage sur CM) utilisé pour la distribution en PPS
Donnees_Interz['tps_TC_MBclCM_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
                                                                '210331_Test75_HPM_2030avecGPE_L17sansT4.txt'), '\t')
# temps TC scénario étudié utilisé pour le bouclage sur le choix modal, à partir de la distribution obtenue à partir
Donnees_Interz['tps_TC_CBclCM_scen'] = Path_sep(os.path.join(dir_dataScen,
                                    'GTFS_20170111_aff_v7_9_coeff2tiers_v2_importG_aff20190424HC1016_TTC.txt'), '\t')
# du temps TC scénario tendanciel en PPM
Donnees_Interz['tps_TC_SBclCM_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
                                                               '210331_Test75_HPS_2030avecGPE_L17sansT4.txt') , '\t')
# temps TC scénario étudié utilisé pour le bouclage sur le choix modal, à partir de la distribution obtenue à partir
# du temps TC scénario tendanciel en PPS
Donnees_Interz['tps_VP_M_scen'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPM_2012.txt'), '\t')
# temps VP scénario tendanciel PPM
Donnees_Interz['tps_VP_C_scen'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PCJ_2012.txt'), '\t')
# temps VP scénario tendanciel PCJ
Donnees_Interz['tps_VP_S_scen'] = Path_sep(os.path.join(dir_dataAct, '191220_TVP_PPS_2012.txt'), '\t')
# temps VP scénario tendanciel PPS

Donnees_Interz['dist_vol_scen'] = Path_sep(os.path.join(dir_dataRef, '090721_DVOL_km.txt'), '\t')
# distance à vol d'oiseau scénario

Donnees_Interz['carte_o_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
                                                         '11FEB2021_CoutTC2030_GPErer_MOTIF_Distancetotale.txt'), '\t')
# coût TC moyen par Moti et OD en scénario
Donnees_Interz['couttc_scen'] = Path_sep(os.path.join(dir_dataScen, '2030 - original',
                                                          '11FEB2021_CoutTC_ABO_TK_2030_GPErer.txt'), '\t')
# if yaml_content[f'cout_TC_{scen}'] != -1:
#     Donnees_Interz['couttc_scen'] = Path_sep(Path(yaml_content[f'cout_TC_{scen}']), '\t')
# else:
#     Donnees_Interz['couttc_scen'] = Path_sep(os.path.join(dir_dataScen, '2030',
#                                                           '11FEB2021_CoutTC_ABO_TK_2030_GPErer.txt'), '\t')

# coût TC par OD en scénario


# 4. Données de flux

# a. Matrices calées

Path_sep_skip = namedtuple('Path_sep', 'path sep skip')  # Un namedtuple de la localisation et le type de
# séparateur à employer et le nombre de lignes à sauter

Mat_Calees = {}     # Un dictionnaire des matrices calées

Mat_Calees[f'CALETC_PPM_{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'Matrice_TC_PPM_calée_19-11-18.fma'), '\s+', 8)
Mat_Calees[f'CALETC_PCJ_{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'TC_PCJ_VG2012.fma'), '\t', 8)
Mat_Calees[f'CALETC_PPS_{caleTC}'] = Path_sep_skip(os.path.join(dir_dataAct, 'Matrice_TC_PPS_calée_19-11-18.fma'), '\s+', 8)

Mat_Calees[f'CALEUVP_PPM_{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, '132_VL_PPM_calée_2012.fma'), '\s+', 8)
Mat_Calees[f'CALEUVP_PCJ_{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, 'UVP_PCJ2012_cordons_corriges.fma'), '\s+', 13)
Mat_Calees[f'CALEUVP_PPS_{caleVP}'] = Path_sep_skip(os.path.join(dir_dataAct, '133_VL_PPS_calée_2012.fma'), '\s+', 8)


# - b. Matrices PL

# -- horizon actuel

Mat_Calees[f'CALEPL_J_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_JOUR_2009_FRETURB.fma'), '\s+', 8)
# Matrice PL FretUrb journalière actuel
Mat_Calees[f'CALEPL_PPM_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '121_Mat_PL_PPM_t-flow.fma'), '\s+', 8)
# Matrice PL calée actuelle PPM
Mat_Calees[f'CALEPL_PCJ_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_PCJ2012_cordons_corriges.fma'), '\s+', 8)
# Matrice PL calée actuelle PCJ à modifier une fois l'HC calée
Mat_Calees[f'CALEPL_PPS_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '122_Mat_PL_PPS_t-flow.fma'), '\s+', 8)
# Matrice PL calée actuelle PPS


# -- horizon scénario

Mat_Calees[f'CALEPL_J_scen'] = Path_sep_skip(os.path.join(dir_dataScen, '2030', '15.02.2021_PL_INTERNE_2030.fma'), '\s+', 13)
# Mat_Calees[f'CALEPL_J_scen'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_JOUR_2009_FRETURB.fma'), '\s+', 8)
# Matrice PL FretUrb journalière scénario
Mat_Calees[f'CALEPL_PPM_scen'] = Path_sep_skip(os.path.join(dir_dataAct, '121_Mat_PL_PPM_t-flow.fma'), '\s+', 7)
# Matrice PL scénario PPM
Mat_Calees[f'CALEPL_PCJ_scen'] = Path_sep_skip(os.path.join(dir_dataAct, 'PL_PCJ2012_cordons_corriges.fma'), '\s+', 13)
# Matrice PL scénario PCJ à modifier une fois l'HC calée
Mat_Calees[f'CALEPL_PPS_scen'] = Path_sep_skip(os.path.join(dir_dataAct, '122_Mat_PL_PPS_t-flow.fma'), '\s+', 7)
# Matrice PL scénario PPS


# - c. cordons routiers

# -- horizon actuel

Mat_Calees[f'CORDVP_PPM_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPM.fma'), '\s+', 13)
Mat_Calees[f'CORDVP_PCJ_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HC.fma'), '\s+', 13)
Mat_Calees[f'CORDVP_PPS_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPS.fma'), '\s+', 13)

Mat_Calees[f'CORDPL_PPM_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HPM.fma'), '\s+', 13)
Mat_Calees[f'CORDPL_PCJ_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HC.fma'), '\s+', 13)
Mat_Calees[f'CORDPL_PPS_actuel'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_PL_HPS.fma'), '\s+', 13)


# -- horizon scénario

Mat_Calees[f'CORDVP_PPM_scen'] = Path_sep_skip(os.path.join(dir_dataScen, '2030', '15.02.2021_cordon_VP_HPM_2030.fma'),
                                               '\t', 8)
# Mat_Calees[f'CORDVP_PPM_scen'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPM.fma'), '\s+', 13)
# Cordon VP scénario PPM en veh/h
Mat_Calees[f'CORDVP_PCJ_scen'] = Path_sep_skip(os.path.join(dir_dataScen, 'cordon_VP_HC_2030.fma'), '\t', 8)
# Cordon VP scénario PCJ en veh/h
Mat_Calees[f'CORDVP_PPS_scen'] = Path_sep_skip(os.path.join(dir_dataScen, '2030', '15.02.2021_cordon_VP_HPS_2030.fma'),
                                             '\t', 8)
# Mat_Calees[f'CORDVP_PPS_scen'] = Path_sep_skip(os.path.join(dir_dataAct, '191021_cordon_VP_HPS.fma'), '\s+', 13)

# Cordon VP scénario PPS en veh/h

Mat_Calees[f'CORDPL_PPM_scen'] = Path_sep_skip(os.path.join(dir_dataScen, '2030', '15.02.2021_cordon_PL_HPM_2030.fma'),
                                             '\s+', 8)
# Cordon PL scénario PPM en veh/h
Mat_Calees[f'CORDPL_PCJ_scen'] = Path_sep_skip(os.path.join(dir_dataScen, 'cordon_PL_HC_2030.fma'), '\s+', 8)
# Cordon PL scénario PCJ en veh/h
Mat_Calees[f'CORDPL_PPS_scen'] = Path_sep_skip(os.path.join(dir_dataScen, '2030', '15.02.2021_cordon_PL_HPS_2030.fma'),
                                             '\s+', 8)
# Cordon PL scénario PPS en veh/h


# - d. vecteurs spécifiques

Vect_spec = {}  # Un dictionnaire des flux des vecteurs spécifiques

# -- horizon actuel

Vect_spec[f'VS_PPM_actuel'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hpm.txt'), '\t')
# Vecteur spécifique VP actuel PPM en veh/h
Vect_spec[f'VS_PCJ_actuel'] = Path_sep(os.path.join(dir_dataAct, '191008_VectSpec2010_hc.txt'), '\t')
# Vecteur spécifique VP actuel PCJ en veh/h
Vect_spec[f'VS_PPS_actuel'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hps.txt'), '\t')
# Vecteur spécifique VP actuel PPS en veh/h

Vect_spec[f'Poids_VS_actuel'] = Path_sep(os.path.join(dir_dataAct, '191008_Poids_2010.txt'), '\t')
# Poids de chaque zones Specifiques

EmpCDGactuel = 85.0     # Nombre de milliers d'emplois sur la plateforme CDG en actuel
PaxCDGactuel = 61.6     # Nombre de millions de passagers annuels transportés à CDG en actuel

Vect_spec[f'VSTC_CDG_PPM_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PPM en voy/h
Vect_spec[f'VSTC_CDG_PCJ_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HC.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PCJ en voy/h
Vect_spec[f'VSTC_CDG_PPS_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010CDG_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC actuel PPS en voy/h

EmpORLactuel = 26.2
PaxORLactuel = 27.2

Vect_spec[f'VSTC_ORLY_PPM_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTC_ORLY_PCJ_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HC.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PCJ en voy/h
Vect_spec[f'VSTC_ORLY_PPS_actuel'] = Path_sep(os.path.join(dir_dataAct, '160721_VSVoyTC2010ORLY_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h


# -- horizon scénario

Vect_spec[f'VS_PPM_scen'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hpm.txt'), '\t')
# Vect_spec[f'VS_PPM_scen'] = Path_sep(os.path.join(dir_dataScen, '2019', '140117_VectSpec2020_hpm.txt'), '\t')
Vect_spec[f'VS_PCJ_scen'] = Path_sep(os.path.join(dir_dataScen, '191023_VectSpec2030_hc.txt'), '\t')
# Vect_spec[f'VS_PPS_scen'] = Path_sep(os.path.join(dir_dataScen, '2019', '140117_VectSpec2020_hps.txt'), '\t')
Vect_spec[f'VS_PPS_scen'] = Path_sep(os.path.join(dir_dataAct, '140117_VectSpec2010_hps.txt'), '\t')

# Vect_spec[f'Poids_VS_scen'] = Path_sep(os.path.join(dir_dataScen, '2025', '210216_Poids_2025.txt'), '\t')
Vect_spec[f'Poids_VS_scen'] = Path_sep(os.path.join(dir_dataAct, '191008_Poids_2010.txt'), '\t')

EmpCDGscen = 92.7   # Nombre de milliers d'emplois sur la plateforme CDG en scénario
# 2012=85.0 ; 2018=92.7 ; 2024=107.3 ; 2028sansT4=110.8 ; 2028avecT4=128.3 ; 2037sansT4=112.9 ; 2037avecT4=165.0
PaxCDGscen = 76.2   # Nombre de millions de passagers annuels transportés à CDG en scénario
# 2012=61.6 ; 2018=70.8 ; 2019=76.2 ; 2024=85.4 ; 2028sansT4=88.9 ; 2028avecT4=95.7 ; 2037sansT4=91.0 ; 2037avecT4=128.8

Vect_spec[f'VSTC_CDG_PPM_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTC_CDG_PCJ_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HC.txt'), '\t')
# Vecteur spécifique voyage ur TC scénario PCJ en voy/h
Vect_spec[f'VSTC_CDG_PPS_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030CDG_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h

EmpORLscen = 29.0   # Nombre de milliers d'emplois sur la plateforme ORLY en scénario
# 2012=26.2 ; 2019=29.0? ; 2028=33.0
PaxORLscen = 31.9   # Nombre de millions de passagers annuels transportés à ORLY en scénario
# 2012=27.2 ; 2018=33.1 ; 2019=31.9 ; 2028=40.0

Vect_spec[f'VSTC_ORLY_PPM_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HPM.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPM en voy/h
Vect_spec[f'VSTC_ORLY_PCJ_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HC.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PCJ en voy/h
Vect_spec[f'VSTC_ORLY_PPS_scen'] = Path_sep(os.path.join(dir_dataScen, '2030', '121011_VSVoyTC2030ORLY_HPS.txt'), '\t')
# Vecteur spécifique voyageur TC scénario PPS en voy/h


# - e. vecteurs emission et attraction voyageurs TC des gares

Vect_gare = {}  # Un dictionnaire des flux des gares.

# -- horizon actuel
Vect_gare['VGTC_PPM_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPM.txt'), '\t')
Vect_gare['VGTC_PCJ_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PCJ.txt'), '\t')
Vect_gare['VGTC_PPS_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPS.txt'), '\t')

# -- horizon scénario

# Vect_gare['VGTC_PPM_scen'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PPM.txt'), '\t')
# Vect_gare['VGTC_PCJ_scen'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PCJ.txt'), '\t')
# Vect_gare['VGTC_PPS_scen'] = Path_sep(os.path.join(dir_dataScen, '2019', 'VG2017_TC_PPS.txt'), '\t')
Vect_gare['VGTC_PPM_scen'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPM.txt'), '\t')
Vect_gare['VGTC_PCJ_scen'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PCJ.txt'), '\t')
Vect_gare['VGTC_PPS_scen'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_TC_PPS.txt'), '\t')


# - . vecteurs emission et attraction voyageurs VP des gares

# -- horizon actuel
Vect_gare['VGVP_PPM_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPM.txt'), '\t')    # non activé
Vect_gare['VGVP_PCJ_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPM.txt'), '\t')    # non activé
Vect_gare['VGVP_PPS_actuel'] = Path_sep(os.path.join(dir_dataAct, 'VG2012_VP_PPS.txt'), '\t')    # non activé

# -- horizon scénario
Vect_gare['VGVP_PPM_scen'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPM.txt'), '\t')    # non activé
Vect_gare['VGVP_PCJ_scen'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPM.txt'), '\t')    # non activé
Vect_gare['VGVP_PPS_scen'] = Path_sep(os.path.join(dir_dataScen, 'VG2030_VP_PPS.txt'), '\t')    # non activé



# Les chemins de fichiers qui n'existaient pas sous SAS.
# Kiko currently not working, not sure why.

Pop_Emp = {}

Pop_Emp['actuel'] = os.path.join(dir_dataAct, 'bdzone2012.sas7bdat')
Pop_Emp['scen'] = os.path.join(dir_dataScen, 'bdzone2022.sas7bdat')

EM_PAR = {}

EM_PAR['PPM'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\em_hpm_par.sas7bdat')
EM_PAR['PCJ'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\em_hc_par.sas7bdat')
EM_PAR['PPS'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\em_hps_par.sas7bdat')

ATT_PAR = {}

ATT_PAR['PPM'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\att_hpm_par.sas7bdat')
ATT_PAR['PCJ'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\att_hc_par.sas7bdat')
ATT_PAR['PPS'] = os.path.join(dir_resultCalibrage,
                                'modus_recalibré_sept_2021\\5_Export\\att_hps_par.sas7bdat')


tx_desagr = {}

tx_desagr['EM_PPM'] = Path_sep(os.path.join(dir_resultCalibrage,
                                        'modus_recalibré_sept_2021\\5_Export\\tx_desagr_em1_hpm.txt')
                                        ,'\t')
tx_desagr['EM_PCJ'] = Path_sep(os.path.join(dir_resultCalibrage,
                                                         'modus_recalibré_sept_2021\\5_Export\\tx_desagr_em1_hc.txt')
                                            ,'\t')
tx_desagr['EM_PPS'] = Path_sep(os.path.join(dir_resultCalibrage,
                                                     'modus_recalibré_sept_2021\\5_Export\\tx_desagr_em1_hps.txt')
                                        ,'\t')
tx_desagr['ATT_PPM'] = Path_sep(os.path.join(dir_resultCalibrage,
                                        'modus_recalibré_sept_2021\\5_Export\\tx_desagr_att1_hpm.txt')
                                        ,'\t')
tx_desagr['ATT_PCJ'] = Path_sep(os.path.join(dir_resultCalibrage,
                                                     'modus_recalibré_sept_2021\\5_Export\\tx_desagr_att1_hc.txt')
                                        ,'\t')
tx_desagr['ATT_PPS'] = Path_sep(os.path.join(dir_resultCalibrage,
                                                     'modus_recalibré_sept_2021\\5_Export\\tx_desagr_att1_hps.txt')
                                        ,'\t')


#Capacité vélib
Capa_Velib = {}

Capa_Velib['actuel'] = Path_sep(os.path.join(dir_dataAct, 'Calcul_CapaVelib_ZoneModus.csv'), ';')
Capa_Velib['scen'] = Path_sep(os.path.join(dir_dataScen, 'Calcul_CapaVelib_ZoneModus.csv'), ';')


#CARACTÉRISTIQUES DU CALIBRAGE

seuilAtt = 30   # temps d'attente (yc correspondance) maximal
seuilRab = 60   # temps de rabattement maximal
seuilMar = 20   # temps de marche maximal
seuilVeh = 180  # temps en véhicule maximal


VCY = 15    # vitesse moyenne des cycles en km/h
VMD = 4

CVPkm = 0.242

# PARAMETRES DU CHOIX MODAL

CM_PAR_DICT = {}

CM_PAR_DICT['PPM'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\cm_parhpm.sas7bdat')
CM_PAR_DICT['PCJ'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\cm_parhc.sas7bdat')
CM_PAR_DICT['PPS'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\cm_parhps.sas7bdat')

# PARAMETRES DE LA DISTRIBUTION

DIST_PAR_DICT = {}
DIST_PAR_DICT['PPM'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\dist_par_hpm.sas7bdat')
# DIST_PAR_DICT['PPM'] = os.path.join(dir_calibrage, '2_Resultats\\200116_HP85-NewTVP-NewTTC-NewCTTKKM-ssFmucombinee\\'
#                                                  '5_Export\\dist_par_hpm.sas7bdat')
DIST_PAR_DICT['PCJ'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\dist_par_hc.sas7bdat')
DIST_PAR_DICT['PPS'] = os.path.join(dir_calibrage, '2_Resultats\\modus_recalibré_sept_2021\\'
                                                 '5_Export\\dist_par_hps.sas7bdat')


att = ['INTTC', 'INTVP', 'INTCY', 'TR_PPM', 'TATT_PPM', 'TTC_PPM', 'TR_PPS', 'TATT_PPS', 'TTC_PPS', 'TR_PCJ',
           'TATT_PCJ', 'TTC_PCJ', 'TVPM', 'TVPS', 'TVPC', 'TMD', 'TCY', 'CTTKKM', 'CTVP', 'CSTATMOY', 'CAPVELIB']

# Charactéristiques de l'étape de distribution
cMaxIterDist = 10
precRMSE = 100

# Mode dans lequel Modus tourne
# dbfile = open(f'{dir_dataTemp}params_user', 'rb')
# params_user = pkl.load(dbfile)

# Liste de dataframes qui entrent dans la BDD des résultats du calcul utilitaire

Motifs_Choix_Dist = defaultdict(list)
# C'est une nouvelle étape dans laquelle on va décrire la transformation des motifs entre le choix model et
# la distribution. Les clés du dictionnaire corréspondent aux motifs - distribution, et les élements aux motifs
# génération (selon diapo 6 de la documentation de Modus)

Motifs_Choix_Dist[1].extend((1, 2))
Motifs_Choix_Dist[2].extend((3,))
Motifs_Choix_Dist[3].extend((4,))
Motifs_Choix_Dist[4].extend((5,))
Motifs_Choix_Dist[5].extend((6,))
Motifs_Choix_Dist[6].extend((7,))
Motifs_Choix_Dist[7].extend((8,))
Motifs_Choix_Dist[8].extend((9,))
Motifs_Choix_Dist[9].extend((10,))
Motifs_Choix_Dist[10].extend((11, 12))
Motifs_Choix_Dist[11].extend((13, 14))

Duplication = np.zeros((22, 28))
for ligne, value in Motifs_Choix_Dist.items():
    for colonne in value:
        Duplication[ligne - 1, colonne - 1] = 1
        Duplication[ligne - 1 + 11, colonne - 1 + 14] = 1





























































