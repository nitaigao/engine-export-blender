import bpy

if "bpy" in locals():
    import imp
    if "exporter_json" in locals():
        imp.reload(exporter_json)

import math
import mathutils
import json

from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

bl_info = {
  "name":         "JSON Model Format",
  "author":       "Nicholas Kostelnik",
  "blender":      (2,7,1),
  "version":      (0,0,1),
  "location":     "File > Import-Export",
  "description":  "Export custom JSON format",
  "category":     "Import-Export"
}

def do_export(filepath):
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


          content = json.dumps({"vertices":vertices, "normals":normals, "indices":indices}, sort_keys=True, indent=4, separators=(',', ': '))
          print(content)

          # filename = "/Users/nk/Development/ideas/wow/models/pandaren.json"

          out = open(filepath, "w", encoding="utf-8")
          out.write(content)
          out.close()

class ExportJSON(bpy.types.Operator, ExportHelper):
  bl_idname       = "export_json.fmt";
  bl_label        = "JSON Exporter";
  bl_options      = {'PRESET'};

  filename_ext    = ".json";


  def execute(self, context):
    do_export(self.filepath)
    return {'FINISHED'};

def menu_func(self, context):
  self.layout.operator(ExportJSON.bl_idname, text="JSON Format(.json)");

def register():
  bpy.utils.register_module(__name__);
  bpy.types.INFO_MT_file_export.append(menu_func);

def unregister():
  bpy.utils.unregister_module(__name__)
  bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
  register()
