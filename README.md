# KPUT - PBR UDIM Tool

A convenience tool that automates the creation of materials from textures, with UDIM support.

1. Select the folder with the textures:

2. Select whether you want the current materials to be replaced by the new ones (unchecked will create materials with the ending: "_imported")

3. Press Create Materials

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

# Current Limitations

Currently only supports map types:

    Base_Color (albedo, diffuse)
    Roughness
    Metallic
    Height
    Normal
    Emissive
    Opacity

