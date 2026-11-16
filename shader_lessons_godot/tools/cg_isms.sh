#!/bin/zsh
# cg_isms.sh: compile-time traps. Each line below is a Cg habit pasted into a minimal Godot spatial shader and run through the series Lab's
# check_shader.sh (Forward+). The result is the compiler's own message. Output: evidence/compile/cg-isms.txt
# usage: tools/cg_isms.sh [abs path of the output file]
set -u
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$PROJ/../youtube/_godot-shaders-series/lab"
OUT="${1:-$PROJ/evidence/compile/cg-isms.txt}"
SCR=/private/tmp/claude-501/sl-scratch-isms
mkdir -p "$SCR" "$(dirname "$OUT")"
: > "$OUT"
echo "# Cg habits that do not compile in Godot 4.7.2 (Lab check_shader.sh, Forward+). One block per habit: the Cg line, then the compiler's reply." >> "$OUT"
typeset -A CASES
ORDER=(control saturate lerp frac float3_type mul_matrix tex2d texcube pow_vec_float assign_vec_to_float int_literal_minus int_literal_times brace_init semantics_colour float4x4_type mat_row_index)
CASES[control]='vec3 c = vec3(0.5); ALBEDO = c;'
CASES[saturate]='float x = saturate(0.5); ALBEDO = vec3(x);'
CASES[lerp]='vec3 c = lerp(vec3(0.0), vec3(1.0), 0.5); ALBEDO = c;'
CASES[frac]='float x = frac(1.25); ALBEDO = vec3(x);'
CASES[float3_type]='float3 c = vec3(0.5); ALBEDO = c;'
CASES[mul_matrix]='vec4 p = mul(PROJECTION_MATRIX, vec4(1.0)); ALBEDO = p.xyz;'
CASES[tex2d]='ALBEDO = tex2D(t, UV).rgb;'
CASES[texcube]='ALBEDO = texCUBE(cm, vec3(0.0, 0.0, 1.0)).rgb;'
CASES[pow_vec_float]='vec3 c = pow(vec3(0.5), 2.0); ALBEDO = c;'
CASES[assign_vec_to_float]='vec3 f = vec3(0.5); float a = f; ALBEDO = vec3(a);'
CASES[int_literal_minus]='float x = 0.25; float y = 1 - x; ALBEDO = vec3(y);'
CASES[int_literal_times]='vec3 c = vec3(0.4) * 2 - 1; ALBEDO = c;'
CASES[brace_init]='vec3 c = {1.0, 0.0, 0.0}; ALBEDO = c;'
CASES[semantics_colour]='vec4 pShader(vec2 uv) : COLOR { return vec4(1.0); } void x() {}'
CASES[float4x4_type]='float4x4 m; ALBEDO = vec3(1.0);'
CASES[mat_row_index]='mat4 m = INV_VIEW_MATRIX; vec3 c = vec3(m[0].w, m[1].w, m[2].w); ALBEDO = c;'
for K in $ORDER; do
  F="$SCR/$K.gdshader"
  printf 'shader_type spatial;\nrender_mode unshaded;\nuniform sampler2D t;\nuniform samplerCube cm;\nvoid fragment() {\n\t%s\n}\n' "${CASES[$K]}" > "$F"
  if [ "$K" = "semantics_colour" ]; then printf 'shader_type spatial;\nrender_mode unshaded;\n%s\nvoid fragment() { ALBEDO = vec3(1.0); }\n' "${CASES[$K]}" > "$F"; fi
  echo "" >> "$OUT"
  echo "## $K   |   ${CASES[$K]}" >> "$OUT"
  RES="$(timeout 90 "$LAB/check_shader.sh" "$F" --kind quad3d --renderer forward_plus 2>&1)"
  CODE=$?
  if [ $CODE -eq 0 ]; then echo "COMPILES (exit 0)" >> "$OUT"; else echo "$RES" | grep -E "SHADER ERROR" | head -3 >> "$OUT"; echo "(exit $CODE)" >> "$OUT"; fi
done
rm -rf "$SCR"
echo "wrote $OUT"
