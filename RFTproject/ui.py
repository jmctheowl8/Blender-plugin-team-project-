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

# == GLOBAL VARIABLES      #('add_version', bpy.props.BoolProperty(name='Add Version', default=True)),
PROPS = [
    ('prefix', bpy.props.StringProperty(name='User', default='')),
    ('suffix', bpy.props.StringProperty(name='PIN', default='')),
    
    ('version', bpy.props.IntProperty(name='Instances', default=1)),
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
    
    
    def execute(self, context):
        user = ""
        pin = ""
        instance = 1
        
        params = (
            context.scene.prefix,
            context.scene.suffix,
            context.scene.add_version
        )
        
        if context.scene.prefix != "":
            context.secne.prefix =''
            
        if context.scene.suffix != "":
            context.secne.suffix = ""
        
        if add_version >= 1 :
            context.scene.add_version        
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