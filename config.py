import configparser

config = configparser.ConfigParser()
config.read('radiostations.ini')


def api():
    return config.get('DEFAULT', 'radio_browser.api')


def player():
    return config.get('DEFAULT', 'player.command')


def options():
    return config.get('DEFAULT', 'player.options')


def maxitems():
    return int(config.get('DEFAULT', 'menu_items.max'))

