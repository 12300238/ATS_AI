class user:
    rh = False

    def __init__(self, name:str, mdp:str, cv_path:str):
        self.name = name
        self.mdp = mdp
        self.cv_path = cv_path

    def set_rh(self):
        self.rh = True

    def unset_rh(self):
        self.rh = False
