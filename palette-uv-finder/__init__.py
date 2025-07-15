bl_info = {
    "name": "UV Plotter",
    "author": "Ziplaw",
    "version": (1, 1),
    "blender": (4, 4, 3),
    "description": "UV Plotter Description",
}

from .ensure_modules import *

bootstrap()

from .vector_math import *
from .solver import *

from .tool import *

import bpy

def register():    
    bpy.utils.register_class(UVPlotter)
    bpy.utils.register_class(UVFindOperator)
    bpy.utils.register_class(UVPlotterPropertyGroup)
    bpy.types.Scene.UVPlotterPropertyGroup = bpy.props.PointerProperty(
            type=UVPlotterPropertyGroup)


def unregister():
    bpy.utils.unregister_class(UVPlotter)
    bpy.utils.unregister_class(UVFindOperator)
    bpy.utils.unregister_class(UVPlotterPropertyGroup)
    del bpy.types.Scene.UVPlotterPropertyGroup