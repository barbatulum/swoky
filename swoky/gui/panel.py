# Done
from dataclasses import dataclass

from maya import cmds

from .. import util
from .. import constants as const
from ..constants import CompatibleKwargs, Panel


@dataclass
class PanelInfo:
    panel: str
    panel_type: str
    editor: str


def get_panel_camera(**kwargs):
    """
    Get the camera from the "model" panel withFocus or underPointer,
    """
    current_panel = cmds.getPanel(
        **util.make_kwargs(compatibles=CompatibleKwargs.getPanel, **kwargs)
    )
    if cmds.getPanel(typeOf=current_panel) == const.PanelType.MODEL_PANEL:
        return current_panel, cmds.modelEditor(current_panel, q=True, camera=True)


def get_gui_editor_name(panel, panel_type):
    """
    Concatenate eitor name in "Maya way".
    """
    if panel:
        return panel + Panel.get(panel_type, "")


def get_visible_panels_of_type(panel_type):
    """
    Get all visible panels by the given type.
    """
    visible_panels = cmds.getPanel(visiblePanels=1)
    panels = []
    for panel in visible_panels:
        panel_info = get_panel_info(panel)
        if panel_info and panel_info.panel_type == panel_type:
            panels.append(panel_info)
    return panels


def get_panel_info(panel=None, **kwargs):
    """
    Get the panel info of the given panel
    """
    if not panel:
        get_kwargs = {}
        for mode in ('withFocus', 'underPointer'):
            if mode in kwargs:
                get_kwargs[mode] = kwargs[mode]
        panel = cmds.getPanel(util.make_kwargs(**kwargs))
    if not panel:
        return

    panel_type = cmds.getPanel(typeOf=panel)
    editor = ''
    if panel_type in (Panel.Outliner, Panel.ModelPanel):
        editor = get_gui_editor_name(panel, panel_type)
    elif panel_type in (Panel.ScriptedPanel,):
        panel_type = getattr(cmds, panel_type)(panel, q=True, type=True)
        editor = get_gui_editor_name(panel, panel_type)

    return PanelInfo(panel, panel_type, editor)

