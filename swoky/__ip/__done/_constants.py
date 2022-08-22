from dataclasses import dataclass
from enum import Enum

# Anim
ANIMATED_CURVE_TYPES = ('animCurveTL', 'animCurveTA', 'animCurveTT', 'animCurveTU')

# pair of playbackSpeed|by|maxPlaybackSpeed
PLAYBACK_SPEED_STEPS = (
    (1, 1, 60),
    (.5, .5, 1),
    (.25, .252, 1),
    (0, 1, 1),
    (0, .1, 15)
)

# Camera
CAMERA_CYCLE_ORDER = ('side', 'front', 'persp')

# Common
XYZ = 'xyz'

# Hotkeys
NUMBER_KEYS_MAPPING = {
    1: {
        'nodeEditorPanel': 'simple',
        'graphEditor': 'spline'
    },
    2: {
        'nodeEditorPanel': 'connected',
        'graphEditor': 'flat'
    },
    3: {
        'nodeEditorPanel': 'all',
        'graphEditor': 'auto'
    },
    4: {
        'nodeEditorPanel': 'custom',
        'graphEditor': 'linear'
    },
}

# UI
EDITOR_STR_MAPPING = {
    'graphEditor': 'GraphEd',
    'nodeEditorPanel': 'NodeEditorEd'
}

@dataclass
class PanelData:
    panel_type: str
    editor: str
    # panel_type: str

class Panel(Enum):
    ModelPanel = PanelData('modelPanel', '')
    GraphEditor = PanelData('graphEditor','GraphEd')
    Outliner = PanelData('outlinerPanel','')
    NodeEditor = PanelData('nodeEditorPanel', 'NodeEditorEd')
    ScriptedPanel = PanelData('scriptedPanel','')

MODEL_PANEL_ELEMENT_SETS = {
    'playblast': [
        {'allObjects': False},
        {'polymeshes': True}
    ],
    'animate': [
        {'allObjects': False},
        {'polymeshes': True, 'nurbsCurves': True, 'nurbsSurfaces': True, 'locators': True, 'manipulators': True}
    ],
    'rig': [
        {'allObjects': False},
        {'polymeshes': True, 'nurbsCurves': True, 'nurbsSurfaces': True, 'locators': True, 'joints': True,
         'manipulators': True}
    ],
    'all': [
        {'allObjects': True},
    ]

}

# Graph Editor
GRAPH_EDITOR_LIST = 'graphEditorList'



class GraphEditor(Enum):
    Selected = 'Selected'
    Curve = 'Displayed'
class CurveState(Enum):
    GE = GraphEditor


class GraphEditorRetrievingParameters(object):
    VALID_MODE = 'visible'
    WORKING_ORDER = ('focus', 'visible')
    REVERSE_VISIBLE_ORDER = False

class GraphEditorState:
    Visible ='visible'
    WithFocus = 'withFocus'
    UnderPointer = 'underPointer'

GEState = GraphEditorState

GRAPH_EDITOR_FALLBACK_ORDER = (
    (GEState.UnderPointer, GEState.WithFocus),
    GEState.WithFocus,
    GEState.UnderPointer,
    GEState.visible
)



# Preferences
ALWAYS_SET_KEYFRAME = True