from maya import cmds, mel

from ..ui import panel_tools
from ..__done._constants import GraphEditorRetrievingParameters as GeParams


def get_selected_curves(fallback_to_nodes=False):
    """
    If not fallback_to_nodes, the function return only selected
    """
    return cmds.keyframe(
        q=True, name=True, **{'sl': fallback_to_nodes}
    ) or []


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


def get_shown_curve(graph_editor_ed):
    """
    Get shown curves of the given graph editor
    """
    return cmds.animCurveEditor(
        graph_editor_ed, q=True, curvesShown=True
    ) or []


def get_shown_curve_from_graph_ed(
        valid_mode=GeParams.VALID_MODE,
        working_order=GeParams.WORKING_ORDER,
        reverse_visible_order=GeParams.REVERSE_VISIBLE_ORDER
):
    """
    Get shown curves of the graph editor from get_a_graph_editor.
    """
    working_graph_editor = panel_tools.get_a_graph_editor(
        valid_mode=valid_mode,
        working_order=working_order,
        reverse_visible_order=reverse_visible_order
    )
    if working_graph_editor:
        return get_shown_curve(working_graph_editor)

def get_ge_or_node_curves(
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
