from maya import cmds, mel


def quick_blast():
    current_workspace = cmds.workspaceLayoutManager(q=1, current=1)
    cmds.workspaceLayoutManager(setCurrent='Playblast')
    # todo: memorize
    #  show options for playblast display
    #  headup display