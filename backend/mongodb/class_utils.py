class user:
    """un profile utilisateur"""
    rh = False

    def __init__(self, name:str, mdp:str, cv_path:str):
        self.name = name
        self.mdp = mdp
        self.cv_path = cv_path

    def set_rh(self):
        """définit l'utilisateur comme rh"""
        self.rh = True

    def unset_rh(self):
        """retire le rôle rh à l'utilisateur"""
        self.rh = False
