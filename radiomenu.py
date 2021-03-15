from python_console_menu import AbstractMenu, MenuItem
import subprocess


class RadioMenu(AbstractMenu):
    def __init__(self, station_list=None):
        super().__init__("Radio Player Menu")
        if station_list is None:
            station_list = []

        for i in range(len(station_list)):
            self.add_menu_item(
                MenuItem(
                    i,
                    station_list[i]["name"] + " " +
                    station_list[i]["codec"] + " " +
                    station_list[i]["bitrate"] + " " +
                    station_list[i]["url"],
                    lambda url=station_list[i]["url"]: subprocess.run(["mpv", "--no-video", url])
                )
            )

    def initialise(self):
        self.add_menu_item(MenuItem(9999, "Exit menu").set_as_exit_option())
