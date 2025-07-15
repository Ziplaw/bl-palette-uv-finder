import bpy
from .vector_math import *
from .solver import *

def find_uv(global_image_path, color_rgb_01, constrain_within_bounds) -> tuple[float,float,float] :
    
    image = iio.imread(global_image_path)

    width = image.shape[1]
    height = image.shape[0]

    color = linearVector(Vector((color_rgb_01[0],color_rgb_01[1],color_rgb_01[2])))*255
    
    best_solve = (0.0,0.0)
    best_solve_distance = 10000
    
    u = 0
    v = 0

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
            
            if len(set([c1,c2,c3,c4])) < 4:
                continue

            v1 = Vector(c1).xyz
            v2 = Vector(c2).xyz
            v3 = Vector(c3).xyz
            v4 = Vector(c4).xyz

            if not constrain_within_bounds or point_in_tetrahedron(v1,v2,v3,v4,srgbVector(color/255)*255):
                if constrain_within_bounds:
                    print(f"point found inside in {(x0,y0)}")
                                
                d = (color-v1).length
                
                if d < 1: # Variation of color in 0-255 is 0
                    print("Found exact color")
                    
                    v1_c = Vector((y0,x0))
                    
                    v = v1_c.x/image.shape[1] + .5/image.shape[1]
                    u = v1_c.y/image.shape[0] + .5/image.shape[0]
                    
                    best_solve = (u,1-v)
                    best_solve_distance = d
                    continue
                
                values = solve_with_gradient(v1,v2,v3,v4,color)

                t1 = values[0]
                t2 = values[1]

                d = (evaluate(v1,v2,v3,v4,t1,t2)-color).length

                if d < best_solve_distance:
                    best_solve_distance = d

                    l1 = Vector((y0,x0)).lerp(Vector((y0+1,x0)),t1)
                    l2 = Vector((y0,x0+1)).lerp(Vector((y0+1,x0+1)),t1)

                    l3 = l1.lerp(l2,t2)

                    v = l3.x/image.shape[1] + .5/image.shape[1]
                    u = l3.y/image.shape[0] + .5/image.shape[0]

                    best_solve = (u,1-v)
    
    return (u,1-v,best_solve_distance)




class UVPlotterPropertyGroup(bpy.types.PropertyGroup):
    img_path : bpy.props.StringProperty(
        name="Image",
        description="Image Path",
        default="",
        subtype='FILE_PATH'
        )
    color : bpy.props.FloatVectorProperty(
        name="Color",
        description="Color to find within the texture",
        default=(0.5,0.5,0.5),
        subtype='COLOR',
        min=0,
        max=1,
        )
    x : bpy.props.FloatProperty(
        name="U",
        description="X or U coordinate of UVs",
        default=0,
        )
    y : bpy.props.FloatProperty(
        name="V",
        description="Y or V coordinate of UVs",
        default=0,
        )
    apply_uv_to_selected : bpy.props.BoolProperty(
        name="Apply UV",
        description="Apply UV Positions to selected vertices in UV Editing Mode",
        default=False,
        )
    max_error : bpy.props.FloatProperty(
        min=0.001,
        soft_max=.1,
        name="Maximum Error",
        description="Maximum difference permitted between target color and obtained color to be considered a match",
        default=0.05,
        step=1
        )
        
        
    def draw(self,context):
        self.layout.prop(self,"export_settings")

class UVFindOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.find_uv_operator"
    bl_label = "Find UV"

    @classmethod
    def poll(cls, context):
        props = context.scene.UVPlotterPropertyGroup
        return bpy.context.area.ui_type == 'UV' and (not props.apply_uv_to_selected or bpy.context.mode == 'EDIT_MESH')

    def execute(self, context):
        props = context.scene.UVPlotterPropertyGroup
        
        result = find_uv(bpy.path.abspath(props.img_path), props.color, False)
        error = result[2]/255.0
        self.report({"INFO"},f"Best Coordinates found for color ({props.color[0]:.3f},{props.color[1]:.3f},{props.color[2]:.3f}): UV=({result[0]},{result[1]}) with error: {error:.4f}") 
        
        if error > props.max_error:
            props.x = 0
            props.y = 0
            self.report({"WARNING"},f"Could not find UV coordinates matching color with less than {props.max_error:.3f} error (minimum error found: {error})")
            return {"CANCELLED"}
        
        props.x = result[0]
        props.y = result[1]
        
        bpy.ops.object.editmode_toggle()
        
        if props.apply_uv_to_selected:
            for uv_layer in bpy.context.active_object.data.uv_layers:
                if uv_layer.active:
                    for i in range(len(uv_layer.uv)):
                        if uv_layer.vertex_selection[i].value:
                            uv_layer.uv[i].vector = Vector((props.x,props.y))
                            
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class UVPlotter(bpy.types.Panel):
    """Creates a Panel for finding UV Coordinates of a color inside a texture"""
    bl_label = "UV Plotter"
    bl_idname = "PT_IE_UVPlotter"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'UV Plotter'

    def draw(self, context):
        layout = self.layout

        props = context.scene.UVPlotterPropertyGroup

        layout.prop(props, "img_path")
        layout.prop(props, "color")
        row = layout.row()
        row.prop(props, "x")
        row.prop(props, "y")
        layout.prop(props, "apply_uv_to_selected")
        layout.prop(props, "max_error")
        
        layout.operator("object.find_uv_operator")


