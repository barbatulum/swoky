from maya import cmds, mel
from .. import panel_tools
from . import ls


def multiply_anim_curves(factor):
    """
    Multiply animation curve by the given factor.
    """
    curves = ls.get_ge_or_node_curves(fallback_to_node_curves=False)

    for curve in curves:
        frames = cmds.keyframe(curve, q=True, timeChange=True)
        values = cmds.keyframe(curve, q=True, valueChange=True)
        for c, frame in enumerate(frames):
            cmds.setKeyframe(curve, t=frame, v=values[c] * factor)


def plot_keys():
    """
    Insert keyframes at all key frames of all anim curves
    """
    curves = ls.get_ge_or_node_curves(fallback_to_node_curves=False)

    all_frames = cmds.keyframe(curves, q=True, timeChange=True)
    if not all_frames:
        return
    cmds.setKeyframe(curves, insert=True, time=all_frames)


##############################################################################
# Cleanup ####################################################################
##############################################################################

def remove_keys_on_static_channel(
        shape=True,
        control_points=False,
        hierarchy=False
):
    """
    # pcStaticalizeChannel
    Hierarchy expansion options. Valid values are "above," "below," "both," and "none."
    """
    hierarchy = {True: 'below', False: 'none'}[hierarchy]
    cmds.delete(
        staticChannels=True,
        unitlessAnimationCurves=False,
        hierarchy=hierarchy,
        controlPoints=control_points,
        shape=shape
    )


def clear_static_key(tolerance=0, break_tangent=True, flat_inside_tangent=True):
    """
    # pcCleanlinear
    If not break_tangent, two keys needs to be preserved
    todo: if the curve gradually change and the value change in between are less than tolerance,
    it might be flatten out, needs a better algorithm. current one only suitable for horizontal kind of curve
    """
    curves = ls.get_ge_or_node_curves(fallback_to_node_curves=True)
    if not curves:
        return
    for curve in curves:
        keyframes = cmds.keyframe(curve, q=True, valueChange=True, indexValue=True) or []
        indexes = keyframes[::2]
        values = keyframes[1::2]
        frame_count = len(indexes)
        deleting_indexes = []
        if not keyframes:
            continue
        if not tolerance:
            if not len(values) > 1:
                continue
            unique_values = set(values)
            if len(unique_values) == 1:
                cmds.cutKey(curve, index=(indexes[1], indexes[-1]))
                continue

        for c, value in enumerate(values):
            if not c:
                continue
            if c + 1 >= frame_count:
                break
            if ((values[c - 1] - tolerance
                 < value
                 < values[c - 1] + tolerance)
                    and (values[c - 1] - tolerance
                         < values[c + 1]
                         < values[c - 1] + tolerance)
            ):
                if not break_tangent:
                    print('not break_tangent')
                    if (c + 2 < frame_count
                            and (values[c - 1] - tolerance
                                 < values[c + 2]
                                 < values[c - 1] + tolerance)
                            and (values[c + 1] - tolerance
                                 < values[c + 2]
                                 < values[c + 1] + tolerance)
                         ):
                        deleting_indexes.append(indexes[c])
                elif (values[c] - tolerance
                      < values[c + 1]
                      < values[c] + tolerance
                      ):
                    deleting_indexes.append(c)

        if not deleting_indexes:
            continue

        threshold = 3 if break_tangent else 4
        left_over_indexes = set(indexes) - set(deleting_indexes)
        if (len(left_over_indexes) < threshold
                and all(values[0] - tolerance < values[i] < values[0] + tolerance for i in left_over_indexes)
        ):
            cmds.cutKey(curve, index=(1, indexes[-1]))
            continue

        if break_tangent:
            for index in indexes:
                pre_key_deleted = (index - 1) in deleting_indexes
                post_key_deleted = (index + 1) in deleting_indexes
                if (index not in deleting_indexes
                        and (pre_key_deleted or post_key_deleted)
                        and index != indexes[0]
                        and index != indexes[-1]
                ):
                    cmds.keyTangent(curve, lock=False, index=(index,))
                if not flat_inside_tangent:
                    continue
                if pre_key_deleted:
                    cmds.keyTangent(curve, index=(index,), itt='flat')
                if post_key_deleted:
                    cmds.keyTangent(curve, index=(index,), ott='flat')

        cmds.cutKey(curve, index=[(i,) for i in deleting_indexes])


def clear_all_curves():
    """
    # pcClearAll
    :return:
    """
    selected = cmds.ls(sl=True)
    anim_curves = cmds.keyframe(selected, q=True, name=True)
    if anim_curves:
        cmds.cutKey(anim_curves)


def template_curves(curves=None):
    """
    Toggle the template-ness of animation curves.  # toggleGEtemplate
    """
    if not curves:
        curves = cmds.keyframe(q=True, name=True, sl=True)
    if not curves:
        return
    state = cmds.getAttr(curves[-1] + '.ktv', l=True)
    for curve in curves:
        cmds.setAttr(curve + '.ktv', l=not state)


def mute_curves():
    """
    Toggle the mute state of selected curves  # toggleGEmute
    """
    curves = cmds.keyframe(q=True, name=True, sl=True)
    if not curves:
        return
    conn = cmds.listConnections(
        curves[-1] + '.output', source=False, destination=True
    )
    init_state = {False: 'true', True: 'false'}[
        any(cmds.nodeType(i) == 'mute' for i in conn)
    ]
    # todo: make it cmds?
    mel.eval(
        'doMuteChannel graphEditor1FromOutliner -{};'.format(init_state)
    )
