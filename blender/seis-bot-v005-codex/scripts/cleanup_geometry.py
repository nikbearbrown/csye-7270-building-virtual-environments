"""Repair genuinely degenerate evaluated geometry before rigid FK binding.

The exact audit threshold is preserved. Only meshes containing evaluated
triangles below that threshold are baked. Their original mesh and modifier
stack are archived as hidden editable objects outside EXPORT and U.PARTS.
No rendering, rig binding, scene reset or file save is performed here.
"""
from __future__ import annotations
import bpy
import bmesh
import json
import math
from pathlib import Path

CROSS_LENGTH_LIMIT = 1e-13
ZERO_FACE_AREA_LIMIT = 5e-14
MERGE_DISTANCE = 1e-7
SOURCE_COLLECTION = 'SOURCE_GEOMETRY'


def _attribute_schema(mesh):
    # Blender's internal topology attributes necessarily change after repairing
    # connectivity. Preserve and verify the user-facing data layers instead.
    return {a.name: {'domain':a.domain,'data_type':a.data_type}
            for a in mesh.attributes
            if not a.name.startswith('.') and a.name not in {'position','material_index'}}


def _triangle_stats(mesh):
    mesh.calc_loop_triangles()
    bad=0
    for tri in mesh.loop_triangles:
        a,b,c=(mesh.vertices[i].co for i in tri.vertices)
        if (b-a).cross(c-a).length < CROSS_LENGTH_LIMIT:
            bad += 1
    nonfinite=sum(1 for v in mesh.vertices if not all(math.isfinite(c) for c in v.co))
    return {'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),
            'triangles':len(mesh.loop_triangles),'degenerate_triangles':bad,
            'nonfinite_vertices':nonfinite}


def _evaluated_stats(obj,depsgraph):
    evaluated=obj.evaluated_get(depsgraph)
    temporary=evaluated.to_mesh(preserve_all_data_layers=True,depsgraph=depsgraph)
    try:
        return _triangle_stats(temporary)
    finally:
        evaluated.to_mesh_clear()


def _source_collection():
    collection=bpy.data.collections.get(SOURCE_COLLECTION)
    if collection is None:
        collection=bpy.data.collections.new(SOURCE_COLLECTION)
        bpy.context.scene.collection.children.link(collection)
    collection.hide_render=True
    collection.hide_viewport=True
    return collection


def _archive(obj,collection):
    source=obj.copy()
    source.data=obj.data.copy()
    source.name='SOURCE_'+obj.name
    source.data.name=source.name
    collection.objects.link(source)
    source.hide_render=True
    source.hide_viewport=True
    source['source_for_export_object']=obj.name
    source['archive_reason']='Original editable mesh and modifiers before degenerate-triangle cleanup'
    source['exclude_from_export']=True
    # Do not pass through U.finish: the archive deliberately has no U.PARTS entry.
    return source


def _repair_mesh(mesh):
    """Repair topology with explicit fixed tolerances; never loosen audit limits."""
    bm=bmesh.new()
    try:
        bm.from_mesh(mesh)
        before={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces)}
        if bm.faces:
            bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        vertices_before_merge=len(bm.verts)
        if bm.verts:
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=MERGE_DISTANCE)
        vertices_after_merge=len(bm.verts)
        if bm.edges:
            bmesh.ops.dissolve_degenerate(bm,dist=MERGE_DISTANCE,edges=list(bm.edges))
        # Dissolving can produce non-triangle polygons. Re-triangulate before
        # removing zero-area faces so the final mesh uses the audited topology.
        if bm.faces:
            bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
        # Match the audit's mathutils cross product exactly. BMFace.calc_area()
        # can differ around this scale because its internal arithmetic differs.
        nontriangles=[face for face in bm.faces if len(face.verts)!=3]
        if nontriangles:
            raise RuntimeError('Triangulation left non-triangle polygons before cleanup')
        zero_faces=[]
        for face in bm.faces:
            a,b,c=(vertex.co for vertex in face.verts)
            cross_length=(b-a).cross(c-a).length
            if cross_length < CROSS_LENGTH_LIMIT or cross_length <= 2*ZERO_FACE_AREA_LIMIT:
                zero_faces.append(face)
        deleted_faces=len(zero_faces)
        if zero_faces:
            bmesh.ops.delete(bm,geom=zero_faces,context='FACES_ONLY')
        # Edges whose vertices coincide can survive after an empty face is
        # removed. Removing them cannot change a visible surface.
        zero_edges=[edge for edge in bm.edges if not edge.link_faces and edge.calc_length() <= MERGE_DISTANCE]
        if zero_edges:
            bmesh.ops.delete(bm,geom=zero_edges,context='EDGES')
        loose_vertices=[v for v in bm.verts if not v.link_edges and not v.link_faces]
        if loose_vertices:
            bmesh.ops.delete(bm,geom=loose_vertices,context='VERTS')
        if bm.faces:
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.normal_update()
        after={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces)}
        bm.to_mesh(mesh)
        mesh.update()
        # A second decision uses the final Mesh triangle buffer, identical to
        # the audit. This also catches coordinate rounding during bm.to_mesh().
        exact_deleted=_prune_mesh_triangles_by_audit(mesh)
        return {'before':before,'after':after,
                'post_mesh_audit_faces_deleted':exact_deleted,
                'vertices_merged':vertices_before_merge-vertices_after_merge,
                'zero_area_faces_deleted':deleted_faces,
                'isolated_degenerate_edges_deleted':len(zero_edges),
                'isolated_vertices_deleted':len(loose_vertices)}
    finally:
        bm.free()



