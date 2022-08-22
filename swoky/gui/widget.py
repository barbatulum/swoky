# Done
from maya import cmds


def set_component_vis(component='ChannelBoxLayerEditor', visible=None, always_collapse=True):
    """
    Force showing/hiding UI element: ChannelBoxLayerEditor, AttributeEditor, ToolSettings.
    """
    if visible is None:
        result_vis = True
        if all((
            not cmds.workspaceControl(component, q=True, collapse=True),
            cmds.workspaceControl(component, q=True, visible=True)
        )):
            result_vis = False
    else:
        result_vis = bool(visible)
    cmds.workspaceControl(component, e=True, collapse=not result_vis)
    if result_vis or always_collapse:
        cmds.workspaceControl(component, e=True, visible=result_vis)
