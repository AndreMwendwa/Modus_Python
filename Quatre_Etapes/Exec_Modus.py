import os
from datetime import date
from Data.CstesStruct import *


out = os.path.join(dir_resultModus, date.today().strftime("%d_%m_%Y"))
out_mat = os.path.join(out, '3_Matrices')


iter_count = 0