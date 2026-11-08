shader_type canvas_item;
// The outer outline (CHARACTER-SHEET.md, CHANGE-BRIEF.md build step 2): a dark
// line of even width around everything solid in a sprite, drawn under its
// edge, so it is the same in every frame whatever the image model drew. Used
// on characters, enemies and hazards, whose textures are stored at 2 texture
// px per game px and keep at least 12 texture px of transparent margin.
//
// A pixel counts as solid from alpha solid_from, fully from solid_to, so the
// faint tail of the slash's trail gets no outline. The sprite's modulate still
// applies, so a flashing sprite flashes with its outline.

uniform vec3 line_color : source_color = vec3(0.1608, 0.0588, 0.0510); // #290F0D, the art's line colour
uniform float width = 8.0; // texture px: 4 game px at 2 texture px per game px (set in outline.tres)
uniform float solid_from = 0.5;
uniform float solid_to = 0.9;

varying vec4 modulate;

void vertex() {
	modulate = COLOR;
}

void fragment() {
	vec4 own = texture(TEXTURE, UV);
	// The most solid neighbour within the width: three rings, the outer one
	// sampled densely enough that a thin tip (the cowlick, the sword's point)
	// still gets a whole line.
	float cover = 0.0;
	for (int ring = 1; ring <= 3; ring++) {
		float radius = width * float(ring) / 3.0;
		int count = 8 * ring;
		for (int i = 0; i < count; i++) {
			float angle = TAU * (float(i) + 0.5 * float(ring - 1)) / float(count);
			vec2 uv = UV + vec2(cos(angle), sin(angle)) * radius * TEXTURE_PIXEL_SIZE;
			cover = max(cover, smoothstep(solid_from, solid_to, texture(TEXTURE, uv).a));
		}
	}
	// The sprite over its outline.
	float alpha = own.a + cover * (1.0 - own.a);
	vec3 rgb = (own.rgb * own.a + line_color * cover * (1.0 - own.a)) / max(alpha, 0.0001);
	COLOR = vec4(rgb, alpha) * modulate;
}
