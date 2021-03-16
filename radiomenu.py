from python_console_menu import AbstractMenu, MenuItem
import subprocess

from config import player, options, maxitems


class RadioMenu(AbstractMenu):
    def __init__(self, station_list=None):
        super().__init__("Radio Player Menu")
        if station_list is None:
            station_list = []

        for i in range(len(station_list)):
            if i < maxitems():  # The very first item is the exit option, so not "<=".
                self.add_menu_item(
                    MenuItem(
                        i,
                        "{:<35}".format(station_list[i]["name"][:35]) + " " +  # force 35 character fixed length
                        "{:<5}".format(station_list[i]["codec"][:5]) + " " +   # force 5 character fixed length
                        "{:<5}".format(station_list[i]["bitrate"][:5]) + " " +
                        station_list[i]["url"],
                        lambda url=station_list[i]["url"]: subprocess.run([player(), options(), url])
                    )
                )
            else:
                break

    def initialise(self):
        self.add_menu_item(MenuItem(maxitems(), "Exit menu").set_as_exit_option())
