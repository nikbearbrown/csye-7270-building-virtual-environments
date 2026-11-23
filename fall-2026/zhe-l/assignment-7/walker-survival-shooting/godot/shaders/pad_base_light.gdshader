shader_type spatial;  // 这是给 3D 物体用的 shader，我们用它画平板的屏幕
render_mode unshaded;  // 屏幕自己发光，不受场景里的灯照亮或照暗，所以我们不让它参与光照
uniform vec4 cold_white: source_color = vec4(0.902, 0.969, 0.969, 1.0);  // 屏幕的冷白色调；画面会被它染上一点点冷色，没有画面时屏幕就是这个颜色
uniform float pad_light_data:hint_range(0.0, 1.0) = 0.0;  // 屏幕亮度：0 = 灭（全黑），1 = 最亮；由 TabletDevice.set_screen_lit() 设成 0 或者 light_strength_percentage
uniform sampler2D screen_image: source_color, filter_linear;  // 屏幕上要显示的画面（平板系统那块画布）；由 TabletDevice 交进来，没交的时候 Godot 给一张纯白图，屏幕就和以前一样是冷白色
void fragment(){  // Godot 画屏幕上的每一个点时都会执行一次这里，决定这个点是什么颜色
	vec3 picture = texture(screen_image, UV).rgb;  // 首先我们按这个点在屏幕上的位置（UV），去画面里取出对应那个点的颜色
	ALBEDO = picture * cold_white.rgb * pad_light_data;  // 然后把画面染上冷白色调，再乘上亮度：亮度 0 时整块屏幕是黑的，亮度越高画面越亮
}
