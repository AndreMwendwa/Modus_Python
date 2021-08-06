# Test TC seulement
import pandas as pd
from Data.A_CstesModus import *

euTC = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_tc.sas7bdat')  # Your own path
euTC.columns = range(22)
euCY = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_cy.sas7bdat')  # Your own path
euCY.columns = range(22)
euMD = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_md.sas7bdat')  # Your own path
euMD.columns = range(22)
euVP = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\eudf_vp.sas7bdat')  # Your own path
euVP.columns = range(22)
seU = euTC + euVP + euCY + euMD
Modus_motcat = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                               '\\modus_motcat_2012_hpm.sas7bdat')  # Your own path
Duplication = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                   '\\Confirmation distribution\\dupplication.sas7bdat')  # Your own path
Duplication.columns = range(28)
Modus_motcat.columns = range(28)
Modus_motcat = Modus_motcat @ Duplication.T
BASE = Modus_motcat/seU
Modus_MD_motcat = BASE * euMD
Modus_MD_motcat_valid = pd.read_sas('D:\\TraDD ENPC 2020-21\\Stage\\MODUSv3.1.3\\M3_Chaine\\Modus_Python\\Other_files'
                              '\\Confirmation distribution\\motcatmd.sas7bdat')   # The dataset created by the SAS code
Modus_MD_motcat_valid.columns = range(22)
diffMD = np.abs(Modus_MD_motcat - Modus_MD_motcat_valid)/Modus_MD_motcat_valid
meandiffMD = diffMD.mean().mean()

diffMD.mean(1).plot()
