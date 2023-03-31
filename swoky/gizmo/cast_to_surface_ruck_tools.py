from maya import cmds

"""
Cast maya dag nodes to a surface, from "some" camera.

todo:
 - decorators:
    undo block
    redraw
 - user configurable(yaml, optionVar or?)
 - installer?

"""
# standard library
import logging
import math
from six import string_types

# maya
from maya import cmds
from maya.api import OpenMaya as om

import ruck_tools.maya.core as mcore
import ruck_tools.maya.ui as mui
import ruck_tools.maya.math as mmath
from ruck_tools import utils

_LOG = logging.getLogger('wage_slave.' + __name__)

_VALID_MESH_TYPES = ['mesh']
_CAST_LOCATORS_ONLY = False
_ACTIVE_CAMERA_INDEX = 0
_ACTIVE_MESH_INDEX = 0
_USE_PANEL_CAMERA = False
_CAST_NO_CAMERA = True
_CAST_NO_MESH = False
_SET_ATTRIBUTES = ('tx', 'ty', 'tz')
_BAIL_OUT_NON_SETTABLE = False
_TANGENT_TYPE = 'linear'


def are_instance(nodes, types):
    return [isinstance(node, types) for node in nodes]


def get_indexed_object(object_list, obj_index, type_str='camera'):
    """
    Try to get an object from list[index] WITH log messages.
    """
    if not object_list:
        _LOG.error("Found no valid '{}' in list '{}'.".format(type_str, object_list))
    try:
        return object_list[obj_index]
    except IndexError:
        _LOG.error("Cannot get a {} by index '{}' from list '{}'".format(
            type_str, obj_index, ', '.join(object_list))
        )
        return


def sort_selection(
        camera_index=_ACTIVE_CAMERA_INDEX,
        mesh_index=_ACTIVE_MESH_INDEX,
        cast_locators_only=_CAST_LOCATORS_ONLY,
        use_panel_camera=_USE_PANEL_CAMERA,
        cast_no_camera=_CAST_NO_CAMERA,
        cast_no_mesh=_CAST_NO_MESH,
):
    """
    Convent function to get require nodes with fallback orders and module constants.
    """
    error_logs = []
    types_of_nodes = mui.get_selection()

    dags = types_of_nodes.get('dags', [])
    locators = types_of_nodes.get('locator', [])

    cameras = types_of_nodes.get('cameras', [])
    camera = None
    if not len(cameras) or use_panel_camera:
        camera, mode_panel = mui.get_panel_camera()
        if not camera:
            if not cameras:
                error_logs.append(
                    "No camera is selected and you're active panel is "
                    "not a modelPanel looking through a camera."
                )
            else:
                _LOG.warning("No panel camera is found, fallback to use indexed camera.")
    if not camera:
        camera = utils.get_indexed_object(cameras, camera_index)
        if not camera:
            error_logs.append("No valid camera.")

    meshes = types_of_nodes.get('meshes', [])
    mesh = utils.get_indexed_object(meshes, mesh_index, type_str='mesh')
    if not mesh:
        error_logs.append("No valid mesh.")

    returns = {'camera': camera, 'mesh': mesh, 'casting_nodes': locators}

    if cast_locators_only:
        if not locators:
            error_logs.append("Found no locator to cast.")
    else:
        returns['casting_nodes'].extend(dags)
        if not cast_no_camera:
            returns['casting_nodes'].extend(set(cameras) - {camera})

        if not cast_no_mesh and not cast_locators_only:
            returns['casting_nodes'].extend(set(meshes) - {mesh})

    if not all(returns.values()):
        error_logs.append("Some object misses to do the cast: {}".format(returns))

    if error_logs:
        for err in error_logs:
            _LOG.error(err)
        return

    return returns


def get_nodes_mlist(nodes):
    if not all(utils.are_instance(nodes, crux.mappings.selections.MSELECTION_ACCEPTABLE_TYPE)):
        _LOG.error("Not all nodes are valid for MSelection.add")
        return
    mlist = om.MSelectionList()
    [mlist.add(n) for n in nodes]
    return mlist


