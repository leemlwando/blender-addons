

def copy_custom_property(source, destination, prop_name):
    """Copy a custom property called prop_name, from source to destination.
    source and destination must be a Blender data type that can hold custom properties.
    For a list of such data types, see:
    https://docs.blender.org/manual/en/latest/files/data_blocks.html#files-data-blocks-custom-properties

    @credit:  {
       "name": "Copy Attributes Menu",
        "author": "Bassam Kurdali, Fabian Fricke, Adam Wiseman, Demeter Dzadik",
        "version": (0, 6, 0),
        "blender": (3, 4, 0),
        "location": "View3D > Ctrl-C",
        "description": "Copy Attributes Menu",
        "doc_url": "{BLENDER_MANUAL_URL}/addons/interface/copy_attributes.html",
        "category": "Interface",
        }
    """

    # Create the property.
    destination[prop_name] = source[prop_name]
    # Copy the settings of the property.
    try:
        dst_prop_manager = destination.id_properties_ui(prop_name)
    except TypeError:
        # Python values like lists or dictionaries don't have any settings to copy.
        # They just consist of a value and nothing else.
        return

    src_prop_manager = source.id_properties_ui(prop_name)
    assert src_prop_manager, f'Property "{prop_name}" not found in {source}'

    dst_prop_manager.update_from(src_prop_manager)

    # Copy the Library Overridable flag, which is stored elsewhere.
    prop_rna_path = f'["{prop_name}"]'
    is_lib_overridable = source.is_property_overridable_library(prop_rna_path)
    destination.property_overridable_library_set(prop_rna_path, is_lib_overridable)
