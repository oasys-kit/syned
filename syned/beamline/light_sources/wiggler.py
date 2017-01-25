__author__ = 'labx'
"""
Implements a wiggler.
"""

from syned.beamline.light_sources.insertion_device import InsertionDevice

class Wiggler(InsertionDevice):

    def __init__(self, K, period_length, periods_number):
        InsertionDevice.__init__(self, K, 0.0, period_length, periods_number)