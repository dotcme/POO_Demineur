class Case:
    def __init__(self):
        self._minee = False
        self._decouverte = False
        self._marquee = False
        self._nb_mines_voisines = 0

    def est_minee(self):
        return self._minee

    def est_decouverte(self):
        return self._decouverte

    def est_marquee(self):
        return self._marquee

    def get_nb_mines_voisines(self):
        return self._nb_mines_voisines

    def poser_mine(self):
        self._minee = True

    def ajouter_mine_voisine(self):
        self._nb_mines_voisines += 1
