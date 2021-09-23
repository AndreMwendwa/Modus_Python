import PySimpleGUI as sg
import sys
from Data.A_CstesModus import *
from Quatre_Etapes import choix_modal
from Quatre_Etapes import generation
sg.theme("Dark Teal 4")


col1 = [sg.Frame('INPUTS:', [[sg.Text("Dossier de données d'entrée      ", size=(25, 1), justification='left'), sg.InputText(key='-file1-', default_text=dir_dataAct), sg.FileBrowse(target='-file1-')],
                                        [sg.Text("Dossier de fichiers intérmediares", size=(25, 1), justification='left'), sg.InputText(key='-file2-', default_text=dir_dataTemp), sg.FileBrowse(target='-file2-')],
                                        [sg.Text("Dossier de résultats             ", size=(25, 1), justification='left'), sg.InputText(key='-file3-', default_text=dir_resultModus), sg.FileBrowse(target='-file3-')],
                                        [sg.Text("Fichier de paramétres clés       ", size=(25, 1), justification='left'), sg.InputText(key='-file4-'), sg.FileBrowse(target='-file4-')],
                                        [sg.Text("Nombre d'itérations de Modus     ", size=(25, 1), justification='left'), sg.Spin(values=[i for i in range(1, 20)], initial_value=10, size=(6, 1))],
                                        [sg.Text("Nombre d'itérations dans VISUM   ", size=(25, 1), justification='left'), sg.Spin(values=[i for i in range(1, 20)], initial_value=10, size=(6, 1))]
                                        ])]

col2 = [sg.Frame('CONFIG:', [[sg.Rad('Lancer 4 étapes            ', 'Config', size=(12, 1))],
                                        [sg.Rad('Lancer 4 sans prétraitement', 'Config', size=(20, 1), default=True)],
                                        [sg.T('Choisis BDInter     ', size=(25, 1), justification='left'), sg.InputText(key='-file6-'), sg.FileBrowse(target='-file6-')],
                                        [sg.Rad('Lancer étapes 2 à 4', 'Config', size=(20, 1))],
                                        [sg.T('Choisis gen_results', size=(25, 1), justification='left'), sg.InputText(key='-file7-'), sg.FileBrowse(target='-file7-')],
                                        [sg.Rad('Lancer étapes 3 à 4', 'Config', size=(20, 1))],
                                        [sg.T('Choisis dist_results', size=(25, 1), justification='left'), sg.InputText(key='-file8-'), sg.FileBrowse(target='-file8-')],
                                        [sg.Rad('Lancer étape 4    ', 'Config', size=(20, 1))],
                                        [sg.T('Choisis dist_results', size=(25, 1), justification='left'), sg.InputText(key='-file9-'), sg.FileBrowse(target='-file9-')],
                                         ])]

col3 = [sg.Frame('SORTIES:', [[sg.T('Lancer calcul des indicateurs', size=(25, 1), justification='left')],
                            [sg.T('Fichier de résultats', size=(15, 1), justification='left'), sg.InputText(key='-fileY-'), sg.FileBrowse(target='-fileY-')]
                              ])]

layout = [[col1, col2, col3, sg.Submit()]]

window = sg.Window('MODUS 3.1.3', layout)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        print(event, values)
        break

print(event, values)
window.close()