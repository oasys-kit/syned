
"""

Base class for a  wiggler.

"""

from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice

class Wiggler(InsertionDevice):

    def __init__(self, K_vertical = 0.0, K_horizontal = 0.0,period_length = 0.0, number_of_periods = 1):
        InsertionDevice.__init__(self,
                                 K_vertical=K_vertical,
                                 K_horizontal=K_horizontal,
                                 period_length=period_length,
                                 number_of_periods=number_of_periods)


