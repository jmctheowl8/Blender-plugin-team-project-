bl_info = {
    # required
    'name': 'Plug_in',
    'blender': (3, 1, 2),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'Mina PÃªcheux',
    'description': 'A quick object renamer to add a prefix, a suffix and an optional version number to the selected objects.',
}

import bpy
import re
import io
import paramiko
from paramiko import SSHClient
from scp import SCPClient

# == GLOBAL VARIABLES      #('add_version', bpy.props.BoolProperty(name='Add Version', default=True)),
PROPS = [
    ('prefix', bpy.props.StringProperty(name='User', default='')),
    ('suffix', bpy.props.StringProperty(name='PIN', default='')),
    ('version', bpy.props.StringProperty(name='Instances', default="")),
]

# == UTILS
#def rename_object(obj, params):
    #(prefix, suffix, version, add_version) = params
    
    #version_str = '-v{}'.format(version) if add_version else ''
    
    #format_regex = r'(?P<prefix>.*)_(?P<main>.*)_(?P<suffix>[^-\n]*)(-v(?P<version>\d+))?'
    #match = re.search(format_regex, obj.name)
    ## if the object has already been renamed previously,
    ## extract the initial name
    #if match is not None:
        #current_name = match.group('main')
    ## else, if it has a "default" name
    #else:
        #current_name = obj.name
        
    #
    #obj.name = '{}_{}_{}{}'.format(prefix, current_name, suffix, version_str)

# == OPERATORS
# render
class ObjectRenamerOperator(bpy.types.Operator):
    
    bl_idname = 'opr.object_renamer_operator'
    bl_label = 'Object Renamer'
    user = ""
    pin = ""
    instance =""
    
    def execute(self, context):
        params = (
            context.scene.prefix,
            context.scene.suffix,
            context.scene.version
        )
    
        if context.scene.prefix != "":
            user = context.scene.prefix
            context.scene.prefix =''
        if context.scene.suffix != "":
            pin = context.scene.suffix
            context.scene.suffix = ""
        if context.scene.version !="" :
            instance = context.scene.version
            context.scene.version = "1"
        
        numNodes = instance # change this to match instances

        # changing model make sure to change all the parts that have the blend file in order to match
        blenderjb = ("#!/bin/bash\n\n"
        "#CC -gcpit c2-standard-4\n\n"
        "#Slurm HPC Scheduler\n\n"
        "#SBATCH -N " + numNodes + "\n\n"
        "export SHARED_FS_NAME=/mnt/orangefs \n\n"
        "#Uncomment this section for use with openMPI\n\n"
        "module add openmpi/3.0.0\n\n"
        "cd $SHARED_FS_NAME/blender/blenderjobs\n\n"
        "mpiexec /software/blender/3.10/blender -b bouncingBall.blend -o $SHARED_FS_NAME/blender/frame_#### -E CYCLES -F png  -a \n\n")

        f = open("blender_render.txt", "w")
        f.write(blenderjb)
        f.close()

        #open and read the file after the appending:
        f = open("blender_render.txt", "r")
        print(f.read()) 

        command = "df"

        # Update the next three lines with your
        # server's information

        host = "35.196.90.221"
        username = "ccqadmin" # change varable
        password = "hackHPC9"  # set variable

        # the belo section actually runs a command 
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        scp = SCPClient(client.get_transport())
        scp.put('bouncingBall.blend', recursive=True, remote_path='/mnt/orangefs/blender/blenderjobs')
        # Downloading files to the server
        #scp.get('CommandWorks.txt')

        _stdin, _stdout,_stderr = client.exec_command("cd /mnt/orangefs/blender/blenderjobs; ccqsub blender_render.txt;") 

        print( _stdout.read().decode())

        #The below code will be were you place the ffmpeg all you have to do is uncomment anf place the ffmpeg command in place of "df"
        #_stdin, _stdout,_stderr = client.exec_command("ccqstat") 
        #print( _stdout.read().decode())
        client.close()
     
                
        return {'FINISHED'}
    
        
    
        
# == PANELS

class ObjectRenamerPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_object_renamer'
    bl_label = 'Cloud rendering'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        col = self.layout.column()
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
            
        col.operator('opr.object_renamer_operator', text='Render')


# == MAIN ROUTINE
CLASSES = [
    ObjectRenamerOperator,
    ObjectRenamerPanel,
]

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
               
if __name__ == '__main__':
    register()
    
    # save changes and install as a addon to get it to work