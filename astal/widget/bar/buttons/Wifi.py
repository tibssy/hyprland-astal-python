from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalNetwork as Network,
)


SYNC = GObject.BindingFlags.SYNC_CREATE


class Wifi(Astal.Icon):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Wifi"])
        self.build_wifi()

    def build_wifi(self):
        if wifi := Network.get_default().get_wifi():
            wifi.bind_property("ssid", self, "tooltip-text", SYNC)
            wifi.bind_property("icon-name", self, "icon", SYNC)