def get_cam_node_relations(node, camera):
    mlist = get_nodes_mlist((node, camera))
    if not mlist:
        _LOG.error("Node type({}): {} and camera type({}): {} are not valid.".format(
            type(node), node, type(camera), camera)
        )
        return
    node_mobj = mlist.getDependNode(0)
    cam_mobj = mlist.getDependNode(1)

    cam_tsf = crux.om2.attribute.get_world_matrix_data.get_world_matrix_data(
        cam_mobj).transformation()
    cam_world_pos = cam_tsf.translation(om2.MSpace.kWorld)  # camera translation

    node_world_pos = crux.om2.attribute.get_world_matrix_data.get_world_matrix_data(
        node_mobj
    ).transformation().translation(om2.MSpace.kWorld)  #

    cam_rotation = cam_tsf.rotation()

    node_cam_vector = node_world_pos - cam_world_pos
    cam_vector = crux.math.rotate_vector(
        (math.degrees(i) for i in cam_rotation),
        rotate_order=crux.mappings.coordinates.ROTATION_ORDER_STRINGS[cam_rotation.order]
    )

    angle = math.get_angle_between_vectors(node_cam_vector, cam_vector)

    # degrees = math.degrees(angle)
    dist_loc_to_cam = get_dist(node_world_pos, cam_world_pos)

    dist_loc_to_cam_proj_point = math.sin(angle) * dist_loc_to_cam
    dist_cam_to_cam_proj_point = math.sqrt(
        dist_loc_to_cam * dist_loc_to_cam
        - dist_loc_to_cam_proj_point * dist_loc_to_cam_proj_point
    )
    return (
        (cam_vector, dist_cam_to_cam_proj_point),
        (node_cam_vector, dist_loc_to_cam)
    )


def get_node_to_plane_distance(node, camera, plane_distance):
    mlist = get_nodes_mlist((node, camera))
    if not mlist:
        _LOG.error("Node type({}): {} and camera type({}): {} are not valid.".format(
            type(node), node, type(camera), camera)
        )
        return
    node_mobj = mlist.getDependNode(0)
    cam_mobj = mlist.getDependNode(1)

    cam_vector, node_cam_vector, dist_cam_to_cam_proj_point = get_cam_node_relations(node, camera)

    distance = plane_distance / math.sin(90 - known_degree) * math.sin(90)
    # distance = perpenticular_dist / sin(90 - known_degree) * sin(90)


def run(anchor_node, nodes, camera, constant_distance=None):
    base_params = get_cam_node_relations(anchor_node, camera)
    if not base_params:
        return
    if constant_distance is not None:
        perpendicular_distance = constant_distance

    # mlist = get_nodes_mlist(nodes)
    for c, node_str in enumerate(nodes):
        if not constant_distance:
            (
                (cam_vector, perpendicular_distance),
                _
                # (node_cam_vector, dist_loc_to_cam)
            ) = base_params
        # node_mobj = mlist.getDependNode(c)
        (cam_vector, _), (node_cam_vector, node_distance) = get_cam_node_relations(camera, node_str)
        angle = ruck_math.get_angle_between_vectors(cam_vector, node_distance)
        distance = perpendicular_distance / math.sin(90 - math.degrees(angle)) * math.sin(90)
        # todo: move to cam by distance


def get_valid_shapes(mesh_transform_str):
    mlist = om2.MSelectionList()
    mlist.add(mesh_transform_str)
    dag_path = mlist.getDagPath(0)
    shape_fns = []
    for c in range(dag_path.numberOfShapesDirectlyBelow()):
        dp = mlist.getDagPath(0)
        dp.extendToShape(c)
        mobj = dp.node()
        if mobj.hasFn(om2.MFn.kMesh):
            shape_fns.append(om2.MFnMesh(mobj))
    return shape_fns


def get_dist(a, b):
    return math.sqrt(sum([(a[c] - b[c]) * (a[c] - b[c]) for c in range(3)]))


def get_closest_index(*args):
    src = args[0]
    length = len(args)
    if length < 3:
        return {0: None, 1: None, 2: 1}.get(length)

    idx = 2
    shortest = get_dist(args[0], args[1])
    for c, dst in enumerate(args[2:]):
        dist = get_dist(src, dst)
        if dist < shortest:
            idx = idx + c
            shortest = dist
    return idx


