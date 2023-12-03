import bpy
import json
import os
import uuid

# each property definition has {name, value, configs}
CONFIGS_KEY = 'configs'
VALUE_KEY = 'value'

def unpack_data(properties, set_obj_active = True, set_select_obj = True):
    """
    Unpacks the data and creates a new object with the data

    WARNING: This will overwrite any existing data on the target object
    """

    meshName = uuid.uuid4().hex

    tmpMesh = bpy.data.meshes.new(meshName)

    tmpObj = bpy.data.objects.new(meshName, tmpMesh)

    #create new temp collection for the object
    tmpCollection = bpy.data.collections.new(meshName)
    bpy.context.scene.collection.children.link(tmpCollection)
    #hide from rendering
    tmpCollection.hide_render = True
    #add the object to the scene collection
    tmpCollection.objects.link(tmpObj)
    #make it active and selected
    if set_obj_active:
        bpy.context.view_layer.objects.active = tmpObj
    if set_select_obj:
        tmpObj.select_set(True)

    for prop in properties:
        for key in prop:
            if key != "name":
                continue              
            # set property value
            tmpObj[prop[key]] = prop[VALUE_KEY]
            ui_prop = tmpObj.id_properties_ui(prop[key])
            #set UI properties
            ui_prop.update(**prop[CONFIGS_KEY])

    return tmpObj, tmpCollection

# unpack to target object
def unpack_to_target_object(target_object, properties):
    """
    Unpacks the data and creates a new object with the data

    WARNING: This will overwrite any existing data on the target object
    """

    for prop in properties:
        for key in prop:
            if key != "name":
                continue              
            # set property value
            target_object[prop[key]] = prop[VALUE_KEY]
            ui_prop = target_object.id_properties_ui(prop[key])
            #set UI properties
            ui_prop.update(**prop[CONFIGS_KEY])

    return target_object