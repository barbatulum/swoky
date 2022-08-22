from maya import cmds, mel

from .constants import ANIMATED_CURVE_TYPES

def list_constraints():
    """
    Get constraint nodes that constraint current selection  # pcSlConstraints
    :return:
    """
    selected = cmds.ls(sl=1)
    constraints = set()
    for sl in selected:
        constraints = constraints | set(
            cmds.listConnections(
                '{}.parentInverseMatrix'.format(sl), type='constraint'
            ) or []
        )

    return list(constraints)


def select_constraints():
    """
    Select constraint nodes that constraint current selected nodes.
    """
    cmds.select(list_constraints())


def sort_nodes(nodes=None, select=True):
    """
    Select selection in an alphabetic order.
    """
    if not nodes:
        nodes = cmds.ls(sl=True, long=True)
    dag_nodes = [i for i in nodes if '|' in i]
    dg_nodes = set(nodes) - set(dag_nodes)
    short_names = {i: i.split('|')[-1] for i in dag_nodes}
    short_names.update({i: i for i in dg_nodes})
    nodes = sorted(short_names.items(), key=lambda x: x[1])
    if select:
        cmds.select([i[0] for i in nodes], noExpand=True)
    return nodes

def select_scene_anim_curves():
    """
    Select all "user animted" anim curves in the scene
    """
    curves = cmds.ls(type=ANIMATED_CURVE_TYPES)
    cmds.select(curves)
    return curves


def select_hierarchy(exclude_init_non_dag=True):
    """
    Select descendents of current selection.
    """
    selected = cmds.ls(sl=True, **transform_kwarg)
    if not selected:
        return

    transform_kwarg = dict()
    if exclude_init_non_dag:
        transform_kwarg = {'type': 'transform'}

    for sl in selected:
        cmds.select(sl)
        cmds.select(cmds.listRelatives(sl, type='transform', ad=1) or [], add=True)


def select_top_down(exclude_non_dag=False, return_selected=False):
    """
    Select the whole hierarchies of selected nodes, from parents to descendents.
    """
    select_hierarchy(exclude_non_dag=exclude_non_dag)
    cmds.select(hi=True)
    if return_selected:
        return cmds.ls(sl=True, long=True)


def reverse_selection(return_selected=False):
    """
    Select current selection in a reversed order.
    """
    selected = cmds.ls(sl=True)
    if len(selected) < 2:
        return
    cmds.select(selected[::-1])
    if return_selected:
        return cmds.ls(sl=True, long=True)


def select_top(exclude_non_dag=False):
    """
    Select the top most parent of current selection.
    """
    selected = cmds.ls(selection=True, long=True)
    dags = [i for i in selected if i.startswith('|')]
    non_dag = set(selected) - set(dags)
    dag_tops = set(['|' + i.split('|')[1] for i in selected if i.startswith('|')])
    cmds.select(dag_tops)
    if not exclude_non_dag:
        cmds.select(non_dag, add=True)

    return non_dag
