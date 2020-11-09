from . import kui_utils
from . import ktexture_utils
from . import knode_utils
from . import kfile_utils
import bpy
from random import randint
from bpy.utils import register_class, unregister_class

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from mathutils import Vector


import sys
import os

import importlib


def get_file_type(file_name):
    extension = file_name[file_name.rfind(".") + 1:]
    if extension == "png":
        return "PNG"
    elif extension == "exr":
        return "OPEN_EXR"
    elif extension == "jpg":
        return "JPEG"
    elif extension == "jpeg":
        return "JPEG"


def create_missing_1001_textures(tex_path, texture_res):
    """
    checks whether all textures in the tex_path have a 1001 frame, and creates
    one if they don't. Currently only creates .png
    """

    texture_res = 1024

    file_sequences = kfile_utils.get_file_seqs(tex_path, "_")

    dir = tex_path

    log = []

    for main in file_sequences:
        found_1001 = False
        some_frame_file_name = ""
        for sub in main:
            some_frame_file_name = sub
            if kfile_utils.get_last_digits(sub, "_") == "1001":
                found_1001 = True
                continue
        if found_1001 is False:
            extension_for_name = kfile_utils.get_extension(
                some_frame_file_name)
            extension_type = get_file_type(some_frame_file_name)

            tex_path = dir + "\\" + \
                kfile_utils.get_filename_wo_digits_or_extension(
                    main[0], "_") + kfile_utils.get_divider_pre_digits(
                        main[0], "_") + "1001." + extension_for_name
            print("sequence lacks 1001, creating texture: ", tex_path)

            use_float = False
            if extension_type == "OPEN_EXR":
                use_float = True

            ktexture_utils.create_empty_texture(
                texture_res, texture_res, tex_path, extension_type, use_float)

            log.append(tex_path)

    return log


def get_pbr_elements(file_name):
    """
    reads a file name, and extracts a dictionary of the file name components
    looking for {'material_name': string, 'type': string, 'digits': string,
    'file_name':string}
    """

    base_color_alts = ["Base_Color", "Base_color",
                       "BaseColor", "Diffuse", "Albedo"]

    base_color = -1
    for alt in base_color_alts:
        result = file_name.find(alt)
        if result != -1:
            base_color = result

    mixed_ao = file_name.find('Mixed_AO')
    ao = file_name.find('Ambient_Occlusion')

    roughness = file_name.find('Roughness')
    metallic = file_name.find('Metallic')
    height = file_name.find('Height')
    normal = file_name.find('Normal_OpenGL')
    normal = file_name.find('Normal')
    emission = file_name.find('Emissive')
    opacity = file_name.find('Opacity')

    mat_type = ""
    text_name_index = -1

    if base_color != -1:
        mat_type = "Base_Color"
        text_name_index = base_color
    elif mixed_ao != -1:
        mat_type = 'Mixed_AO'
        text_name_index = mixed_ao
    elif ao != -1:
        mat_type = 'Ambient_occlusion'
        text_name_index = ao
    elif roughness != -1:
        mat_type = "Roughness"
        text_name_index = roughness
    elif metallic != -1:
        mat_type = "Metallic"
        text_name_index = metallic
    elif height != -1:
        mat_type = "Height"
        text_name_index = height
    elif normal != -1:
        mat_type = "Normal_OpenGL"
        text_name_index = normal
    elif normal != -1:
        mat_type = "Normal"
        text_name_index = normal
    elif emission != -1:
        mat_type = "Emissive"
        text_name_index = emission
    elif opacity != -1:
        mat_type = "Opacity"
        text_name_index = opacity

    texture_name = file_name[:text_name_index-1]

    return_object = {'material_name': texture_name, 'type': mat_type,
                     'digits': kfile_utils.get_last_digits(file_name, "_"),
                     'file_name': file_name}

    return return_object


def get_pbr_element_by_type(files, material_name, type):
    return_element = None

    for i in range(len(files)):
        for f in range(len(files[i])):
            element = get_pbr_elements(files[i][f])

            if (element['type'] == type and element['material_name']
                    == material_name):
                return_element = element
                break

    return return_element


