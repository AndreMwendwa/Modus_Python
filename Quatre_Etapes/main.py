from Data.CstesStruct import *
import pickle as pkl


from Traitement.gui3 import *
from Quatre_Etapes import choix_modal
modus_mode, bdinter, gen_results, dist_results, choix_results = None, None, None, None, None

submit = GUI()

if submit['-Bdinter_res-']:
    modus_mode = 1
    bdinter = submit['-bdinter-']
elif submit['-Gen_res-']:
    modus_mode = 2
    gen_results = submit['-gen_results-']
elif submit['-dist_results-']:
    modus_mode = 3
    dist_results = submit['-dist_results-']
elif submit['-choix_results-']:
    modus_mode = 4
    choix_results = submit['-choix_results-']


params_user = {'modus_mode': modus_mode, 'bdinter': bdinter, 'gen_results': gen_results,
                             'dist_results': dist_results, 'choix_results': choix_results}

dbfile = open(f'{dir_dataTemp}params_user', 'wb')
pkl.dump(params_user, dbfile)
dbfile.close()

n = submit[2]
per = submit[3]

Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat = choix_modal.choix_modal(n, per)






