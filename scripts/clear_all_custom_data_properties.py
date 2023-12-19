"""
@author : Lee M. Lwando
@email: leemlwando@gmail.com
@project-github: https://github.com/leemlwando/blender-addons/tree/development
@project-name: clear all custom data properties on all objects returned bt bpy.data
@use-case: usefull for reseting objects custom data properties
@reccommendation: to add new custom properties on either selected, active or random objects use the bulk edit custom data properties addon https://github.com/leemlwando/blender-addons/tree/development/bulk-edit-custom-properties
"""

import bpy
import pprint

def clear_all_custom_data_properties():
        """Clear custom data properties"""
        for data in bpy.data.objects:
            data.id_properties_clear()
        pprint.pprint("[OPERATION][STATUS] DONE")
            
            
# call this with caution            
# clear_all_custom_data_properties()