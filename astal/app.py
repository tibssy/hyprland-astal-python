#!/usr/bin/env python3
import sys
import versions
from gi.repository import AstalIO, Astal, Gio
from widget.bar.Bar import Bar
from widget.Notification import NotifWindow
from pathlib import Path


scss = str(Path(__file__).parent.resolve() / "style.scss")
css = "/tmp/style.css"


class App(Astal.Application):
    def do_astal_application_request(self, msg: str, conn: Gio.SocketConnection) -> None:
        AstalIO.write_sock(conn, "hello")

    def do_activate(self) -> None:
        self.hold()
        AstalIO.Process.execv(["sass", scss, css])
        self.apply_css(css, True)

        monitor_index = 1

        if monitor_index in range(len(monitors := self.get_monitors())):
            self.add_window(Bar(monitors[monitor_index]))
            self.add_window(NotifWindow(monitors[monitor_index]))
        else:
            for mon in monitors:
                self.add_window(Bar(mon))
                self.add_window(NotifWindow(mon))


instance_name = "python"
app = App(instance_name=instance_name)


if __name__ == "__main__":
    try:
        app.run(None)
    except Exception as e:
        print(AstalIO.send_message(instance_name, "".join(sys.argv[1:])))
