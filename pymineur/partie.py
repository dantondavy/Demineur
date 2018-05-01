"""
Module contenant la description de la classe Partie qui permet de jouer une partie du jeu démineur.
Doit être démarré en appelant la méthode jouer(). Cette classe contient les informations sur une partie et
utilise un objet tableau_mines (une instance de la classe Tableau).
"""

# On importe la classe Tableau du package pymineur
from pymineur.tableau import Tableau


class Partie:
    """
    La classe Partie ne fait seulement que créer une instance de la classe Tableau.

    Attributes:
        tableau_mines (Tableau): Le tableau de cases où les mines sont cachées avec lequel se
                déroule la partie.
    """

    def __init__(self):
        # Création d'une instance de la classe Tableau, qui sera manipulée par les méthodes de la classe.
        self.tableau_mines = Tableau()
