from codetiming import Timer
from Quatre_Etapes import choix_modal

t = Timer(name="class")


t.start()
Modus_MD_motcat, Modus_CY_motcat, Modus_VP_motcat, Modus_TC_motcat = choix_modal.choix_modal('actuel', 'PPM')
t.stop()


