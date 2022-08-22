from maya import cmds, mel

from ..gui.graph_editor import get_a_graph_editor


def set_key_tangent(*args):
    """
    # pcTgTypeSwi
    Wrapper of setting key tangents
    # tangent_type: spline, flat, linear
    """
    if len(args) == 1:
        args = args * 2
    cmds.keyTangent(inTangentType=args[0], outTangentType=args[1])


def toggle_tangent_break():
    """
    # pcTangentBreakSwitch
    Toggle the break-ness of tangent
    """
    lock_states = cmds.keyTangent(q=True, lock=True)
    if lock_states:
        cmds.keyTangent(lock=not lock_states[-1])


def select_tangent_handle(side=(True, False), set_tool=True):
    """
    Select in or out tangent of selected anim curves.
    """
    tangent_args = (True, False)
    if side:
        tangent_args = (False, True)

    curve_frame_map = {}
    anim_curves = cmds.keyframe(q=True, selected=True, name=True)
    if not anim_curves:
        return
    for curve in anim_curves:
        keyframes = cmds.keyframe(
            curve, q=True, selected=True, timeChange=True
        )
        if keyframes:
            curve_frame_map[curve] = keyframes

    for c, curve in enumerate(anim_curves):
        frames = curve_frame_map.get(curve, [])
        for d, frame in enumerate(frames):
            cmds.selectKey(
                curve,
                add=any((c, d)),
                time=(frame,),
                inTangent=tangent_args[0],
                outTangent=tangent_args[1]
            )
    if set_tool:
        cmds.setToolTo(mel.eval("$temp=$gMove"))


def set_tangent(
    tangent_type,
    current_time=True,
    in_view_message=True
):
    """
    Fallback order:
    1. Works on selected curve/keys
        if graph editor is visible.
    2. Visible curves at the current time
        if graph editor is visible and no curve is selected.
    3. Works on selected objects at the current time
        if graph editor is not visible.
    :param tangent_type:
    :param current_time: When no curve/key selected, set tangent only on keys at current frame
    """

    msg = None
    success_msg = "<hl>" + tangent_type + "</hl>"
    curves_selected = cmds.keyframe(q=True, sl=True, name=True)
    ge_info = get_a_graph_editor()

    current_time = cmds.currentTime(q=True)
    if not current_time:
        current_time = ()

    if ge_info and curves_selected:
        cmds.keyTangent(itt=tangent_type, ott=tangent_type)
        msg = success_msg
    elif ge_info and not curves_selected:
        shown_curves = cmds.animCurveEditor(
            ge_info.editor, q=True, curvesShown=True
        )
        if shown_curves:
            cmds.keyTangent(
                shown_curves,
                t=current_time,
                itt=tangent_type,
                ott=tangent_type
            )
            msg = success_msg
    elif not ge_info:
        cmds.keyTangent(t=current_time, itt=tangent_type, ott=tangent_type)
        msg = success_msg

    if in_view_message and msg:
        cmds.inViewMessage(smg=msg, fade=True, pos='topCenter')
