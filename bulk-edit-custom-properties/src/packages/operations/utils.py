

PANEL_CATEGORY = "Bulk Edit Custom Data"
CONFIGS_KEY = 'configs'
VALUE_KEY = 'value'
NAME_KEY = 'name'
DEFAULT_TITLE = "Untitled"
UUID_KEY = 'uuid'

#get selected template from list
def get_selected_template_data(self, context, data):
    """Get the selected template from the list"""
    my_list = self.get_list(context)
        
    active_index = self.get_active_index(context)

    uuid = my_list[active_index][UUID_KEY]

    # return template data where uuid matches
    for template in data:
        if template[UUID_KEY] == uuid:
            return template
        

def get_context_attr(context, data_path):
    """Return the value of a context member based on its data path."""
    return context.path_resolve(data_path)


def set_context_attr(context, data_path, value):
    """Set the value of a context member based on its data path."""
    owner_path, attr_name = data_path.rsplit('.', 1)
    owner = context.path_resolve(owner_path)
    setattr(owner, attr_name, value)