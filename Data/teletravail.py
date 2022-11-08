import pandas as pd
import numpy as np
from Data.A_CstesModus import *
from Data.CstesStruct import *

def teletravail(n):   # Kiko - Il me semble que scen et n parlent finalement de la même chose. À confirmer.

    TTVAQ = pd.read_csv(tauxTTVAQ.path, sep=tauxTTVAQ.sep)
    Modus_BD_zone = pd.DataFrame()      # Crées un dataframe vide pour aider à mettre les colonnes dans le bon ordre.
    if n == 'actuel':
        Modus_BD_zone_Temp = pd.read_sas(os.path.join(dir_dataAct, 'bdzone2012.sas7bdat'))
    elif n == 'scen':
        Modus_BD_zone_Temp = pd.read_sas(os.path.join(dir_dataScen, 'bdzone2022.sas7bdat'))
    # Kiko - There's a problem here. You've confused per and hor I think.

    for var in ['ZONE', 'PACT', 'PACTHQ', 'PACTAQ', 'ETOT', 'EMPHQ', 'EMPAQ']:
        Modus_BD_zone[var] = Modus_BD_zone_Temp[var]

    Modus_BD_zone = pd.merge(TTVAQ, Modus_BD_zone, on = 'ZONE')     # Equivalent du merge sur la ligne 22 de
    # 2_Modus entre TTVAQ et Modus.BDzone&scen

    # What was there before 01/08/22
    Modus_BD_zone['tauxTTVact'] = np.where(Modus_BD_zone.PACT > 0,
                                    (Modus_BD_zone.PACTHQ * tauxTTVHQ + Modus_BD_zone.PACTAQ * tauxTTVAQact)/Modus_BD_zone.PACT,
                                    1)      # Si Modus_BD_zone.PACT > 0, il met le résultat du calcul, sinon 1
    Modus_BD_zone['tauxTTVemp'] = np.where(Modus_BD_zone.PACT > 0,
                                    (Modus_BD_zone.EMPHQ * tauxTTVHQ + Modus_BD_zone.EMPAQ * tauxTTVAQact)/Modus_BD_zone.PACT,
                                    1)

    # # Change made on 01/08/22
    # Modus_BD_zone['tauxTTVact'] = np.where(Modus_BD_zone.PACT > 0,
    #                                        (
    #                                                    Modus_BD_zone.PACTHQ * tauxTTVHQ + Modus_BD_zone.PACTAQ * tauxTTVAQact) / Modus_BD_zone.PACT,
    #                                        1)  # Si Modus_BD_zone.PACT > 0, il met le résultat du calcul, sinon 1
    # Modus_BD_zone['tauxTTVemp'] = np.where(Modus_BD_zone.ETOT > 0,
    #                                        (
    #                                                    Modus_BD_zone.EMPHQ * tauxTTVHQ + Modus_BD_zone.EMPAQ * tauxTTVAQemp) / Modus_BD_zone.ETOT,
    #                                        1)

    Result = pd.DataFrame()     # Nouveau variable, pas dans les fichier sas, utilisé à sauvegarder les résultats du
    # calcul

    Result['ZONE'] = Modus_BD_zone['ZONE']
    Result['HQpro'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVHQ
    Result['AQproact'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQact
    Result['AQproemp'] = 1 + ((jourTTV * varJTTVpro + (1 - jourTTV) * varJLTHpro) * partTTV + (1 - partTTV) - 1) * tauxTTVAQemp
    Result['ACTacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVact']
    Result['EMPacc'] = 1 + ((jourTTV * varJTTVacc + (1 - jourTTV) * varJLTHacc) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVemp']
    Result['ACTaut'] = 1 + ((jourTTV * varJTTVaut + (1 - jourTTV) * varJLTHaut) * partTTV + (1 - partTTV) - 1) * Modus_BD_zone['tauxTTVact']
    Result.index = Result['ZONE']
    del Result['ZONE']

    return Result


if __name__ == '__main__':
    teletravail('scen')