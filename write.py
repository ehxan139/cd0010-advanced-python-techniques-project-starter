"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
     saved.
    """
    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous')
    results = list(results)

    data_list = []
    for result in results:
        data = {key: [] for key in fieldnames}
        data['datetime_utc'] = result.time
        data['distance_au'] = result.distance
        data['velocity_km_s'] = result.velocity
        data['designation'] = result.neo.designation
        data['name'] = result.neo.name or ''
        data['diameter_km'] = str(result.neo.diameter)
        data['potentially_hazardous'] = result.neo.hazardous
        data_list.append(data)

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
     saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'neo')
    neo_field_names = (
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous')
    results = list(results)

    data_list = []
    for result in results:
        data = {key: [] for key in fieldnames}
        data['datetime_utc'] = datetime_to_str(result.time)
        data['distance_au'] = result.distance
        data['velocity_km_s'] = result.velocity
        data['neo'] = {key: [] for key in neo_field_names}
        data['neo']['designation'] = result.neo.designation
        data['neo']['name'] = result.neo.name or ''
        data['neo']['diameter_km'] = result.neo.diameter
        data['neo']['potentially_hazardous'] = result.neo.hazardous

        data_list.append(data)

    with open(filename, 'w') as jsonfile:
        json.dump(data_list, jsonfile, indent=4)
