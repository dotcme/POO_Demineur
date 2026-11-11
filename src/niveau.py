from enum import Enum


class Niveau(Enum):
    """ Les 3 niveaux de difficulté : (nb lignes, nb colonnes, nb mines).
    """

    FACILE = (9, 9, 10)
    MOYEN = (16, 16, 40)
    DIFFICILE = (16, 30, 99)

    def __init__(self, nb_lignes, nb_colonnes, nb_mines):
        """ Initialisation d'un niveau.

        Args:
            nb_lignes (int): nb lignes de la grille
            nb_colonnes (int): nb colonnes de la grille
            nb_mines (int): nb mines à placer
        """
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.nb_mines = nb_mines
