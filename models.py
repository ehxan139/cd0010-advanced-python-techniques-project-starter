"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        if info.get('designation') is None or info['designation'] == '':
            self.designation = None
        else:
            self.designation = info['designation']

        if info.get('name') is None or info['name'] == '':
            self.name = None
        else:
            self.name = info['name']

        if info.get('diameter') is None or info['diameter'] == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(info['diameter'])

        if info.get('hazardous') is None or info['hazardous'] == '':
            # self.hazardous = None
            self.hazardous = False
        else:
            self.hazardous = info['hazardous'] == "Y"

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is None:
            return self.designation
        else:
            return self.designation + " (" + self.name + ")"

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return (f"{self.fullname} has a diameter of {self.diameter:.3f} "
                    f"km and is potentially hazardous.")
        else:
            return (f"{self.fullname} has a diameter of {self.diameter:.3f} "
                    f"km and is not potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        if info.get('_designation') is None or info['_designation'] == '':
            self._designation = None
        else:
            self._designation = info['_designation']

        if info.get('time') is None or info['time'] == '':
            self.time = None
        else:
            self.time = cd_to_datetime(info['time'])

        if info.get('distance') is None or info['distance'] == '':
            self.distance = float('nan')
        else:
            self.distance = float(info['distance'])

        if info.get('velocity') is None or info['velocity'] == '':
            self.velocity = float('nan')
        else:
            self.velocity = float(info['velocity'])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s  approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
         in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time}, '{self.neo.fullname}' approaches Earth at a "
                f"distance of {self.distance:.2f} au and a velocity of "
                f"{self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of  this object."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
