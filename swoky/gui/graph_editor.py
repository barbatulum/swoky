from maya import cmds


from ..anim.curves import get_selected_key_frames
from ..constants import FixedGui, GEState, Panel
from ..preferences import GE_FALLBACK_ORDER
from .panel import get_panel_info, get_visible_panels_of_type


def get_a_graph_editor(order=GE_FALLBACK_ORDER, vis_ge_index=-1):
    """
    Get a graph editor by the given fallback order.
    (
        GEState.Visible,
        (GEState.UnderPointer, GEState.WithFocus),
        GEState.WithFocus
    )
    """
    candidates = {}

    visible_ges = [
        get_panel_info(i) for i in cmds.getPanel(visiblePanels=True)
    ]
    visible_ges = [
        panel_info for panel_info in visible_ges
        if panel_info.panel_type == Panel.GraphEditor
    ]
    if visible_ges:
        candidates[GEState.Visible] = visible_ges[vis_ge_index]

    with_focus = get_panel_info(cmds.getPanel(withFocus=True))
    if with_focus and with_focus.panel_type == Panel.GraphEditor:
        [GEState.WithFocus] = with_focus

    under_pointer = get_panel_info(cmds.getPanel(underPointer=True))
    if under_pointer and under_pointer.panel_type == Panel.GraphEditor:
        [GEState.UnderPointer] = under_pointer

    for state in order:
        if isinstance(state, str):
            candidate = candidates.get(state)
            if candidate:
                return candidate
        else:  # Multiple states
            reversed_candidates = {}
            for state, candidate in candidates.items():
                reversed_candidates.setdefault(
                    candidate, set(state)
                ).add(state)

            for candidate, states in reversed_candidates.items():
                if states == set(state):
                    return candidate

def get_panel_or_ge_panel(panel=None):
    if panel:
        panel_info = get_panel_info(panel)
    else:
        panel_info = get_a_graph_editor()
    return panel_info


def create_new_graph_editor():
    """
    Bring up or create a new graph editor.
    :return:
    """
    invisibles = cmds.getPanel(invisiblePanels=True)
    for inv_panel in invisibles:
        panel_info = get_panel_info(inv_panel)
        if panel_info.panel_type == Panel.GraphEditor:
            cmds.scriptPanel(inv_panel, e=True, tearOff=True)
            return True

    length = Panel.GraphEditor

    panel_names = [
        (
            panel_info.panel[length:]
            if panel_info.panel.startswith(Panel.GraphEditor)
            else panel_info.panel
        )
        for panel_info in get_visible_panels_of_type(Panel.GraphEditor)
    ]
    digits = [i for i in sorted(set(panel_names)) if i.isdigit()]

    if digits:
        new_digits = int(digits[-1]) + 1
    else:
        new_digits = 1
    # mel.eval('tearOffPanel "Graph Editor {}"
    # "graphEditor" true'.format(new_digits))
    cmds.scriptedPanel(
        "graphEditor{}".format(new_digits), typ='graphEditor', to=True
    )


def center_at_current_time(panel=None):
    """
    Center the graph editor view at the current time.
    """
    panel_info = get_panel_or_ge_panel(panel)
    if not panel_info:
        return
    if panel_info:
        cmds.animCurveEditor(panel_info.editor, edit=True, lookAt="currentTime")


def frame_ge_to_min_max(panel=None, margin=1):
    panel_info = get_panel_or_ge_panel(panel)
    if panel_info:
        cmds.animView(
            panel_info.panel_type,
            startTime=cmds.playbkackOptions(q=True, min=True - margin),
            endTime=cmds.playbkackOptions(q=True, max=True + margin)
        )

def normalize_curves(panel=None):
    """
    Toggle the normalizing mode of graph editor
    """
    panel_info = get_panel_or_ge_panel(panel)
    if not panel_info:
        return

    toggle_state = 1 - cmds.animCurveEditor(
        panel_info.editor, q=True, displayNormalized=True
    )
    cmds.animCurveEditor(
        panel_info.editor, e=True, displayNormalized=toggle_state
    )