def get_material_names(files):
    material_names = []
    for i in range(len(files)):
        for f in range(len(files[i])):
            element = get_pbr_elements(files[i][f])
            material_name = element['material_name']
            already_exists = False
            for m in material_names:
                if material_name == m:
                    already_exists = True
            if already_exists is False:
                material_names.append(material_name)
    return material_names


def create_materials(
                    file_seqs, replace_original_mats, replace_imported_mats,
                    texture_dir, use_udims):

    # gets the material names of the files
    material_names = get_material_names(file_seqs)

    print("-- material_names to be created:")
    print(material_names)

    print('file_seqs')
    print(file_seqs)

    log = []

    for material_name in material_names:

        # Create a material
        material_suffix = "_imported"
        material_name_w_suffix = material_name + material_suffix

        existing_mat_w_same_name = None

        if replace_original_mats:
            material_name_to_match = material_name
        else:
            material_name_to_match = material_name_w_suffix

        if replace_imported_mats:
            for mat in bpy.data.materials:

                print("-- replacing imported mats")
                print(mat.name)
                if material_name_to_match == mat.name:
                    print("removing material: ", mat.name)
                    existing_mat_w_same_name = mat

        if existing_mat_w_same_name is not None:
            material = existing_mat_w_same_name
            print("-- creating material: " + material.name)
            print("removing nodes from old material to replace")
            print(material)
            for n in material.node_tree.nodes:
                if n.name != "Material Output" and n.name != "Principled BSDF":
                    material.node_tree.nodes.remove(n)

        else:
            material = bpy.data.materials.new(name=material_name_w_suffix)

        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        shader_node = nodes["Principled BSDF"]

        # Reuse the material output node that is created by default
        material_output = nodes.get("Material Output")

        #
        # Connect all elements

        y_coord = 800
        y_distance = 280
        x_offset = -600

        tex_coordinate_node = nodes.new("ShaderNodeTexCoord")
        tex_coordinate_node.location = [x_offset - 300, 0]

        # In case there existed multiple shaders in material before any
        # replacement, connect the shader to the output to ensure that
        # something is connected to the surface input

        output_links = links.new(material_output.inputs['Surface'],
                                 shader_node.outputs["BSDF"])

        log.append("")
        log.append("Name: " + material_name)
        log_material_list = []

        print("***************************************************")
        print("creating material nodes")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Base_Color')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord], None, (0.6, 0.5, 0.5), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            links.new(node.outputs["Color"], shader_node.inputs['Base Color'])
            log_material_list.append("BaseColor")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Metallic')
        if file_name_elements:

            print("** creating metallic")
            print('file_name_elements')
            print(file_name_elements)
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord - (y_distance * 1)], 'Non-Color',
                (0.5, 0.6, 0.5), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            links.new(node.outputs["Color"], shader_node.inputs['Metallic'])
            log_material_list.append("Metallic")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Roughness')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],

                [x_offset, y_coord - (y_distance * 2)], 'Non-Color',
                (0.5, 0.5, 0.6), use_udims)
            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            links.new(node.outputs["Color"], shader_node.inputs['Roughness'])
            log_material_list.append("Roughness")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Emissive')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord - (y_distance * 3)], 'Non-Color',
                (0.6, 0.6, 0.5), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            links.new(node.outputs["Color"], shader_node.inputs['Emission'])
            log_material_list.append("Emissive")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Opacity')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord - (y_distance * 4)], 'Non-Color',
                (0.5, 0.3, 0.5), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            links.new(node.outputs["Color"], shader_node.inputs['Alpha'])
            log_material_list.append("Opacity")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Normal')
        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Normal_OpenGL')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord - (y_distance * 5)], 'Non-Color',
                (0.4, 0.4, 0.4), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            normal_map_node = nodes.new("ShaderNodeNormalMap")
            normal_map_node.location = [
                x_offset / 2, y_coord - (y_distance * 5)]
            links.new(node.outputs["Color"], normal_map_node.inputs['Color'])
            links.new(normal_map_node.outputs["Normal"],
                      shader_node.inputs['Normal'])
            log_material_list.append("Normal")

        file_name_elements = get_pbr_element_by_type(
            file_seqs, material_name, 'Height')
        if file_name_elements:
            node = knode_utils.create_udim_texture_node(
                nodes, texture_dir, file_name_elements['file_name'],
                [x_offset, y_coord - (y_distance * 6)], 'Non-Color',
                (1.0, 1.0, 1.0), use_udims)

            links.new(node.inputs["Vector"], tex_coordinate_node.outputs["UV"])
            displacement_node = nodes.new("ShaderNodeDisplacement")
            displacement_node.location = [
                x_offset / 2, y_coord - (y_distance * 6)]
            links.new(node.outputs["Color"],
                      displacement_node.inputs['Height'])
            links.new(material_output.inputs["Displacement"],
                      displacement_node.outputs["Displacement"])
            log_material_list.append("Height")

        log_maps = "- Maps: "
        for m in log_material_list:
            log_maps += m + " "

        log.append(log_maps)

        print("--- created material: " + material_name)

    return log


