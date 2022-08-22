import importlib
import sys
from maya import cmds

package_path = 'C:/repos/contextual_anim_shortcuts'
if package_path not in sys.path:
    sys.path.append(package_path)

from contextual_anim_shortcuts import (
    anim, camera, constants, lssl, manipulators, misc, playblast,
    time_control,
)

from contextual_anim_shortcuts.shortcut import (
    contextual_shortcuts, shortcut  # , assign
)

from contextual_anim_shortcuts.ui import (
    layer, panel_tools, maya_gui
)

for module in (
        camera,
        constants,
        lssl,
        manipulators,
        misc,
        playblast,
        time_control,
        contextual_shortcuts,
        shortcut,
        layer,
        panel_tools,
        maya_gui,
        anim,
        # assign,
):
    importlib.reload(module)

for module_name_str, module in sys.modules.items():
    if module_name_str.startswith('contextual_anim_shortcuts'):
        importlib.reload(module)

_RELEASE_NAME_CMD = shortcut.create_runtime_name_command(
    "", language="python", category="animation"
)
_INVOKE_LAST_ACTION = shortcut.create_runtime_name_command(
    "manipulators.invoke_last_action()", language="python", category="animation"
)


def set_anim_shortcuts(category='animation'):
    ##########################################################################
    # Zero keys
    ##########################################################################

    # Zero selected anim curves
    name_command = shortcut.create_runtime_name_command(
        "anim.setkey.reset_graph_editor_selected_anim_curves()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='q', alt=True)

    # Zero TRS
    for key, attr in zip('wer', ('translate', 'rotate', 'scale')):
        name_command = shortcut.create_runtime_name_command(
            "anim.setkey.zero_axis({})".format(attr),
            language="python", category=category
        )
        shortcut.assign_hotkey(name=name_command, key=key, alt=True)

    # Zero select attributes in channelbox
    name_command = shortcut.create_runtime_name_command(
        "anim.setkey.reset_attrs(anim.gui.get_selected_channel_box_attrs() or [])",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='q', ctrl=True)

    ##########################################################################
    # Timeline keys
    ##########################################################################
    # todo: remap cmd/win key to ctrl+alt+shift AHK

    for key, command in zip(
            'WASD', (
                    'clear_time_slider_keys',
                    'cut_time_slider_keys',
                    'copy_time_slider_keys',
                    'paste_time_slider_keys'
            )
    ):
        print(key)
        name_command = shortcut.create_runtime_name_command(
            "anim.keys.{}()".format(command),
            language="python", category=category
        )
        shortcut.assign_hotkey(name=name_command, key=key, ctrl=True, alt=True)

    ##########################################################################
    # Moving keys
    ##########################################################################

    ##########################################################################
    # Timeline Navigation
    ##########################################################################

    # todo: previous and next frame shall go one more keyframe outside time range
    shortcut.assign_hotkey(name='NameComGo_to_previous_keyframe', key='a')
    shortcut.assign_hotkey(name='NameComGo_to_next_keyframe', key='d')
    shortcut.assign_hotkey(releaseName=_RELEASE_NAME_CMD, key='a')
    shortcut.assign_hotkey(releaseName=_RELEASE_NAME_CMD, key='d')

    shortcut.assign_hotkey(name='Name_Frame_Backward', key='a', alt=True)
    shortcut.assign_hotkey(name='Name_Frame_Forward', key='d', alt=True)
    shortcut.assign_hotkey(releaseName =_RELEASE_NAME_CMD, key='a', alt=True)
    shortcut.assign_hotkey(releaseName =_RELEASE_NAME_CMD, key='d', alt=True)



    for key, direction in zip('ad', ('False', 'True')):
        name_command = shortcut.create_runtime_name_command(
            "time_control.go_to_playback_or_timeline_edge(forward={})".format(direction),
            language="python", category=category
        )
        shortcut.assign_hotkey(name=name_command, key=key, shift=True)

    ##########################################################################
    # Contextual (numbers)
    ##########################################################################
    # todo: Assigning here
    for count in range(1, 5):
        name_command = shortcut.create_runtime_name_command(
            "contextual_shortcuts.on_number_key_pressed({})".format(count),
            language="python", category=category
        )
        shortcut.assign_hotkey(name=name_command, key=str(count))

    # Isolate
    # todo: node editor:clear_others, model_panel:isolate_select, graph_panel:breakTrangent?
    # shortcut.assign_hotkey(name='NameComToggle_Isolate_Select', key='`', alt=True)
    name_command = shortcut.create_runtime_name_command(
        "contextual_shortcuts.pin_or_view_isolate()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='`', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "contextual_shortcuts.add_to_isolated()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='1', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "contextual_shortcuts.select_visible_or_isolated()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='2', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "contextual_shortcuts.remove_sled_or_sled_from_isolated()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='3', alt=False)

    ##########################################################################
    # Setkey (s)
    # todo: setKeyframe seems to be able evaluate on setting key
    ##########################################################################

    shortcut.assign_hotkey(name='NameComSave_File', key='s', alt=True, ctrl=True)
    shortcut.assign_hotkey(name='NameComSet_Keyframe', key='S', ctrl=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.setkey.key_channel_box_attrs()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='s', ctrl=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.setkey.set_key_on_selected_curves()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='s', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.setkey.set_key_on_selected_or_keyed()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='S')

    name_command = shortcut.create_runtime_name_command(
        "contextual_shortcuts.smart_key()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='s')


    ##########################################################################
    # Curves
    ##########################################################################

    name_command = shortcut.create_runtime_name_command(
        "anim.curves.clear_all_curves()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='/', ctl=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.tangent.toggle_tangent_break",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='`')

    ##########################################################################
    # Manipulator
    ##########################################################################
    # todo: Are WER(TRS) name commmand needs to be assigned too?
    name_command = shortcut.create_runtime_name_command(
        "manipulators.trs_key_released('Move')",
        language="python", category=category
    )
    shortcut.assign_hotkey(releaseName=name_command, key='w')

    name_command = shortcut.create_runtime_name_command(
        "manipulators.trs_key_released('Rotate')",
        language="python", category=category
    )
    shortcut.assign_hotkey(releaseName=name_command, key='e')

    name_command = shortcut.create_runtime_name_command(
        "manipulators.scale_region_lattice_switch()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='r')

    name_command = shortcut.create_runtime_name_command(
        "manipulators.trs_key_released('Scale')",
        language="python", category=category
    )
    shortcut.assign_hotkey(releaseName=name_command, key='r')

    name_command = shortcut.create_runtime_name_command(
        "manipulators.activate_tool(context='insertKeySuperContext')",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='c')

    ##########################################################################
    # Playback
    ##########################################################################

    name_command = shortcut.create_runtime_name_command(
        "time_control.play_with_handle()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='v')

    name_command = shortcut.create_runtime_name_command(
        "time_control.toggle_playback_speed()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='X')


def set_gui_shortcuts(category='gui'):

    ##########################################################################
    # camera
    ##########################################################################

    name_command = shortcut.create_runtime_name_command(
        "camera.cycle_builtin_camera()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='z', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "camera.cycle_persp_cameras()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='z', ctrl=True)

    ##########################################################################
    # View - F key switch
    # todo: stacked curve?
    ##########################################################################

    shortcut.assign_hotkey(name='NameComVirtual_timeslider_modifier', key='x')
    shortcut.assign_hotkey(releaseName='NameComVirtual_timeslider_modifier_release', key='x')

    name_command = shortcut.create_runtime_name_command(
        "anim.gui.center_at_current_time()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='f', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.gui.normalize_curves()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='f', shift=True)

    name_command = shortcut.create_runtime_name_command(
        "anim.gui.frame_min_max()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='f', ctrl=True)

    name_command = shortcut.create_runtime_name_command(
        "maya_gui.set_ui_element_visibility(element='ChannelBoxLayerEditor')",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='1', ctrl=True)

    name_command = shortcut.create_runtime_name_command(
        "maya_gui.set_ui_element_visibility(element='AttributeEditor')",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='2', ctrl=True)

    name_command = shortcut.create_runtime_name_command(
        "maya_gui.set_ui_element_visibility(element='ToolSettings')",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='3', ctrl=True)


def set_misc_shortcuts(category='misc'):

    shortcut.assign_hotkey(name='NameComDuplicate_Selected', key='d', ctl=True, alt=True)
    shortcut.assign_hotkey(name='NameComDuplicate_Special', key='D', ctl=True, alt=True)

    name_command = shortcut.create_runtime_name_command(
        "misc.safe_copy_paste()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='v', ctl=True)

    name_command = shortcut.create_runtime_name_command(
        "manipulators.toggle_select_tool()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='q')

    name_command = shortcut.create_runtime_name_command(
        "misc.toggle_nurbs_curve_selection_mask()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='`', ctrl=True)

    ##########################################################################
    # Snap
    ##########################################################################

    for key, mode in zip('xcv', ('grid', 'curve', 'poit')):
        name_command = shortcut.create_runtime_name_command(
            "misc.snap_switch(mode='{}')".format(mode),
            language="python", category="animation"
        )
        shortcut.assign_hotkey(name=name_command, key=key, alt=True)

    ##########################################################################
    # Selection
    ##########################################################################

    name_command = shortcut.create_runtime_name_command(
        "lssl.select_top()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='Home', alt=True)

    name_command = shortcut.create_runtime_name_command(
        "cmds.select(hi=True)",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='Home', alt=True, ctl=True)

    name_command = shortcut.create_runtime_name_command(
        "lssl.select_hierarchy_dag()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='Home', alt=True)

    ##########################################################################
    # Nodes/Objects
    ##########################################################################

    name_command = shortcut.create_runtime_name_command(
        "misc.create_look_at_locator()",
        language="python", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='l', ctl=True)

    # Geometry smooth level
    shortcut.assign_hotkey(name='NameComLow_Quality_Display_Setting', key='!', ctrl=True, alt=True)
    shortcut.assign_hotkey(name='NameComMedium_Quality_Display_Setting', key='@', ctrl=True, alt=True)
    shortcut.assign_hotkey(name='NameComHigh_Quality_Display_Setting', key='#', ctrl=True, alt=True)

    ##########################################################################
    # Find
    # todo 2022.1 Ctrl-F to other shortcut
    ##########################################################################
    name_command = shortcut.create_runtime_name_command(
        "findMenuItem()",
        language="mel", category=category
    )
    shortcut.assign_hotkey(name=name_command, key='F1', ctl=True)
