#!/usr/bin/env bash
# What version control shows for the same one-value change (PostMetal metallic 0.8 -> 0.2) in the two glTF forms.
# Needs out/{a,b}_{gltf,glb}/ from:  Blender -b --factory-startup --python-exit-code 1 --python export_forms.py
set -u
cd "$(dirname "$0")"
T=$(mktemp -d)
cp out/a_gltf/checkpoint_post.gltf "$T/old.gltf"; cp out/b_gltf/checkpoint_post.gltf "$T/new.gltf"
cp out/a_glb/checkpoint_post.glb   "$T/old.glb";  cp out/b_glb/checkpoint_post.glb   "$T/new.glb"
{
  echo '$ git diff --no-index old.gltf new.gltf'; (cd "$T" && git --no-pager diff --no-index old.gltf new.gltf)
  echo; echo '$ git diff --no-index old.glb new.glb'; (cd "$T" && git --no-pager diff --no-index old.glb new.glb)
  echo; echo '$ ls -l out/a_gltf out/a_glb'; ls -l out/a_gltf out/a_glb | sed 's/@//'
} | tee out/forms-diff.log
rm -rf "$T"
