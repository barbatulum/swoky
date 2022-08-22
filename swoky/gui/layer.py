# Done
from maya import cmds
from ..constants import FixedGui


def set_layers_vis(layers=None, visibility=None):
    """
    Set layer visibilities
    If no layer is given, act on all layers
    If no value is given, toggle the visibilities based on the last layer
    """
    if not layers:
        layers = cmds.layout(FixedGui.LayerEditorList, q=1, childArray=1)
    if not layers:
        return

    if visibility is None:
        visibility = 1 - cmds.getAttr(layers[-1] + '.visibility')

    for layer in layers:
        cmds.setAttr(layer + '.visibility', visibility)
        cmds.layerButton(layer, e=True, layerVisible=bool(visibility))


def get_layers_vis(reverse=False):
    """
    Get visible and invisible layers as {layer: visibility}
    or reversed: {True:[visible_layers], False[invisible_layers]}
    """
    layers = {}
    for layer in cmds.layout(FixedGui.LayerEditorList, q=1, childArray=1):
        layers.setdefault(cmds.layerButton(layer, q=True, select=True), []).append(layer)
    if not reverse:
        layers = {layer: vis for vis, lyrs in layers.items() for layer in lyrs}
    return layers


def get_node_layer(name):
    """
    Get the layer the given object belongs to.
    """
    draw_override = name + '.drawOverride'
    if not cmds.objExists(draw_override):
        return
    conns = cmds.listConnections(
        draw_override, type='displayLayer', source=True, destination=False
    )
    if conns:
        return conns[0]


def get_nodes_pertained_layer(nodes):
    """
    Get the layer of all ancestor nodes
    """
    long_names = [
        ln for ln in cmds.ls(nodes, long=True, recursive=True)
        if ln.startswith("|")
    ]
    if len(long_names) != len(nodes):
        raise RuntimeError(
            "There are no or multiple nodes match names {}".format(nodes)
        )

    layers_vis = {}
    for cnt, name in enumerate(long_names):
        ancestors = name.split('|')
        hierarchy = ['|'.join(ancestors[:c + 1]) for c in range(len(ancestors))]
        hierarchy = [i for i in hierarchy if i]
        for _node in hierarchy:
            layer = get_node_layer(_node)
            if layer:
                layers_vis.setdefault(nodes[cnt], []).append({_node: layer})
    return layers_vis


def set_ancestor_layers_vis(nodes=None, visibility=None):
    """
    Set the visibilities of layers of all parents object.
    """
    if not nodes:
        nodes = cmds.ls(sl=True)
    layers_vis = get_nodes_pertained_layer(nodes)
    layers = {
        lyr
        for parent_nodes_layers in layers_vis.values()
        for layer_mapping in parent_nodes_layers
        for lyr in layer_mapping.values()
    }
    set_layers_vis(list(layers), visibility=visibility)
