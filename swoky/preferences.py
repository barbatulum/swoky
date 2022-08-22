# Done
from .constants import GraphEditorState


ALWAYS_SET_KEYFRAME = True

GRAPH_EDITOR_FALLBACK_ORDER = (
    (GraphEditorState.UnderPointer, GraphEditorState.WithFocus),
    GraphEditorState.WithFocus,
    GraphEditorState.UnderPointer,
    GraphEditorState.visible
)

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
        {
            'polymeshes': True, 'nurbsCurves': True, 'nurbsSurfaces': True,
            'locators': True, 'joints': True, 'manipulators': True
        }
    ],
    'all': [
        {'allObjects': True},
    ]

}

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
