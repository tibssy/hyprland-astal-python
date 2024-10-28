from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalTray as Tray,
)


SYNC = GObject.BindingFlags.SYNC_CREATE


class SysTray(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.items = {}
        # print(f'items: {self.items}')
        tray = Tray.get_default()
        tray.connect("item_added", self.add_item)
        tray.connect("item_removed", self.remove_item)

    def add_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            return

        item = Tray.get_default().get_item(id)
        theme = item.get_icon_theme_path()

        if theme is not None:
            from app import app

            app.add_icons(theme)

        menu = item.create_menu()
        btn = Astal.Button(visible=True)
        icon = Astal.Icon(visible=True)

        def on_clicked(btn):
            if menu:
                menu.popup_at_widget(btn, Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, None)

        def on_destroy(btn):
            if menu:
                menu.destroy()

        btn.connect("clicked", on_clicked)
        btn.connect("destroy", on_destroy)

        item.bind_property("tooltip-markup", btn, "tooltip-markup", SYNC)
        item.bind_property("gicon", icon, "gicon", SYNC)
        self.add(btn)
        self.items[id] = btn
        self.show_all()

    def remove_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            del self.items[id]