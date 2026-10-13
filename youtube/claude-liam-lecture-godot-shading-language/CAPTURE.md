# Capture protocol
Native engine: /Applications/Godot.app/Contents/MacOS/Godot
Version: 4.7.2.stable.official.ed1daf0bf
Renderer: Compatibility / OpenGL 4.1 Metal / Apple M4 Pro.

From books/:
```bash
/Applications/Godot.app/Contents/MacOS/Godot --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/godot -- --capture > /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/evidence/godot-run.log 2>&1
/Applications/Godot.app/Contents/MacOS/Godot --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/godot --script res://negative.gd > /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/evidence/negative-type.log 2>&1
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/verify_evidence.py
```

This is a shader teaching harness. Scripted parameters and actual viewport readbacks, not human play or a real-time speed measurement. Local GPU rendering is used, not the headless dummy renderer. The test does not alter an existing student game. The fixed source and image hashes are in evidence/sha256.json.

Native editor capture: opened only this lab in Godot; selected preview.tscn, 2D, ColorRect, and its Material field; captured through cua. No editor preferences were changed. Browser screenshots and exact URL/status records are retained separately. Concept diagrams are labeled and are not engine screenshots.
