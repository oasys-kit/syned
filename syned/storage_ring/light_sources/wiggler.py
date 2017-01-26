
"""
Implements a wiggler.
"""

from syned.storage_ring.light_sources.insertion_device import InsertionDevice

class Wiggler(InsertionDevice):

    def __init__(self,
                 name="Undefined",
                 K = 0.0,
                 period_length = 0.0,
                 periods_number = 1):
        InsertionDevice.__init__(self,
                                 name = name,
                                 K_vertical=K,
                                 K_horizontal=0.0,
                                 period_length=period_length,
                                 periods_number=periods_number)