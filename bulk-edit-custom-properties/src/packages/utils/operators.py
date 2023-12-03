#define utility funtions for operators
from .constants import DEFAULT_TITLE

def clear_add_template_input_fields(self, context):
    """Clear input fields and reset defaults"""
    context.scene.add_template_fields.title = DEFAULT_TITLE
    context.scene.add_template_fields.description = ""