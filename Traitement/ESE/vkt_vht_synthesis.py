import pandas as pd
import pickle as pkl
import PySimpleGUI as sg

def GetFilesToCompare():
    '''Pour séléctionner les dossiers avec les résultats'''
    form_rows = [[sg.Text('Veuillez choisir les dossiers qui contiennent des résultats que vous aimeriez comparer')],
                 [sg.Text('Fichier de résultats', size=(20, 1)),
                  sg.InputText(key='-file1-'), sg.FileBrowse()],
                 [sg.Text('Dossier de stockage de résultats', size=(20, 1)), sg.InputText(key='-file2-'),
                  sg.FolderBrowse(target='-file2-')],
                 [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Choix de scénarios', form_rows)
    event, values = window.read()
    window.close()
    return event, values

def vkt_vht():
    button, values = GetFilesToCompare()
    f1, f2 = values['-file1-'], values['-file2-']

    dbfile = open(f1, 'rb')
    dfs = pkl.load(dbfile)
    # Résultats ESE
    vkt_vht_df = pd.concat(dfs.values(), ignore_index=False)
    vkt_vht_df.to_excel(f2 + '/vkt_vht_totals.xlsx')

if __name__ == '__main__':
    # file = r'C:\Users\mwendwa.kiko\Documents\RFTM\Modus_ESE_new_results\result_dfs'
    vkt_vht()