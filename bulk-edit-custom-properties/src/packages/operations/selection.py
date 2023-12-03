import random
import bpy

# This module provides the definition for selection operations
# The following operations are defined:
# - Current Selection: where a user can select any object in the scene i.e custom selection
# - Selection by Collection: where all objects in a collection are selected
# - Random Selection: where a random number of objects are selected



def select_all_objects(context, toggle):
    """Select all objects in the scene"""
    bpy.ops.object.select_all(action='SELECT' if toggle else 'DESELECT')


def select_by_collection(context, collection_name, selected):
    """Select all objects in a collection"""
    select_all_objects(context, False)
    for object in bpy.data.collections[collection_name].all_objects[:]:
        object.select_set(True)

def select_random(context):
    """Select a random number of objects in the scene"""
    select_all_objects(context, False)
    bpy.ops.object.select_random(action='SELECT', seed=random.randint(0, 100))


def get_current_selection(self, context):
    """Get the current selection"""
    selected = context.selected_objects
    return selected