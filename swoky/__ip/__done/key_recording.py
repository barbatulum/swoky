from maya import cmds, mel


_SELECTED_ANIM_CURVE_KEYS = {}


def get_selected_anim_curve_keys():
    """
    Get the selected anim curves
    """
    selection = dict()
    selective_curves = cmds.keyframe(q=True, sl=True, name=True)
    if not selective_curves:
        return
    for curve in selective_curves:
        selection[curve] = dict()
        selection[curve]['selected'] = cmds.keyframe(curve=True, q=True, sl=True, name=True)
        selection[curve]['existed'] = cmds.keyframe(curve=True, q=True, name=True)
        selection[curve]['plug'] = cmds.listConnections(
            curve + '.output', source=False, destination=True, plugs=True
        )
        selection[curve]['curve_type'] = cmds.nodeType(curve)
    return selection


def memorize_selected_anim_curve_keys():
    """
    global the selected anim curves  # pcRecordSledKeysInGE pcSlRecordSledKeysInGE
    """
    global _SELECTED_ANIM_CURVE_KEYS
    selection = get_selected_anim_curve_keys()
    if selection:
        _SELECTED_ANIM_CURVE_KEYS = copy.deepcopy(selection)


def reselect_anim_curve_keys():
    """
    Reselect the previously globaled memorized anim curves# pcSlRecordSledKeysInGE pcUndoSledKeys
    """
    global _SELECTED_ANIM_CURVE_KEYS
    # current_selected = get_selected_animcurve_keys()
    last_selected = _SELECTED_ANIM_CURVE_KEYS.copy()
    memorize_selected_anim_curve_keys()
    if not last_selected:
        return
    cmds.selectKey(cl=True)
    for curve in last_selected:
        if not cmds.objExists(curve):
            plug = _SELECTED_ANIM_CURVE_KEYS[curve]['plug']
            if not cmds.objExists(plug):
                continue
            new_curve = cmds.listConnections(plug, source=True, destination=False)
            if not new_curve:
                continue
            if cmds.nodeType(new_curve) != _SELECTED_ANIM_CURVE_KEYS[curve]['curve_type']:
                continue
            curve = new_curve

        selected_frame = last_selected[curve]['selected']
        # existed = last_selected[curve]['existed']
        for frame in selected_frame:
            cmds.selectKey(
                curve,
                add=True,
                time=(frame,),
            )

        # todo:
        #  first, last
        #  if all selected, select all
        #  check if is shifted, if so, also shift
        #  if pre and post are selected, the key is the only one inbetween as old select, do so
        #  if pre and post are selected, select the one which distance to pre and post are equal
        #  what about multiple keys in between?
        #  for time in selected:
        #      if time == selected[0] and time == existed[0]:
        #          selecting.append(time)
        #      elif time == selected[0] and time == existed[0]:
