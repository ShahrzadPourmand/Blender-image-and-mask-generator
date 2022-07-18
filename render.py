import bpy
import sys
sys.path.append("C:/Users/pourmand/Documents/_mask and render/") 
import sceneGenerator
from random import uniform,randint

path_out = "C:/Users/pourmand/Documents/_mask and render/output/"
# render settings

bpy.context.scene.render.resolution_x = 256 #224
bpy.context.scene.render.resolution_y = 256 #224
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format= 'PNG'
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.view_settings.view_transform = 'Filmic'
bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
#bpy.context.scene.render.filepath = "C:/Users/pourmand/Documents/_mask and render/output/image" + str(currentImg) + ".PNG"

numOfImages = 100
sceneGenerator.init()

for currentImg in range(numOfImages):
    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.name != 'Plane':
            bpy.data.objects.remove(obj, do_unlink=True)
    name = str(currentImg) + "0001"
    sceneGenerator.generate_scene(name, path_out)
    #camera:
    rand_x=uniform(-4,4)
    rand_y=uniform(-4,4)
    rand_z=uniform(3,5)
    
    cam = bpy.context.scene.objects.get("Camera")
    if cam:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Camera'].select_set(True)
        bpy.data.objects['Camera'].location  = (rand_x,rand_y,rand_z)
        bpy.data.objects['Camera'].constraints["Track To"].target = bpy.data.objects['Plane']
    else:
        bpy.ops.object.select_all(action='DESELECT')    
        bpy.ops.object.camera_add(location=(rand_x ,rand_y ,rand_z), rotation=(0,0,0))
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects['Plane']

    bpy.context.scene.camera = bpy.data.objects["Camera"]
    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True
    #bpy.context.scene.use_nodes = True

    # switch on nodes and get reference
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    #render node
    render_node = tree.nodes.new('CompositorNodeRLayers')
    #convertor node
    convertor_node = tree.nodes.new('CompositorNodeIDMask')
    convertor_node.location = 400,0 
    convertor_node.index = 1
       
    # create output node
    out_node = tree.nodes.new('CompositorNodeOutputFile')   
    out_node.location = 700,0
    out_node.base_path = path_out
    out_node.file_slots['Image'].path = "image" + str(currentImg)
    mask = "mask"+ str(currentImg)
    out_node.layer_slots.new(mask)
    out_node.file_slots[mask].use_node_format = False
    out_node.file_slots[mask].format.color_mode = 'BW'
    out_node.file_slots[mask].format.color_depth = '8'
    #out_node.active_input_index = 1
        

    # link nodes
    links = tree.links
    link = links.new(render_node.outputs[3], convertor_node.inputs[0])
    link2 = links.new(render_node.outputs[0], out_node.inputs[0])
    link3 = links.new(convertor_node.outputs[0], out_node.inputs[1])

    bpy.ops.render.render(write_still=True)