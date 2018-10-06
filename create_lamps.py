import bpy
import os

fixture_dic = {
        "dimmer": "obj.data.energy = watt * 10 * (values[i] / 255)",
        "rgb": "obj.data.energy = watt * 10\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "rgbw": "obj.data.energy = watt * 10\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "rbg_dimmer": "obj.data.energy = watt * 10 * (values[i+3] / 255)\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "dimmer_rgb": "obj.data.energy = watt * 10 * (values[i] / 255)\nobj.data.color = ((values[i+1] / 255),(values[i+2] / 255),(values[i+3] / 255))",
        "uv": "obj.data.energy = watt * 10 * (values[i] / 255)\nobj.data.color = (127, 26, 229)"
        }

lamps = []
for i in range(512):
    lamps.append([])

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Add lamp to scene"
    
    dmx_address = bpy.props.IntProperty(name="Starting DMX Address")
    fixture_type = bpy.props.StringProperty(name="Fixturetype")
    watts = bpy.props.FloatProperty(name="Watts")
    last = bpy.props.BoolProperty(name="Last one?")

    def execute(self, context):
        if int(self.dmx_address) > 0:
            lamps[int(self.dmx_address)-1] = [str(self.fixture_type), float(self.watts)]
        
        if self.last == 0:
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
        else:
            basedir = os.path.dirname(bpy.data.filepath)
            lamps_file = open(str(basedir)+'/lamps_file.csv', 'w')
            for a in range(len(lamps)):
                if len(lamps[a]) > 0:
                    bpy.ops.mesh.primitive_cube_add()
                    bpy.data.objects['Cube'].name = "%03d" % (a+1)
                    bpy.ops.object.light_add(type='SPOT')
                    bpy.data.objects['Spot'].data.spot_size = 0.450295
                    bpy.data.objects['Spot'].data.spot_blend = 0.420
                    bpy.data.objects['Spot'].data.shadow_soft_size = 0.367
                    bpy.data.objects['Spot'].name = "%03d_lamp" % (a+1)
                    bpy.data.objects["%03d_lamp" % (a+1)].parent = bpy.data.objects["%03d" % (a+1)]
                    if lamps[a][0] == 'dimmer':
                        bpy.data.objects["%03d" % (a+1)].data = bpy.data.objects['Theater'].data
                    elif lamps[a][0] == 'rgb':
                        bpy.data.objects["%03d" % (a+1)].data = bpy.data.objects['LED'].data
                    else:
                        bpy.data.objects["%03d" % (a+1)].data = bpy.data.objects['Profiler'].data
                    for b in range(len(lamps[a])):
                        lamps_file.write(str(lamps[a][b])+";")
                lamps_file.write("\n")
            lamps_file.close()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

bpy.utils.register_class(DialogOperator)

bpy.ops.object.dialog_operator('INVOKE_DEFAULT')