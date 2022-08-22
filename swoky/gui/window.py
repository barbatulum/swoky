# Done
from maya import cmds


def close_front_window():
    front_window = cmds.window(q=True, frontWindow=True)
    if front_window != 'unknown' and not cmds.window(front_window, q=True, mainWindow=True):
        cmds.window(front_window, edit=True, visible=False)
