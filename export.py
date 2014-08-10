import bpy
import math
import mathutils

for mesh in bpy.data.meshes:
    X_ROT = mathutils.Matrix.Rotation(-math.pi/2, 4, 'X')
        
    vertices = ""
    for vertex in mesh.vertices:
        v = X_ROT * vertex.co
        vertices += "{0} {1} {2} ".format(v.x, v.y, v.z)
    print(vertices)

    indices = ""
    for polygon in mesh.polygons:
        if len(polygon.vertices) == 4:
            a = polygon.vertices[0]
            b = polygon.vertices[1]
            c = polygon.vertices[2]                                    
            
            d = polygon.vertices[2]
            e = polygon.vertices[3]
            f = polygon.vertices[0]                                    
            
            indices += "{0} {1} {2} {3} {4} {5} ".format(a, c, b, d, e, b)
            
        if len(polygon.vertices) == 3:
            a = polygon.vertices[0]
            b = polygon.vertices[1]
            c = polygon.vertices[2]                                    
            
            indices += "{0} {1} {2} ".format(a, c, b)
            
        print(indices)
