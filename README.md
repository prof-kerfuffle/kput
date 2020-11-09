# KPUT - PBR UDIM Tool

A convenience tool that automates the creation of materials from texture maps, with UDIM support.

Example exporting two UDIM based materials from Substance Painter to Blender:

![Substance_to_blender_example](http://marcus.krupa.se/blender/addons/kput/instructional/kput_substance_import_a01.gif)

[Download zip](https://www.dropbox.com/s/kavyr8ez0e89zl8/kput_pbr_udim_tool.zip?dl=1)

# Naming Guidelines

For the import to work, use the following naming convention, and use under-scores, instead of spaces:

MATERIAL-NAME_MAP-TYPE

  Examples:
  
    Skin_Roughness.png
    Skin_Opacity.png
    
For UDIM textures, make sure they end with a tile number of the kind:

  Examples:
  
    Skin_Roughness_1001.png
    Skin_Opacity_1003.png

# Good to know

In order for Blender to recognize UDIM textures, it seems that currently (2.9) there has to be a 1001 tile present. To deal with this, the addon will create blank 1001 textures if one isn't found. You can disable this in the Advanced options section, if preferred.

# Current Limitations

Currently only supports map types:

    Base_Color (albedo, diffuse)
    Roughness
    Metallic
    Height
    Normal
    Emissive
    Opacity