def _prune_mesh_triangles_by_audit(mesh):
    """Delete only faces whose stored Mesh triangles fail the unchanged audit.

    Topology has already been triangulated, so polygon_index maps each flagged
    loop triangle to exactly one face. No polygon containing good triangles is
    discarded. Test coordinates are read after bm.to_mesh, not inferred from
    bmesh area calculations.
    """
    total=0
    for attempt in range(3):
        mesh.calc_loop_triangles()
        bad_polygons=set()
        for tri in mesh.loop_triangles:
            a,b,c=(mesh.vertices[i].co for i in tri.vertices)
            cross_length=(b-a).cross(c-a).length
            if cross_length < CROSS_LENGTH_LIMIT or cross_length <= 2*ZERO_FACE_AREA_LIMIT:
                if len(mesh.polygons[tri.polygon_index].vertices)!=3:
                    raise RuntimeError('Audit pruning encountered a non-triangle polygon')
                bad_polygons.add(tri.polygon_index)
        if not bad_polygons:
            return total
        prune=bmesh.new()
        try:
            prune.from_mesh(mesh)
            prune.faces.ensure_lookup_table()
            targets=[prune.faces[index] for index in sorted(bad_polygons)]
            bmesh.ops.delete(prune,geom=targets,context='FACES_ONLY')
            total+=len(targets)
            if prune.faces:
                bmesh.ops.recalc_face_normals(prune,faces=list(prune.faces))
            prune.normal_update()
            prune.to_mesh(mesh)
            mesh.update()
        finally:
            prune.free()
    return total


def _triangle_diagnostics(mesh,limit=20):
    mesh.calc_loop_triangles()
    output=[]
    for tri in mesh.loop_triangles:
        a,b,c=(mesh.vertices[i].co for i in tri.vertices)
        cross_length=(b-a).cross(c-a).length
        if cross_length < CROSS_LENGTH_LIMIT:
            output.append({'triangle':tri.index,'polygon':tri.polygon_index,
                           'cross_length':cross_length,
                           'vertices':[list(a),list(b),list(c)]})
            if len(output)>=limit: break
    return output


