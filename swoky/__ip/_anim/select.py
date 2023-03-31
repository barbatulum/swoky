from maya import cmds,mel
from ..ui import panel_tools
from .. import constants as const


def select_visible_keys_at_frame(frame, select=True):
    """
    # selectVisKeyAtCurrentTime selectAllVisibleKeys
    If no frame specified and at_current is True: select all visible curves
    elif no frame specified and is not at_current: select all visible.
    :param frame:
    :param at_current:
    :return:
    """
    if not frame:
        frame = cmds.currentTime(q=True)
    panel, _, editor = panel_tools.get_a_graph_editor()
    if not editor:
        return
    shown_curves = cmds.animCurveEditor(editor, q=True, curvesShown=True)

    # todo: is this required?
    #   frame = (frame,)
    valid_curves = []
    for curve in shown_curves:
        frames = cmds.keyframe(curve, q=True, timeChange=True) or []
        if frame in frames:
            valid_curves.append(curve)
    if valid_curves:
        cmds.selectKey(cl=True)
        cmds.selectKey(valid_curves, t=frame, tgl=True)


def select_visible_curves():
    """
    Select visible curves in graph editor
    """
    panel, _, editor = panel_tools.get_a_graph_editor()
    if not editor:
        return
    shown_curves = cmds.animCurveEditor(editor, q=True, curvesShown=True)
    if shown_curves:
        cmds.selectKey(shown_curves)


def select_following_keys(include_current_frame=True):
    """
    Select all visible curve keys in graph editor "after" current time.
    # todo: active on selected, shown, nodes'
    # selectKeyBaseOnCurrentSelectedCurve_startFromCtTime, selectFollowingKeysAdv
    # selectKeysFromNowAndCurrentSelection, selectFollowingKeys, pcSlFcrvPointAfter
    # pcSlFcrvPointAfter
    """
    graph_panel = panel_tools.get_a_graph_editor()
    anim_curve_editor = const.EDITOR_STR_MAPPING.get(graph_panel)
    if not graph_panel:
        return

    shown_curves = cmds.keyframe(q=True, sl=True, name=True)
    if not shown_curves:
        shown_curves = cmds.animCurveEditor(anim_curve_editor, q=True, curvesShown=True)
    if not shown_curves:
        return

    current_time = cmds.currentTime(q=True)
    if include_current_frame:
        current_time -= 1
    keyed_frames = sorted(set(cmds.keyframe(shown_curves, q=True, timeChange=True) + [current_time]))
    start_frame = keyed_frames.index(current_time) + 1
    cmds.selectKey(shown_curves, t=(start_frame, keyed_frames[-1]))

