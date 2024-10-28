from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalBattery as Battery,
)


SYNC = GObject.BindingFlags.SYNC_CREATE


class BatteryLevel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Battery"])
        print(Battery.get_default())

        icon = Astal.Icon()
        label = Astal.Label()

        self.add(icon)
        self.add(label)

        bat = Battery.get_default()
        bat.bind_property("is-present", self, "visible", SYNC)
        bat.bind_property("battery-icon-name", icon, "icon", SYNC)
        bat.bind_property(
            "percentage",
            label,
            "label",
            SYNC,
            lambda _, value: f"{int(value * 100)}%",
        )