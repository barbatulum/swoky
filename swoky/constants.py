# Done
from enum import Enum

# Anim
ANIMATED_CURVE_TYPES = ('animCurveTL', 'animCurveTA', 'animCurveTT', 'animCurveTU')

# Maya Kwargs
class CompatibleKwargs:
    getPanel = ('underPointer', 'withFocus')

# UI

class FixedGUI:
    LayerEditor = 'LayerEditorDisplayLayerLayout'

class Panel(Enum):
    # INGEST = dict(width=50, desc="Ingest", order=0)
    ModelPanel = dict(
        panel_type='modelPanel',
        editor=''
    )
    GraphEditor = dict(
        panel_type='graphEditor',
        editor='GraphEd'
    )
    Outliner = dict(
        panel_type='outlinerPanel',
        editor=''
    )
    NodeEditor = dict(
        panel_type='nodeEditorPanel',
        editor='NodeEditorEd'
    )
    ScriptedPanel = dict(
        panel_type='scriptedPanel',
        editor=''
    )


    def __init__(self, *args):
        for k, v in args[0].items():
            setattr(self, k, v)

    @classmethod
    def get(cls, type_string):
        if not hasattr(cls, '_map'):
            cls._map = {panel.panel_type: panel for panel in cls.__members__.values()}
        return cls._map.get(type_string)

    def __eq__(self, other):
        if hasattr(other, 'panel_type'):
            other = other.panel_type
        elif not isinstance(other, str):
            other = str(other)
        return self.panel_type == other


# todo: Find the way to query it
class FixedGui:
    GraphEditorList = "graphEditorList"


class GraphEditor(Enum):
    Selected = 'Selected'
    Curve = 'Displayed'


class CurveState(Enum):
    GE = GraphEditor


class GraphEditorState:
    Visible ='visible'
    WithFocus = 'withFocus'
    UnderPointer = 'underPointer'
