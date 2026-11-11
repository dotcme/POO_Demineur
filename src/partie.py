from grille import Grille
from niveau import Niveau


class Partie:
    """ Déroulement d'une partie de démineur en console.
    """

    def __init__(self):
        """ Initialisation de la partie, le niveau et la grille sont créés au lancement.
        """
        self._niveau = None
        self._grille = None
        self._terminee = False
        self._gagnee = False
        self._nb_coups = 0

    def _choisir_niveau(self):
        """ Demande au joueur de choisir un niveau.

        Returns:
            Niveau: le niveau choisi
        """
        print("Choisissez un niveau :")
        print("1: Facile (9x9, 10 mines)")
        print("2: Moyen (16x16, 40 mines)")
        print("3: Difficile (16x30, 99 mines)")

        niveaux = {"1": Niveau.FACILE, "2": Niveau.MOYEN, "3": Niveau.DIFFICILE}
        choix = input("> ").strip()

        while choix not in niveaux:
            choix = input("Choix invalide, recommencez : ").strip()

        return niveaux[choix]

    def afficher(self):
        """ Affiche la grille, le nb de coups et les drapeaux restants.
        """
        print()
        print(self._grille)
        print("Coups joués: " + str(self._nb_coups))
        print("Drapeaux restant: " + str(self._niveau.nb_mines - self._grille.nb_marques()))

    def _demander_coup(self):
        """ Demande une action au joueur jusqu'à avoir une saisie valide.

        Returns:
            tuple: (action, ligne, colonne), ligne et colonne à partir de 0
        """
        while True:
            saisie = input("Action (d pour decouvrir, m pour marquer) puis ligne et colonne: ").split()

            if len(saisie) != 3 or saisie[0] not in ("d", "m"):
                print("Exemple : d 3 5 ou m 3 5")
                continue

            try:
                lig = int(saisie[1]) - 1
                col = int(saisie[2]) - 1
            except ValueError:
                print("La ligne et la colonne doivent etre des nombres")
                continue

            if not self._grille.est_dans_grille(lig, col):
                print("Cette case n'est pas dans la grille")
                continue

            return saisie[0], lig, col

    def jouer_coup(self, action, lig, col):
        """ Joue un coup sur la grille et met à jour l'état de la partie.

        Args:
            action (str): "d" pour découvrir, "m" pour marquer
            lig (int): ligne de la case
            col (int): colonne de la case
        """
        self._nb_coups += 1


        if action == "m":
            if not self._grille.changer_marque(lig, col):
                print("Déja découverte")
            return

        if self._grille.decouvrir(lig, col):
            self._terminee = True
            self._gagnee = False
        else:
            self._verifier_fin()

    def _verifier_fin(self):
        """ Termine la partie si le joueur a gagné.
        """
        if self._grille.est_gagnee():
            self._terminee = True
            self._gagnee = True


    def est_terminee(self):
        """ Indique si la partie est finie.

        Returns:
            bool: True si la partie est terminée
        """
        return self._terminee

    def _demander_rejouer(self):
        """ Demande au joueur s'il veut rejouer.

        Returns:
            bool: True si le joueur répond "o"
        """
        reponse = input("Voulez-vous rejouer ? (o/n) ").strip()
        while reponse not in ("o", "n"):
            reponse = input("Repondez par o ou n: ").strip()
        return reponse == "o"

    def lancer(self):
        """ Boucle principale : choix du niveau, partie, puis proposition de rejouer.
        """
        rejouer = True

        while rejouer:
            self._niveau = self._choisir_niveau()
            self._grille = Grille(self._niveau.nb_lignes, self._niveau.nb_colonnes, self._niveau.nb_mines)
            self._terminee = False
            self._gagnee = False
            self._nb_coups = 0

            while not self.est_terminee():
                self.afficher()
                action, lig, col = self._demander_coup()
                self.jouer_coup(action, lig, col)

            self._grille.devoiler_mines()
            self.afficher()

            if self._gagnee:
                print("Bravo!!! tu as gagné :))")
            else:
                print(":((( perdu")

            rejouer = self._demander_rejouer()
