class Case:
    """ Une case de la grille, minée ou non, avec son état et le nb de mines autour.
    """

    def __init__(self):
        """ Initialisation d'une case cachée, sans mine et sans drapeau.
        """
        self._minee = False
        self._decouverte = False
        self._marquee = False
        self._nb_mines_voisines = 0

    def est_minee(self):
        """ Indique si la case contient une mine.

        Returns:
            bool: True si la case est minée
        """
        return self._minee

    def est_decouverte(self):
        """ Indique si la case a été découverte.

        Returns:
            bool: True si la case est découverte
        """
        return self._decouverte

    def est_marquee(self):
        """ Indique si la case a un drapeau.

        Returns:
            bool: True si la case est marquée
        """
        return self._marquee

    def get_nb_mines_voisines(self):
        """ Renvoie le nb de mines autour de la case.

        Returns:
            int: nb de mines dans les 8 cases voisines
        """
        return self._nb_mines_voisines

    def poser_mine(self):
        """ Place une mine sur la case.
        """
        self._minee = True

    def ajouter_mine_voisine(self):
        """ Ajoute 1 au nb de mines voisines.
        """
        self._nb_mines_voisines += 1

    def decouvrir(self):
        """ Découvre la case, sauf si elle est déjà découverte ou marquée.

        Returns:
            bool: True si la case découverte est une mine
        """
        if self._decouverte or self._marquee:
            return False
        self._decouverte = True
        return self._minee

    def changer_marque(self):
        """ Pose le drapeau s'il n'y en a pas, l'enlève sinon.

        Returns:
            bool: False si la case est déjà découverte, True sinon
        """
        if self._decouverte:
            return False
        self._marquee = not self._marquee
        return True

    def __str__(self):
        """ Affichage de la case.

        Returns:
            str: "F" drapeau, "." cachée, "*" mine, " " vide ou le nb de mines voisines
        """
        if self._marquee:
            return "F"
        if not self._decouverte:
            return "."
        if self._minee:
            return "*"
        if self._nb_mines_voisines == 0:
            return " "
        return str(self._nb_mines_voisines)
