from maya import cmds, mel
from . import constants as const


_current_frame_rate = 1


# todo: Go to previous key shown in Graph editor

def play_with_handle(rewind=6):
    """
    # pcPlayWUndo
    todo: ass undo decorator
    :param rewind:
    :return:
    """
    if cmds.play(q=True, state=True):
        cmds.play(state=False)
    else:
        start_time = cmds.currentTime(q=True) - rewind
        min_time = cmds.playbackOptions(q=True, min=True)
        if start_time < min_time:
            start_time = min_time
        cmds.currentTime(start_time)
        cmds.play(state=True)


def toggle_playback_speed():
    """
    Speed up/down the playback
    todo: should consider user framerate settings
    """
    # pair of playbackSpeed | by | maxPlaybackSpeed
    global _current_frame_rate
    current_pbs = cmds.playbackOptions(q=True, playbackSpeed=True)
    current_by = cmds.playbackOptions(q=True, by=True)
    current_mpbs = cmds.playbackOptions(q=True, maxPlaybackSpeed=True)
    next_setting_index = 0
    current_setting = (current_pbs, current_by, current_mpbs)
    if current_setting in const.PLAYBACK_SPEED_STEPS:
        next_setting_index = const.PLAYBACK_SPEED_STEPS.index(current_setting) + 1
        if next_setting_index >= len(const.PLAYBACK_SPEED_STEPS):
            next_setting_index = 0
    print("next_setting_index", next_setting_index)
    next_setting = const.PLAYBACK_SPEED_STEPS[next_setting_index]
    cmds.playbackOptions(
        e=True,
        playbackSpeed=next_setting[0],
        by=next_setting[1],
        maxPlaybackSpeed=next_setting[2]
    )


def go_to_playback_or_timeline_edge(forward=False):
    """
    Forward toggle max/aet, otherwise min/ast
    todo: add screen notification
    """
    args = {'min': True}, {'ast':True}
    if forward:
        args = {'max': True}, {'aet': True}
    current_time = cmds.currentTime(q=True)
    playback_in = cmds.playbackOptions(q=True, **args[0])
    timeline_in = cmds.playbackOptions(q=True, **args[1])
    if current_time == playback_in:
        cmds.currentTime(timeline_in)
    else:
        cmds.currentTime(playback_in)


def step_frames(frame):
    """
    todo: exclude this fron undo
    Maya builtin "nextOrPreviousFrame \"next\"" steps BY the "playback by preference setting" instead of frame
    :param frame:
    :return:
    """
    cmds.currentTime(cmds.currentTime(q=True)+frame)


def go_to_previous_shown_key():
    """
    todo: is this and go_to_next_shown_key really necessary?
    :return:
    """