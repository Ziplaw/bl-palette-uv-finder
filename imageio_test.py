bl_info = {
    "name": "UV Plotter",
    "author": "Ziplaw",
    "version": (1, 0),
    "blender": (3, 6, 14),
    "description": "UV Plotter Description",
}

import sys
import imageio.v3 as iio
import math
from mathutils import Vector

# import bpy
# import os

# class BatchExportPropertyGroup(bpy.types.PropertyGroup):
#     filepath : bpy.props.StringProperty(
#         name="Path",
#         description="Path to export all models",
#         default="C:/tmp/",
#         )
#     only_selected : bpy.props.BoolProperty(
#         name="Only Selected",
#         description="Only export selected models",
#         default=True,
#         )
#     apply_rotations : bpy.props.BoolProperty(
#         name="Apply Rotation and Scale",
#         description="Apply Rotation and Scale before exporting",
#         default=False,
#         )
#     move_to_world_center : bpy.props.BoolProperty(
#         name="Reset Position",
#         description="Moves each object to 0,0,0 before exporting and back to their original position afterwards",
#         default=True,
#         )
#     export_settings : bpy.props.EnumProperty(
#         items=
#         [
#             ('UNITY', "Unity", "Unity's Export Settings",1),
#             ('UE5', "Unreal Engine 5", "Unreal Engine 5's Export Settings",2),
#         ],
#         name="Export Settings",
#         description="",
#         default='UNITY'
#         )
        
        
#     def draw(self,context):
#         self.layout.prop(self,"export_settings")

# class BatchExportOperator(bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "object.batch_export_operator"
#     bl_label = "Batch Export"

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         props = context.scene.BatchExportPropertyGroup
        
#         if props.only_selected:
#             selected_objects = context.selected_objects
#         else:
#             selected_objects = bpy.data.objects
        
        
#         for object in selected_objects:
#             object.select_set(False)
        
#         for object in selected_objects:
#             object.select_set(True)
            
#             if props.apply_rotations:
#                 bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
#             original_position = object.location
            
#             if props.move_to_world_center:
#                 object.location = 0,0,0
#                 print(original_position)
                            
#             match props.export_settings:
#                 case 'UNITY':
#                     bpy.ops.export_scene.fbx(filepath= (f"{props.filepath}/{object.name}.fbx"),use_selection=True,apply_scale_options='FBX_SCALE_ALL',object_types={'MESH'},bake_space_transform=True, apply_unit_scale=True, add_leaf_bones=False, use_armature_deform_only=False, bake_anim=False,axis_forward='-Z', axis_up = 'Y')
                    
#                 case 'UE5':
#                     bpy.ops.export_scene.fbx(filepath= (f"{props.filepath}/{object.name}.fbx"),use_selection=True,apply_scale_options='FBX_SCALE_ALL',object_types={'MESH'},bake_space_transform=True, apply_unit_scale=True, add_leaf_bones=False, use_armature_deform_only=False, bake_anim=False,axis_forward='-Z', axis_up = 'Y')
                    
#                 case _:
#                     raise Exception('Export Settings not Implemented')
            
#             if props.move_to_world_center:
#                 print(original_position)
#                 object.location = original_position
        
#         os.startfile(props.filepath)
#         return {'FINISHED'}

# class BatchExporter(bpy.types.Panel):
#     """Creates a Panel for exporting objects in batch."""
#     bl_label = "Batch Exporter"
#     bl_idname = "PT_BatchExporter"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Batch Export'

#     def draw(self, context):
#         layout = self.layout

#         props = context.scene.BatchExportPropertyGroup

#         layout.prop(props, "filepath")
#         layout.prop(props, "only_selected")
#         layout.prop(props, "apply_rotations")
#         layout.prop(props, "move_to_world_center")
#         layout.prop(props, "export_settings")
        
#         row = layout.row()
#         op = row.operator("object.batch_export_operator")


# def register():
#     bpy.utils.register_class(BatchExporter)
#     bpy.utils.register_class(BatchExportOperator)
#     bpy.utils.register_class(BatchExportPropertyGroup)
#     bpy.types.Scene.BatchExportPropertyGroup = bpy.props.PointerProperty(
#             type=BatchExportPropertyGroup)


# def unregister():
#     bpy.utils.unregister_class(BatchExporter)
#     bpy.utils.unregister_class(BatchExportOperator)
#     bpy.utils.unregister_class(BatchExportPropertyGroup)
#     del bpy.types.Scene.MyPropertyGroup


# if __name__ == "__main__":
#     register()

image = iio.imread(r"C:\Users\Usuario\source\repos\bl-uv-plotter-testimages\T_Main_Color_Palette.png")

width = image.shape[1]
height = image.shape[0]

color = Vector((141, 160, 110))
max_iterations = 100

#tetrahedron is point inside:
def same_side(v1, v2, v3, v4, p):
    
    normal = (v2 - v1).cross(v3 - v1)
    dotV4 = (normal).dot(v4 - v1)
    dotP = (normal).dot(p - v1)
    return math.copysign(1,dotV4) == math.copysign(1,dotP)

