import os
from datetime import date
from Data.CstesStruct import *
from Data.CstesStruct import dir_root


# Nom de la simulation
name = 'with_TTV_gen_dist0.75_recalibré_factech_4motif_nonwk_2'
dir_dataTemp = dir_root + f'\\M3_Chaine\\Modus_Python\\Other_files\\{name}\\'   # Pour garder les
# résultats intérmediaire

try:
    os.mkdir(dir_dataTemp)
except OSError:
    pass

# out = os.path.join(dir_resultModus, date.today().strftime("%d_%m_%Y"))
out = dir_dataTemp    # Kiko: Temporaire, à supprimer
out_mat = os.path.join(out, '3_Matrices')
out_bcl = os.path.join(out, '2_Bouclage')

dir_iter = out_bcl

try:
    os.mkdir(out)
except OSError:
    pass

try:
    os.mkdir(out_mat)
except OSError:
    pass

try:
    os.mkdir(out_bcl)
except OSError:
    pass





