import uuid
import bpy
import os
import json
import pprint
from bpy.props import (
    StringProperty,
    IntProperty,
    PointerProperty,
    CollectionProperty,
    )

from bpy.types import (
    Context, 
    Panel,
    Operator,
    PropertyGroup,
    Scene,
    UIList
    )

from .manage_context_menu import (
    draw_menu
)

from ..utils.constants import (
    PANEL_CATEGORY_KEY,
    CONFIGS_KEY, 
    VALUE_KEY, 
    NAME_KEY, 
    DEFAULT_TITLE, 
    UUID_KEY,
    
    SCENE_TEMPLATE_LIST_KEY,
    SCENE_TEMPLATE_LIST_INDEX_KEY
    )

from ..operations.api import (
    load_data_to_template_panel_List,
    fetch_data,
    update_data
)

from ..operations.selection import (
    select_random
)

from ..operations.utils import (
    get_context_attr,
    set_context_attr,

    get_selected_template_data
)

from ..operations.unpack import (
    unpack_data,
    unpack_to_target_object
)

from ..operations.copy import (
    copy_custom_property
)

from ..utils.messages import (
    no_properties_found_message,
    no_selection_found_message,
    ACTION_SUCCESS_MESSAGE
)


from ..utils.operators import (
    clear_add_template_input_fields
)

class AssignTemplateMenuItems(bpy.types.Menu):
    bl_label = "Bulk Edit Custom Data Properties"
    bl_idname = "OBJECT_MT_base_menu_items"

    def draw(self, context):
        layout = self.layout

        # layout.operator('object.assign_template_collection', text="Active Collection")

        layout.operator("object.assign_template_to_active_object", text="Active")

        layout.operator("object.assign_template_to_selection", text="Selection")

        layout.operator("object.assign_to_random_selection", text=" Random")

class GenericUIListOperator:
    """Mix-in class containing functionality shared by operators
    that deal with managing Blender list entries."""
    bl_options = {
        'REGISTER', 
        'UNDO',
        'INTERNAL'
        }

    list_path: StringProperty(name="List Path", default=SCENE_TEMPLATE_LIST_KEY)
    active_index_path: StringProperty(name="Active Index Path", default=SCENE_TEMPLATE_LIST_INDEX_KEY)

    def get_list(self, context):
        return get_context_attr(context, self.list_path)

    @classmethod
    def poll(cls, context):
        return True

    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.alignment = 'CENTER'
        layout.label(text=ACTION_SUCCESS_MESSAGE, icon="INFO")

    def execute(self, context):
        print("EXECUTE")
        return {'FINISHED'}

    def get_active_index(self, context):
        return get_context_attr(context, self.active_index_path)

    def set_active_index(self, context, index):
        set_context_attr(context, self.active_index_path, index)

class TemplatePanelExportFieldDescription(bpy.types.PropertyGroup):
    """Export Panel Field Description"""
    title: bpy.props.StringProperty(name="Title", default="Untitled")
    description: bpy.props.StringProperty(name="Description")