class MyProperties(PropertyGroup):

    bool_create_1001s: BoolProperty(
        name="Create missing 1001 textures",
        description="""Keep checked unless you know what you're doing. \n
If checked, any maps with a missing 1001 texture file, will have
a blank one created, this to get around blender's current (2.9)
requirement of having a 1001 file present to interpret a sequence
as an UDIM sequence.""",
        default=True
    )

    bool_replace_mats: BoolProperty(
        name="Replace original materials",
        description="""If checked, will replace the original materials. \n\n
If unchecked, will create new materials, with the same names, but
with a suffix""",
        default=False
    )

    bool_use_udims: BoolProperty(
        name="UDIM Materials",
        description="Check if the materials have UDIM tiles",
        default=True
    )

    my_int: IntProperty(
        name="Int Value",
        description="A integer property",
        default=23,
        min=10,
        max=100
    )

    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
    )

    texture_path: StringProperty(
        name="",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )


def get_maps_in_dir(dir):
    files = kfile_utils.list_files(dir)

    divided_file_list = []
    for f in files:
        divided_file_list.append([f])

    print("get_maps_in_dir")
    print(divided_file_list)

    return divided_file_list


def import_textures(context, use_udims):
    scene = context.scene
    mytool = scene.my_tool

    texture_dir = mytool.texture_path
    # DIR_PATH operator will give us a relative path,
    # something like \\Texture\, bpy.path.abspath will
    # turn it into an absolute string
    texture_dir = bpy.path.abspath(mytool.texture_path)

    print(texture_dir)
    print("absolute tex dir")
    print(bpy.path.abspath(texture_dir))

    # use_udims = mytool.bool_use_udims

    log = []

    # Check if it looks like a UDIM texture setup

    udim_textures_but_not_selected = False
    udim_selected_but_no_matching_files = False
    is_likely_udim = False
    udim_check = get_maps_in_dir(texture_dir)
    for m in udim_check:
        if kfile_utils.has_digits(m[0], "_"):
            is_likely_udim = True

    if is_likely_udim and use_udims is False:
        udim_textures_but_not_selected = True

    if is_likely_udim is False and use_udims is True:
        udim_selected_but_no_matching_files = True

    if texture_dir and texture_dir is not None and texture_dir != "":

        print("-------------------")
        print("texture_dir")
        print(texture_dir)

        replace_original_mat = mytool.bool_replace_mats

        print("Replace materials?")
        print(replace_original_mat)

        # Legacy setting, think it determines whether imported materials,
        # with the _import suffix, should be replaced, when new ones are
        # are created

        replace_imported_mat = True

        if is_likely_udim:
            print("create missing textures start")
            missing_texture_log = create_missing_1001_textures(
                texture_dir, 1024)

            print("-- create missing textures end")

            file_seqs = kfile_utils.get_file_seqs(texture_dir, "_")
        else:
            file_seqs = get_maps_in_dir(texture_dir)

        print("** file seqs start")
        print(file_seqs)
        print("-- file seqs end")

        print('create materials start')

        create_materials_log = create_materials(
            file_seqs, replace_original_mat, replace_imported_mat,
            texture_dir, is_likely_udim)

        print('-- create materials end')

        if (len(create_materials_log) > 0):
            log.append("Created materials: ")
            for m in create_materials_log:
                log.append(m)
            log.append("")
        if is_likely_udim is True:
            if (len(missing_texture_log) > 0):
                log.append("Created missing textures: ")
                log.append("")
                created_textures = ""
                for m in missing_texture_log:
                    print(m[m.rfind("\\")+1:])
                    log.append("-- " + m[m.rfind("\\")+1:])
            else:
                log.append(
                    "No 1001 textures were missing, so didn't create any.")
                log.append("")

        if is_likely_udim is True:
            log.insert(0, "")
            log.insert(0, "Imported textures as UDIMs")
        else:
            new_log = [
                        "Imported textures as NON-UDIMs",
                        "",
                        "If this is not correct, see the Guidelines",
                        ""
                      ]
            new_log.extend(log)
            log = new_log

        log.insert(0, "")
        log.insert(0, "Everything seems fine.")

    else:
        kui_utils.show_multiline_message_box(
            "Need to select a texture directory before importing", " ",
            "ERROR")
    kui_utils.show_multiline_message_box(log, "Import log")


