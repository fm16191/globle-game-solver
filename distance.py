#!/usr/bin/env python3

import json
import numpy as np
from sys import argv
from math import sin, cos, sqrt, atan2, radians
import os


def distance(lat1, lon1, lat2, lon2):
    r = 6378.0 # Approximate Earth radius in km

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


# Shittiest way of parsing arrays, but so fucking many incoherent array shapes !!
def make_borders(cdata):
    coordinates = cdata["geometry"]["coordinates"]
    coordinates = str(coordinates).replace(" ", "").replace("[", "").replace("]", "").replace("],", "").split(",")
    coordinates = np.array(coordinates, dtype=float).reshape((-1, 2))
    return coordinates


def distances(target_country, target_distance):
    fo = open("country_data.json")
    data = json.load(fo)
    fo.close()

    target_cdata = None

    for cdata in data["features"]:
        if cdata["properties"]["NAME"].lower() == target_country.lower() or cdata["properties"]["ABBREV"].lower() == target_country.lower():
            target_cdata = cdata
            break

    if not target_cdata:
        print(f"Country \"{target_country}\" not found !")
        exit()

    target_borders = make_borders(target_cdata)

    results = {}

    for cdata in data["features"]:
        country_name = cdata["properties"]["NAME"]
        # country_name = cdata["properties"]["ABBREV"]
        if country_name == target_country: continue
        # geometry_type = cdata["geometry"]["type"]

        borders = make_borders(cdata)

        for ib in target_borders:
            for b in borders:
                d = distance(ib[0], ib[1], b[0], b[1])
                if country_name not in results or d < results[country_name]:
                    results[country_name] = d

                # distance_goal = abs(target_distance - d)
                # if country_name not in results:
                #     results[country_name] = distance_goal
                # elif distance_goal < results[country_name]:
                #     results[country_name] = distance_goal

    results.update((x, abs(y - target_distance)) for x, y in results.items())
    results = sorted(results.items(), key=lambda x: x[1])
    return results


def couleur(d, d_max):
    color = int(d / d_max * 255)
    cmd = """perl -e 'foreach $a(@ARGV){print "\e[48:2::".join(":",unpack("C*",pack("H*",$a)))."m \e[49m "}'"""
    return os.popen(f"{cmd} {255:02x}{color:02x}{color:02x}").read()


if __name__ == "__main__":
    if len(argv) < 3:
        print(f"Usage : {argv[0]} <Country Name> <distance to closest border in KM>")
        exit()

    target_country = argv[1].lower()
    target_distance = float(argv[2])

    results = distances(target_country, target_distance)

    # for cname, d in results[::-1][-20:]:
    d_max = results[-1][1]
    for cname, d in results[:-20 if target_distance != 0 else -1]:
        print(f"{couleur(d, d_max)}{d:5.1f} {cname}")