from .attribute import Attribute


class Position(Attribute):
    """
    Position of a macroparticle
    """
    PICONGPU_NAME = "position<position_pic>"

    def __init__(self):
        pass