class Import_udim_button_operator(bpy.types.Operator):
    """Imports the textures from the chosen directory"""
    bl_idname = "import_udim."
    bl_label = "Import UDIM Materials"

    def execute(self, context):
        import_textures(context, True)

        return {'FINISHED'}


class Import_standard_button_operator(bpy.types.Operator):
    """Imports the textures from the chosen directory"""
    bl_idname = "import_standard."
    bl_label = "Import non-UDIM Materials"

    def execute(self, context):
        import_textures(context, True)

        return {'FINISHED'}

        udim_layout.prop(mytool, "bool_create_1001s")


class Help_button_operator(bpy.types.Operator):
    """Help popup with guidelines for compatible texture naming conventions"""
    bl_idname = "help_udim."
    bl_label = "Guidelines for the textures"

    def execute(self, context):
        kui_utils.show_multiline_message_box(
            [
                "Guidelines",
                "",
                "All textures need to have names starting with:",
                "",
                "  MATERIALNAME_MAPTYPE",
                "",
                "  Examples",
                "     skin_Base_Color",
                "     skin_Roughness",
                "",
                "UDIM textures also need a TILENUMBER",
                "",
                "  Examples",
                "     skin_Base_Color_1001, skin_Base_Color_1002",
                "     skin_Roughess_1005, skin_Roughess_1009",
            ])

        return {'FINISHED'}


class Main_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "KPUT - PBR UDIM Tool"
    bl_idname = "KPUT_PT_main"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "KPUT"

    def draw(self, context):
        scene = context.scene
        mytool = scene.my_tool

        layout = self.layout

        obj = context.object

        main_layout = layout.box()
        main_layout.label(text="Texture directory")
        main_layout.prop(mytool, "texture_path")

        options_layout = layout.box()
        options_layout.prop(mytool, "bool_replace_mats")

        button_layout = layout.box()
        button_layout.operator(Import_udim_button_operator.bl_idname,
                               text="Create Materials", icon='RENDERLAYERS')

        help_layout = layout.box()
        help_layout.operator(Help_button_operator.bl_idname,
                             text="Help - Guidelines", icon='QUESTION')


class UDIM_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UDIM Based Textures"
    bl_idname = "PBRUI_UDIM_PT_panelid"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_parent_id = "KPUT_PT_main"

    def draw(self, context):
        scene = context.scene
        mytool = scene.my_tool

        layout = self.layout
        obj = context.object
        layout.operator(Import_udim_button_operator.bl_idname,
                        text="Create UDIM Materials", icon='RENDERLAYERS')


class Advanced_options_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Advanced Options"
    bl_idname = "PBRUI_ADV_PT_panelid"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "KPUT_PT_main"

    def draw(self, context):
        scene = context.scene
        mytool = scene.my_tool

        layout = self.layout
        obj = context.object

        main_layout = layout.box()
        main_layout.prop(mytool, "bool_create_1001s")


_classes = [Import_udim_button_operator,
            Import_standard_button_operator,
            MyProperties,
            Main_panel,
            Help_button_operator,
            Advanced_options_panel,
            ]


def register():
    for cl in _classes:
        register_class(cl)

    # apparently needed to get my_tool to work
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

    print('post register')


def unregister():
    for cl in _classes:
        unregister_class(cl)


if __name__ == "__main__":
    register()
