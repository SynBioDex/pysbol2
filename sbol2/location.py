from .identified import Identified
from .constants import *
from .property import IntProperty
from .property import LiteralProperty
from .property import OwnedObject
from .property import ReferencedObject
from .property import URIProperty
from rdflib import URIRef


class Location(Identified):
    """The Location class specifies the strand orientation of a Component."""
    def __init__(self, uri=URIRef('example'), orientation=SBOL_ORIENTATION_INLINE,
                 type_uri=SBOL_LOCATION):
        super().__init__(type_uri, uri)
        self._orientation = URIProperty(self, SBOL_ORIENTATION,
                                        '1', '1', [], orientation)
        self.sequence = ReferencedObject(self, SBOL_SEQUENCE_PROPERTY,
                                         SBOL_SEQUENCE, '0', '1', [])

    @property
    def orientation(self):
        return self._orientation.value

    @orientation.setter
    def orientation(self, new_orientation):
        self._orientation.set(new_orientation)


class Range(Location):
    """A Range object specifies a region via discrete,
    inclusive start and end positions that correspond to indices
    for characters in the elements String of a Sequence.
    Note that the index of the first location is 1,
    as is typical practice in biology, rather than 0,
    as is typical practice in computer science."""
    def __init__(self, uri=URIRef('example'), start=1, end=2, type_uri=SBOL_RANGE):
        super().__init__(uri=uri, type_uri=type_uri)
        self._start = IntProperty(self, SBOL_START, '0', '1', None, start)
        self._end = IntProperty(self, SBOL_END, '0', '1', None, end)

    @property
    def start(self):
        return self._start.value

    @start.setter
    def start(self, val):
        self._start.set(val)

    @property
    def end(self):
        return self._end.value

    @end.setter
    def end(self, val):
        self._end.set(val)

    def precedes(self, comparand):
        if self.end < comparand.start:
            return comparand.start - self.end
        else:
            return 0

    def follows(self, comparand):
        if self.start > comparand.end:
            return comparand.end - self.start
        else:
            return 0

    def adjoins(self, comparand):
        if comparand.end + 1 == self.start:
            return 1
        if self.end + 1 == comparand.start:
            return 1
        return 0

    def contains(self, comparand):
        if self.start <= comparand.start and self.end >= comparand.end:
            return comparand.length()
        else:
            return 0

    def overlaps(self, comparand):
        if self.start == comparand.start and self.end == comparand.end:
            return 0
        elif self.start < comparand.start and self.end < comparand.end \
                and self.end >= comparand.start:
            return self.end - comparand.start + 1
        elif self.start > comparand.start and self.end > comparand.end \
                and self.start <= comparand.end:
            return comparand.end - self.start + 1
        elif comparand.contains(self):
            return comparand.contains(self)
        else:
            return 0

    def length(self):
        return self.end + 1 - self.start


class Cut(Location):
    """The Cut class specifies a location between
    two coordinates of a Sequence's elements."""
    def __init__(self, uri=URIRef('example'), at=1, type_uri=SBOL_CUT):
        super().__init__(uri=uri, type_uri=type_uri)
        self._at = IntProperty(self, SBOL_AT, '1', '1', [], at)

    @property
    def at(self):
        return self._at.value

    @at.setter
    def at(self, new_at):
        self._at.set(new_at)


class GenericLocation(Location):
    """the GenericLocation class is included as a starting point
    for specifying regions on Sequence objects with
    encoding properties other than IUPAC and potentially nonlinear structure.
    This class can also be used to set the orientation of a SequenceAnnotation
    and any associated Component when their parent ComponentDefinition is
    a partial design that lacks a Sequence."""
    def __init__(self, uri=URIRef('example'), type_uri=SBOL_GENERIC_LOCATION):
        super().__init__(uri=uri, type_uri=type_uri)


class OwnedLocation(OwnedObject):
    def __init__(self, property_owner, sbol_uri, lower_bound, upper_bound,
                 validation_rules=None, first_object=None):
        """Initialize a container and optionally put the first object in it.
        If validation rules are specified, they will be checked upon initialization.

        builder is a function that takes a single argument, a string,
        and constructs an object of appropriate type for this
        OwnedObject instance. For instance, if this OwnedObject is
        intended to hold ComponentDefinitions, then the builder should
        return an object of type ComponentDefinition.

        """
        super().__init__(property_owner, sbol_uri, Location, lower_bound, upper_bound,
                         validation_rules, first_object)

    def createRange(self, uri=URIRef('example')):
        return self.create(uri, Range)

    def createCut(self, uri=URIRef('example')):
        return self.create(uri, Cut)

    def createGenericLocation(self, uri=URIRef('example')):
        return self.create(uri, GenericLocation)

    def getRange(self, uri=''):
        range = self.get(uri)
        if isinstance(range, Range):
            return range
        raise TypeError('Found object is not of type Range')

    def getCut(self, uri=''):
        cut = self.get(uri)
        if isinstance(cut, Cut):
            return cut
        raise TypeError('Found object is not of type Cut')