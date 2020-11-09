import bpy


def create_empty_texture(res_x, res_y, path, file_format="PNG",
                         use_float=False, use_alpha=False):
    """File formats: PNG, OPEN_EXR, JPEG
    """

    # blank image
    image = bpy.data.images.new(
        "temp_empty_image", width=res_x, height=res_y, alpha=use_alpha, 
        float_buffer=use_float)

    print('creating empty texture with path:')
    print(path)

    # write image
    image.filepath_raw = path
    image.file_format = file_format
    image.save()

    # NOTE temp image must be removed for some reason, probably since
    # it shares the same path as the image that is then loaded later,
    # even though the name should be different

    bpy.data.images.remove(image)