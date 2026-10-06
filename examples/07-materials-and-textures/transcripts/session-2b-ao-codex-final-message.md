Implemented and verified the hull AO change.

Changes:

- Added external `ORMMaterial3D` using hull diffuse, normal, and ARM textures.
- Corrected the glTF importer’s nested `Use External` mapping so reimports preserve it.
- ARM channels now map as R=AO, G=roughness, B=metallic.
- Preserved hull transparency, culling, metallic/roughness scalars, texture channels, albedo, and normal settings.
- The separate metallic/roughness texture slots were replaced by `orm_texture`; this is required by ORM packing.
- Rigging and sails remain importer-generated `StandardMaterial3D` resources with their audited settings unchanged.
- Deleted `godot/diag.gd` and its generated UID.
- No commit was created.

Validation output:

```text
test_materials.gd:
RESULT 100 checks, 0 failures; headless state only — see below for limitations

test_settings.gd:
RESULT 17 checks, 0 failures; headless state only, no pixel/performance proof
```

The required headless reimport completed successfully. Godot printed nonfatal sandbox-related warnings about macOS certificates, log files, and editor settings.

Human checks for the running scene:

- Compare recessed hull seams, plank gaps, fittings, and other crevices before and after the change; they should gain subtle AO darkening.
- Confirm exposed hull surfaces do not become broadly or unnaturally darker.
- Check that hull base color, glossiness, metal fittings, normal detail, and double-sided rendering otherwise look unchanged.
- Inspect the hull under both direct and ambient lighting.
- Confirm rigging and sails show no visual change.
- Check for AO artifacts around UV seams or strongly contrasting texels in the ARM map.