from maya import cmds, mel

from . import ls
from .. import constants as const
from ..constants import GraphEditorRetrievingParameters as GeParams
from ..ui import panel_tools
from . import gui


def key_channel_box_attrs():
    """
    Key selected attributes in channelbox.
    """
    selected_attrs = gui.get_selected_channel_box_attrs()
    if selected_attrs:
        cmds.setKeyframe(selected_attrs)


def key_all_keyed_attrs(nodes):
    """
    setkey on all keyed channel of selected objects
    todo: seems duplicated
    """
    anim_curves = cmds.keyframe(nodes, q=True, name=True)
    if anim_curves:
        cmds.setKeyframe(anim_curves)


def select_curve_keys(curves, time_to_select=None):
    if not curves:
        return
    if time_to_select is None:
        time_to_select = [cmds.currentTime(q=True)]
    cmds.selectKey(clear=True)
    for curve in curves:
        for frame in time_to_select:
            cmds.selectKey(curve, add=True, k=True, t=(frame,))
    # if not cmds.keyframe


def set_key_on_selected_or_keyed():
    curves = ls.get_selected_curves() or ls.get_selected_node_curves()
    if curves:
        cmds.setKeyframe(curves)
        select_curve_keys(curves)


def set_key_on_selected_curves():
    curves = ls.get_selected_curves()
    if curves:
        cmds.setKeyframe(curves)
        select_curve_keys(curves)


def set_selected_keys_values(value, mode='absolute'):
    """
    Wrapper of setting key values  # pcSetSledKeysTo, pcSetSledKeys
    """
    abs_rel_arg = {'absolute': True}
    if mode == 'relative':
        abs_rel_arg = {'relatives': True}
    cmds.keyframe(animation='keys', valueChange=value, **abs_rel_arg)


def zero_axis(parent_attr, only_process_all_axis=False, set_keyframe=const.ALWAYS_SET_KEYFRAME):
    """
    Zero out the xyz axis of a "parent" attribute, such as t, rotate and etc...
    only_process_all_axis argument determines whether to zero out attributes if some channels are un-settable.
    # pcZeroTrans pcZeroRot
    """
    nodes = cmds.ls(sl=True)
    result_curves = []
    keyed = False
    for node in nodes:
        children = cmds.attributeQuery(parent_attr, node=node, listChildren=True)
        if not children:
            continue
        if not ''.join(sorted(i[-1].lower() for i in children)) == "xyz":
            continue
        attrs = [node + '.' + i for i in children]
        if only_process_all_axis and not all([cmds.getAttr(i, settable=True) for i in attrs]):
            continue
        for attr in children:
            try:
                keyed = set_attr_or_keyframe(
                    node,
                    attr,
                    cmds.attributeQuery(
                        attr, node=node, listDefault=True
                    )[0] or 0,
                    set_keyframe=set_keyframe
                ) if not keyed else True # Only change keyed value if it's not True

                if not keyed:
                    continue
                src_crv = cmds.listConnections('{}.{}'.format(node, attr), source=True, destination=False) or []
                # Doesn't look like a solid way to query the anim curves?
                src_crv = [i for i in src_crv if cmds.nodeType(i) in const.ANIMATED_CURVE_TYPES]
                result_curves.extend(src_crv)
                # cmds.setAttr(attr, 0)
            except RuntimeError:
                pass
    if keyed:
        select_curve_keys(result_curves)


def reset_attrs(attrs, default=0, set_keyframe=const.ALWAYS_SET_KEYFRAME):
    """
    Set given attributes their default values or the given default value
    If not set_keyframe:
      if autoKeyframe is OFF:
        if value is not changed:
          nothing will happen
        else:
          value will change but no key will be set
      elif autoKeyframe is ON:
        if value is not changed:
          Nothing happens
        else:
          value will be set
    else:
       keyframe will be set and selected
    """
    # todo: attr like scale will be set to 1, should we add another ctrl+alt+q/w/e/r to set to zero instead?
    #       or query all values, if all value or last value are 1,
    #       set to zero instead(kind like toggle between default and 0/1)
    for long_attr in attrs:
        if not cmds.getAttr(long_attr, settable=True):
            continue
        node, _, attr = long_attr.rpartition('.')
        set_attr_or_keyframe(
            node,
            attr,
            cmds.attributeQuery(
                attr, node=node, listDefault=True
            )[0] or default,
            set_keyframe=set_keyframe
        )


def set_attr_or_keyframe(node, attr, value, set_keyframe=True):
    if set_keyframe:
        result = cmds.setKeyframe(
            node,
            at=attr,
            v=value
        )
    else:
        result = cmds.setAttr(
            '{}.{}'.format(node,attr),
            value
        )
    # if attribute is changed or keyed, it will return a Non-None value,
    # The return value helps other process to determine if it's going to select newly set keys
    return result


def reset_anim_curves(anim_curves, default=0):
    """
    Reset given anim_curves
    """
    attrs = ls.get_anim_curve_target(anim_curves)
    if attrs:
        reset_attrs(attrs, default=default)


def reset_graph_editor_selected_anim_curves(
        valid_mode=GeParams.VALID_MODE,
        working_order=GeParams.WORKING_ORDER,
        reverse_visible_order=GeParams.REVERSE_VISIBLE_ORDER,
        select_keys=True
):
    # We don't use the graph editor but the function
    # only works when user have a valid one.
    working_graph_editor = panel_tools.get_a_graph_editor(
        valid_mode=valid_mode,
        working_order=working_order,
        reverse_visible_order=reverse_visible_order
    )
    if not working_graph_editor[0]:
        return
    anim_curves = cmds.keyframe(q=True, sl=True, name=True)
    if not anim_curves:
        return
    reset_anim_curves(anim_curves)
    if select_keys:
        select_curve_keys(anim_curves)




def set_breakdown_keys_by(between='closest'):
    """

    :param between:
            closest: evaluate all curves on the closest keyframes
            keyframes: each curve evalutate it's own closest keyframes
            (time,time): By given time (through e)
    :return:
    """
    # get time
    # set_breakdown_keys(time)