def point_in_tetrahedron(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector):
    return same_side(v1, v2, v3, v4, p) and same_side(v2, v3, v4, v1, p) and same_side(v3, v4, v1, v2, p) and same_side(v4, v1, v2, v3, p)

#rudimentary solver

def evaluate(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, t_1 : float, t_2 : float) -> Vector:
    return ((1 - t_2) * ((1 - t_1) * v1 + v2 * t_1) + ((1 - t_1) * v3 + v4 * t_1) * t_2)

def solve(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector) -> tuple[float,float]:

    size = 10
    resolutions = []

    for j in range(size):
        for i in range(size):
            t_1 = i/float(size)
            t_2 = j/float(size)
            i=0
            d=.01

            c7 = evaluate(v1, v2, v3, v4, t_1, 0)
            c8 = evaluate(v1, v2, v3, v4, t_1, 1)
            s = evaluate(v1, v2, v3, v4, t_1, t_2)
            

            last_dot = abs((p-s).normalized().dot((c8-c7).normalized()))
            root_found = False

            while i < max_iterations:
                t_1 += d
                    
                c7 = evaluate(v1, v2, v3, v4, t_1, 0)
                c8 = evaluate(v1, v2, v3, v4, t_1, 1)
                
                s = evaluate(v1, v2, v3, v4, t_1, t_2)

                dot = abs((p - s).normalized().dot((c8 - c7).normalized()))
                if dot < last_dot:
                    d *= -.75
                
                if t_1 > 1 or t_1 < 0:
                    d *= -1

                last_dot = dot
                i+=1

                if dot >= .9999:
                    root_found = True
                    break

            if t_2 > 0 and t_2 < 1:
                resolutions.append((t_1,t_2))

    min = 10000
    min_index = 0

    for i in range(len(resolutions)):
        res = resolutions[i]
        length = (p - (lerp(lerp(v1,v2,res[0]),lerp(v3,v4,res[0]),res[1]))).length

        if length < min:
            min = length
            min_index = i


    return (resolutions[min_index][0],resolutions[min_index][1])

    


#lerp

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def lerp(a: Vector, b: Vector, t: float) -> Vector:
    return (1.0 - t) * a + t * b

def inverse_lerp (a : Vector,b: Vector, v : Vector):
    ab = b-a
    av = v-a
    return av.dot(ab) / ab.dot(ab)

#gamma correction
def linearVector(a : Vector) -> Vector:
    #return Vector((linear(a.x),linear(a.y),linear(a.z)))
    return a

def linear(f : float) -> float:
    return ((f/255.0)**(1/2.2))*255

def srgbVector(a : Vector) -> Vector:
    #return Vector((srgb(a.x),srgb(a.y),srgb(a.z)))
    return a

def srgb(f : float) -> float:
    return ((f/255.0)**2.2)*255

best_solve = (0.0,0.0)
best_solve_distance = 100

for y0 in range(height):
    for x0 in range(width):

        if x0+1 >= width:
            continue
        if y0+1 >= height:
            break

        c1 = tuple([int(i) for i in image[y0,x0]])
        c2 = tuple([int(i) for i in image[y0+1,x0]])
        c3 = tuple([int(i) for i in image[y0,x0+1]])
        c4 = tuple([int(i) for i in image[y0+1,x0+1]])

        if len(set([c1,c2,c3,c4])) != 4:
            continue

        c_linear = linearVector(color)

        v1 = linearVector(Vector(c1).xyz)
        v2 = linearVector(Vector(c2).xyz)
        v3 = linearVector(Vector(c3).xyz)
        v4 = linearVector(Vector(c4).xyz)

        if point_in_tetrahedron(v1,v2,v3,v4,c_linear):
            #print(f"point found inside in {(x0,y0)}")

            #bounds check
            #t1 = inverse_lerp(v1,v2,c_linear)
            #t2 = inverse_lerp(v3,v4,c_linear)

            #if(t1 < 0 or t1 > 1 or t2 < 0 or t2 > 1):
            #    continue

            values = solve(v1,v2,v3,v4,c_linear)

            t1 = values[0]
            t2 = values[1]

            #print((t1,t2))

            v5 = v1.lerp(v2,t1)
            v6 = v3.lerp(v4,t1)
            v7 = v5.lerp(v6,t2)

            d = (v7-c_linear).length

            if d < best_solve_distance:
                best_solve_distance = d

                l1 = Vector((y0,x0)).lerp(Vector((y0+1,x0)),t1)
                l2 = Vector((y0,x0+1)).lerp(Vector((y0+1,x0+1)),t1)

                l3 = l1.lerp(l2,t2)

                v = l3.x/image.shape[1] + .5/image.shape[1]
                u = l3.y/image.shape[0] + .5/image.shape[0]

                best_solve = (u,1-v)
            
print(best_solve)
print(best_solve_distance)
