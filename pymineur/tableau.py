"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.
"""

# On importe la Classe case du package pymineur et le module random
from pymineur2.pymineur.case import Case
import random


class Tableau:
    """
    Documentation de la classe Tableau, implémentée avec un dictionnaire de cases

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau (un tuple x, y), x étant le numéro de la rangée,
            y étant le numéro de la colonne.
            Les éléments sont des objets de la classe Case.

    """

    def __init__(self):
        # On construit notre classe Tableau en y ajoutant ses attributs
        self.dimension_rangee = 5
        self.dimension_colonne = 5
        self.nombre_mines = 5

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        # On appelle la fontion de la classe initialiser_tableau()
        self.initialiser_tableau()

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau.
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard.
            3) À chaque fois qu'on ajoute une mine dans une case, on incrémente dans chacune des cases
            voisines un attribut qui représentera le nombre de mines voisines pour ces cases.

        Args: None

        Returns: None

        """
        # On initialise le nombre de mines placées dans le tableau
        mines_placees = 0

        # On crée un dictionnaire avec les tuples comme clés et des instances de Cases comme valeurs dans ces clés
        for x in range(1, self.dimension_rangee + 1):
            for y in range(1, self.dimension_rangee + 1):
                self.dictionnaire_cases[(x, y)] = Case()

        # On ajoute des mines aléatoirement dans le tableau
        while mines_placees <= self.nombre_mines - 1:
            # On utilise la fonction randint du module random pour déterminer la position de la mine à ajouter
            position_x = random.randint(1, self.dimension_rangee)
            position_y = random.randint(1, self.dimension_colonne)

            # Pour tester si on obtient deux fois la même case random, dans ce cas on incrémente pas mines_placees on
            # recherche une autre case
            if self.dictionnaire_cases[(position_x, position_y)].contient_mine():
                continue
            # On ajoute une mine dans la case du dictionnaire correspondante si ne contient pas déjà une mine
            self.dictionnaire_cases[(position_x, position_y)].ajouter_mine()
            mines_placees += 1

            # Pour aller voir si on a des mines dans le voisinage et incrémenter notre chiffre de la case en question
            case_voisines = self.obtenir_voisins(position_x, position_y)
            for voisine in case_voisines:
                self.dictionnaire_cases[voisine].ajouter_une_mine_voisine()

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            liste_coordonnees_cases_voisines : Liste des coordonnées (tuple x, y) valides des cases voisines
            de la case dont les coordonnées sont reçues en arguments
        """

        # Initialiser la liste des cases voisines
        liste_coordonnees_cases_voisines = []

        voisinage = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

        # Déterminer les cases voisines de la case à l'aide du tuple VOISINAGE
        for voisins in voisinage:
            case_valide = self.valider_coordonnees(rangee_x + voisins[0], colonne_y + voisins[1])
            # Si la case n'est pas valide, on continue pour un autre tuple de VOISINAGE sans remplir notre liste
            if not case_valide:
                continue
            # On ajoute une tuple à notre liste à chaque case voisine valide de la case choisie (rangee_x, colonne_y)
            liste_coordonnees_cases_voisines.append((rangee_x + voisins[0], colonne_y + voisins[1]))

        return liste_coordonnees_cases_voisines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """

        # Tester si les coordonnées sont dans le tableau avec les dimensions entrées (dimension_rangee et
        # et dimension_colonne)
        if rangee_x < 1 or rangee_x > self.dimension_rangee \
                or colonne_y < 1 or colonne_y > self.dimension_colonne:
            return False

        return True

    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler

        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """

        if self.nombre_cases_sans_mine_a_devoiler > 0:
            return True
        return False

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument. Si la case ne
        contient pas de mine, on décrémente l'attribut qui représente le nombre de cases sans mines à dévoiler.

        Args :
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler
        """

        self.nombre_cases_sans_mine_a_devoiler -= 1

        self.dictionnaire_cases[(rangee_x, colonne_y)].devoiler()

    def case_contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine
        Returns
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """

        if self.dictionnaire_cases[(rangee_x, colonne_y)].contient_mine():
            return True

        return False
