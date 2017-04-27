

class WidgetDecorator(object):

    @classmethod
    def syned_input_data(cls):
        return ("Syned Data", object, "receive_syned_data")

    def receive_syned_data(self, data):
        raise NotImplementedError("Should be implemented")