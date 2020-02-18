import sys


def start(verbosity=False):
    """
    Returns valid parameters for main program
    :return:
    """
    print("You have opened your map generator)")
    try:
        latitude = float(input("Your location latitude: "))
        longtitude = float(input("Your location longtitude: "))
        year = int(input("Year wanted: "))
    except ValueError:
        sys.exit("Wrong info. Re-launch an application.")
    if input("Using verbose mode? Enter t/f: ") == "t":
        verbosity = True
    return (latitude, longtitude), verbosity, year


def finish(filename):
    """Says "bye" to the user"""
    print("Your HTML-map is saved in {}".format(filename))
