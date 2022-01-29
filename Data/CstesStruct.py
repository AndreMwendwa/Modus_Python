'''
FICHIER DE CONSTANTES DE STRUCTURES DES REPERTOIRES
Date 15 juin 2021
d'après la version crée le 19 août 2007
'''

# Bibliothéques de python qui sont nécessaires
import os
from pathlib import Path
# from Quatre_Etapes import Exec_Modus

# 1. Répertoires et versions des logiciels
# !!! ATTENTION : si la version de Davisum n'est pas la 11, il faut modifier le programme Wait2.exe

vers_Visum=16
dir_7zip = os.path.join('C:\\', 'Program Files', '7-Zip')

# 2. Répertoire des données
dir_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', '..', '..'))    # Pour créér
# le fichier .exe
# dir_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..'))      # Pour tourner MODUS depuis
# le IDE
dir_data = os.path.join(dir_root, 'Donnees')    # répertoire racine de stockage des données
dir_EGT = os.path.join(dir_data, 'EGT')     # répertoire de stockage des données de l'EGT
dir_zonage = os.path.join(dir_data, 'Zonage')    # répertoire de stockage des données de zonage
dir_macros = os.path.join(dir_data, 'Macros')   # répertoire de stockage des fonctions, pour améliorer la tracabilité,
# on a gardé ici le même nom qui était utilisé à l'époque du SAS
dir_dataRef = os.path.join(dir_data, 'Input', '0_Reference')    # répertoire de stockage des données actuelles
dir_dataAct = os.path.join(dir_data, 'Input', '1_Actuel')   # répertoire de stockage des données actuelles
dir_dataScen = os.path.join(dir_data, 'Input', '2_Scenario')    # répertoire de stockage des données en mode scenario
dir_modus_py = os.path.join(dir_root, 'M3_Chaine', 'Modus_Python')




# 3. Répertoires du calibrage
dir_calibrage = os.path.join(dir_root, 'M3_Calibrage')  # répertoire de calibrage
dir_progCalibrage = os.path.join(dir_calibrage, '0_Programmes', 'PPM-PC-PPS-tous-modes')    # répertoire de stockage des
#  programmes de calibrage
dir_tblCalibrage = os.path.join(dir_calibrage, '1_Tables')  # répertoire de stockage des tables de calibrage
dir_resultCalibrage = os.path.join(dir_calibrage, '2_Resultats')    # répertoire de stockage des résultats de calibrage

# 4. Répertoires de MODUS

# dir_modus = os.path.join(dir_root, 'M3_Chaine', 'Modus_Python') # répertoire de MODUS sous SAS
# dir_progModus = os.path.join(dir_modus, '0_Programmes')     # répertoire de stockage des programmes de MODUS sous SAS
# dir_tblModus = os.path.join(dir_modus, '1_Tables')      # répertoire de stockage des tables de MODUS sous SAS
# dir_resultModus = os.path.join(dir_modus, '2_Resultats')    # répertoire des résultats de l'exécution de MODUS

