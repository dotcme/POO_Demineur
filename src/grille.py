import random

from case import Case


class Grille:
    """ La grille du démineur. Les mines sont placées au premier coup.
    """

    def __init__(self, nb_lignes, nb_colonnes, nb_mines):
        """ Initialisation de la grille avec des cases vides, sans mines.

        Args:
            nb_lignes (int): nb lignes de la grille
            nb_colonnes (int): nb colonnes de la grille
            nb_mines (int): nb mines à placer au premier coup
        """
        self._nb_lignes = nb_lignes
        self._nb_colonnes = nb_colonnes
        self._nb_mines = nb_mines
        self._cases = [[Case() for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        self._mines_placees = False
        self._nb_cases_decouvertes = 0

    def est_dans_grille(self, lig, col):
        """ Vérifie que la position est bien dans la grille.

        Args:
            lig (int): ligne, à partir de 0
            col (int): colonne, à partir de 0

        Returns:
            bool: True si la case existe
        """
        return 0 <= lig < self._nb_lignes and 0 <= col < self._nb_colonnes

    def _voisins(self, lig, col):
        """ Liste des positions autour d'une case.

        Args:
            lig (int): ligne de la case
            col (int): colonne de la case

        Returns:
            list: tuples (ligne, colonne) des voisins, 8 au maximum
        """
        voisins = []

        for dl in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dl == 0 and dc == 0:
                    continue
                if self.est_dans_grille(lig + dl, col + dc):
                    voisins.append((lig + dl, col + dc))

        return voisins

    def placer_mines(self, lig_depart, col_depart):
        """ Placement aléatoire des mines, sauf sur la case de départ et autour.

        Args:
            lig_depart (int): ligne du premier coup
            col_depart (int): colonne du premier coup
        """
        interdites = self._voisins(lig_depart, col_depart)
        interdites.append((lig_depart, col_depart))
        possibles = []

        for lig in range(self._nb_lignes):
            for col in range(self._nb_colonnes):
                if (lig, col) not in interdites:
                    possibles.append((lig, col))

        for lig, col in random.sample(possibles, self._nb_mines):
            self._cases[lig][col].poser_mine()

        self._calculer_mines_voisines()
        self._mines_placees = True

    def _calculer_mines_voisines(self):
        """ Calcul du nb de mines voisines pour chaque case.
        """
        for lig in range(self._nb_lignes):
            for col in range(self._nb_colonnes):
                if self._cases[lig][col].est_minee():
                    for l, c in self._voisins(lig, col):
                        self._cases[l][c].ajouter_mine_voisine()

    def decouvrir(self, lig, col):
        """ Découvre une case. Place les mines si c'est le premier coup et
        ouvre les voisins si la case n'a aucune mine autour.

        Args:
            lig (int): ligne de la case
            col (int): colonne de la case

        Returns:
            bool: True si la case est une mine
        """
        case = self._cases[lig][col]
        if case.est_decouverte() or case.est_marquee():
            return False

        if not self._mines_placees:
            self.placer_mines(lig, col)

        if case.decouvrir():
            return True

        self._nb_cases_decouvertes += 1
        if case.get_nb_mines_voisines() == 0:
            self._ouvrir_zone(lig, col)
        return False

    def _ouvrir_zone(self, lig, col):
        """ Ouvre les voisins d'une case à 0, de façon récursive.

        Args:
            lig (int): ligne de la case
            col (int): colonne de la case
        """
        for l, c in self._voisins(lig, col):
            voisine = self._cases[l][c]
            if not voisine.est_decouverte() and not voisine.est_marquee():
                voisine.decouvrir()
                self._nb_cases_decouvertes += 1
                if voisine.get_nb_mines_voisines() == 0:
                    self._ouvrir_zone(l, c)

    def changer_marque(self, lig, col):
        """ Pose ou enlève un drapeau sur une case.

        Args:
            lig (int): ligne de la case
            col (int): colonne de la case

        Returns:
            bool: False si la case est déjà découverte, True sinon
        """
        return self._cases[lig][col].changer_marque()

    def nb_marques(self):
        """ Compte les drapeaux posés sur la grille.

        Returns:
            int: nb de drapeaux
        """
        nb = 0
        for ligne in self._cases:
            for case in ligne:
                if case.est_marquee():
                    nb += 1
        return nb

    def est_gagnee(self):
        """ Vérifie si toutes les cases sans mine sont découvertes.

        Returns:
            bool: True si la partie est gagnée
        """
        return self._nb_cases_decouvertes == self._nb_lignes * self._nb_colonnes - self._nb_mines

    def devoiler_mines(self):
        """ Découvre toutes les mines à la fin de la partie.
        """
        for ligne in self._cases:
            for case in ligne:
                if case.est_minee():
                    case.decouvrir()

    def __str__(self):
        """ Affichage de la grille avec les numéros de lignes et colonnes.

        Returns:
            str: la grille sous forme de texte
        """
        texte = "    "

        for col in range(self._nb_colonnes):
            if col + 1 < 10:
                texte += "  " + str(col + 1)
            else:
                texte += " " + str(col + 1)
        texte += "\n"

        for lig in range(self._nb_lignes):
            if lig + 1 < 10:
                texte += "  " + str(lig + 1) + " "
            else:
                texte += " " + str(lig + 1) + " "

            for col in range(self._nb_colonnes):
                texte += "  " + str(self._cases[lig][col])
            texte += "\n"

        return texte
