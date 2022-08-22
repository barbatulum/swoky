import sys

package_path = "C:/repos/swoky"
if package_path not in sys.path:
    sys.path.append(package_path)

from maya import cmds


from swoky._library.ui import layer
imp.reload(layer)

