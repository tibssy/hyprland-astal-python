import math
from .buttons.Workspaces import Workspaces
from .buttons.Wifi import Wifi
from .buttons.Audio import AudioSlider
from .buttons.Battery import BatteryLevel
from .buttons.Media import Media
from .buttons.Tray import SysTray
from .buttons.Clock import Time
from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalBattery as Battery,
    AstalWp as Wp,
    AstalNetwork as Network,
    AstalTray as Tray,
    AstalMpris as Mpris,
    AstalHyprland as Hyprland,
)

SYNC = GObject.BindingFlags.SYNC_CREATE


class FocusedClient(Gtk.Label):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Focused"])
        Hyprland.get_default().connect("notify::focused-client", self.sync)
        self.sync()

    def sync(self, *_):
        client = Hyprland.get_default().get_focused_client()
        if client is None:
            return self.set_label("")

        client.bind_property("title", self, "label", SYNC)


class Left(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(hexpand=True, halign=Gtk.Align.START)
        self.add(Workspaces())
        self.add(FocusedClient())


class Center(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.add(Time())
        self.add(Media())


class Right(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(hexpand=True, halign=Gtk.Align.END)
        self.add(SysTray())
        self.add(AudioSlider())
        self.add(Wifi())
        self.add(BatteryLevel())


class Bar(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor):
        super().__init__(
            anchor=Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.RIGHT
            | Astal.WindowAnchor.TOP,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
        )

        Astal.widget_set_class_names(self, ["Bar"])

        self.add(
            Astal.CenterBox(
                start_widget=Left(),
                center_widget=Center(),
                end_widget=Right(),
            )
        )

        self.show_all()
