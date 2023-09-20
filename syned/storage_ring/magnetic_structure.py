from syned.syned_object import SynedObject

class MagneticStructure(SynedObject):
    """
    Base clase for magnetic structures (from where BM, Wiggler and Undulator will heritate)
    """
    def __init__(self):
        super().__init__()
