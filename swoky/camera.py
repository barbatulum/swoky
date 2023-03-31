from maya import cmds

from .gui.panel import get_panel_camera
from .preferences import CAMERA_CYCLE_ORDER


def is_startup(cam):
    return cmds.camera(cam, q=True, startupCamera=True)


def get_ortho_cam(is_orthographic=True, startup=None):
    """
    Get cameras in the scene by the orthographic-ness
    startup: get the startup cam, not, or both(None)
    """
    # Get orthographic only or vice versa
    cameras = [
        i for i in cmds.ls(type='camera')
        if cmds.getAttr(i + '.orthographic') is is_orthographic
    ]

    # Filter the startup/non-startup camera or not
    if startup is not None:
        cameras = [
            i for i in cameras if is_startup(i) == startup
        ]

    cameras = [cmds.listRelatives(i, parent=True)[0] for i in cameras]
    return cameras


def cycle_builtin_camera(order=CAMERA_CYCLE_ORDER, startup=True):
    """
    Cycle the look through camera of current panel by a specific order, side-front-persp by default.
    # todo: use camera angle to determine what a camera actually is
    """
    # If no order is given, cycle through all orthographic and then non-ortho
    if not order:
        order = get_ortho_cam(is_orthographic=True, startup=startup)
        order += get_ortho_cam(is_orthographic=False, startup=startup)

    panel_camera = get_panel_camera(withFocus=True)
    if not panel_camera:
        return

    current_panel, panel_cam = panel_camera
    try:
        index = order.index(panel_cam)
        if index == len(order) - 1:
            index = 0
        else:
            index += 1
    except ValueError:
        index = 0
    cmds.lookThru(order[index], current_panel)


def cycle_persp_cameras(startup='both'):
    """
    Cycle the look through camera by non-orthographic camera.
    """
    non_ortho_cameras = get_ortho_cam(is_orthographic=False, startup=startup)

    panel_camera = get_panel_camera()
    if not panel_camera:
        return

    current_panel, panel_cam = panel_camera
    try:
        index = non_ortho_cameras.index(panel_cam)
        if index == len(non_ortho_cameras) - 1:
            index = 0
        else:
            index += 1
    except ValueError:
        index = 0
    cmds.lookThru(non_ortho_cameras[index], current_panel)
