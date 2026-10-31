"""The final, measured layout settings for the A5 film."""
from pathlib import Path
import json

def apply_layout(sheet):
    beats={b["beat_id"]:b for b in sheet["beats"]}
    beats["B01"]["shot"]["remotion"]["props"].update({"fontSize":120,"lineSpacing":1.55,"charMs":22,"jitter":10,"brandLabel":"@NikBearBrown"})
    beats["B02"]["narration_text"]="Spatial makes this a three-dimensional surface program. Unshaded keeps fire independent of lights. The project uses Forward Plus with Direct Three D twelve. Forward Plus supports the ground Decal and scene S S I L; Compatibility would lose both. Without an explicit assignment, ALBEDO is white. COLOR carries vertex color, not a sampled texture."
    beats["B02"]["shot"]["remotion"]["props"]["notes"]=[{"label":"Shader type","value":"spatial; fire is unshaded"},{"label":"Renderer / driver","value":"Forward+ / D3D12\nDecal + SSIL\nCompatibility loses both"}]
    beats["B07"]["qc"]={"full_bleed":True,"contrast_reason":"The engine viewport intentionally fills the frame. Its full-color world has no flat page background. The essential visible health readout is checked locally; shader measurements are shown separately.","contrast_regions":[{"label":"Health readout, white text on the HUD","box":[0.064,0.298,0.082,0.311]}]}
    return sheet

if __name__=="__main__":
    path=Path(__file__).resolve().parents[2]/"youtube/claude-liam-downfall-a5-shaders-gamedev/beat_sheet.json"
    sheet=apply_layout(json.loads(path.read_text(encoding="utf-8")))
    path.write_text(json.dumps(sheet,indent=2)+"\n",encoding="utf-8")
