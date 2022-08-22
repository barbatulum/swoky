from maya import cmds, mel
from ..ui import panel_tools
from .. import constants as const


def shift_anim_curve_keys(shift, curves=None):
    """
    Shift animation keys by frame.
    """
    if curves is None:
        curves = ()
    cmds.keyframe(
        *curves,
        animation='keysOrObjects',
        option='over',
        relative=True,
        timeChange=shift
    )


def shift_all_selected_object_keys(shift):
    """
    Remove or add inbetween. (Pull the keyframes backward or push them forward)
    """
    last_frame = cmds.findKeyframe(cmds.ls(type='animCurve'), which='last')
    cmds.keyframe(
        time=(cmds.currentTime(q=True), last_frame),
        relative=True,
        timeChange=shift,
        option='over'
    )


def shift_selected_or_all_curve_keys(shift, consider_graph_editor=True, on_active_graph_editor_only=True):
    """
    Move the keyframes or remove/add inbetweens
    Fallback order:
        A. Works on keys selected if some keys are selected and graph editor is visible
        B. By default args, works on the visible animation curves if graph editor is visible and has focus
        C. If graph editor is not visible, works on all keys on selected objects.

    :param shift: How many frame to shift
    :param consider_graph_editor: If graph editor visibility would be considered
    :param on_active_graph_editor_only:
        When graph editor visibility is taken into consideration,
        Would the withFocus states of it's panel be considered.
    """
    # todo: insertInbetween shall not move the curves shown in the graph editor,
    #       it's a rare case, keep it simple to MoveSelected/InsertRemoveInbetween?
    #       Ctrl+A - contextual Move selected / Insert inbetween
    #       Ctrl+Shift+A - Insert inbetween

    key_selected = cmds.keyframe(q=True, sl=True, keyframeCount=True)
    graph_panel_info = panel_tools.get_a_graph_editor()
    focus_panel = cmds.getPanel(q=True, withFocus=True)

    if graph_panel_info:
        for panel_info in graph_panel_info:
            panel, _, editor = panel_info
            graph_panel_active = bool(panel == focus_panel)
            if key_selected:
                shift_anim_curve_keys(shift)
            elif consider_graph_editor:
                # Not on_active_graph_editor_only
                # on_active_graph_editor_only and "Graph editor is active"
                if not on_active_graph_editor_only or graph_panel_active:
                    shown_curves = cmds.animCurveEditor(editor, q=True, curvesShown=True)
                    shift_anim_curve_keys(shift, curves=shown_curves)
    else:
        shift_all_selected_object_keys(shift)


def offset_scene_animation(offset, anim_curves=None):
    """
    Offset given anim curves or all anim curves in the scene by given offset value as frames.
    """
    anim_curves = anim_curves or cmds.ls(type=const.ANIMATED_CURVE_TYPES)
    if anim_curves:
        cmds.keyframe(anim_curves, animation='objects', option='over', relative=True, timeChange=offset)


def offset_scene_animation_to(start_at):
    """
    Offset scene animation to start at given frame.
    """
    anim_curves = cmds.ls(type=const.ANIMATED_CURVE_TYPES)
    first_frame = cmds.findKeyframe(anim_curves, which='first')
    offset_scene_animation(start_at - first_frame, anim_curves=anim_curves)


##############################################################################
# Time slider  ###############################################################
##############################################################################

def cut_time_slider_keys():
    """
    Cut time slider(selected) keys
    """
    time_slider = mel.eval('$temp=$gPlayBackSlider')
    cmds.cutKey(
        animation='objects',
        includeUpperBound=False,
        t=tuple(cmds.timeControl(time_slider, q=True, rangeArray=True)),
        option='keys'
    )


def copy_time_slider_keys():
    """
    Copy time slider(selected) keys
    """
    time_slider = mel.eval('$temp=$gPlayBackSlider')
    cmds.copyKey(
        animation='objects',
        includeUpperBound=False,
        t=tuple(cmds.timeControl(time_slider, q=True, rangeArray=True)),
        option='keys'
    )


def paste_time_slider_keys():
    """
    Pasting copied keys to time slider
    """
    time_slider = mel.eval('$temp=$gPlayBackSlider')
    args = {
        'animation': 'objects',
        'includeUpperBound': False,
        'connect': False,
    }
    if cmds.timeControl(time_slider, q=True, rv=True):
        args.update({
            'option': 'scaleReplace',
            'time': tuple(cmds.timeControl(time_slider, q=True, rangeArray=True))
        })
    else:
        current_time = cmds.currentTime(q=True)
        args.update({
            'option': 'replace',
            'time': (current_time, current_time + .99),
        })

    cmds.pasteKey(
        **args
    )


def clear_time_slider_keys():
    """
    Clear keys on time slider current time or selected range
    """
    time_slider = mel.eval('$temp=$gPlayBackSlider')
    cmds.cutKey(
        clear=True,
        iub=False,
        animation='objects',
        time=tuple(cmds.timeControl(time_slider, q=1, rangeArray=1)),
        option='keys'
    )


def clear_keys_at_current_time():
    """
    todo: Is the difference between clear_time_slider_keys that
          the later only clear those shown on the slider?
    """
    selected = cmds.ls(sl=True)
    if selected:
        cmds.cutKey(cmds.keyframe(selected, q=True, name=True), time=(cmds.currentTime(q=1),))
