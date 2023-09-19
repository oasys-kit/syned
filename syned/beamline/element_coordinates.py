"""
Position coordinates of a beamline component.
"""

from syned.syned_object import SynedObject

class ElementCoordinates(SynedObject):
    """

    """
    def __init__(self, p = 0.0, q = 0.0, angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=None):
        """

        Parameters
        ----------
        p : float, optional
            distance from previous element in m.
        q : float, optional
            distance to next element in m.
        angle_radial : float, optional
            Radial inclination angle in rads.
        angle_azimuthal : float, optional
            Azimuthal inclination angle in rads.
        angle_radial_out : float, optional
            The radial angle in rads in the output direction (default=None, the same as angle_radial).

        """
        self._p               = p
        self._q               = q
        self._angle_radial    = angle_radial
        self._angle_azimuthal = angle_azimuthal
        self._angle_radial_out = angle_radial_out

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("p",                "distance from previous continuation plane", "m"    ),
                    ("q",                "distance to next continuation plane",       "m"    ),
                    ("angle_radial",     "incident angle [to normal]",                "rad"  ),
                    ("angle_radial_out", "output angle [to normal]",                  "rad"),
                    ("angle_azimuthal",  "rotation along beam axis",                  "rad"  ),
                ])

    def p(self):
        """
        Returns the distance from previous element.

        Returns
        -------
        float

        """
        return self._p

    def q(self):
        """
        Returns the distance to next element.

        Returns
        -------
        float

        """
        return self._q

    def angle_radial(self):
        """
        Returns the radial angle.

        Returns
        -------
        float

        """
        return self._angle_radial

    def angle_radial_out(self):
        """
        Returns the radial angle in the output direction.

        Returns
        -------
        float

        """
        if self._angle_radial_out is None:
            return self.angle_radial()
        else:
            return self._angle_radial_out

    def angle_azimuthal(self):
        """
        Returns the azimuthal angle.

        Returns
        -------
        float

        """
        return self._angle_azimuthal

    def set_positions(self, p=0.0, q=0.0, angle_radial=0.0, angle_radial_out=None, angle_azimuthal=0.0):
        """
        Sets the coordinates.

        Parameters
        ----------
        p : float, optional
            distance from previous element in m.
        q : float, optional
            distance to next element in m.
        angle_radial : float, optional
            Radial inclination angle in rads.
        angle_azimuthal : float, optional
            Azimuthal inclination angle in rads.
        angle_radial_out : float, optional
            The radial angle in rads in the output direction (default=None, the same as angle_radial).

        """
        self._p = p
        self._q = q
        self._angle_radial = angle_radial
        self._angle_radial_out = angle_radial_out
        self._angle_azimuthal = angle_azimuthal

    def get_positions(self):
        """
        Gets the coordinates.

        Returns
        -------
        tuple
            (p, q, angle_radial, angle_radial_out, angle_azimuthal)

        """
        return self.p(), \
            self.q(), \
            self.angle_radial(), \
            self.angle_radial_out(), \
            self.angle_azimuthal()

    def set_p_and_q(self, p=0.0, q=0.0):
        """
        Set the distances p and q.

        Parameters
        ----------
        p : float, optional
            distance from previous element in m.
        q : float, optional
            distance to next element in m.

        """
        self._p = p
        self._q = q

    def get_p_and_q(self):
        """
        Gets p and q.

        Returns
        -------
        tuple
            (p,q).

        """
        return self.p(), self.q()

    def set_angles(self, angle_radial=0.0, angle_radial_out=None, angle_azimuthal=0.0):
        """
        Sets the angles.

        Parameters
        ----------
        angle_radial : float, optional
            Radial inclination angle in rads.
        angle_azimuthal : float, optional
            Azimuthal inclination angle in rads.
        angle_radial_out : float, optional
            The radial angle in rads in the output direction (default=None, the same as angle_radial).

        Returns
        -------

        """
        self._angle_radial = angle_radial
        self._angle_radial_out = angle_radial_out
        self._angle_azimuthal = angle_azimuthal

    def get_angles(self):
        """
        Get the angles.

        Returns
        -------
        tuple
            (angle_radial, angle_radial_out, angle_azimuthal)

        """
        return self.angle_radial(), self.angle_radial_out(), self.angle_azimuthal()
