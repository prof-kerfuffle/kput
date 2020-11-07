import bpy
path = "D:\\blender_generated_a01.png"


def create_empty_texture(res_x, res_y, path):

    # blank image
    image = bpy.data.images.new(
        "temp_empty_image", width=res_x, height=res_y)

    print('creating empty texture with path:')
    print(path)

    # write image
    image.filepath_raw = path
    image.file_format = 'PNG'
    image.save()

    # NOTE temp image must be removed for some reason, probably since
    # it shares the same path as the image that is then loaded later,
    # even though the name should be different

    print('removing image')
    bpy.data.images.remove(image)
    print("texture generated: ", path)
