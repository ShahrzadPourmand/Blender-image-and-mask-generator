import bpy
import random
from math import radians

objectTextures = "C:/Users/pourmand/Documents/_mask and render/objectTextures/"
tableTextures =  "C:/Users/pourmand/Documents/_mask and render/tableTextures/"
HDRI_Path = "C:/Users/pourmand/Documents/_mask and render/HDRI/"

def init():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
     
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

    for i in range(1,47):
        name = "o"+str(i) + ".jpg"
        bpy.data.images.load(objectTextures + name)
    for i in range(1,83):
        name = str(i) + ".jpg"
        bpy.data.images.load(tableTextures + name)
    for i in range(1,121):
        name = "img"+ str(i) + ".hdr"
        bpy.data.images.load(HDRI_Path + name )
    #plane
    bpy.ops.mesh.primitive_plane_add(size = 5,location=(0,0,0))
    plane = bpy.context.active_object
    plane_mat = bpy.data.materials.new(name="plane material")
    plane.data.materials.append(plane_mat)
    plane_mat.use_nodes = True
    global plane_node_texture
    plane_node_texture = plane_mat.node_tree.nodes.new(type="ShaderNodeTexImage")
    
    plane_node_texture.location = -300,0
    node_BSDF = plane_mat.node_tree.nodes['Principled BSDF']
    link = plane_mat.node_tree.links.new(plane_node_texture.outputs["Color"], node_BSDF.inputs["Base Color"])  
    #HDRI
    # Get the environment node tree of the current scene
    node_tree = bpy.context.scene.world.node_tree
    tree_nodes = node_tree.nodes

    # Clear all nodes
    tree_nodes.clear()

    # Add Background node
    global node_environment 
    node_environment = tree_nodes.new('ShaderNodeTexEnvironment')  
    node_environment.location = -300,0
    # Add Output node
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')   
    node_output.location = 200,0

    # Link all nodes
    links = node_tree.links
    link = links.new(node_environment.outputs["Color"], node_output.inputs["Surface"])
def save_values(name,address,rough,colorR,colorG,colorB):
    f = open(address + name + ".txt", "x")
    textt = "{roug:.3f} {cR:.3f} {cG:.3f} {cB:.3f}"
    f.write(textt.format(roug = rough, cR = colorR, cG = colorG, cB = colorB))
    f.close()
    
    
def generate_scene(name,address):
    global node_environment
    global plane_node_texture
    plane_node_texture.image = bpy.data.images[str(random.randint(1, 82))+ ".jpg"]
    node_environment.image = bpy.data.images["img"+str(random.randint(1, 120))+ ".hdr"]
    rot_z = radians(random.uniform(0.0, 360.0))
    node_environment.texture_mapping.rotation[2] = rot_z
    
    objectTypes = ["Cone", "Sphere", "Cube", "Cylinder", "Torus","Ico_sphere", "Monkey", "teapot", "beam"]
    randObj = random.choice(objectTypes)
    #randObj = "Cylinder"
    if randObj == "beam": 
        rot = random.uniform(0.0,180)
        beamx = random.uniform(0.7,1.3)
        beamy = random.uniform(1.4,2.5)
        beamz = random.uniform(0.8,1.2)
        bpy.ops.mesh.add_beam(align='WORLD', location=(0,0, beamz/2), rotation=(0,0 , radians(rot)), change=False, beamZ = beamz, beamX = beamx, beamY = beamy)
    
    if randObj == "teapot":
        rot = random.uniform(0.0,360)
        size = random.uniform(0.2,0.38)
        offset = random.uniform(-0.015,0.015)
        bpy.ops.mesh.primitive_teapot_add(align='WORLD', location=(0,0,0), rotation=(0,0 , radians(rot)), resolution=9)
        bpy.ops.object.shade_smooth()
        bpy.context.object.scale = (size,size,size+offset)
    if randObj == "Sphere":
        rad = random.uniform(0.45,0.6) #0.03,0.1
        bpy.ops.mesh.primitive_uv_sphere_add(radius = rad,location=(0,0,rad))
        bpy.ops.object.shade_smooth()
    if randObj == "Cube":
        size1 = random.uniform(0.35,0.8) #0.05,0.13
        size2 = random.uniform(0.45,0.8)
        size3 = random.uniform(0.45,0.8)
        bpy.ops.mesh.primitive_cube_add(location=(0,0,size3/2), scale=(size1,size2,size3))
    if randObj == "Cylinder":
        ver = random.randint(3,40)
        cylinderRadius = random.uniform(0.4,0.7) #0.03,0.1
        cylinderDepth = random.uniform(0.25,0.95) #0.03,0.1
        bpy.ops.mesh.primitive_cylinder_add(vertices= ver,radius=cylinderRadius, depth=cylinderDepth,location=(0,0,cylinderDepth/2))
        #obj = bpy.context.active_object
        #rot = [(radians(0),radians(0),radians(0)),(radians(0),radians(90),radians(0)),(radians(90),radians(0),radians(0))]
        #obj.rotation_euler = random.choice(rot)
            
    if randObj == "Cone":
        coneDepth = random.uniform(0.8,1.5) #0.03,0.15
        rad = random.uniform(0.4,0.8) #0.03,0.1
        ver = random.randint(3,35)
        bpy.ops.mesh.primitive_cone_add(vertices= ver,radius1 = rad ,depth=coneDepth ,location=(0,0,coneDepth/2))
            
    if randObj == "Torus":
        major = random.uniform(0.5,0.7)#0.03,0.15
        minor = random.uniform(0.09,0.22)#0.02,0.03
        bpy.ops.mesh.primitive_torus_add(location=(0,0,minor), major_radius = major, minor_radius = minor)
        bpy.ops.object.shade_smooth()
        
    if randObj == "Ico_sphere":
        rad = random.uniform(0.5,0.65)#0.03,0.1
        bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,rad), radius = rad, subdivisions = random.choice([1,2]))
            
    if randObj == "Monkey":
        s = random.uniform(0.8,1.1) #0.03,0.15
        bpy.ops.mesh.primitive_monkey_add(size =s,location=(0,0,s/2))
        obj = bpy.context.active_object
        rot_z = random.uniform(0,360)
        obj.rotation_euler = [radians(-90),radians(0),radians(rot_z)]
        
    obj = bpy.context.active_object
    obj.pass_index = 1
    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True

    mat = bpy.data.materials.new(name=("material "+randObj))
    obj.data.materials.append(mat)
    mat.use_nodes = True
    
    #r_choice = random.choice(["nonspec","spec"])
    #if r_choice == "nonspec":
    #    roughness = 1.0
    #    metallic = 0.0
    #else:
    #    metallic = random.uniform(0.0, 1.0)
    #    if metallic > 0.5:
    #        roughness = random.uniform(0.0, 0.5)
    #    else:
    #        roughness = random.uniform(0.0, 1.0)
    roughness = random.uniform(0.0, 1.0)
    metallic = 0.0
    if roughness < 0.3:
        if roughness < 0.15:
            metallic = random.uniform(0.5, 1.0)
        else:
            metallic = random.uniform(0.3, 0.8)
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness #Roghness
    mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = metallic #Metallic

    colorR = random.uniform(0.0, 1)
    colorG = random.uniform(0.0, 1)
    colorB = random.uniform(0.0, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (colorR , colorG, colorB, 1) #color
    save_values(name,address,roughness,colorR , colorG, colorB)
    return obj

#out = "C:/Users/pourmand/Documents/_mask and render/output/"
#init()        
#generate_scene("01",out)