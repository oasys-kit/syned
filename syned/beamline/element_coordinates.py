"""
Position of a beamline component within a beamline.
"""

class ElementCoordinates(object):
    def __init__(self, p = 0.0, q = 0.0, angle_radial=0.0, angle_azimuthal=0.0):
        """

        :param p: distance from previous element.
        :param q: distance to next element.
        :param angle_radial: Radial inclination angle.
        :param angle_azimuthal: Azimuthal inclination angle.
        :return:
        """
        self._p = p
        self._q = q

        self._angle_radial = angle_radial
        self._angle_azimuthal = angle_azimuthal


    def p(self):
        return self._p

    def q(self):
        return self._q

    def angleRadial(self):
        return self._angle_radial

    def angleAzimuthal(self):
        return self._angle_azimuthal