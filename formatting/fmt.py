def two_digits_min(num: int):
    return "{:02d}".format(num)


def dec_places_min(f: float, places: int):
    return ("{price:." + str(places) + "f}").format(price=f)
