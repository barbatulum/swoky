import math

from maya import cmds
from maya.api import OpenMaya as om2
from maya.api import OpenMayaAnim as oma2


def get_matrix_data(node_mobj):
    matrix_data = om2.MFnMatrixData(
        om2.MPlug(
            node_mobj,
            om2.MFnDependencyNode(
                node_mobj
            ).attribute("worldMatrix")
        ).elementByLogicalIndex(0).asMObject()
    )
    return matrix_data


def get_animation_full_frames(includes=False):
    """
    Get floor and ceil of ast/aet
    """
    frame_range = [
        math.floor(oma2.MAnimControl.animationStartTime().value),
        math.ceil(oma2.MAnimControl.animationEndTime().value) + 1
    ]

    frames = list(range(*(int(frame) for frame in frame_range)))
    if includes:
        frames = sorted(set(frames + frame_range))
    return frames


def validate_settable_attrs(node, attrs):
    valid = []
    for attr in attrs:
        attr = '{}.{}'.format(node, attr)
        if not cmds.objExists(attr):
            valid = False
            break
        if not cmds.getAttr(attr, settable=True):
            valid = False
            break
        if cmds.listConnections(attr, source=True, destination=False):
            valid = False
            break
        valid.append(attr)
    return valid