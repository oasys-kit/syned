
from syned.beamline.beamline import Beamline

class WidgetDecorator(object):
    """
    Definition of a widget decorator (to be used by widget implementations).

    """

    @classmethod
    def syned_input_data(cls):
        """
        A string to help defining SYNED data in OASYS.

        Returns
        -------
        list
            [("SynedData", Beamline, "receive_syned_data")]

        """
        return [("SynedData", Beamline, "receive_syned_data")]

    @classmethod
    def append_syned_input_data(cls, inputs):
        """

        Parameters
        ----------
        inputs


        """
        for input in WidgetDecorator.syned_input_data():
            inputs.append(input)

    def receive_syned_data(self, data):
        """
        To be implemented in the main object.

        Parameters
        ----------
        data

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError("Should be implemented")