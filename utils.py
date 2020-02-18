from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import logging

from constants import FILTERED_FILE


# Functions for locating purposes
def get_coordinates(location):
    """
    (str) -> (tuple)
    This function returns tuple of latitude and longitude for certain location,
    e.g. city or country with different permutations.
    >>> get_coordinates("Germany")
    (51.0834196, 10.4234469)
    >>> get_coordinates("Berlin")
    (52.5170365, 13.3888599)
    >>> get_coordinates("Berlin, Germany")
    (52.5170365, 13.3888599)
    >>> get_coordinates("Germany, Berlin")
    (52.5170365, 13.3888599)
    """
    geolocator = Nominatim(user_agent="imdb-map", timeout=None, scheme="http")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location_data = geolocator.geocode(location)
    if location_data:
        return location_data.latitude, location_data.longitude
    return (0,0)


def reverse_coordinates(coordinates):
    """
    Returns location by coordinates.
    >>> reverse_coordinates((52.882591, 7.864018))
    'Brügger Weg, Grönheim, Molbergen, Landkreis Cloppenburg,\
Lower Saxony, 49696, Germany'
    """
    logging.info("Defining your location")
    geolocator = Nominatim(user_agent="imdb-map", timeout=None, scheme="http")
    address = geolocator.reverse(coordinates, language='en')
    return address.address


# Functions for file management
def dataset_manager(filename, year, location):
    """
    Filters information and forms smaller set in separate file
    :param filename: str name of source file
    :param year:  year of searched films
    :param location: string location of user
    :return:
    """
    with open(filename, 'r', errors='ignore') as source:
        logging.info("Reading data from {}".format(filename))
        rows = [x for x in source.readlines() if str(year) in x and
                location in x]
        with open(FILTERED_FILE, "w") as result:
            for row in rows:
                result.write(row)
    logging.info("Filtered data saved in file {}".format(FILTERED_FILE))


def figure_10_closest(point, filename=FILTERED_FILE):
    """
    Returns information about 10 films with closest location
    :param point:
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        films = [x.split(")")[:2] for x in f.readlines()]
        for film in films:
            film[0] = film[0] + ")"
            logging.info("Processing info for {}".format(film[0]))
            film[1] = film[1].strip()
            film.append(get_coordinates(film[1]))
            length = round(distance.distance(point, film[2]).km, 3)
            film.append(length)
        logging.info("Filtered locations in your area")
    if len(films) < 11:
        return films
    return films[:10]


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
