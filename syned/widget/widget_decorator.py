
from syned.beamline.beamline import Beamline

class WidgetDecorator(object):

    @classmethod
    def syned_input_data(cls):
        return [("SynedData", Beamline, "receive_syned_data")]

    @classmethod
    def append_syned_input_data(cls, inputs):
        for input in WidgetDecorator.syned_input_data():
            inputs.append(input)

    def receive_syned_data(self, data):
        raise NotImplementedError("Should be implemented")