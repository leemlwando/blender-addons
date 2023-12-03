
# draw drop down menu for assignment action buttond [ assign | selection | random ]
def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("OBJECT_MT_base_menu_items", icon="DOCUMENTS")
    return {"FINISHED"}