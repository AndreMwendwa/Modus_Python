'''
Conversion des flux PPM en HPM en appliquant les taux de redressement développés par J. Perun de la DRIEAT.
'''
import numpy as np
import pandas as pd
import pickle as pkl

from Data.A_CstesModus import *
from Quatre_Etapes.dossiers_simul import *
import win32com.client as win32
import Data.VisumPy.helpers2 as helpers

class pp_hp:
    # Variables de classe pour enregistrer les taux de redressement qu'on va utiliser
    vl_ppm = {}   # Dictionnaire qu'on convertira ensuite en dataframe
    vl_ppm['PC_PC_cl1'] = 2.1  # Déplacement entre Paris/PC et Paris/PC à l'HPM pour les VL et la classe de distance 1
    vl_ppm['PC_PC_cl1'] = 2.1     # Déplacement entre Paris/PC et Paris/PC à l'HPM pour les VL et la classe de distance 1
    vl_ppm['GC_GC_cl1'] = 2.2      # Déplacement entre GC et GC à l'HPM pour les VL et la classe de distance 1
    vl_ppm['PC_GC_cl1'] = 1.2      # Déplacement entre Paris/PC et GC à l'HPM pour les VL et la classe de distance 1
    vl_ppm['GC_PC_cl1'] = 1.2  # On doit le répêter, puisque le pd.merge utilisé dans redresse_matrice en dépend
    vl_ppm['PC_PC_cl2'] = 1.6      # Déplacement entre Paris/PC et Paris/PC à l'HPM pour les VL et la classe de distance 2
    vl_ppm['GC_GC_cl2'] = 1.7      # Déplacement entre GC et GC à l'HPM pour les VL et la classe de distance 2
    vl_ppm['PC_GC_cl2'] = 1.9      # Déplacement entre Paris/PC et GC à l'HPM pour les VL et la classe de distance 2
    vl_ppm['GC_PC_cl2'] = 1.9  # On doit le répêter, puisque le pd.merge utilisé dans redresse_matrice en dépend
    vl_ppm['PC_PC_cl3'] = 1.3      # Déplacement entre Paris/PC et Paris/PC à l'HPM pour les VL et la classe de distance 3
    vl_ppm['GC_GC_cl3'] = 1.6      # Déplacement entre GC et GC à l'HPM pour les VL et la classe de distance 2
    vl_ppm['PC_GC_cl3'] = 1.2      # Déplacement entre Paris/PC et GC à l'HPM pour les VL et la classe de distance 3
    vl_ppm['GC_PC_cl3'] = 1.2  # On doit le répêter, puisque le pd.merge utilisé dans redresse_matrice en dépend
    vl_ppm = pd.Series(vl_ppm)
    # Pour l'HPS et les PL
    pl_PPM = 0.92      # PL pendant l'HPM
    vl_PPS = 1.1       # VL pendant l'HPS
    pl_PPS = 0.81       # PL pendant l'HPS

    # Distance à vol d'oiseau
    DVOL = pd.read_csv(Donnees_Interz['dist_vol_scen'].path, sep=Donnees_Interz['dist_vol_scen'].sep)

    # Départements
    zone_dept = pd.read_csv(zone_commune.path, sep=zone_commune.sep)

    # Les numéros des départements corréspondant à la Petite Couronne et Grande Couronne.
    # Le calcul des taux de redressements traite Paris et la Petite Couronne de la même manière, donc ils sont combinés ici
    PC = [92, 93, 94, 75]   # Petite Couronne
    GC = [77, 78, 91, 95]  # Grande Couronne

    def __init__(self, H, dir_itern, Iter):
        with open(f'{dir_dataTemp}MODUSCaleUVP_df_{H}_scen', 'rb') as dbfile:
            self.matVP = self.rajout_dept_couronne_classedvol(pkl.load(dbfile))   # On rajoute le dept, la couronne et
            # la classe de distance
        self.H = H
        self.dir_itern = dir_itern
        self.Iter = Iter

    def rajout_dept_couronne_classedvol(self, mat_in):
        # Il y a des zones qui sont dans plusieurs communes, et des communes dans plusieurs zones, mais ça ne nous
        # intéresse pas donc on applique drop_duplicates() sur les lignes doublés
        zone_dept = self.zone_dept[['ZONE', 'INSEEDPT']].drop_duplicates()
        # On rajoute les départements
        mat_in = (pd.merge(mat_in, zone_dept, left_on='ZONEO', right_on='ZONE')
                  .rename(columns={'INSEEDPT': 'OR_DEP'}).drop('ZONE', axis=1))
        mat_in = (pd.merge(mat_in, zone_dept, left_on='ZONED', right_on='ZONE')
                  .rename(columns={'INSEEDPT': 'DEST_DEP'}).drop('ZONE', axis=1))
        # On rajoute les couronnes
        mat_in['OR_COUR'] = np.where(mat_in['OR_DEP'].isin(self.PC), 'PC', 'GC')
        mat_in['DEST_COUR'] = np.where(mat_in['DEST_DEP'].isin(self.PC), 'PC', 'GC')

        # On rajoute la classe de distance
        mat_in['CLASSEDVOL'] = np.where(
            self.DVOL['DVOL'] <= 2, 'cl1', np.where(
                self.DVOL['DVOL'] <= 9, 'cl2', 'cl3'
            )
        )
        return mat_in

    def redresse_matrice(self):
        if self.H == 'PPM':
            self.matVP['couronne_classedvol'] = (self.matVP[['OR_COUR', 'DEST_COUR', 'CLASSEDVOL']]
                                                 .apply(lambda row: '_'.join(row.values.astype(str)), axis=1))
            self.matVP = (pd.merge(self.matVP, self.vl_ppm.to_frame(), left_on='couronne_classedvol', right_index=True)
                          .rename(columns={0 : 'Taux_redressement'}))
            self.matVP['FLUX'] *= self.matVP['Taux_redressement']
        else:
            self.matVP['FLUX'] *= self.vl_PPS
        with open(f'{dir_dataTemp}flux_derniere_iteration_{self.H}', 'wb') as dbfile:
            pkl.dump(self.matVP[['FLUX']].to_numpy().reshape(cNbZone, cNbZone), dbfile)
        return self.matVP[['FLUX']].to_numpy().reshape(cNbZone, cNbZone)

    def affect(self):
        matVP = self.redresse_matrice()
        myvisum = win32.Dispatch("Visum.Visum")
        myvisum.LoadVersion(Donnees_Res[f'Version_{self.H}_scen'])
        mat_grand = np.zeros((1327, 1327))
        mat_grand[:1289, :1289] = matVP
        helpers.SetODMatrix(myvisum, 'V', mat_grand)
        # myvisum.procedures.Execute()
        myvisum.SaveVersion(os.path.join(self.dir_itern, f'Vers{self.H}_scen_iter{self.Iter}.ver'))


if __name__ == '__main__':
    # pp_hp = pp_hp('PPS')
    # pp_hp.redresse_matrice()
    pass





