import bpy
import math
import mathutils
import json

def do_export(filepath):
  submeshes_data = []
  for ob in bpy.data.objects:
      if ob.type == 'MESH':
          mesh = ob.to_mesh(bpy.context.scene, True, 'RENDER')
          X_ROT = mathutils.Matrix.Rotation(-math.pi/2, 4, 'X')

          vertices = []
          normals = []
          for vertex in mesh.vertices:
              v = X_ROT * vertex.co
              vertices.append(v.x)
              vertices.append(v.y)
              vertices.append(v.z)

              n = X_ROT * vertex.normal
              n.normalize()

              normals.append(n.x)
              normals.append(n.y)
              normals.append(n.z)

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

          submesh_data = {"vertices":vertices, "normals":normals, "indices":indices}
          submeshes_data.append(submesh_data)

  mesh_data = {"submeshes" : submeshes_data}
  content = json.dumps(mesh_data, sort_keys=True, indent=4, separators=(',', ': '))
  out = open(filepath, "w", encoding="utf-8")
  out.write(content)
  out.close()