from ...rendering import RenderedObject
import typing


class Constant(RenderedObject):
    """
    unmodifiable property of a species

    Equal for all macroparticles, e.g. mass, charge, ionization levels etc.
    Owned by **exactly one** species.

    PIConGPU term: "particle flags"

    Parent class for actual SpeciesConstants

    A Constant can have the following dependencies:
    - species objects
        - dependency species must be available for the init manager
        - code for dependency species will be generated *before* the code for
          this species
    - attributes (types)
        - dependency attributes must be generated by *any* property on the
          species with this constant
        - there are no further checks employed, the constant is never shown the
          concrete attribute object of its species
    - constants (types)
        - dependency constants must be present before the initmanager performs
          any actions
        - checks on the value of constants are not possible, only if a constant
          of a given type is present
        - (the concrete constant that is being checked is never passed to this
          constant)
    """

    def __init__(self):
        raise NotImplementedError()

    def check(self) -> None:
        """
        ensure validity of self

        If ok passes silently, else raises.
        Intendend to check for invalid value (ranges), perhaps types etc.

        Must be overwritten in child implementation.
        """
        raise NotImplementedError()

    # note: forward declaration requires "Species" to be defined, which is not
    # always the case -> no type declaration
    def get_species_dependencies(self) -> typing.List:
        """
        get dependencies for definition

        Returns a list of species which this flags requires being present.
        Mainly intended for ionization flags, i.e. should typically return [].
        """
        raise NotImplementedError()

    def get_attribute_dependencies(self) -> typing.List[type]:
        """
        get required attributes (during execution)

        During execution some constants require an attribute to be present,
        e.g. the pusher required the Momentum attribute

        This method returns a list of attribute types which it requires on its
        species.
        """
        raise NotImplementedError()

    def get_constant_dependencies(self) -> typing.List[type]:
        """
        get required constants (during execution)

        Some constants (e.g. those selecting algorithms) may require other
        constants to be present.

        This method returns the types of constants that must be present for
        this constant to be valid.
        Checking the value of these dependency constants is **NOT** possible.

        Dependencies between constants **MAY** be circular.
        Rationale: Only presence of constants is checked, a reordering (as for
        inter-species-dependencies) is not performed, hence circular
        dependencies between constants can be handled.

        However, as self-references do not make sense (theoretically speaking
        are always true), they are considered a programmer error and therefore
        self-references are **NOT** allowed.

        This has no influence on the order of code generation.
        """
        raise NotImplementedError()