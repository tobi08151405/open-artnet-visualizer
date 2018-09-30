import bpy
import socket

class ModalTimerOperator(bpy.types.Operator):
    """timed sniffer"""
    bl_idname = "wm.timed_sniffer"
    bl_label = "Timed Sniffer"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # change theme color, silly!
                watt = 100
                UDP_IP = '' #listen to any address
                UDP_PORT = 6454 #set Artnet port
                sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP
                sock.bind((UDP_IP, UDP_PORT))
                data, addr = sock.recvfrom(4576)
                if len(data) == 530:
                    #print("received message:", data)
                    values = [bytes for bytes in data[18:]]
                    #print(values)
                    for i in range(len(values)):
                        try:
                            obj = bpy.data.objects["%03d" % (i+1)].children[0]
                            obj.data.energy = watt * 10 * (values[i] / 255)
                            print(obj, values[i], obj.data.energy)
                        except KeyError:
                            pass

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.timed_sniffer()
