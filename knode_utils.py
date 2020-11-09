import bpy


def create_udim_texture_node(nodes, dir, file, pos, color_space, color, udim):
    """
    Creates a shader editor texture node, with ability to choose udim tiles,
    using what seems to be a necesary hack, opening the image with an
    bpy.ops operator, instead of the proper one bpy.data.images.load.

    For udims to work properly, there needs to be a 1001 tile/file in the
    sequence, otherwise it won't be recognized, and only one tile will be
    loaded
    """

#    print("** create udim texture node 01")
#    print('file')
#    print(file)

#    print('dir')
#    print(dir)
    path = dir + file
#    print('path')
#    print(path)

#    print("pre open")
    imaage = bpy.ops.image.open(
        filepath=path,
        directory=dir,
        files=[{"name": file}],
        show_multiview=False)
#    print(imaage)
#    print("post open")

    return_node = nodes.new("ShaderNodeTexImage")

#    print("bpy.data.images")
#    for i in bpy.data.images:
#        print(i)
#    print("-- post bpy.data.images")

#    print("pre bpy.data.images[file]")
#    print('file')
#    print(file)
    return_node.image = bpy.data.images[file]
#    print("-- post bpy.data.images[file]")

    if udim:
        return_node.image.source = 'TILED'
    return_node.location = pos

    if color_space:
        return_node.image.colorspace_settings.name = color_space
    else:
        return_node.image.colorspace_settings.name = 'sRGB'
    if color:
        return_node.color = color  # (r=0.0000, g=1.0000, b=0.0000)
    return_node.use_custom_color = True

    return return_node