def toggle_stack_curves():
    """
    Toggle the stacked mode of graph editor
    """
    ge_info = get_a_graph_editor()
    if not ge_info:
        return

    if cmds.animCurveEditor(ge_info.editor, q=True, stackedCurves=True):
        cmds.animCurveEditor(ge_info.editor, e=True, stackedCurves=False)
        cmds.optionVar(intValue=('graphEditorStackedCurves', 0))
        if cmds.optionVar(q='stackedCurvesDisableNormalized'):
            cmds.animCurveEditor(
                ge_info.editor, edit=True, displayNormalized=False
            )
            cmds.optionVar(intValue=('graphEditorDisplayNormalized', 0))
    else:
        cmds.animCurveEditor(
            ge_info.editor,
            edit=True,
            stackedCurvesMin=1,
            stackedCurvesMax=1,
            stackedCurvesSpace=0.2,
            stackedCurves=True
        )


def toggle_view_buffer_curves():
    """
    Toggle the buffer curve visibilities  # showHideBufferCurve
    """
    ge_info = get_a_graph_editor()
    if ge_info:
        toggle_state = not cmds.animCurveEditor(
                    ge_info.editor, q=True, showBufferCurves=True
                )
        cmds.animCurveEditor(
            ge_info.editor, edit=True, showBufferCurves=toggle_state
        )


def buffer_curves(graph_editor_ed, mode='overwrite'):
    """
    Snapshot or swap the curve (buffer)
    - 'overwrite': snapshot curve
    - 'swap': swap curve
    """
    selected = cmds.keyframe(selected=True, q=True, name=True)
    if not selected:
        return
    cmds.animCurveEditor(graph_editor_ed, edit=1, showBufferCurves=1)
    cmds.bufferCurve(animation='keys', **{mode: True})


def set_selected_curve_color(color=None):
    selected_curves = cmds.keyframe(q=True, sl=True, name=True)
    if not selected_curves:
        return

    if not color:
        color = cmds.colorEditor(result=True)
        color = [float(i) for i in color.split(' ') if i]

    for curve in selected_curves:
        cmds.setAttr(curve + '.curveColor', *color[:3])
        cmds.setAttr(curve + '.useCurveColor', True)

def get_ge_outliner_nodes():
    """
    Get the object list of the nodes displayed in graph editor's outliner
    """
    return cmds.selectionConnection(FixedGui.GraphEditorList, q=True, object=True)


def get_outliner_selection(panel=None):
    """
    Get the selected attribute and nodes in graph editor's outliner
    """
    panel_info = get_panel_or_ge_panel(panel)
    if not panel_info:
        return

    return cmds.selectionConnection(panel_info.panel + "OutlineEd", q=True, object=True)


def select_nodes_in_outliner(panel=None, keep_selection=True):
    # todo:
    pre_selection = None
    if keep_selection:
        pre_selection = get_selected_key_frames() or {}

    panel_info = get_panel_or_ge_panel(panel)
    if not panel_info:
        return

    outliner = panel_info.panel + "OutlineEd"
    cmds.selectionConnection(outliner, e=True, clear=True)
    ge_objects = cmds.selectionConnection(FixedGui.GraphEditorList, q=True, object=True)
    if not ge_objects:
        return
    for obj in ge_objects:
        cmds.selectionConnection(outliner, e=True, select=obj)
    if keep_selection and pre_selection:
        for curve, frames in pre_selection.items():
            for frame in frames:
                cmds.selectKey(curve, add=True, t=(frame,))
    return ge_objects


def get_shown_curve(graph_editor_ed):
    """
    Get shown curves of the given graph editor
    """
    return cmds.animCurveEditor(
        graph_editor_ed, q=True, curvesShown=True
    ) or []


def get_shown_curve_from_graph_ed(order=GE_FALLBACK_ORDER, vis_ge_index=-1):
    """
    Get shown curves of the graph editor from get_a_graph_editor.
    """
    working_graph_editor = get_a_graph_editor(
        order=order, vis_ge_index=vis_ge_index
    )
    if working_graph_editor:
        return get_shown_curve(working_graph_editor)
