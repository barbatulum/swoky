# dotSign
# todo: what is it?
def dotSign():
    currentPanel = pm.getPanel(withFocus=1)
    if 'modelPanel' in currentPanel:
        pcSlMaskSw()
    elif 'nodeEditorPanel' in currentPanel:
        ned = mm.eval("getCurrentNodeEditor")
        if ned:
            mm.eval('nodeEdGraphControl(\"' + ned + '\", "nodeEditor -e -rfs -ups -ds ");')


for t in cmds.getPanel(allTypes=1):
    print(t)
    print('\t', cmds.getPanel(type=t))

for t in cmds.getPanel(allScriptedTypes=1):
    print(t)
    print('\t', cmds.getPanel(scriptType=t))
invisible_panels = cmds.getPanel(invisiblePanels=1)
visible_panels = cmds.getPanel(visiblePanels=1)
for p in visible_panels:
    print(p, cmds.getPanel(typeOf=p))

cmds.panel
cmds.window
cmds.lsUI
cmds.panel('nodeEditorPanel1', q=1, ctl=1)
cmds.panel('graphEditor1', q=1, ctl=1)
print(cmds.lsUI(type='window'))
cmds.animCurveEditor('graphEditor1GraphEd', q=True, cs=True)
"""
https://vimsky.com/zh-tw/examples/detail/python-method-maya.cmds.getPanel.html
https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=__CommandsPython_index_html

"""

for t in cmds.getPanel(allTypes=1):
    print(t)
    print('\t', cmds.getPanel(type=t))

for t in cmds.getPanel(allScriptedTypes=1):
    print(t)
    print('\t', cmds.getPanel(scriptType=t))
cmds.keyframe(q=True, sl=True)
print(cmds.lsUI(type='window'))
invisible_panels = cmds.getPanel(invisiblePanels=1)
visible_panels = cmds.getPanel(visiblePanels=1)
cmds.outlinerPanel

cmds.scriptedPanel(panel, q=True, type=True) == 'graphEditor'
for p in visible_panels:
    print(p, cmds.getPanel(typeOf=p))
cmds.scriptedPanel('graphEditor1', q=1, type=1)
cmds.panel('graphEditor1', q=1, parent=1)
cmds.panel('graphEditor1', q=1, control=1)
cmds.panel('graphEditor1', q=1, type=1)
cmds.editor('graphEditor1GraphEd', q=1, control=1)
cmds.editor('graphEditor1GraphEd', q=1, panel=1)
for t in cmds.getPanel(allTypes=1):
    print(t)
    print('\t', cmds.getPanel(type=t))

