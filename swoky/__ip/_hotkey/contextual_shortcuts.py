from maya import cmds, mel
from .. import constants as const
from ..anim import tangent, setkey, ls
from ..ui import panel_tools, maya_gui


def on_number_key_pressed_node_editor(number, editor):
    """
    Wrapper to switch node editor view mode
    """
    cmds.nodeEditor(editor, e=True, nodeViewMode=const.NUMBER_KEYS_MAPPING.get(number).get('nodeEditorPanel'))


def on_number_key_pressed(number):
    """
    Switch tangent type or node editor view mode based on the focused panel.
    # nodeE_1~4
    """
    panel_info = panel_tools.get_panel_info(withFocus=True)
    if not panel_info:
        return
    if panel_info.panel_type == const.PanelType.NODE_EDITOR:
        on_number_key_pressed_node_editor(number, panel_info.editor)
    else:
        tangent.set_tangent(const.NUMBER_KEYS_MAPPING.get(number).get(panel_info.panel_type))


def pin_or_view_isolate():
    """
    # pinOrViewIsolate
    modelPanel:
        Isolate view with selection.
    nodeEditorPanel:
        Clear the graph and then add selected nodes into it.
    """
    panel_info = panel_tools.get_panel_info(withFocus=True)
    if panel_info.panel_type == const.PanelType.MODEL_PANEL:
        # mel.eval(
        #     'string $currentPanel = `getPanel -withFocus`;'
        #     'string $state = `isolateSelect -q -state $currentPanel`;'
        #     'if ($state) enableIsolateSelect $currentPanel false;'
        #     'else enableIsolateSelect $currentPanel true;'
        # )
        state = cmds.isolateSelect(panel_info.panel, q=True, state=True)
        mel.eval('enableIsolateSelect {} {}'.format(
            panel_info.panel, {True: 'false', False: 'true'}[state])
        )
        # C:/Program Files/Autodesk/Maya2022/scripts/others/createModelPanelMenu.mel
        # main_list_connections = cmds.editor(editor, q=True, mainListConnection=True)

    elif panel_info.panel_type == const.PanelType.NODE_EDITOR:
        # todo: Why selection changed after this block? ne flag?
        selected = cmds.ls(sl=True)
        cmds.nodeEditor(panel_info.editor, e=1, rootNode=selected)


# selectIsolated
def select_visible_or_isolated():
    """
    modelPanel:
        Selected objects in isolated view
    nodeEditorPanel:
        Select all visible
    """
    panel_info = panel_tools.get_panel_info()
    if not panel_info:
        return
    if panel_info.panel_type == 'modelPanel':
        cmds.select(str(panel_info.panel) + 'ViewSelectedSet')
    elif panel_info.panel_type == 'nodeEditorPanel':
        # node_editor = focus_panel + 'NodeEditorEd'
        # mel.eval('nodeEditor -e -selectAll ' + node_editor)
        cmds.nodeEditor(panel_info.editor, e=True, selectAll=True)


# removeFromIsolated
def remove_sled_or_sled_from_isolated():
    """
    modelPanel:
        Removed selected in isolated view
    nodeEditorPanel:
        Removed selected from node editor
    """
    panel_info = panel_tools.get_panel_info()
    if not panel_info:
        return
    if panel_info.panel_type == 'modelPanel':
        cmds.isolateSelect(panel_info.panel, removeSelected=True)
    elif panel_info.panel_type == 'nodeEditorPanel':
        cmds.nodeEditor(panel_info.editor, e=True, removeNode=True)


# addToIsolated
def add_to_isolated():
    """
    modelPanel:
        Add selected to isolated view
    nodeEditorPanel:
        Add selected to node editor
    """
    panel_info = panel_tools.get_panel_info()
    if not panel_info:
        return
    if panel_info.panel_type == 'modelPanel':
        cmds.isolateSelect(panel_info.panel, addSelectedObjects=True)
    elif panel_info.panel_type == 'nodeEditorPanel':
        cmds.nodeEditor(panel_info.editor, e=True, frameAll=True, addNode='')


def smart_key(
        valid_mode='visible',
        working_order=('focus', 'visible'),
        reverse_visible_order=False
):
    working_graph_editor = panel_tools.get_a_graph_editor(
        valid_mode=valid_mode,
        working_order=working_order,
        reverse_visible_order=reverse_visible_order
    )
    if working_graph_editor:
        shown_curve = ls.get_shown_curve(working_graph_editor)
        if shown_curve:
            cmds.setKeyframe(shown_curve)
        else:
            working_graph_editor = False

    if not working_graph_editor:
        setkey.set_key_on_selected_or_keyed()

