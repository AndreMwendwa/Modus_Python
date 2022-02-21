import os
from datetime import date
from Data.CstesStruct import *
# from Data.CstesStruct import dir_root

import yaml

yaml_file = open(f'{dir_modus_py}\\Data\\config_yml.yml', 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

# dir_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', '..', '..'))   # Pour créér
# le fichier .exe
dir_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..'))   # Pour tourner MODUS depuis
# le IDE
dir_modus = os.path.join(dir_root, 'M3_Chaine', 'Modus_Python') # répertoire de MODUS sous SAS



# Nom de la simulation
if yaml_content['idBcl'] != -1:
    name = yaml_content['name']
else:
    name = 'test_pyinstaller'  # Maintenant YML
out = dir_root + f'\\M3_Chaine\\Modus_Python\\Other_files\\{name}\\'   # Pour garder les
# résultats intérmediaire

try:
    os.mkdir(out)
except OSError:
    pass

# out = os.path.join(dir_resultModus, date.today().strftime("%d_%m_%Y"))
dir_dataTemp = os.path.join(out, '1_Fichiers_intermediares\\')
out_bcl = os.path.join(out, '2_Bouclage')
programmes = os.path.join(out, '0_Programmes')

dir_iter = out_bcl


try:
    os.mkdir(dir_dataTemp)
except OSError:
    pass

try:
    os.mkdir(out_bcl)
except OSError:
    pass

try:
    os.mkdir(programmes)
except OSError:
    pass




