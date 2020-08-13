#!/bin/env python3

"""
Small module to download and extract a dataframe with the
Pharmacy Duties in Athens, Greece, through the official portal
fsa.gr
"""
m
import datetime
from itertools import islice
from time import sleep
from typing import List, Tuple
from urllib.parse import urlencode

import bs4
import pandas
import requests
from requests.models import Response

from models.Pharmacy import Duty, DutyOrm, Pharmacy, PharmacyOrm

print(f"Loading @{datetime.datetime.now()}")
TEMPLATE = "prevcat=1&prevcat1=&dateduty=5%2F10%2F2019&areaid=0&x=30&y=10"
TQS = {"prevcat": 1, "dateduty": "29/02/2020", "areaid": 0, "x": 30, "y": 10}

U = "http://www.fsa.gr/duties.asp"

PharmaT = Tuple[str, str, str, str, str]
DateT = str
AreaT = Tuple[str, str]


def tuple_to_duty(tpl):
    return Duty(fsa_id=tpl[0], name=tpl[1], area=tpl[2], time=tpl[3], date=tpl[4])


def tuple_to_pharma(tpl):
    return Pharmacy(fsa_id=tpl[4], name=tpl[0], area=tpl[2], tel=tpl[3], address=tpl[1])


def parse_dates_areas(response: Response) -> Tuple[List[AreaT], List[DateT]]:
    """Parses the home page and gets the options for dates & areas"""
    html = bs4.UnicodeDammit(response.content, ["greek", "iso8859_7"]).unicode_markup
    soup = bs4.BeautifulSoup(html, features="lxml")
    options = soup.find_all("option")
    dates = [
        (a.attrs["value"])
        for a in options
        if "value" in a.attrs.keys() and "/" in a.attrs["value"]
    ]  # Includes All areas coded '0'
    areas = [
        (a.text.strip(), a.attrs["value"])
        for a in options
        if "/" not in a.attrs["value"]
    ][1:]
    # This removes "(Επιλέξτε Ημερομηνία, 0)"

    return areas, dates


def parse_page(response: Response, date: DateT = None) -> Tuple[List[PharmaT], bool]:
    """Process a page with active pharmacies. parse_date helper function.
    This fn acts as an aggregator, the date argument is just being passed around
    to have handy across iterations"""
    soup = bs4.BeautifulSoup(response.content.decode("iso8859_7"), features="lxml")
    trs = soup.find_all("table")[2].find_all("tr")[1:]
    id_onclick = lambda el: el.find("a").attrs["onclick"].split("&")[0].split("=")[2]
    list_ = []

    for tr_elem in trs:
        _id = id_onclick(tr_elem)
        a_val, b_val, c_val = [td.text.strip() for td in tr_elem.find_all("td")]
        list_.append((_id, a_val, b_val, c_val, date))
    # Test if it is the last page
    try:
        a_elem = soup.find_all("table")[3].find_all("a")
        t_val = len(a_elem) == 4 or ">>" in a_elem[1].attrs["href"]
    except Exception as e:
        print("error")
        # On error stop iteration for this date and continue
        t_val = False

    return list_, t_val


def parse_date(date: DateT) -> List[PharmaT]:
    """Returns a list of Pharmacies that are on duty on a given date.
    Uses parse_page to get the data"""
    i = 1
    d_val = {"areaid": 0, "dateduty": date}
    url = U + "?" + urlencode(d_val)
    nr_val = requests.get(url)
    pharmas, cont = parse_page(nr_val, date)

    while cont:
        d_val.update({"list_PagingMove": ">", "PrevAbsolutePage": i})
        url = U + "?" + urlencode(d_val)
        nr_val = requests.get(url)
        ext, cont = parse_page(nr_val, date)
        pharmas.extend(ext)
        print("Date {}, page {}".format(date, i))
        i += 1
        sleep(0.2)

    return pharmas


def parse_pharma(_id: str):
    """parse pharmacy"""
    url = "http://fsa.gr/pharmacyshow.asp?pharmacyid={}&programmeid=11".format(_id)
    nr_val = requests.get(url)
    soup = bs4.BeautifulSoup(nr_val.content.decode(), features="lxml")
    tds = [a.text.strip() for a in soup.find_all("td")[5:][::3]][1:]
    tds.append(_id)
    ## TODO define types for this
    return tds


def run(xlOut=False):
    """Include here default running"""
    duties = requests.get(U)

    if duties.ok:
        _, dates = parse_dates_areas(duties)
        ps_val = []

        for date in dates:
            print(date)
            ps_val.extend(parse_date(date))
        df_val = pandas.DataFrame(ps_val)
        df_val.columns = ["id", "name", "area", "time", "date"]
        print("Getting pharmas")
        pharmas = []

        for _id in df_val.id.drop_duplicates():
            pharmas.append(parse_pharma(_id))
            print(_id)
            sleep(0.2)

        if xlOut:
            pandas.DataFrame(pharmas).to_excel("pharmas.xlsx")
            df_val.to_excel("{}_fsa.xlsx".format(dates[0]).replace("/", "-"))
    else:
        print("sorry something is wrong")


if __name__ == "__main__":
    run_with_db()


def run_with_db(N=None):
    """Include here default running with database"""
    duties = requests.get(U)

    if duties.ok:
        _, dates = parse_dates_areas(duties)
        ps_val = []
        ids = set()
        n = N if N is not None else len(dates)
        for date in islice(dates, n):
            print(date)
            ps_val.extend(parse_date(date))
        for duty in ps_val:
            tpl = tuple_to_duty(duty)
            ids.add(tpl.fsa_id)
            db_tpl = (
                DutyOrm.session.query(DutyOrm)
                .filter(DutyOrm.fsa_id == tpl.fsa_id, DutyOrm.date == tpl.date)
                .first()
            )
            if db_tpl:
                for key, value in tpl.dict().items():
                    setattr(db_tpl, key, value)
                db_tpl.updated_at = datetime.datetime.now(datetime.timezone.utc)
                db_tpl.save(commit=False)
            else:
                dutyOrm = DutyOrm(**tpl.dict())
                dutyOrm.save(commit=False)
        pharmas = []
        for _id in list(ids):
            pharmas.append(parse_pharma(_id))
            print(_id)
            sleep(0.1)
        for pharma in pharmas:
            tpl = tuple_to_pharma(pharma)
            db_tpl = (
                PharmacyOrm.session.query(PharmacyOrm)
                .filter(PharmacyOrm.fsa_id == tpl.fsa_id)
                .first()
            )
            if db_tpl:
                for key, value in tpl.dict().items():
                    setattr(db_tpl, key, value)
                db_tpl.updated_at = datetime.datetime.now(datetime.timezone.utc)
                db_tpl.save(commit=False)
            else:
                pharmaOrm = PharmacyOrm(**tpl.dict())
                pharmaOrm.save(commit=False)
        try:
            DutyOrm.session.commit()
            PharmacyOrm.session.commit()
        except Exception as e:
            pass
        return ps_val, pharmas
