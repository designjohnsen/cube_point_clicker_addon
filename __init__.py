bl_info = {
    "name": "Cube Point Clicker",
    "author": "F. Johnsen",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > Cube Point Clicker",
    "description": "Clicker game in Blender. Run Timeline (Shift+Space) when playing.",
    "warning": "",
    "wiki_url": "",
    "category": "Game",
}

import bpy
from . import cube_point_clicker

def register():
    cube_point_clicker.register()

def unregister():
    cube_point_clicker.unregister()

if __name__ == "__main__":
    register()
