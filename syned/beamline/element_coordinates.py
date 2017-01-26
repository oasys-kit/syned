"""
Position of a beamline component within a beamline.
"""

class ElementCoordinates(object):
    def __init__(self, z, x=0.0,y=0.0, angle_radial=0.0, angle_azimuthal=0.0):
        """

        :param z: Longitudinal position.
        :param x: Off-axis shift in vertical direction.
        :param y: Off-axis shift in horizontal direction.
        :param angle_radial: Radial inclination angle.
        :param angle_azimuthal: Azimuthal inclination angle.
        :return:
        """
        self._z = z
        self._x = x
        self._y = y

        self._angle_radial = angle_radial
        self._angle_azimuthal = angle_azimuthal

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z

    def angleRadial(self):
        return self._angle_radial

    def angleAzimuthal(self):
        return self._angle_azimuthal