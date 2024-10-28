from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalMpris as Mpris,
)


SYNC = GObject.BindingFlags.SYNC_CREATE


class Media(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.players = {}
        mpris = Mpris.get_default()
        Astal.widget_set_class_names(self, ["Media"])
        mpris.connect("notify::players", self.sync)
        self.sync()

    def sync(self):
        mpris = Mpris.get_default()
        for child in self.get_children():
            child.destroy()

        if len(mpris.get_players()) == 0:
            self.add(Gtk.Label(visible=True, label="Nothing Playing"))
            return

        player = mpris.get_players()[0]
        label = Gtk.Label(visible=True)
        cover = Gtk.Box(valign=Gtk.Align.CENTER)
        Astal.widget_set_class_names(cover, ["Cover"])

        self.add(cover)
        self.add(label)

        player.bind_property(
            "title",
            label,
            "label",
            SYNC,
            lambda *_: f"{player.get_artist()} - {player.get_title()}",
        )

        def on_cover_art(*_):
            Astal.widget_set_css(
                cover, f"background-image: url('{player.get_cover_art()}')"
            )

        id = player.connect("notify::cover-art", on_cover_art)
        cover.connect("destroy", lambda _: player.disconnect(id))
        on_cover_art()