from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalHyprland as Hyprland,
)


class Workspaces(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Workspaces"])

        self.hypr = Hyprland.get_default()
        self.hypr.connect("notify::workspaces", self.sync)
        self.hypr.connect("notify::focused-workspace", self.sync)

        self.sync()

    def sync(self, *_):
        self.clear_children()
        sorted_workspaces = self.get_sorted_workspaces()

        for workspace in sorted_workspaces:
            self.add(self.create_workspace_button(workspace))

    def clear_children(self):
        for child in self.get_children():
            child.destroy()

    def get_sorted_workspaces(self):
        return sorted(self.hypr.get_workspaces(), key=lambda ws: ws.get_id())

    def create_workspace_button(self, workspace):
        button = Gtk.Button(visible=True)
        button.add(Gtk.Label(visible=True, label=workspace.get_id()))

        if self.hypr.get_focused_workspace() == workspace:
            Astal.widget_set_class_names(button, ["focused"])

        button.connect("clicked", lambda *_: workspace.focus())
        return button