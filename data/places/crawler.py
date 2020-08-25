import googlemaps
from models.Place import PlaceDetail, PlaceSearch
from settings import MAPSKEY


def text_search():
    gmaps = googlemaps.Client(key=MAPSKEY)
    if N <= 0:
        return 0
    unprocessed = (
        PlaceSearch.session.query(PlaceSearch).filter(PlaceSearch.data == None).first()
    )
    if unprocessed:

        result = gmaps.find_place(
            input=unprocessed.text_input,
            input_type=unprocessed.input_type,
            location_bias=unprocessed.locationbias,
        )
        unprocessed.data = result
        unprocessed.save(commit=True)
        return 1
    else:  # No places left ungeocoded
        return 0


def create_place_detail():
    """after doing text search, PlaceSearch.data field will contain
        useful information. Propagate this to PlaceDetail table
        to continue crawling"""
    place = (
        PlaceSearch.session.query(PlaceSearch)
        .filter(PlaceSearch.places == None)
        .first()
    )
    if place is None:
        return 0
    if place.data.get("status") == "OK":
        place_list = []
        candidates = place.data.get("candidates", [])
        for candidate in candidates:
            place_list.append(PlaceDetail(gmaps_id=candidate.get("place_id")))
        place.places = place_list
        place.save()
        return place.places.length
    return 0
