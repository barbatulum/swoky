from maya import cmds, mel


def clear_all_curves():
    """
    # pcClearAll
    :return:
    """
    selected = cmds.ls(sl=True)
    anim_curves = cmds.keyframe(selected, q=True, name=True)
    if anim_curves:
        cmds.cutKey(anim_curves)

def get_selected_curves(fallback_to_nodes=False):
    """
    If not fallback_to_nodes, the function return selected only.
    """
    return cmds.keyframe(
        q=True, name=True, **{'sl': fallback_to_nodes}
    ) or []


def get_anim_curves(
    fallback_to_node_curves=False,
    order=()
):
    """
    Get: - Selected curves (only if there's one)
         - shown curve in graph editor
         - anim curves of selected nodes
    """
    working_graph_editor = panel_tools.get_a_graph_editor()
    curves = None
    if working_graph_editor:
        curves = get_selected_curves(fallback_to_nodes=False)
    if not curves:
        curves = get_shown_curve(working_graph_editor)
    if not curves and fallback_to_node_curves:
        curves = get_selected_node_curves()
    return curves


def multiply_anim_curves(factor):
    """
    Multiply animation curve by the given factor.
    """
    curves = get_anim_curves(fallback_to_node_curves=False)

    for curve in curves:
        frames = cmds.keyframe(curve, q=True, timeChange=True)
        values = cmds.keyframe(curve, q=True, valueChange=True)
        for c, frame in enumerate(frames):
            cmds.setKeyframe(curve, t=frame, v=values[c] * factor)


def get_selected_node_curves():
    """
    Returns anim curves of selected nodes.
    """
    nodes = cmds.ls(sl=True)
    if nodes:
        return cmds.keyframe(nodes, q=True, name=True) or []


def get_anim_curve_target(anim_curve):
    """
    Get connected target attributes of given anim curves.
    """
    connected_attrs = []
    for curve in anim_curve:
        output = curve + '.output'
        dst_plugs = cmds.listConnections(output, source=False, destination=True, plugs=True) or ()
        connected_attrs.extend(dst_plugs)
    return connected_attrs

def get_selected_key_frames():
    """
    Get selected anim curves and frames as {anim_curves:[frames]}
    """
    selection = dict()
    selected_curves = cmds.keyframe(q=1, name=1, sl=True) or []
    for curve in selected_curves:
        selection.setdefault(curve, []).extend(
            cmds.keyframe(curve, q=1, timeChange=True, selected=True)
        )
    return selection


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

def remove_static_channel_keys(
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


def plot_keys():
    """
    Insert keyframes at all key frames of all anim curves
    """
    curves = get_anim_curves(fallback_to_node_curves=False)

    all_frames = cmds.keyframe(curves, q=True, timeChange=True)
    if not all_frames:
        return
    cmds.setKeyframe(curves, insert=True, time=all_frames)