class AddTemplate(Operator):
    """Add New Template"""
    bl_idname = "object.add_template"
    bl_label = "Add Template"

    # def draw(self, context):
    #     layout = self.layout

    def draw(self, context: Context):
        layout = self.layout
        layout.scale_x = 1.5
        layout.scale_y = 1.5
        layout.prop(context.scene.add_template_fields, "title")
        layout.prop(context.scene.add_template_fields, "description")


    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.active_object is not None
    

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):

        # Get the active object
        active_object = context.active_object

        # Get input field from scene
        scene = context.scene
        fields = scene.add_template_fields

        if fields.title == "":
            bpy.context.window_manager.popup_menu(no_properties_found_message, title="Title Required", icon="ERROR")
            return {'FINISHED'}
        

        # get all custom properties and add to properties dict
        properties = []

        #add property to properties list
        for key,value in active_object.items():
            if value is not None and isinstance(value, (int, float, str, bool)):
                property = {}
                property[NAME_KEY] = key
                property[VALUE_KEY] = value
                property[CONFIGS_KEY] = active_object.id_properties_ui(key).as_dict()
                properties.append(property)
     

        pprint.pprint(properties)

        # # abort if no properties found
        if len(properties) < 1:
            bpy.context.window_manager.popup_menu(no_properties_found_message, title="No Properties Found", icon="ERROR")
            return {'FINISHED'}
        

        # # configure output directory & file
        templateFileName = "templates.json"
        templateDataDir =  os.path.join(os.path.dirname(__file__), '..', '..', 'data', templateFileName)
        templateFile = templateDataDir

        # create new template
        template_uuid = uuid.uuid4()
        title = fields.title
        description = fields.description

        template = {
            "uuid": str(template_uuid),
            "title": title,
            "description": description,
            "properties": properties
        }

        # # write template to json file [ templates.json ] 
        with open(templateFile, 'r+') as f:

            templateFileDatabase = json.load(f)

            templateFileDatabase["data"].append(template)

            # pprint.pprint(templateFileDatabase)
            # Move the file pointer to the beginning of the file
            f.seek(0)

            json.dump(templateFileDatabase, f, indent=4)

            # Truncate the file to remove any leftover data from the previous write
            f.truncate()

        # clear input fields
        clear_add_template_input_fields(self, context)

        # reload data
        load_data_to_template_panel_List()

        return {'FINISHED'}

class RemoveTemplate(GenericUIListOperator,Operator):
    """Remove Selected Template"""
    bl_idname = "object.remove_template"
    bl_label = "Remove Selected Template"

    @classmethod
    def poll(cls, context):
        #check if list item is selected
        return context.scene.templates_list_index >= 0

    def execute(self, context):

        list_to_draw = get_context_attr(context, SCENE_TEMPLATE_LIST_KEY)

        if len(list_to_draw) == 0:
            return {'FINISHED'}

        my_list = self.get_list(context)
        
        active_index = self.get_active_index(context)

        uuid = my_list[active_index][UUID_KEY]

        my_list.remove(active_index)

        to_index = min(active_index, len(my_list) - 1)

        self.set_active_index(context, to_index)

        update_data(my_list,active_index,uuid)

        return {'FINISHED'}

class BaseAssignmentClass:
    """ Base Assignment class """
    selected_objects =  CollectionProperty(name="Selected Properties")

    def assign_properties(self, context):
            
        selected_objects = self.selected_objects
    
        # get active template
        template_list_item = get_selected_template_data(self, context, context.scene.templates_list)

        if template_list_item is None:
            bpy.context.window_manager.popup_menu(no_selection_found_message, title="No Matching Template Found", icon="ERROR")
            return {'CANCELLED'}

         # fetch data from json file
        templates, file = fetch_data()

        #get template where uuid matches
        matching_template = next((template for template in templates["data"] if template['uuid'] == template_list_item[UUID_KEY]), None)

        if matching_template is None:
            bpy.context.window_manager.popup_menu(no_selection_found_message, title="No Matching Template Found", icon="ERROR")
            return {'CANCELLED'}
        
        #unpack template into temperary object
        source_object,source_collection = unpack_data(matching_template["properties"], set_obj_active=False, set_select_obj=False)

        #copy properties from source object to target object
        for target_object in selected_objects:
           for key,value in source_object.items():
                copy_custom_property(source_object, target_object, key)
            
        # cleanup by deleting temp object and collection
        bpy.data.objects.remove(source_object, do_unlink=True)
        bpy.data.collections.remove(source_collection, do_unlink=True)

class AssignTemplateFromCollectionOperator(BaseAssignmentClass,Operator):
    bl_label = "Assign template to collection"
    bl_idname = "object.assign_template_collection"

    @classmethod
    def poll(cls, context):
        return context.collection

class AssignTemplateToSelection(GenericUIListOperator,BaseAssignmentClass,Operator):
    """
    Assign Template to current viewport Selection

    WARNING: This will overwrite any existing data on the target objects
    """
    bl_idname = "object.assign_template_to_selection"
    bl_label = "Assign Template By Active Selection"

    @classmethod
    def poll(cls, context):
        return context.scene.templates_list_index >= 0 and (len(context.selected_objects) > 0)

    def draw(self, context):
        layout = self.layout
        layout.alignment = "CENTER"
        layout.label(text=ACTION_SUCCESS_MESSAGE, icon="INFO")

    def execute(self, context):
        self.selected_objects = bpy.context.selected_objects
        self.assign_properties(context)
        return {'FINISHED'}
    
