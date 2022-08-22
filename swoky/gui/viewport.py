# Done
from ..constants import Panel
from .panel import get_panel_info

from maya import cmds


def set_node_type_vis(element, value=None):
    """
    Set panel show/hide elements  # pcShowHide* pcShowHideAll
    """
    panel_info = get_panel_info()
    if panel_info.panel_type != Panel.MODEL_PANEL:
        return
    value = {element: bool(value)}
    if value is None:
        current_vis = cmds.modelEditor(
            panel_info.panel, q=1, **{element: True}
        )
        value = {element: 1 - int(current_vis)}

    cmds.modelEditor(
        panel_info.panel,
        e=True,
        **value
    )


def set_hud_element_vis(element='HUDCurrentFrame',state=None):
    """
    Toggle head up display elements
    """
    option_var_mapping = {
        'HUDCurrentFrame': 'currentFrameVisibility'
    }
    if cmds.headsUpDisplay(element, ex=True):
        if state is None:
            state = not cmds.headsUpDisplay(element, q=True, vis=True)
        cmds.headsUpDisplay(
            element,
            e=True, vis=state
        )
        cmds.optionVar(iv=(option_var_mapping[object], state))
