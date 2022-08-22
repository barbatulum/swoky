from maya import cmds
from functools import partial
import re


def create_runtime_name_command(function_str, language='python', annotation=None, category='main'):
    # func_name = "{}.{}".format(function.__module__, function.__name__)
    # func_str = func_name.replace(".", "_")
    flatten_function = re.sub(r'[^\w]', '_', function_str)
    runtime_command_name = "runtime_command_{}".format(flatten_function)
    name_command_name = "name_command_{}".format(flatten_function)

    if annotation is None:
        annotation = '{} command: {}'.format(language, function_str)

    edit_kwarg = {}
    if cmds.runTimeCommand(runtime_command_name, q=True, ex=True):
        edit_kwarg['edit'] = True

    cmds.runTimeCommand(
        runtime_command_name,
        category=category,
        commandLanguage=language,
        command=function_str,
        **edit_kwarg)

    cmds.nameCommand(
        name_command_name,
        command=runtime_command_name,
        annotation=annotation
    )

    return name_command_name


def assign_hotkey(name=None, releaseName=None,autoSave=True, **kwargs):
    if releaseName is None and name is None:
        raise RuntimeError("You need to specify either one of the name and release name command.")

    keyShortcut = kwargs.get('keyShortcut', kwargs.get('key', kwargs.get('k')))
    if not keyShortcut:
        raise RuntimeError("A 'key' is required.")

    alt = bool(kwargs.get('alt', kwargs.get('altModifier')))
    ctl = bool(kwargs.get('ctl', kwargs.get('ctrl', kwargs.get('ctrlModifier'))))
    sht = bool(kwargs.get('sht', kwargs.get('shift', kwargs.get('shiftModifier'))))
    ctxClient = kwargs.get('ctxClient', kwargs.get('cc'))
    dragPress = kwargs.get('dragPress', False)
    pressCommandRepeat = kwargs.get('pressCommandRepeat', False)
    releaseCommandRepeat = kwargs.get('releaseCommandRepeat', False)

    maya_cmd_kwargs = dict(
        keyShortcut=keyShortcut,
        alt=alt,
        ctl=ctl,
        sht=sht,
        dragPress=dragPress,
        pressCommandRepeat=pressCommandRepeat,
        releaseCommandRepeat=releaseCommandRepeat
    )

    if name:
        maya_cmd_kwargs['name'] = name
    if releaseName:
        maya_cmd_kwargs['releaseName'] = releaseName
    if ctxClient:
        maya_cmd_kwargs['ctxClient'] = ctxClient
    print("maya_cmd_kwargs", maya_cmd_kwargs)
    cmds.hotkey(autoSave=bool(autoSave))
    cmds.hotkey(**maya_cmd_kwargs)
