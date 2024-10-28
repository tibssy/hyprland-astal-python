from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
)



class Time(Astal.Label):
    def __init__(self, format="%H:%M - %A %e."):
        super().__init__()
        self.format = format
        self.interval = AstalIO.Time.interval(1000, self.sync)
        self.connect("destroy", self.interval.cancel)
        Astal.widget_set_class_names(self, ["Time"])

    def sync(self):
        self.set_label(GLib.DateTime.new_now_local().format(self.format))