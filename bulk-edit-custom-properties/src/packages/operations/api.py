import os
import json
import bpy

from ..utils.constants import (
    DATA_KEY,
    UUID_KEY
)

def fetch_data(close_file=True):
    """Fetch the data from the template file"""

    templateFileName = "templates.json"
    templateDataDir =  os.path.join(os.path.dirname(__file__), '..', '..', 'data', templateFileName)
    templateFile = templateDataDir

    file = open(templateFile, '+r')
    data = json.load(file)

    if close_file:
        file.close()

    return data,file

def update_data(new_data,active_index, uuid):

    current_data, file = fetch_data(close_file=False)

    current_data[DATA_KEY] = [ item for item in current_data[DATA_KEY] if item[UUID_KEY] != uuid ]
    # Go back to the start of the file
    file.seek(0)

    # Write the updated data back to the file
    json.dump(current_data, file, indent=4)

    # Remove any leftover content
    file.truncate()

    file.close()

def load_data_to_template_panel_List():
    """Load the data from the template file to the template panel list"""

    templateFileData,file = fetch_data()

    template_list = bpy.context.scene.templates_list
    template_list.clear()

    for index, item in enumerate(templateFileData[DATA_KEY]):
        template = template_list.add()
        template.index = index
        for key in item:
            setattr(template, key, item[key])
