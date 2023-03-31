import copy

def combine_dicts(*args):
    """
    Combine multiple dictionaries
    """
    init_dict = copy.deepcopy(args[0])
    for arg in args[1:]:
        init_dict.update(arg)
    return init_dict


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