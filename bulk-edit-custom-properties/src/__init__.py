bl_info = {
    "name": "Bulk Edit Custom Data Properties",
    "author": "Lee M. Lwando <leemlwando@gmail.com>",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Edit Custom Properties",
    "description": "Bulk edit custom data properties",
    "warning": "",
    "doc_url": "https://github.com/leemlwando/blender-addons/blob/main/bulk-edit-custom-properties/README.md",
    "category": "Object"
}

# import sys
# import bpy
# import os

# def clear_terminal():
#     os.system('cls' if os.name == 'nt' else 'clear')

# clear_terminal()


#register my packages
# blend_dir = bpy.path.abspath("//")

# packagesPath = blend_dir + '/packages'

# avoid appending twice
# if packagesPath not in sys.path:
#     sys.path.append(packagesPath)


from .packages.UI import manage_template_list
from .packages.operations import utils,api,copy,selection,unpack


if "bpy" in locals():
    """Reload modules if already imported."""
    import importlib
    importlib.reload(utils)
    importlib.reload(manage_template_list)
    importlib.reload(api)
    importlib.reload(copy)
    importlib.reload(selection)
    importlib.reload(unpack)
 

def register():
    """Register all classes"""
    manage_template_list.register()

def unregister():
    """Unregister all classes"""
    manage_template_list.unregister()

if __name__ == "__main__":
    register()
    # loading initial data to template panel list
    api.load_data_to_template_panel_List() 