from maya import cmds, mel

from .constants import Panel
from .gui.panel import get_panel_info

def snap_switch(mode='grid',force=None):
    # grid, curve, point
    value = force
    if force is None:
        value =not cmds.snapMode(q=True, **{mode: True})
    cmds.snapsMode(**{mode: value})


def set_select_type(element, value=None):
    """
    Set selection mask  # pcToggle*Mask
    """
    if value is None:
        value = not cmds.selectType(q=True, **{element: True})
    cmds.selectType(**{element: value})


def toggle_nurbs_curve_selection_mask():
    value = cmds.selectType(q=True, nurbsCurve=True)
    set_select_type('allObjects', value=value)
    set_select_type('nurbsCurve', value=1 - value)


def toggle_select_tool():
    g_select = mel.eval('$temp=$gSelect')
    if g_select == cmds.currentCtx():
        cmds.setToolTo('ShowManips')
    else:
        mel.eval('buildSelectMM')

def switch_scale_region_and_lattice():
    """
    Switching between key region/lattice tools
    when the focus panel is graph editor.
    """
    panel_info = get_panel_info()
    if not panel_info:
        return
    current_ctx = cmds.currentCtx()
    launch_scale = False
    if panel_info.panel_type == Panel.GraphEditor:
        if current_ctx == 'scaleSuperContext':
            cmds.setToolTo('regionSelectKeySuperContext')
        elif current_ctx == 'regionSelectKeySuperContext':
            cmds.setToolTo('latticeDeformKeySuperContext')
            cmds.toolPropertyWindow()
        else:
            launch_scale = True
    else:
        launch_scale = True
    if launch_scale:
        mel.eval('buildScaleMM')


def activate_tool(context='insertKeySuperContext'):
    """
    Activate tool
    """
    last_context = cmds.currentCtx()
    eval_string = last_context
    if cmds.contextInfo(last_context, ex=True):
        cmds.setToolTo(last_context)
    else:
        cmds.setToolTo('selectSuperContext')
        eval_string = 'selectSuperContext'
    mel.eval(
        'global string $gLastAction;$gLastAction='
        '"restoreLastContext {}";'.format(eval_string)
    )
    cmds.setToolTo(context)

def transform_tool_key_released(mode):
    """
    Maya key pressed marking menu:
    Move/Rotate/Scale Tool With Snap Marking Menu / *ToolsWithSnapMarkingMenu
    :param mode: move|rotate|scale
    """
    mode = mode.capitalize()
    mel.eval("destroySTRSMarkingMenu {}Tool".format(mode))
    last_context = cmds.currentCtx()

    for i in ('move', 'rotate', 'scale'):
        mel.eval("$temp=$g{};".format(i.capitalize()))

    manip_cmd = getattr(cmds, 'manip{}Context'.format(mode))
    current_active_axis = manip_cmd(mode, q=1, activeHandle=1)
    new_axis = current_active_axis + 1
    if last_context != locals().get('g_{}'.format(mode)):
        new_axis -= 1
    if new_axis > 3:
        new_axis = 0
    cmds.manipMoveContext(mode, e=True, ah=new_axis)


def invoke_last_action():
    """
    Deactivate tool  # pcInsertKDeactive
    """
    mel.eval(mel.eval("$temp=$gLastAction;"))
