from typeguard import typechecked
from .rendering import RenderedObject


@typechecked
class Solver:
    """
    represents a field solver

    Parent class for type safety, does not contain anything.
    """
    pass


@typechecked
class YeeSolver(Solver, RenderedObject):
    # note: has no parameters

    def _get_serialized(self) -> dict:
        return {
            "name": "Yee",
        }
