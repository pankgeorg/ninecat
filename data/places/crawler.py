import googlemaps

from models.Place import PlaceDetail, PlaceSearch
from settings import MAPSKEY


def place_search_fill_data():
    unprocessed = (
        PlaceSearch.session.query(PlaceSearch).filter(PlaceSearch.data == None).first()
    )
    if unprocessed:
        gmaps = googlemaps.Client(key=MAPSKEY)
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


def place_detail_fill_data():
    query = PlaceDetail.session.query
    place = (
        query(PlaceDetail).filter(PlaceDetail.data == None).first()
    )  # Get an unfilled item
    if not place or not place.gmaps_id:
        return 0
    gmaps = googlemaps.Client(key=MAPSKEY)
    result = gmaps.place(
        place.gmaps_id
    )  # Empty "Fields" means, get all data. Billing for that is big
    place.data = result
    place.save(commit=True)


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
        return len(place.places) if place_list else 0
    return 0
