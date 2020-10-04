import bpy
import os
import csv
import select
import socket

artnet_config = {
    "address": "",
    "port": 6454,
    "net": 0,
    "update_interval": 0.01
}

fixture_dic = {
    "dimmer": "obj.data.energy = watt * 1000 * (values[i] / 255)",
    "rgb": "obj.data.energy = watt * 1000\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
    "rgbw": "obj.data.energy = watt * 1000\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
    "rbg_dimmer": "obj.data.energy = watt * 1000 * (values[i+3] / 255)\nobj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))",
    "dimmer_rgb": "obj.data.energy = watt * 1000 * (values[i] / 255)\nobj.data.color = ((values[i+1] / 255),(values[i+2] / 255),(values[i+3] / 255))",
    "uv": "obj.data.energy = watt * 1000 * (values[i] / 255)\nobj.data.color = (127, 26, 229)"
}

lamps = []


def handle():
    ready = select.select([sock], [], [], artnet_config["update_interval"])
    if ready[0]:
        data = sock.recv(4200)
        if artnet_config["net"] == int.from_bytes((data[14:16]), "little"):
            values = [bytes for bytes in data[18:]]
            for i in range(len(values)):
                try:
                    watt = lamps[i][1]
                    obj = bpy.data.objects["%03d" % (i+1)].children[0]
                    exec(fixture_dic[lamps[i][0]])
                except (KeyError, IndexError):
                    pass


class ArtnetListener(bpy.types.Operator):
    """artnet listener"""
    bl_idname = "wm.artnet_listener"
    bl_label = "Artnet Listener"

    _timer = None

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(time_step=0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            print("END")
            self.cancel(context)
            return {"FINISHED"}

        if event.type == 'TIMER':
            handle()

        return {'PASS_THROUGH'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        sock.close()


def register():
    bpy.utils.register_class(ArtnetListener)


def unregister():
    print("unregister")
    bpy.utils.unregister_class(ArtnetListener)


if __name__ == "__main__":
    register()

    addr = (artnet_config["address"], artnet_config["port"])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4200)
    sock.bind(addr)

    sock.setblocking(0)

    basedir = os.path.dirname(bpy.data.filepath)
    file_ = open(str(basedir)+'/lamps_file.csv', newline='')
    file_lamps = csv.reader(file_, delimiter=";", quotechar='|')
    zahl = 0
    for row in file_lamps:
        lamps.append([])
        zahl1 = 0
        if len(row) != 0:
            for a in row[:-1]:
                if zahl1 == 1:
                    lamps[zahl].append(float(a))
                else:
                    lamps[zahl].append(str(a))
                zahl1 += 1
        zahl += 1
    file_.close()
    #print(lamps)

    bpy.ops.wm.artnet_listener('INVOKE_DEFAULT')
