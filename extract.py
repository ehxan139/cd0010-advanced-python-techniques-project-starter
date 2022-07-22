"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
     objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        neos = []
        for row in reader:
            neos.append(
                NearEarthObject(
                    designation=row['pdes'],
                    name=row['name'],
                    diameter=row['diameter'],
                    hazardous=row['pha']))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close
     approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path) as jsonfile:
        jsondata = json.load(jsonfile)
        approaches = []
        data = jsondata['data']
        for each_d in data:
            approaches.append(
                CloseApproach(
                    _designation=each_d[0],
                    time=each_d[3],
                    distance=each_d[4],
                    velocity=each_d[7]))
    return approaches
