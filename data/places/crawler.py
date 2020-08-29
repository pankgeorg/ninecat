import datetime
from time import sleep

import googlemaps
from sqlalchemy import text

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
        unprocessed.updated_at = datetime.datetime.now()
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
    place.updated_at = datetime.datetime.now()
    place.save(commit=True)


def create_place_detail():
    """after doing text search, PlaceSearch.data field will contain
        useful information. Propagate this to PlaceDetail table
        to continue crawling"""
    place = (
        PlaceSearch.session.query(PlaceSearch)
        .filter(PlaceSearch.places == None)
        .filter(text("CAST(places.place_text_search.data->>'status' AS TEXT) = 'OK'"))
        .first()
    )
    if place is None:
        return 0
    if place.data and place.data.get("status") == "OK":
        place_list = []
        candidates = place.data.get("candidates", [])
        for candidate in candidates:
            place_detail = PlaceDetail(
                gmaps_id=candidate.get("place_id"), updated_at=datetime.datetime.now()
            )
            place_list.append(place_detail)
        place.places = place_list
        place.updated_at = datetime.datetime.now()
        place.save()
        return len(place.places) if place_list else 0
    return 0


NEARBY = "nearby"
TEXT = "text"
FIND_PLACE = "find_place_only"
DETAILS = "details"


def try_again(fn, attempt, **kwargs):
    if attempt > 10:
        raise Exception("Tried 10 times, does not work man!")
    sleep(2 * attempt)
    try:
        return fn(**kwargs)
    except googlemaps.exceptions.ApiError:
        print(f"Retrieving failed: Trying for {attempt +1} time")
        sleep(1)
        return try_again(fn, attempt + 1, **kwargs)


def place_query_request():
    place_request = (
        PlaceSearch.session.query(PlaceSearch)
        .filter(PlaceSearch.data == None)
        .filter(PlaceSearch.endpoint_type != None)
        .filter(PlaceSearch.input_params != None)
        .first()
    )
    if not place_request:
        return
    endpoint_type = place_request.endpoint_type
    p = place_request.input_params
    gmaps = googlemaps.Client(key=MAPSKEY)
    if endpoint_type == NEARBY:
        location = p.get("location").split(",")
        radius = p.get("radius")
        keyword = p.get("keyword")
        result = gmaps.places_nearby(location=location, radius=radius, keyword=keyword)
        page_token = result.get("next_page_token", None)
        while page_token:
            sleep(0.5)
            next_page = try_again(
                gmaps.places_nearby,
                1,
                location=location,
                radius=radius,
                keyword=keyword,
                page_token=page_token,
            )
            result["results"].extend(next_page.get("results", []))
            result["html_attributions"].extend(next_page.get("html_attributions", []))
            page_token = next_page.get("page_token")

        place_request.data = result
        place_request.updated_at = datetime.datetime.now()
        place_request.save(commit=True)
