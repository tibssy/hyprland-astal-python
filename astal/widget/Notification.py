from datetime import datetime

from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    Pango,
    AstalNotifd as Notifd
)

class Notification(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(visible=True, orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.notification = None
        Astal.widget_set_class_names(self, ["Notification"])
        self.notifd = Notifd.get_default()
        self.notifd.connect("notified", self.on_notified)

    def on_notified(self, _, id, *args):
        self.notification = self.notifd.get_notification(id)

        notification_container = Astal.Box(spacing=10)
        notification_container.pack_start(self.create_text_container(), True, True, 0)
        notification_container.pack_start(self.set_close_button(notification_container), False, False, 0)

        self.pack_end(notification_container, False, False, 0)
        self.show_all()

    def create_header(self):
        header = Astal.Box()

        title = Astal.Label()
        title_text = self.notification.get_summary() or self.notification.get_app_name()
        title.set_markup(f'<span font="12" weight="bold">{title_text}</span>')
        title.set_halign(Gtk.Align.START)
        header.pack_start(title, True, True, 0)

        time_stamp_text = self.get_time_stamp()
        time_stamp = Astal.Label(label=time_stamp_text)
        header.pack_start(time_stamp, False, False, 0)

        return header

    def create_text_container(self):
        text_container = Astal.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        text_container.pack_start(self.create_header(), True, True, 0)

        if content_text := self.notification.get_body():
            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            text_container.pack_start(separator, True, True, 0)

            content = Astal.Label(label=content_text)
            content.set_halign(Gtk.Align.START)
            content.set_line_wrap(True)
            text_container.pack_start(content, True, True, 0)

        return text_container

    def set_close_button(self, instance):
        close_button = Astal.Button()
        close_button.connect("clicked", lambda x: instance.destroy())
        close_button.add(Astal.Icon(icon='window-close-symbolic'))
        return close_button

    def get_time_stamp(self):
        timestamp = self.notification.get_time()
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object.strftime('%H:%M')


class NotifWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.TOP,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP
        )

        Astal.widget_set_class_names(self, ["Notifications"])

        self.add(Notification())
        self.show_all()