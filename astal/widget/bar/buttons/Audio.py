from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalWp as Wp,
)


SYNC = GObject.BindingFlags.SYNC_CREATE


class AudioSlider(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["AudioSlider"])
        Astal.widget_set_css(self, "min-width: 140px")

        icon = Astal.Icon()
        slider = Astal.Slider(hexpand=True)

        self.add(icon)
        self.add(slider)

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume-icon", icon, "icon", SYNC)
        speaker.bind_property("volume", slider, "value", SYNC)
        slider.connect("dragged", lambda *_: speaker.set_volume(slider.get_value()))