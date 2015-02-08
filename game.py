class Game(object):
    """
    Holds all variables relevant to this game session.
    Loaded a pickled instance of Game restores a game session.
    """
    def __init__(self):
        self.player_name = 'Kalinae'
        self.player_gold = 0
        self.player_mHp = 100
        self.player_hp = self.player_mHP
        self.player_mAp = 100
        self.player_ap = self.player_mAp
        self.player_str = 10
        self.player_dex = 10
        # ... more player variables
        self.boiz = []
        # self.boiz.append( new Boi(...

