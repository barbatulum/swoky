import math
from maya.api import OpenMaya as om2

def get_vector_from_rotation(rotation, aim_vector=(0, 0, -1), rotate_order="xyz"):
    """
    get the vector of an euler rotation.
    """
    if not isinstance(aim_vector, om2.MVector):
        aim_vector = om2.MVector(*aim_vector)
    for axis in rotate_order:
        aim_vector = aim_vector.rotateBy(
            {"x": 0, "y": 1, "z": 2}[axis]
            , math.radians(rotation["xyz".index(axis)])
        )
    return aim_vector