def clean(U):
    """Call after transforms are applied and before any FK vertex groups exist."""
    output=Path(U.ROOT)/'reports'/'geometry-cleanup.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    collection=bpy.data.collections.get('EXPORT')
    if collection is None:
        raise RuntimeError('Expected EXPORT collection before geometry cleanup')
    objects=[o for o in collection.objects if o.type=='MESH']
    report={
        'asset':'SEIS_BOT_V005','operation':'evaluated degenerate geometry cleanup',
        'status':'RUNNING','audit_cross_length_limit':CROSS_LENGTH_LIMIT,
        'face_area_delete_limit':ZERO_FACE_AREA_LIMIT,
        'merge_and_degenerate_edge_distance_metres':MERGE_DISTANCE,
        'source_collection':SOURCE_COLLECTION,
        'source_preservation':'Original editable mesh and modifier stack are hidden outside EXPORT; Python model source remains unchanged.',
        'examined_meshes':len(objects),'objects_baked':0,
        'degenerate_triangles_before':0,'degenerate_triangles_after':0,
        'objects':[],'errors':[],
    }
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    archive_collection=None
    for obj in objects:
        try:
            before=_evaluated_stats(obj,depsgraph)
            report['degenerate_triangles_before']+=before['degenerate_triangles']
            if before['nonfinite_vertices']:
                report['errors'].append(f'{obj.name}: nonfinite vertices already present; refused to conceal them')
            if not before['degenerate_triangles']:
                continue
            if obj.vertex_groups:
                report['errors'].append(f'{obj.name}: vertex groups already exist; cleanup must run before rig binding')
                report['degenerate_triangles_after']+=before['degenerate_triangles']
                continue
            if any(abs(value-1)>1e-6 for value in obj.scale) or any(abs(value)>1e-6 for value in obj.rotation_euler):
                report['errors'].append(f'{obj.name}: rotation or scale is not applied; refused to bake in this state')
                report['degenerate_triangles_after']+=before['degenerate_triangles']
                continue
            evaluated=obj.evaluated_get(depsgraph)
            baked=bpy.data.meshes.new_from_object(evaluated,preserve_all_data_layers=True,depsgraph=depsgraph)
            original_attributes=_attribute_schema(baked)
            original_materials=[m.name if m else None for m in baked.materials]
            modifier_names=[m.name for m in obj.modifiers]
            if archive_collection is None:
                archive_collection=_source_collection()
            archive=_archive(obj,archive_collection)
            entry={'name':obj.name,'source_archive':archive.name,'before':before,
                   'baked_modifiers':modifier_names,
                   'materials_before':original_materials,
                   'attributes_before':original_attributes,'repair_passes':[]}
            report['objects'].append(entry)
            # Replace only this problematic object's mesh. Hidden archive owns a
            # separate copy of its editable pre-bake mesh and modifier stack.
            previous_mesh=obj.data
            obj.data=baked
            obj.modifiers.clear()
            if previous_mesh.users==0:
                bpy.data.meshes.remove(previous_mesh)
            else:
                previous_mesh.name='PREBAKE_'+obj.name
            baked.name=obj.name
            obj['geometry_cleanup_source']=archive.name
            obj['geometry_cleanup_tolerance']=CROSS_LENGTH_LIMIT
            report['objects_baked']+=1
            for attempt in range(3):
                entry['repair_passes'].append(_repair_mesh(baked))
                stats=_triangle_stats(baked)
                if stats['degenerate_triangles']==0:
                    break
            attributes_after=_attribute_schema(baked)
            materials_after=[m.name if m else None for m in baked.materials]
            entry['materials_after']=materials_after
            entry['attributes_after']=attributes_after
            lost=[name for name,schema in original_attributes.items() if attributes_after.get(name)!=schema]
            if lost:
                report['errors'].append(f'{obj.name}: custom attributes missing or changed schema: '+', '.join(lost))
            if materials_after!=original_materials:
                report['errors'].append(f'{obj.name}: material slots changed during cleanup')
            bpy.context.view_layer.update()
            depsgraph=bpy.context.evaluated_depsgraph_get()
            after=_evaluated_stats(obj,depsgraph)
            entry['after']=after
            if after['degenerate_triangles']:
                entry['remaining_triangle_diagnostics']=_triangle_diagnostics(baked)
            report['degenerate_triangles_after']+=after['degenerate_triangles']
            if after['degenerate_triangles']:
                report['errors'].append(f'{obj.name}: {after["degenerate_triangles"]} evaluated degenerate triangles remain at the unchanged audit threshold')
            if after['nonfinite_vertices']:
                report['errors'].append(f'{obj.name}: nonfinite vertices after cleanup')
            print('GEOMETRY CLEANUP',obj.name,before['degenerate_triangles'],'->',after['degenerate_triangles'],flush=True)
        except Exception as exc:
            report['errors'].append(f'{obj.name}: {type(exc).__name__}: {exc}')
            report['status']='FAIL'
            output.write_text(json.dumps(report,indent=2),encoding='utf-8')
            raise
    # Full fresh evaluated scan catches any dependency changes from modifier
    # baking; none are hidden by checking only the repaired local mesh.
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    remaining=[]
    for obj in objects:
        stats=_evaluated_stats(obj,depsgraph)
        if stats['degenerate_triangles'] or stats['nonfinite_vertices']:
            remaining.append({'name':obj.name,**stats})
    report['remaining_problem_objects']=remaining
    report['degenerate_triangles_after']=sum(o['degenerate_triangles'] for o in remaining)
    report['status']='PASS' if not report['errors'] and not remaining else 'FAIL'
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','examined_meshes','objects_baked','degenerate_triangles_before','degenerate_triangles_after','errors')},indent=2),flush=True)
    if report['status']!='PASS':
        raise RuntimeError(f'Geometry cleanup did not pass; inspect {output}')
    return report
