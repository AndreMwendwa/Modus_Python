import os
from datetime import date
from Data.CstesStruct import *

Iter = 1

out = os.path.join(dir_resultModus, date.today().strftime("%d_%m_%Y"))
out_mat = os.path.join(out, '3_Matrices')
out_bcl = os.path.join(out, '2_Bouclage')

dir_iter = out_bcl

try:
    os.mkdir(out)
    os.mkdir(out_mat)
    os.mkdir(out_bcl)
except OSError:
    pass

dir_iter = os.path.join(out_bcl, f'Iter{Iter}')

iter_count = 0



