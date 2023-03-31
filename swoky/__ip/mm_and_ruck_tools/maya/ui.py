from maya import cmds


# UI

def get_selection():
    """
    Get the selection as a dictionary of some node types
    """
    selected = cmds.ls(sl=True, long=True)
    returns = dict()
    for node in selected:
        shapes = cmds.listRelatives(node, shapes=True)
        #
        if not cmds.objectType(node, isAType='transform'):
            continue
        # Empty transform
        if not shapes:
            returns.setdefault('dags', []).append(node)
            continue
        for shape in shapes:
            if cmds.nodeType(shape) == 'camera':
                returns.setdefault('cameras', []).append(node)
                break
            if cmds.nodeType(shape) in _VALID_MESH_TYPES:
                returns.setdefault('meshes', []).append(node)
                break
            if cmds.nodeType(shape) in _VALID_MESH_TYPES:
                returns.setdefault('locator', []).append(node)
                break
        else:
            returns.setdefault('dags', []).append(node)
    return returns


# GUI
def get_panel_camera(mode='withFocus'):
    """
    Get the camera from the "model" panel withFocus or underPointer,
    """
    current_panel = cmds.getPanel(**{mode: True})
    if not cmds.getPanel(typeOf=current_panel) == 'modelPanel':
        return None, None
    return current_panel, cmds.modelEditor(current_panel, q=True, camera=True)