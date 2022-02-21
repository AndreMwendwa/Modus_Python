import pandas as pd
import pickle as pkl
from pathlib import Path
import PySimpleGUI as sg

def GetFiles():
    form_rows = [[sg.Text('Fichier à comparer avec')],
                 [sg.Text('File 1', size=(15, 1)),
                  sg.InputText(key='-file1-'), sg.FileBrowse()],
                 [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Conversion de fichier en CSV', form_rows)
    event, values = window.read()
    window.close()
    return event, values

def main():
    while True:
        button, values = GetFiles()
        if button == sg.WIN_CLOSED:
            break
        f1 = values['-file1-']
        dbfile = open(Path(f1), 'rb')
        file = pd.DataFrame(pkl.load(dbfile))
        name_file = f1.split('\\')[-1]
        file.to_csv(f"{name_file}.csv")

if __name__ == '__main__':
    main()





