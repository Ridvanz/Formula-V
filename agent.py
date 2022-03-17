class Agent:
    """Plays the game."""

    def __init__(self):
        self.saved = None
    
    def act(self, states):
        
        u_x = 0
        u_y = 1
        
        return u_x, u_y