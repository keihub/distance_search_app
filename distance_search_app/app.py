import pandas as pd
import pathlib
import urllib
import random
import requests
from geopy.distance import geodesic


def geocoding_addr(target_addr):
    url = "https://msearch.gsi.go.jp/address-search/AddressSearch"
    params = {
        "q": target_addr,
    }
    encoded_params = urllib.parse.urlencode(params)
    req_url = url + "?" + encoded_params
    fetched_geocode = requests.get(req_url)
    format_geocode = fetched_geocode.json()[0]["geometry"]["coordinates"]
    format_geocode.reverse()
    return tuple(format_geocode)


def fetch_distance():
    excel_path = pathlib.Path("data/test.xlsx")
    excel_df = pd.read_excel(str(excel_path))
    excel_df["point_a_lat_lon"] = excel_df["point_a"].apply(lambda x: geocoding_addr(x))
    excel_df["point_b_lat_lon"] = excel_df["point_b"].apply(lambda x: geocoding_addr(x))

    excel_df["distance(km)"] = excel_df.apply(
        lambda x: geodesic(x["point_a_lat_lon"], x["point_b_lat_lon"]).km, axis=1
    )
    random_number = random.randint(1, 20)
    with pd.ExcelWriter(str(excel_path), mode="a") as f:
        excel_df.to_excel(f, sheet_name=f"new_sheet{random_number}")


if __name__ == "__main__":
    fetch_distance()
    # TODO: google mapに表示される時間も取得できる様にする