class AssignTemplateToActiveObject(GenericUIListOperator,BaseAssignmentClass,Operator):
    """
    Assign Template to Active Object

    WARNING: This will overwrite any existing data on the target object
    """
    bl_idname = "object.assign_template_to_active_object"
    bl_label = "Assign Template By Active Object"

    @classmethod
    def poll(cls, context):
        return context.scene.templates_list_index >= 0 and context.selected_objects and context.active_object is not None

    def execute(self, context):
        # active_object = context.active_object
        #add to an array to satify the self.selected_objects rna struct
        self.selected_objects = [context.active_object]
        self.assign_properties(context)

        return {'FINISHED'}
    
class AssignToRandomSelection(GenericUIListOperator,BaseAssignmentClass,Operator):
    """
    Assign Custom Properties to randomly selected objects

    WARNING: This will overwrite any existing data on the target object
    """
    bl_idname = "object.assign_to_random_selection"
    bl_label = "Assign To Random Selection"

    @classmethod
    def poll(cls, context):
        return context.scene.templates_list_index >= 0

    def execute(self, context):
        select_random(context)
        self.selected_objects = context.selected_objects
        self.assign_properties(context)
        return {'FINISHED'}

class TemplatesListItem(PropertyGroup):
    """Defines each item of the list"""
    index: IntProperty()
    uuid: StringProperty(
        name="UUID", 
        default="00000000-0000-0000-0000-000000000000"
        )
    title: StringProperty(
        name="Title", 
        default="Untitled", 
        description="Template title",
        )
    description: StringProperty(
        name="Description", 
        default="No description"
        )

class TemplateList(UIList):
    """Defines the list view"""
    bl_idname = "OBJECT_UL_templates_list"

    def filter_items(self, context, data, property):
        # Default return values.
        flt_flags = []
        flt_neworder = []

        return flt_flags, flt_neworder

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
     
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.title)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class TemplatesListPanel(Panel):
    """Creates a Panel to display template list and relevant call to action buttons"""
    bl_label = "Custom Data Properties Templates"
    bl_idname = "OBJECT_PT_templates_list_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = PANEL_CATEGORY_KEY


    def draw(self, context):
        layout = self.layout

        row = layout.row()

        row.template_list(
            "OBJECT_UL_templates_list",
            "", 
            context.scene, 
            "templates_list", 
            context.scene, 
            "templates_list_index", 
            rows=3, 
            maxrows=5, 
            sort_reverse=True, 
            sort_lock=True
        )
    
        col = row.column()

        col.operator("object.add_template", icon="ADD", text="")

        col = col.row()
        col.operator("object.remove_template", icon="REMOVE", text="")

        row = layout.row()

        row.alignment = "CENTER"

        row.label(text="Assign Template To")
     
        row = layout.row(align=True)

        # action buttons [ assign to active|selection|random ]

        row.operator("object.assign_template_to_active_object", text="Active")

        row.operator("object.assign_template_to_selection", text="Selection")

        row.operator("object.assign_to_random_selection", text=" Random")

classes = (
    TemplatePanelExportFieldDescription,
    AddTemplate,
    RemoveTemplate,
    AssignTemplateToSelection,
    AssignTemplateToActiveObject,
    AssignToRandomSelection,
    AssignTemplateMenuItems,
    # AssignTemplateFromCollectionOperator,
    TemplatesListItem,
    TemplateList,
    TemplatesListPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Scene.templates_list = CollectionProperty(type=TemplatesListItem)
    Scene.templates_list_index = IntProperty()
    Scene.add_template_fields = PointerProperty(type=TemplatePanelExportFieldDescription)
    bpy.types.OUTLINER_MT_collection.append(draw_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del Scene.templates_list
    del Scene.templates_list_index
    del Scene.add_template_fields
    bpy.types.OUTLINER_MT_collection.remove(draw_menu)
