import PySimpleGUI as sg
from Quatre_Etapes import choix_modal
from Quatre_Etapes import generation

def main():
    sg.theme("Dark Teal 4")

    # Define the window layout

    layout = [
        [sg.Button('Valider Presence de Fichiers', size=(30, 1))],
        [sg.Text('Lancer MODUS', size=(45, 1))],
        [sg.Button('Lancer Quatre Etapes')],
        [sg.Text('Indicateurs', size=(45, 1))],
        [sg.Button('Lancer Indicateurs')]
    ]

    window = sg.Window('MODUS 3.1.3', layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Lancer Quatre Etapes':
            generation.generation('actuel','PPM')
        elif event == 'Lancer Indicateurs':
            pass
    window.close()

main()
