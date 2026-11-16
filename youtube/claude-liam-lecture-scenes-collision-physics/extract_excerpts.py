from pathlib import Path
import json
R=Path(__file__).resolve().parent
# Real excerpts preserve exact executed lines, and record their line ranges.
def excerpt(key,file,start,end=None):
 lines=(R/file).read_text().splitlines()
 a=next(i for i,x in enumerate(lines) if start in x)
 b=next((i for i in range(a+1,len(lines)) if end and end in lines[i]),len(lines))
 picked=lines[a:b]
 while picked and not picked[-1].strip():picked.pop()
 (R/'excerpts'/f'{key}.txt').write_text('\n'.join(picked)+'\n')
 return {'file':file,'start_line':a+1,'end_line':a+len(picked),'key':key}
M=[]
M.append(excerpt('scene','godot/actor.tscn','[gd_scene'))
M.append(excerpt('instances','godot/lab.gd','    var a := packed.instantiate','    check("independent'))
M.append(excerpt('block','godot/block.gd','func bump'))
M.append(excerpt('format','godot/lab.gd','    var packed := PackedScene','    var a := packed'))
M.append(excerpt('impulse','godot/lab.gd','    rb.position=','    label("mass'))
M.append(excerpt('minimal','godot/player.gd','func _physics_process','func step'))
M.append(excerpt('bits','godot/layers.gd','static func bit'))
M.append(excerpt('unique','godot/supplemental.gd','    left.shape = shape','    left.free'))
M.append(excerpt('methods','godot/player.gd','    move_and_slide()','    # Floor state'))
M.append(excerpt('gravity','godot/player.gd','    var g :=','    var rate'))
M.append(excerpt('horizontal','godot/player.gd','    var rate :=','    if buffer'))
M.append(excerpt('cut','godot/player.gd','    if released','    move_and_slide()'))
M.append(excerpt('platform','godot/platform.gd','extends'))
M.append(excerpt('coin','godot/coin.gd','func _on_body_entered','    # This lab'))
M.append(excerpt('enemy','godot/enemy.gd','func on_top','func on_side'))
M.append(excerpt('tiles','godot/lab.gd','    var td:=','    p=player(Vector2(200'))
M.append(excerpt('contact','godot/tile_hit.gd','static func'))
M.append(excerpt('drop','godot/player.gd','func drop_through'))
M.append(excerpt('respawn','godot/player.gd','func respawn','func drop_through'))
M.append(excerpt('debris','godot/debris.gd','        add_child(piece)'))
# Additional exact lines are appended with source comments and a mapping.
for key,file,needle in [('minimal','godot/player.gd','    move_and_slide()'),('methods','godot/lab.gd','    var sweep:=p.move_and_collide'),('bits','godot/lab.gd','    check("layer 3 bit"'),('cut','godot/player.gd','    velocity.y = jump_velocity * 0.6'),('platform','godot/player.gd','            rb.apply_central_impulse'),('debris','godot/debris.gd','    spawn.call_deferred(at)')]:
 lines=(R/file).read_text().splitlines();idx=next(i for i,x in enumerate(lines) if needle in x)
 p=R/'excerpts'/f'{key}.txt';p.write_text(p.read_text()+'\n# Also executed: '+file+':'+str(idx+1)+'\n'+lines[idx]+'\n')
 M.append({'key':key,'file':file,'start_line':idx+1,'end_line':idx+1})
(R/'evidence/excerpt-map.json').write_text(json.dumps(M,indent=2))
(R/'CONVENTIONS.md').write_text('''# Suggested project conventions — review before adopting

Engine: Godot 4.7.x for this lab; record the actual version and backend.

- Prefer reusable scenes with injected dependencies or signals. Run each scene in a suitable standalone fixture.
- Keep internal references local; parents wire children. Autoloads hold persistent state when needed.
- Preserve existing scene and resource identifiers. Save generated scene trees through PackedScene/ResourceSaver.
- Name collision layers in project settings and mirror one-based numbers in layers.gd.
- Resize shape resources rather than scaling physics bodies. Duplicate shared resources when independence is intended.
- In overlap callbacks, defer physics-server mutations; use an immediate gameplay latch for one-time events.
- Use physics callbacks for collision-based motion. Acceleration uses delta; move_and_slide consumes velocity directly.
- Distinguish previous-move floor state from current-move floor state. Reset interpolation after teleports.
- Use contacts and coordinate conversion for tile selection; document probe distance and boundary behavior.
- Treat timestep travel distance as a diagnostic, never a sufficient no-tunneling proof.
- Run the isolated physics tests, inspect errors, and record the version. Report untested behaviors and human-playtest needs.
- No universal claim that all scenes run without context or all agents lack vision: state the actual harness and available evidence.

Do not replace a reference game's existing AGENTS.md or CLAUDE.md without reviewing these policies in that project's context.
''')
(R/'excerpts/conventions.txt').write_text('Engine: Godot 4.7.x for this lab; record version and backend.\n\nName layers; mirror one-based numbers.\nResize shapes; duplicate shared resources deliberately.\nUse physics callbacks for collision-based motion.\nDefer physics mutations in overlap callbacks.\nRecord what ran and what still needs a playtest.\n')
