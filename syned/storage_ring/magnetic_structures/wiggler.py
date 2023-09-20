from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice

class Wiggler(InsertionDevice):
    """
    Constructor.

    Parameters
    ----------
    K_vertical : float, optional
        The deflection K parameter corresponding to magnetic field in the vertical direction.
    K_horizontal : float, optional
        The deflection K parameter corresponding to magnetic field in the horizontal direction.
    period_length : float, optional
        The ID period in m.
    number_of_periods : float, optional
        The number of periods. It may be a float, considering that number_of_periods = ID_length / period_length.

    """

    def __init__(self, K_vertical = 0.0, K_horizontal = 0.0,period_length = 0.0, number_of_periods = 1):
        InsertionDevice.__init__(self,
                                 K_vertical=K_vertical,
                                 K_horizontal=K_horizontal,
                                 period_length=period_length,
                                 number_of_periods=number_of_periods)


