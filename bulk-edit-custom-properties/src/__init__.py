
'''
Copyright (C) 2015-2020 Team C All Rights Reserved

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Bulk Edit Custom Data Properties",
    "author": "Lee M. Lwando",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Edit Custom Properties",
    "description": "Bulk edit custom data properties",
    "warning": "",
    "doc_url": "https://github.com/leemlwando/blender-adddons/tree/master/bulk-edit-custom-data",
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

# import importlib
# importlib.reload(utils)
# importlib.reload(manage_template_list)
# importlib.reload(api)
# importlib.reload(copy)
# importlib.reload(selection)
# importlib.reload(unpack)


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