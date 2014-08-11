import bpy
import math
import mathutils
import json

for mesh in bpy.data.meshes:
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
            indices.append(c) 
            indices.append(d) 
            indices.append(c) 
            indices.append(a) 
            indices.append(b)
            
        if len(polygon.vertices) == 3:
            a = polygon.vertices[0]
            b = polygon.vertices[1]
            c = polygon.vertices[2]                                    
            
            indices.append(a) 
            indices.append(c) 
            indices.append(b)
            
           
    content = json.dumps({"vertices":vertices, "normals":normals, "indices":indices}, sort_keys=True, indent=4, separators=(',', ': '))
    print(content)
    
    filename = "/Users/nk/Development/ideas/wow/models/cube.json"
    
    out = open(filename, "w", encoding="utf-8")
    out.write(content)
    out.close() 

