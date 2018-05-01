# C'est ici qu'on crée l'interface graphique du jeu de démineur et qu'on démarre la Partie.

# On importe la classe Partie du package pymineur et les méthode et classe de tkinter qu'on a besoin
from tkinter import Tk, Button, DISABLED, RAISED, SUNKEN, messagebox
from pymineur2.pymineur.partie import Partie


class FenetreDemineur(Tk):
    """Classe qui hérite de Tk et qui est la fenêtre principale de notre tableau démineur

        Attributs:
        dictionnaire_boutons (dict): Un dictionnaire dans lequel les clés représentes les coordonnées des cases
                                    et les valeurs sont des objets de la classe Bouton de Tk
        title (str): Titre de la fenêtre principale
        self.partie (Partie): Instance de la classe partie
        self.bouton_partie (Button): Bouton Tk pour commencer la partie
        self.bouton_instructions (Button): Bouton Tk pour les instructions sur le jeu démineur
        self.bouton_quitter (Button): Bouton Tk pour quitter le jeu démineur

        """

    def __init__(self):
        """On construit notre classe FenetreDemineur"""

        # Appeler le constructeur de la classe parente Tk
        super().__init__()

        # Nommer la fenêtre globale du jeu démineur
        self.title("Démineur")
        self.config(padx=5, pady=5)

        # Initialiser le dictionnaire de bouton
        self.dictionnaire_boutons = {}

        # Création d'une instance de Partie au démarrage du programme
        self.partie = Partie()

        # On crée les boutons démarrer, quitter et instruction et on les lie à la bonne action
        self.bouton_partie = Button(self, width=12, relief=RAISED, command=self.nouvelle_partie, text="Nouvelle Partie")
        self.bouton_partie.grid(row=2, column=self.partie.tableau_mines.dimension_colonne + 1)
        self.bouton_instructions = Button(self, width=12, relief=RAISED, command=self.instructions,
                                          text="Instructions")
        self.bouton_instructions.grid(row=3, column=self.partie.tableau_mines.dimension_colonne + 1)
        self.bouton_quitter = Button(self, width=12, relief=RAISED, command=self.quitter, text="Quitter")
        self.bouton_quitter.grid(row=4, column=self.partie.tableau_mines.dimension_colonne + 1)

        # On appelle une méthode création des boutons pour les cases à dévoiler
        self.intialiser_boutons_cases()

    def intialiser_boutons_cases(self):
        """Méthode qui crée les boutons de toutes les cases et
        lit l'évènement click droit de la souris pour dévoiler les cases

        Args: None

        Returns:
            None

        """

        # On va chercher nos attributs du tableau de mines et les mets dans deux variables
        dimension_rangee = self.partie.tableau_mines.dimension_rangee
        dimension_colonne = self.partie.tableau_mines.dimension_colonne

        # On crée l'ensemble de nos boutons du jeu sans dévoilement initial et on associe la commande lambda pour
        # lier l'évènement à la méthode évloiler_case
        for x in range(1, dimension_rangee + 1):
            for y in range(1, dimension_colonne + 1):
                self.dictionnaire_boutons[(x, y)] = Button(self, relief=RAISED, width=2, height=1,
                                                           command=lambda rangee=x, colonne=y:
                                                           self.devoiler_case(rangee, colonne))
                self.dictionnaire_boutons[(x, y)].grid(row=x, column=y)

    def devoiler_case(self, rangee, colonne):
        """Méthode qui dévoile les cases lorsqu'on click sur le bouton

        Args:
            rangee (int): la rangée du bouton enfoncé
            colonne (int): la colonne du bouton enfoncé

        Returns:
           self.nouvelle_partie(texte2) : On retourne la fonction nouvelle partie avec le texte correspondant

        """

        # On traite le cas où la case dévoilée est une mine
        if self.partie.tableau_mines.case_contient_mine(rangee, colonne):
            self.devoiler_tableau()
            return self.nouvelle_partie(texte2="Partie perdue ! Voulez-vous rejouer ?")

        # On traite le deuxième cas où la case dévoilée n'est pas minée et a une mine à proximité
        elif self.partie.tableau_mines.dictionnaire_cases[(rangee, colonne)].est_voisine_d_une_mine():
            texte = self.partie.tableau_mines.dictionnaire_cases[(rangee, colonne)].obtenir_nombre_mines_voisines()
            self.enfoncer_bouton(rangee, colonne, texte)

        # On traite le dernier cas où on doit lancer l'effet en cascade, car pas de mine à proximité
        else:
            self.devoiler_cascade(rangee, colonne)

        # On vérifie si toutes les cases sans mine sont dévoilées
        if not self.partie.tableau_mines.contient_cases_a_devoiler():
            self.devoiler_tableau()
            return self.nouvelle_partie(texte2="PARTIE GAGNÉE, BRAVO ! Voulez-vous rejouer ?")

    def devoiler_cascade(self, rangee, colonne):
        """
        Méthode qui dévoile en cascade de manière simplifiée le voisinage d'une case initiale qui avait 0 mine dans
        le voisinage

        Args:
            rangee (int):     Numéro de la rangée du bouton
            colonne (int):    Numéro de la colonne du bouton

        Returns:
            None

        """

        # On dévoile la première case sélectionnée
        self.enfoncer_bouton(rangee, colonne)

        # Pour dévoiler la ligne complète et la colonne complète jusqu'aux cases avec chiffre ou limites du tableau
        for mouvement in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nouvelle_rangee = rangee + mouvement[0]
            nouvelle_colonne = colonne + mouvement[1]
            # On valide si les coordonnées des cases observées sont dans le tableau selon les divers déplacements
            while self.partie.tableau_mines.valider_coordonnees(nouvelle_rangee, nouvelle_colonne):
                # On obtient le nombre de mines voisines et on le met dans la variable texte
                texte = self.partie.tableau_mines.dictionnaire_cases[(nouvelle_rangee, nouvelle_colonne)] \
                    .obtenir_nombre_mines_voisines()
                # Si la nouvelle case observée est aussi de valeur 0, on dévoile cette case avec le chiffre 0
                # en on continue notre déplacement à la case suivante
                if not self.partie.tableau_mines.dictionnaire_cases[(nouvelle_rangee, nouvelle_colonne)]. \
                        est_voisine_d_une_mine():
                    self.enfoncer_bouton(nouvelle_rangee, nouvelle_colonne, texte)
                    nouvelle_rangee += mouvement[0]
                    nouvelle_colonne += mouvement[1]
                else:
                    # On dévoile la case et quitte le while
                    self.enfoncer_bouton(nouvelle_rangee, nouvelle_colonne, texte)
                    break

    def enfoncer_bouton(self, rangee, colonne, texte=0):
        """Méthode qui change les propriétés des boutons pour les mettre enfoncer et faire apparaître le texte

        Args:
            rangee (int) : rangee du bouton à enfoncer
            colonne (int) : colonne du bouton à enfoncer
            texte (str) : texte du nombre de mines ou de la bombe dévoilée

        Returns:
            None
        """

        self.dictionnaire_boutons[(rangee, colonne)].config(state=DISABLED, relief=SUNKEN, text=texte)
        self.partie.tableau_mines.devoiler_case(rangee, colonne)

    def nouvelle_partie(self, texte="Démineur", texte2="Voulez-vous jouer une nouvelle partie ?"):
        """Méthode qui change les propriétés des boutons pour les mettre enfoncer et faire apparaître le texte

        Args:
            texte (str) : Texte en haut sur messagebox
            texte2 (str) : Texte pour poser la question sur le messagebox

        Returns:
            None
        """

        # On crée un messagebox avec les informations pour débuter une partie
        message_debut_partie = messagebox.askokcancel(texte, texte2)

        # Si on débute une nouvelle partie, on ininitalise le tableau et démarre une nouvelle partie
        if message_debut_partie:
            self.partie = Partie()
            self.intialiser_boutons_cases()

    def devoiler_tableau(self):
        """Méthode qui change les propriétés des boutons pour les mettre enfoncer et faire apparaître le texte

        Args: None

        Returns:
            None
        """

        # On affiche toutes les cases du tableau et on affiche un msgbox avec le message de partie perdue
        for x in range(1, self.partie.tableau_mines.dimension_rangee + 1):
            for y in range(1, self.partie.tableau_mines.dimension_colonne + 1):
                case = self.partie.tableau_mines.dictionnaire_cases[(x, y)]
                if case.contient_mine():
                    valeur_devoilee = "M"
                else:
                    valeur_devoilee = self.partie.tableau_mines.dictionnaire_cases[
                        (x, y)].obtenir_nombre_mines_voisines()
                # Pour afficher les cases on enfonce les boutons avec cette méthode
                self.enfoncer_bouton(x, y, valeur_devoilee)

    @staticmethod
    def instructions():
        """Méthode qui donne les instructions du jeu démineur avec un messagebox

        Args: None

        Returns:
            None
        """

        message_instructions = """
        Vous devez cliquer sur une des cases non-dévoilée.

        Le but du jeu est de dévoiler toutes les cases ne contenant pas de mine.

        Si vous dévoiler une case avec une mine, la lettre M sera indiqué et la partie sera perdue.

        Le chiffre indiqué indique le nombre de mines qui se retrouve dans les cases adjacentes (diagonales incluses).

        Bonne Chance !
        """

        messagebox.showinfo("Démineur", message_instructions)

    def quitter(self):
        """Création d'un message box lorsqu'on appuie sur le bouton quitter

        Args: None

        Returns:
            None

        """

        # On affiche un messagebox pour s'assurer que la personne veut vraiment quitter le jeu
        message_quitter_jeu = messagebox.askokcancel("Démineur", "Voulez-vous vraiment quitter ?")
        if message_quitter_jeu:
            self.quit()
        return None