def cast_to_surface(
        camera,
        mesh,
        casting_nodes,
        frames,
        key=True,
        at_current_frame=False,
        bail_out_non_settable=_BAIL_OUT_NON_SETTABLE,
        set_attributes=_SET_ATTRIBUTES,
        static_distance=False,
):
    castable_nodes = [
        node for node in casting_nodes
        if all((core.is_attr_settable(node, attr) for attr in set(list(set_attributes) + ['t'])))
    ]
    if not castable_nodes:
        _LOG.error("All casting nodes are not settable.")
        return

    if bail_out_non_settable and castable_nodes != casting_nodes:
        _LOG.error(
            "Not all casting nodes are settable "
            "and you set to bail out on non settable node."
        )
        return

    mesh_fns = get_valid_shapes(mesh)
    if not mesh_fns:
        _LOG.error("No valid mesh found under: {}.".format(mesh))
        return

    casting_node_mlist = om2.MSelectionList()
    [casting_node_mlist.add(node) for node in castable_nodes]

    cam_mlist = om2.MSelectionList()
    cam_mlist.add(camera)
    cam_mobj = cam_mlist.getDependNode(0)

    if at_current_frame:
        frames = (oma2.MAnimControl.currentTime().value,)

    for frame in frames:
        cmds.currentTime(frame)
        cast_source = crux.om2.attribute.get_world_matrix_data.get_world_matrix_data(
            cam_mobj
        ).transformation().translation(om2.MSpace.kWorld)  # camera translation

        for c, node_str in enumerate(castable_nodes):
            cast_dest = crux.om2.attribute.get_world_matrix_data.get_world_matrix_data(
                casting_node_mlist.getDependNode(c)
            ).transformation().translation(om2.MSpace.kWorld)  #

            direction = cast_dest - cast_source
            hit_points = []
            for mesh_fn in mesh_fns:
                # todo: test this
                hit_params = mesh_fn.closestIntersection(
                    cast_source,  # raySource,
                    direction,  # rayDirection
                    om2.MSpace.kWorld,
                    # maxParam, testBothDirections, tolerance=kIntersectTolerance
                )

                if hit_params:
                    hit_points.append(hit_params[0])

            closest_index = get_closest_index(*([cast_source] + hit_points))
            # (hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2)
            if closest_index is None:
                continue

            hit_point = [hit_points[closest_index][c] for c in range(3)]
            cmds.xform(node_str, translation=hit_point, worldSpace=True)
            if key:
                cmds.setKeyframe(
                    node_str,
                    at=set_attributes,
                    inTangentType=_TANGENT_TYPE,
                    outTangentType=_TANGENT_TYPE
                )


def cast_to_surface_by_selection(
        key=True,
        at_current_frame=False,
        bail_out_non_settable=_BAIL_OUT_NON_SETTABLE,
        set_attributes=_SET_ATTRIBUTES
):
    parameters = sort_selection()
    parameters.update({
        'frames': crux.om2.get_animation_range_frames(),
        'key': key,
        'at_current_frame': at_current_frame,
        'bail_out_on_non_settable': bail_out_non_settable,
        'set_attributes': set_attributes,
    })
    cast_to_surface(**parameters)



# UI

def get_selection():
    """
    Get the selection as a dictionary of some node types
    """
    selected = cmds.ls(sl=True, long=True)
    returns = dict()
    for node in selected:
        shapes = cmds.listRelatives(node, shapes=True)
        #
        if not cmds.objectType(node, isAType='transform'):
            continue
        # Empty transform
        if not shapes:
            returns.setdefault('dags', []).append(node)
            continue
        for shape in shapes:
            if cmds.nodeType(shape) == 'camera':
                returns.setdefault('cameras', []).append(node)
                break
            if cmds.nodeType(shape) in _VALID_MESH_TYPES:
                returns.setdefault('meshes', []).append(node)
                break
            if cmds.nodeType(shape) in _VALID_MESH_TYPES:
                returns.setdefault('locator', []).append(node)
                break
        else:
            returns.setdefault('dags', []).append(node)
    return returns


# GUI
def get_panel_camera(mode='withFocus'):
    """
    Get the camera from the "model" panel withFocus or underPointer,
    """
    current_panel = cmds.getPanel(**{mode: True})
    if not cmds.getPanel(typeOf=current_panel) == 'modelPanel':
        return None, None
    return current_panel, cmds.modelEditor(current_panel, q=True, camera=True)


if __name__ == '__main__':
    cast_to_surface_by_selection()