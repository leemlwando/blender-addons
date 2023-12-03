#define system messages and dialog, pop ups etc.


def no_properties_found_message(self, context):
    # align text to center
    self.layout.alignment = 'CENTER'
    self.layout.label(text="No properties to export")

def no_selection_found_message(self, context):
    # align text to center
    self.layout.alignment = 'CENTER'
    self.layout.label(text="Cannot Assign Template To Selection")


ACTION_SUCCESS_MESSAGE = "Action was successful"