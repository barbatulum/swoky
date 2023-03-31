from maya import cmds, mel

from .gui.panel import get_panel_info, get_panel_camera
from .constants import Panel


def safe_copy_paste():
    """
    Warn user when he is not copy/paste in graph editor.
    """
    panel_info = get_panel_info()
    if not panel_info:
        return

    paste = False
    if panel_info.panel_type == Panel.GraphEditor:
        paste = True
    else:
        result = cmds.confirmDialog(
            title="Confirm paste",
            button=('Yes', 'No'),
            message='Paste(import)?',
            defaultButton="No",
            cancelButton="No",
            dismissString="No"
        )
        if result == 'Yes':
            paste = True

    if paste:
        mel.eval('cutCopyPaste "paste"')


def parent_shapes(nodes=None, maintain_offset=True, delete_parented=True):
    """
    Combine the shapes under the transformation of the last given nodes.
    Use selection if none is given.
    """
    if not nodes:
        nodes = cmds.ls(sl=True)
    if len(nodes) < 2:
        return

    parent_to = nodes[-1]
    for node in nodes[:-1]:
        cmds.makeIdentity(node, apply=maintain_offset, t=True, r=True, s=True, n=False)
        for shape in cmds.listRelatives(node, shapes=True) or []:
            cmds.parent(shape, parent_to, shape=True, relative=True)
        if delete_parented:
            cmds.delete(node)


def zero_out_transform(*args, prefix='null', suffix='', base_name=None):
    """
    Create a null group on top of given nodes, or selected nodes if none is
    given. Joints need some special handling on their orientation.
    todo: this looks ugly...
    """
    selected = cmds.ls(sl=True)
    if not args:
        args = selected

    all_groups = {}
    for sel in args:
        parent = cmds.listRelatives(sel, parent=True)
        jo = None
        if cmds.nodeType(sel) == 'joint':
            jo = cmds.getAttr(sel + '.jo')
        if not base_name:
            base_name = sel
        if prefix:
            base_name = '_'.join((prefix, base_name))
        if suffix:
            base_name = '_'.join((base_name, suffix))
        null_group = cmds.group(n=base_name, em=True)
        cmds.xform(
            null_group, ws=True, t=cmds.xform(sel, q=True, ws=True, t=True)
        )
        cmds.xform(
            null_group, ws=True, ro=cmds.xform(sel, q=True, ws=True, ro=True)
        )

        try:
            cmds.parent(sel, null_group, a=True)
            all_groups[sel] = null_group
            if jo:
                cmds.setAttr(sel + '.jo', *jo[0])
                cmds.setAttr(sel + '.r', 0, 0, 0)
            if parent:
                null_group = cmds.parent(null_group,parent)
        except RuntimeError:
            cmds.delete(null_group)
    cmds.select(selected)
    return all_groups


def create_look_at_locator(name=None, at='aim'):
    """
    Create locator around the camera of the focused panel
    :param name: Name of locator
    :param at: Create locator at:
            front: Distance from the camera(in front of it)
            aim: Center of interest
    :return:
    # todo: xform is too slow, try matrices
    """
    panel_camera = get_panel_camera()
    if not panel_camera:
        return
    panel, cam = panel_camera
    cam_shape = cmds.listRelatives(cam, shapes=True)[0]
    args = {}
    if name:
        args['name'] = name
    locator = cmds.spaceLocator(**args)
    if at != 'aim':
        try:
            position = float(at)
        except ValueError:
            at = 'aim'
    if at == 'aim':
        position = (0 - cmds.getAttr('{}.centerOfInterest'.format(cam_shape)))

    cmds.xform(
        locator[0],
        worldSpace=True,
        translation=cmds.xform(
            cam, q=True, worldSpace=True, translation=True
        ),
        rotation=cmds.xform(
            cam, q=True, worldSpace=True, rotation=True
        )
    )
    cmds.move(
        locator[0], r=True, objectSpace=True, worldSpaceDistance=position
    )

    cmds.modelEditor(panel, e=True, locators=True)
    cmds.setAttr('.r'.format(locator[0], 0, 0, 0))
