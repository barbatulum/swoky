# Done
from maya import cmds


def get_selected_channel_box_attrs(
    main=True, shape=True, history=True, output=True,
    channel_box='mainChannelBox'
):
    """
    Get attributes that are selected in the channelbox
    """
    cb_attr_types = ('main', 'shape', 'history', 'output',)
    result_attrs = []
    for attr_type in cb_attr_types:
        if not locals().get(attr_type):
            continue
        # cmd_args.append(('{}ObjectList'.format(attr_type),))
        objects = cmds.channelBox(
            channel_box,
            q=True,
            **{'{}ObjectList'.format(attr_type): True}
        )
        attrs = cmds.channelBox(
            channel_box,
            q=True,
            **{'selected{}Attributes'.format(attr_type.capitalize()): True}
        )
        if not objects or not attrs:
            continue
        for attr in ['{}.{}'.format(obj, attr) for obj in objects for attr in attrs]:
            if cmds.getAttr(attr, settable=True):
                result_attrs.append(attr)
    return result_attrs
