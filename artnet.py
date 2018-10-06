import bpy
import socket
import os
import csv

fixture_dic = {
        "dimmer": "obj.data.energy = watt * 10 * (values[i] / 255)",
        "rgb": "obj.data.energy = watt * 10\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "rgbw": "obj.data.energy = watt * 10\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "rbg_dimmer": "obj.data.energy = watt * 10 * (values[i+3] / 255)\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
        "dimmer_rgb": "obj.data.energy = watt * 10 * (values[i] / 255)\nobj.data.color = ((values[i+1] / 255),(values[i+2] / 255),(values[i+3] / 255))",
        "uv": "obj.data.energy = watt * 10 * (values[i] / 255)\nobj.data.color = (127, 26, 229)"
        }

class timed_sniffer(bpy.types.Operator):
    """timed sniffer"""
    bl_idname = "wm.timed_sniffer"
    bl_label = "Timed Sniffer"

    _timer = None

    def modal(self, context, event):
        global lamps
        global fixture_dic
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            UDP_IP = '' #listen to any address
            UDP_PORT = 6454 #set Artnet port
            sock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP
            sock.bind((UDP_IP, UDP_PORT))
            data, addr = sock.recvfrom(4576)
            if len(data) == 530:
                values = [bytes for bytes in data[18:]]
                for i in range(len(values)):
                    try:
                        watt=lamps[i][1]
                        obj = bpy.data.objects["%03d" % (i+1)].children[0]
                        exec(fixture_dic[lamps[i][0]])
                    except (KeyError, IndexError):
                        pass

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(timed_sniffer)


def unregister():
    bpy.utils.unregister_class(timed_sniffer)


if __name__ == "__main__":
    lamps=[]
    basedir = os.path.dirname(bpy.data.filepath)
    file_ = open(str(basedir)+'/lamps_file.csv', newline='')
    file_lamps = csv.reader(file_, delimiter=";", quotechar='|')
    zahl = 0
    for row in file_lamps:
        lamps.append([])
        zahl1=0
        if len(row) != 0:
            for a in row[:-1]:
                if zahl1 == 1:
                    lamps[zahl].append(float(a))
                else:
                    lamps[zahl].append(str(a))
                zahl1 += 1
        zahl += 1
    file_.close()
    print(lamps)
    register()
    
    bpy.ops.wm.timed_sniffer()