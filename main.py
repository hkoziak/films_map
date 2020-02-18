import folium
import logging
import os
import sys

import communicator
import utils
from constants import RAW_DATASET, FILTERED_FILE, MAP_FILE


def main():
    """
    Program main body.
    @author: hkoziak, 18.02.2020
    :return:
    """
    user_location, verbosity, year = communicator.start()
    if verbosity:
        logging.basicConfig(level=logging.INFO)

    user_address = utils.reverse_coordinates(user_location)
    logging.info("Your location considered as {}".format(user_address))

    logging.info("Preparation of dataset.")
    if os.path.exists(FILTERED_FILE):
        os.remove(FILTERED_FILE)
    if os.path.exists(RAW_DATASET):
        utils.dataset_manager(RAW_DATASET, year, user_address.split(",")[-1])
    else:
        sys.exit("You didn't provide dataset, or use a wrong name")
    films_elements = utils.figure_10_closest(user_location)

    map = folium.Map(location=user_location, zoom_start=6)

    film_markers = folium.FeatureGroup(name=str(year))
    for film in films_elements:
        film_markers.add_child(folium.Marker(location=film[2],
             popup=str(film[0]), icon=folium.Icon()))
    map.add_child(film_markers)

    population_layer = folium.FeatureGroup(name = "Population")
    population_layer.add_child(folium.GeoJson(data=open('world.json', 'r',
         encoding='utf-8-sig').read(),
         style_function=lambda x: {
            'fillColor':'green' if x['properties']['POP2005'] < 10000000
            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
            else 'red'}))

    map.add_child(population_layer)
    map.add_child(folium.LayerControl())
    map.save(MAP_FILE)
    communicator.finish(MAP_FILE)


if __name__ == "__main__":
    main()
