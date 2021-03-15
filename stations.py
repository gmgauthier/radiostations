import argparse
import DNS
import json
import requests
import secrets

from config import api
from radiomenu import RadioMenu


def ipaddr(hostname, rectype='A'):
    return DNS.dnslookup(hostname, rectype, 3)


def nsname(ipaddrs, rectype='A'):
    return DNS.revlookup(ipaddrs, 3)


def get_host():
    hosts = ipaddr(api())
    preferred_host = secrets.choice(hosts)
    return nsname(preferred_host)


def get_stations(qstring, host):
    resp = requests.get(f"https://{host}/json/stations/search?{qstring}&limit=100000")
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        return [{"response_code": resp.status_code, "reason": resp.reason}]


def search_stations(name=None, country=None, state=None, tags=None, status="up"):
    if tags is None:
        tags = []
    query = ""

    if name:
        if query != "":
            query = query + "&"
        query = query + "name=" + name
    if country:
        if query != "":
            query = query + "&"
        query = query + "country=" + country
    if state:
        if query != "":
            query = query + "&"
        query = query + "state=" + state
    if len(tags) > 0:
        if query != "":
            query = query + "&"
        tag_string = ','.join(tags)  # Be careful here! the tag list is order-dependent in the http call :(
        query = query + "tag=" + tag_string

    stations = get_stations(query, get_host())
    filtered_list = []
    for station in stations:
        station_stat = "down"
        if str(station["lastchecktime"]) == str(station["lastcheckoktime"]):
            station_stat = "up"

        if len(tags) > 1 and station["tags"] == "":  # If searching with tags, but no tags, don't include the station.
            continue

        if station_stat == status:  # only add the entry if it matches the up/down status specified.
            station_entry = {
                "name": str(station["name"]).replace('"', "'").replace(",", " - "),
                "url": str(station["url"].replace(",", "%2C")),
                "codec": str(station["codec"]),
                "bitrate": str(station["bitrate"]),
                "countrycode": str(station["countrycode"]),
                "favicon": str(station["favicon"]).replace(" ", "%20").replace("(", "%28").replace(")", "%29"),
                "tags": str(station["tags"].split(",")).replace(",", ";"),
                "status": str(station_stat)
            }
            filtered_list.append(station_entry)
    return filtered_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, help="Name of station", default=None)
    parser.add_argument("-c", "--country", type=str, help="Station country", default=None)
    parser.add_argument("-s", "--state", type=str, help="Station state (if in US)", default=None)
    parser.add_argument("-t", "--tags", type=str, help="search tag or tags (if more than one, comma-separated", default="")
    args = parser.parse_args()

    station_list = search_stations(name=args.name, country=args.country, state=args.state, tags=args.tags.split(","))

    mainMenu = RadioMenu(station_list)
    mainMenu.display()
