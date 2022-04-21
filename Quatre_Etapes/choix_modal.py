# Cette partie assure l'importation des constants,
# et que une fois des fichiers avec des constants changés et sauvegardés les changements sont enregistrés
from Data.A_CstesModus import *

# dbfile = open(f'{dir_dataTemp}params_user', 'rb')
# params_user = pkl.load(dbfile)
from Quatre_Etapes.dossiers_simul import dir_dataTemp


def choix_modal(n, hor, itern):
    dbfile = open(f'{dir_dataTemp}UTIL_DB', 'rb')
    db = pkl.load(dbfile)

    euTC = db['util_TC']
    euVP = db['util_VP']
    euCY = db['util_CY']
    euMD = db['util_MD']
    # Modus_motcat = distribution.distribution(n, hor)
    dbfile = open(f'{dir_dataTemp}Modus_motcat_{n}_{hor}', 'rb')
    Modus_motcat = pkl.load(dbfile)

    Modus_motcat = Modus_motcat @ Duplication.T

    seU = euTC + euVP + euCY + euMD



    if n == 'actuel':

        BASE = Modus_motcat/seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_MD_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl < 3 or itern == 1:
        BASE = Modus_motcat / seU
        Modus_MD_motcat = BASE * euMD
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_MD_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl == 3 and itern > 1:
        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'rb')
        Modus_MD_motcat = pkl.load(dbfile)
        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'rb')
        Modus_CY_motcat = pkl.load(dbfile)

        BASE = (Modus_motcat - Modus_MD_motcat - Modus_CY_motcat)/seU
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()

    elif idBcl == 4 and itern > 1:
        dbfile = open(f'{dir_dataTemp}Modus_MD_motcat_{n}_{hor}', 'rb')
        Modus_MD_motcat = pkl.load(dbfile)

        BASE = (Modus_motcat - Modus_MD_motcat) / seU
        Modus_CY_motcat = BASE * euCY
        Modus_VP_motcat = BASE * euVP
        Modus_TC_motcat = BASE * euTC

        dbfile = open(f'{dir_dataTemp}Modus_CY_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_CY_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_VP_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_VP_motcat, dbfile)
        dbfile.close()
        dbfile = open(f'{dir_dataTemp}Modus_TC_motcat_{n}_{hor}', 'wb')
        pkl.dump(Modus_TC_motcat, dbfile)
        dbfile.close()
        if n == 'actuel':
            if hor == 'PPM':
                print(
                    f"\t Choix modal terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Matin")
            elif hor == 'PCJ':
                print(
                    f"\t Choix modal terminé pour l'année de calage du modèle ({actuel}), pour la Période Creuse de la journée")
            else:
                print(
                    f"\t Choix modal terminé pour l'année de calage du modèle ({actuel}), pour la Période de Pointe du Soir")
        else:
            if hor == 'PPM':
                print(
                    f"\t Choix modal terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Matin")
            elif hor == 'PCJ':
                print(
                    f"\t Choix modal terminé pour l'année de scénario du modèle ({scen}), pour la Période Creuse de la journée")
            else:
                print(
                    f"\t Choix modal terminé pour l'année de scénario du modèle ({scen}), pour la Période de Pointe du Soir")

    # return Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat

if __name__ == '__main__':
    choix_modal('actuel', 'PPS', 1)









