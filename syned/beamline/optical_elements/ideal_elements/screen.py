from syned.beamline.optical_elements.ideal_elements.ideal_element import IdealElement

class Screen(IdealElement):
    """
    Defines an ideal screen (a plane perpendiculat to the optical axis).

    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.

    """
    def __init__(self, name="Undefined"):
        IdealElement.__init__(self, name=name)