import bpy
import math
import mathutils
import json

vertices_template = '"vertices": [{0}]'
indices_template = '"indices": [{0}]'

for mesh in bpy.data.meshes:
    X_ROT = mathutils.Matrix.Rotation(-math.pi/2, 4, 'X')
        
    vertices = []
    for vertex in mesh.vertices:
        v = X_ROT * vertex.co
        vertices.append(v.x)
        vertices.append(v.y)
        vertices.append(v.z)
        #vertices += "{0} {1} {2} ".format(v.x, v.y, v.z)
    #print(vertices)

    indices = []
    for polygon in mesh.polygons:
        if len(polygon.vertices) == 4:
            a = polygon.vertices[0]
            b = polygon.vertices[1]
            c = polygon.vertices[2]                                    
            
            d = polygon.vertices[2]
            e = polygon.vertices[3]
            f = polygon.vertices[0]                                    
            
            indices.append(a) 
            indices.append(c) 
            indices.append(b) 
            indices.append(d) 
            indices.append(e) 
            indices.append(b)
            #indices += "{0} {1} {2} {3} {4} {5} ".format(a, c, b, d, e, b)
            
        if len(polygon.vertices) == 3:
            a = polygon.vertices[0]
            b = polygon.vertices[1]
            c = polygon.vertices[2]                                    
            
            indices.append(a) 
            indices.append(c) 
            indices.append(b) 
            
            #indices += "{0} {1} {2} ".format(a, c, b)
            
        #print(indices)
        
        
    #vertices_output = vertices_template.format(vertices.strip())
    #indices_output = indices_template.format(indices.strip())
    
    #print(vertices_output)
    #print(indices_output)
    
    print(json.dumps({"vertices":vertices, "indices":indices}, sort_keys=True, indent=4, separators=(',', ': ')))
