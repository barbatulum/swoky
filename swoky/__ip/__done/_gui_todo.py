
def shade_switch():
    """
    wireframe-shaded-lighted three phase switch
    """

from maya import cmds, mel

from . import panel_tools
from .. import constants as const
from ..constants import PanelType



setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);
setAnimationDetailsVisibility(!`optionVar -q animationDetailsVisibility`);


element_mapping = {
    "Animation Details": ("setAnimationDetailsVisibility", "animationDetailsVisibility"),

    }


element = "Animation Details"
# ToggleAnimationDetails;
eval_cmd = "{0}(!`optionVar -q {1}`)".format(*element_mapping[element])
mel.eval(eval_cmd)
setAnimationDetailsVisibility(!`optionVar -q animationDetailsVisibility`);

ToggleCacheVisibility;
from maya.plugin.evaluator.CacheUiHud import CachePreferenceHud; CachePreferenceHud().set_value( not CachePreferenceHud().get_value() )

ToggleCameraNames;
setCameraNamesVisibility(!`optionVar -q cameraNamesVisibility`);

ToggleCapsLockDisplay;
setCapsLockVisibility(!`optionVar -q capsLockVisibility`);

ToggleCurrentContainerHud;
setCurrentContainerVisibility(!`optionVar -q currentContainerVisibility`);

ToggleCurrentFrame;
setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);

ToggleEvaluationManagerVisibility;
ToggleEvaluationManagerHUDVisibility;
ToggleFocalLength;
setFocalLengthVisibility(!`optionVar -q focalLengthVisibility`);

ToggleFrameRate;
setFrameRateVisibility(!`optionVar -q frameRateVisibility`);

ToggleHikDetails;
setHikDetailsVisibility(!`optionVar -q hikDetailsVisibility`);

ToggleMaterialLoadingDetailsVisibility;
ToggleMaterialLoadingDetailsHUDVisibility(!`optionVar -q materialLoadingDetailsVisibility`);

ToggleObjectDetails;
setObjectDetailsVisibility(!`optionVar -q objectDetailsVisibility`);

ToggleOriginAxis;
toggleAxis -o (!`toggleAxis -q -o`);

ToggleParticleCount;
setParticleCountVisibility(!`optionVar -q particleCountVisibility`);

TogglePolyCount;
setPolyCountVisibility(!`optionVar -q polyCountVisibility`);

ToggleSceneTimecode;
setSceneTimecodeVisibility(!`optionVar -q sceneTimecodeVisibility`);

ToggleSelectDetails;
setSelectDetailsVisibility(!`optionVar -q selectDetailsVisibility`);

ToggleSymmetryDisplay;
setSymmetryVisibility(!`optionVar -q symmetryVisibility`);

ToggleViewAxis;
setViewAxisVisibility(!`optionVar -q viewAxisVisibility`);

ToggleViewCube;
viewManip -v (! `viewManip -q -v`);

ToggleViewportRenderer;
setViewportRendererVisibility(!`optionVar -q viewportRendererVisibility`);

ToggleXGenDisplayHUD;
setXGenHUDVisibility(!`optionVar -q xgenHUDVisibility`);





def set_node_vis_preset(preset, panel=None):
    """
    Based on the preset, set the visibilities of elements of a panel
    todo: an UI for user to set the vis
    """

    panel_info = panel_tools.get_panel_info(panel=panel)

    if not panel_info or panel_info.panel_type != PanelType.MODEL_PANEL:
        return
    presets = const.MODEL_PANEL_ELEMENT_SETS.get(preset)
    if not presets:
        return
    for _preset in presets:
        cmds.modelEditor(panel, e=True, **_preset)

