"""
Represents a beamline.

BeamlineComponents can be attached at positions(BeamlinePosition), i.e. longitudinal, off-axis and inclined.
We can iterate of the components, find their positions or look for a specific component.
"""

class Beamline(object):
    def __init__(self):
        self._components = []
        self._positions = []

    def _findComponentInsertionIndex(self, beamline_position):
        insert_index = 0

        for position in self._positions:
            if position.z()>beamline_position.z():
                break

            insert_index += 1

        return insert_index

    def attach_component_at(self, beamline_component, beamline_position):

        insert_index = self._findComponentInsertionIndex(beamline_position)

        self._components.insert(insert_index,beamline_component)
        self._positions.insert(insert_index,beamline_position)

    def position_of(self, beamline_component):
        component_index = self._components.index(beamline_component)
        position = self._positions[component_index]

        return position

    def component_by_index(self, index):
        if index < len(self._components):
            return self._components[index]

        return None

    def component_by_name(self, component_name):
        for component in self._components:
            if component.name() == component_name:
                return component

        return None

    def next_component(self, component):
        component_index = self._components.index(component)

        if len(self._components) <= component_index+1:
            next_component = None
        else:
            next_component = self._components[component_index+1]

        return next_component

    def previous_component(self, component):
        component_index = self._components.index(component)

        if component_index == 0:
            previous_component = None
        else:
            previous_component = self._components[component_index-1]

        return previous_component

    def __iter__(self):
        return iter(self._components)
