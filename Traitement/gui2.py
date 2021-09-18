import PySimpleGUI as sg
from Quatre_Etapes import choix_modal
from Quatre_Etapes import generation
sg.theme("Dark Teal 4")

col1 = sg.Column([[sg.Frame('INPUTS:', [[sg.Text("Dossier de données d'entrée      "), sg.InputText(key='-file1-'), sg.FileBrowse(target='-file1-')],
                                        [sg.Text("Dossier de fichiers intérmediares"), sg.InputText(key='-file2-'), sg.FileBrowse(target='-file2-')],
                                        [sg.Text("Dossier de résultats             "), sg.InputText(key='-file3-'), sg.FileBrowse(target='-file3-')],
                                        [sg.Text("Fichier de paramétres clés       "), sg.InputText(key='-file4-'), sg.FileBrowse(target='-file4-')],
                                        [sg.Text("Nombre d'itérations de Modus     "), sg.Spin(values=[i for i in range(1, 20)], initial_value=10, size=(6, 1))],
                                        [sg.Text("Nombre d'itérations dans VISUM   "), sg.Spin(values=[i for i in range(1, 20)], initial_value=10, size=(6, 1))]
                                        ])]], pad=(0,0))

col2 = sg.Column([[sg.Frame('CONFIG:', [[sg.Rad('Lancer 4 étapes            ', 'Config', size=(12, 1))],
                                        [sg.Rad('Lancer 4 sans prétraitement', 'Config', size=(20, 1), default=True)],
                                        [sg.T('Choisis BDInter'), sg.InputText(key='-file6-'), sg.FileBrowse(target='-file6-')],
                                        [sg.Rad('Lancer étapes 2 à 4', 'Config', size=(20, 1))],
                                        [sg.T('Choisis gen_results'), sg.InputText(key='-file7-'), sg.FileBrowse(target='-file7-')],
                                        [sg.Rad('Lancer étapes 3 à 4', 'Config', size=(20, 1))],
                                        [sg.T('Choisis dist_results'), sg.InputText(key='-file8-'), sg.FileBrowse(target='-file8-')],
                                        [sg.Rad('Lancer étape 4', 'Config', size=(20, 1))],
                                        [sg.T('Choisis dist_results'), sg.InputText(key='-file9-'), sg.FileBrowse(target='-file9-')],
                                         ])]], pad=(0, 0))

col3 = sg.Column([[sg.Frame('SORTIES:', [[sg.InputText(key='-fileY-'), sg.FileBrowse(target='-fileY-')]])]], pad=(0,0))

layout = [[[col1, col2], col3]]

window = sg.Window('MODUS 3.1.3', layout)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()