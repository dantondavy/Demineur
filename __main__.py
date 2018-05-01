"""
Module principal du package pymineur2. C'est ce module que nous allons exécuter pour démarrer le jeu de démineur.
"""

# On importe la classe FenetreDemineur du dossier interface
from interface.demineur_gui import FenetreDemineur

if __name__ == '__main__':

    # On crée une instance de la classe FenetreDemineur qui hérite de Tk, puis on démarre sa boucle principale
    fenetre_demineur = FenetreDemineur()
    fenetre_demineur.mainloop()
