from enum import Enum


class Niveau(Enum):
    FACILE = (9, 9, 10)
    MOYEN = (16, 16, 40)
    DIFFICILE = (16, 30, 99)

    def __init__(self, nb_lignes, nb_colonnes, nb_mines):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.nb_mines = nb_mines
