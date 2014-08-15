#bpy.data.objects[3].to_mesh(bpy.context.scene, True, 'RENDER').vertices[0].groups[0].group
#bpy.data.objects[3].vertex_groups[0].name

import bpy
import math
import mathutils
import json

def do_export(filepath):
  
  armatures_data = []
  for armature in bpy.data.armatures:
    bones_data = []
    for bone in armature.bones:
      translation = bone.head
      matrix = bone.matrix
      scale = matrix.to_scale()
      orientation = matrix.to_quaternion()
      bones_data.append({
        "name" : bone.name, 
        "scale" : {"x" : scale.x, "y" : scale.y, "z" : scale.z},
        "translation" : {"x" : translation.x, "y" : translation.y, "z" : translation.z},
        "orientation" : {"x" : orientation.x, "y" : orientation.y, "z" : orientation.z, "w" : orientation.w }
      })
    armatures_data.append({"name" : armature.name, "bones" : bones_data})

  submeshes_data = []
  for obj in bpy.data.objects:
      if obj.type == 'MESH':
          mesh = obj.to_mesh(bpy.context.scene, True, 'RENDER')
          X_ROT = mathutils.Matrix.Rotation(-math.pi/2, 4, 'X')
          mesh.transform(X_ROT * obj.matrix_world)
          mesh.update(calc_tessface=True)
          mesh.calc_normals()

          vertices = []
          normals = []
          weights = []
          vertex_groups = []

          for group in obj.vertex_groups:
            vertex_groups.append({"name":group.name,"index":group.index})
          
          for vertex in mesh.vertices:
              v = vertex.co
              vertices.append(v.x)
              vertices.append(v.y)
              vertices.append(v.z)

              n = vertex.normal
              n.normalize()

              normals.append(n.x)
              normals.append(n.y)
              normals.append(n.z)

              vertex_weights = []
              for group in vertex.groups:
                bone_name = obj.vertex_groups[group.group].name

                bone_index = 0
                for bone in armature.bones:
                  if (bone.name == bone_name):
                    vertex_weights.append({"index":bone_index, "weight":group.weight})
                  bone_index = bone_index + 1
                
              weights.append(vertex_weights)

          indices = []
          for polygon in mesh.polygons:
              if len(polygon.vertices) == 4:
                  a = polygon.vertices[0]
                  b = polygon.vertices[1]
                  c = polygon.vertices[2]
                  d = polygon.vertices[3]

                  indices.append(a)
                  indices.append(b)
                  indices.append(c)
                  indices.append(c)
                  indices.append(d)
                  indices.append(a)

              if len(polygon.vertices) == 3:
                  a = polygon.vertices[0]
                  b = polygon.vertices[1]
                  c = polygon.vertices[2]

                  indices.append(a)
                  indices.append(b)
                  indices.append(c)

          armature = ""

          if obj.parent and obj.parent.type == 'ARMATURE':
            armature = obj.parent.name

          submesh_data = {
            "armature":armature, 
            "vertices":vertices, 
            "normals":normals, 
            "indices":indices, 
            "weights":weights,
            "groups":vertex_groups
          }
          submeshes_data.append(submesh_data)

  mesh_data = {"submeshes" : submeshes_data, "armatures" : armatures_data}
  content = json.dumps(mesh_data, sort_keys=True, indent=4, separators=(',', ': '))
  out = open(filepath, "w", encoding="utf-8")
  out.write(content)
  out.close()