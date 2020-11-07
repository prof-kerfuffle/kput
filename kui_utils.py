import os
import bpy


def show_message_box(message="", title="Message Box", icon='INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def show_multiline_message_box(
        messages=["row1", "row2"], title="Message Box", icon='INFO'):

    def draw(self, context):
        for m in messages:
            self.layout.label(text=m)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
