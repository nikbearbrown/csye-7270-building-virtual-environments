extends SceneTree
func _initialize():
 for cls in ["BaseMaterial3D","ParticleProcessMaterial","GPUParticlesCollisionBox3D"]:
  for key in ClassDB.class_get_integer_constant_list(cls):
   if key in ["SHADING_MODE_UNSHADED","BLEND_MODE_ADD","BILLBOARD_PARTICLES","TRANSPARENCY_ALPHA","EMISSION_SHAPE_BOX","EMISSION_SHAPE_SPHERE","COLLISION_RIGID"]:
    print(cls," ",key," = ",ClassDB.class_get_integer_constant(cls,key))
 var collision=GPUParticlesCollisionBox3D.new();assert(collision.get("size")!=null);print("Collision box size ",collision.size);collision.free();quit()
