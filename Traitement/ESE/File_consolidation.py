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


def read_and_consolidate():
    button, values = GetFilesToCompare()
    f1, f2 = values['-file1-'], values['-file2-']

    dbfile = open(f1, 'rb')
    dfs = pkl.load(dbfile)
    sums = {k: [v[0].loc['Total change in surplus, PPM','Total Cost per hour (€) - différence between scénarios'],
                v[2].loc['Total change in surplus, PPS','Total Cost per hour (€) - différence between scénarios']]
            for k, v in dfs.items()}
    sums_df = pd.DataFrame(sums)
    sums_df.to_excel(f2 + '/sums_of_consumer_surpluses.xlsx')


def read_and_not_consolidate():
    button, values = GetFilesToCompare()
    f1, f2 = values['-file1-'], values['-file2-']

    dbfile = open(f1, 'rb')
    dfs = pkl.load(dbfile)
    sums = pd.DataFrame()
    for key, value in dfs.items():
        title = pd.DataFrame([key], index=['Title'])
        res = pd.concat([title, value[0].loc[:, 'Total Cost per hour (€) - différence between scénarios'],
                         value[2].loc[:,'Total Cost per hour (€) - différence between scénarios']])
        sums = pd.concat([sums, res], axis=1)
    sums.columns = sums.loc['Title', :]
    sums.drop('Title', inplace=True)
    # sums = {k: [v[0].loc[:, 'Total Cost per hour (€) - différence between scénarios'],
    #             v[2].loc[:,'Total Cost per hour (€) - différence between scénarios']]
    #         for k, v in dfs.items()}
    # sums_df = pd.DataFrame(sums)
    sums.to_excel(f2 + '/sums_of_consumer_surpluses.xlsx')

if __name__ == '__main__':
    # file = r'C:\Users\mwendwa.kiko\Documents\RFTM\Modus_ESE_new_results\result_dfs'
    read_and_not_consolidate()


