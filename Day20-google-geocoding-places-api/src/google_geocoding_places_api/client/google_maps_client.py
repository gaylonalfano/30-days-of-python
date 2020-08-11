#!/usr/bin/env python
# coding: utf-8

# In[11]:


import typing as t
from urllib.parse import urlencode, urlparse, parse_qsl

import requests

from google_geocoding_places_api import settings


# In[12]:


API_KEY = settings.API_KEY


# In[13]:


class GoogleMapsAPIClient(object):
    lat: t.Optional[float] = None
    lng: t.Optional[float] = None
    data_type: str = "json"  # or lookup_type
    location_query: t.Optional[str] = None
    api_key: t.Optional[str] = None

    def __init__(
        self,
        api_key: t.Optional[str] = None,
        address_or_postal_code: t.Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if api_key is None:
            raise Exception("Must provide an API key.")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query is not None:
            self.extract_latlng()

    # We have our 'url' ready for the request but we want to return the latitude and longitude
    # Let's convert this into a function
    def extract_latlng(self, location: t.Optional[str] = None) -> t.Tuple:
        # set 'loc_query' to original default self.location_query set from instantiation
        loc_query: str = self.location_query
        # If 'location' is passed/provided, then update self.location_query
        if location is not None:
            # NOTE ?? - Why not just set self.location_query = location?
            loc_query = location

        # outputFormat
        params: t.Dict = {"address": loc_query, "key": self.api_key}
        url_params: str = urlencode(params)
        endpoint: str = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        url: str = f"{endpoint}?{url_params}"

        # Now we have our request url let's make the request
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            print(f"Request failed! {url}")
            return {}

        # Try to set/extract the lat lng data from 'location' key
        # r.json()['results'][0]['geometry']['location']
        # {'lat': 37.4220578, 'lng': -122.0840897}
        latlng: t.Dict[str, float] = {}
        try:
            latlng = r.json()["results"][0]["geometry"]["location"]
        except:
            pass

        # Set these lat,lng values back to the class variables
        lat: float = latlng.get("lat")
        lng: float = latlng.get("lng")
        self.lat = lat
        self.lng = lng

        # Use .get('key') to get result or None. If I use d['key'] could get KetError
        # return latlng.get('lat'), latlng.get('lng')  # (None, None)
        return lat, lng

    # Let's try the Nearby Search request to get multiple results
    def search(
        self,
        keyword: str = "Tex-Mex food",
        location: t.Optional[str] = None,
        radius: int = 1000,
    ) -> t.Dict:
        # https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters
        # Reference the class variables first:
        lat: float
        lng: float
        lat, lng = self.lat, self.lng
        # Check if location was passed
        if location is not None:
            # Updated lat, lng values by extracting
            # ?? Don't we have to pass 'location' to this extract_latlng() fn? YES!
            lat, lng = self.extract_latlng(location=location)
        base_endpoint: str = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        params: t.Dict = {
            "key": self.api_key,
            "location": f"{lat},{lng}",  # reference local 'lat' instead of class self.lat
            "radius": radius,  # meters
            "keyword": keyword,
        }
        params_encoded: str = urlencode(params)
        places_endpoint: str = f"{base_endpoint}?{params_encoded}"

        r = requests.get(places_endpoint)
        if r.status_code not in range(200, 299):
            print(f"Search request failed: {places_endpoint}")
            return {}
        return r.json()  # Could refine later

    def detail(
        self,
        place_id: str = "ChIJ8ZTVZJmwj4ARQFv0RXspg3A",
        fields: t.List[str] = [
            "name",
            "rating",
            "formatted_phone_number",
            "formatted_address",
        ],
    ) -> t.Dict:
        # Once we get our place either from Place or Nearby request we can
        # use Place Detail along with place_id for a detail_lookup_request
        # https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY
        base_details_endpoint: str = f"https://maps.googleapis.com/maps/api/place/details/{self.data_type}"
        params: t.Dict = {
            "place_id": f"{place_id}",
            "fields": ",".join(fields),
            "key": self.api_key,
        }
        params_encoded: str = urlencode(params)
        details_endpoint: str = f"{base_details_endpoint}?{params_encoded}"

        r = requests.get(details_endpoint)
        if r.status_code not in range(200, 299):
            print(f"Detail request failed: {details_endpoint}")
            return {}
        return r.json()  # Could refine later


# In[14]:


client = GoogleMapsAPIClient(
    api_key=API_KEY, address_or_postal_code="Austin, TX"
)

# print(client.lat, client.lng)  # 30.267153 -97.7430608


# In[15]:


# Let's test out some search() and detail()
client.search("Tacos", location="Georgetown, TX")  # works!


# In[16]:


# Dos Salsas 'ChIJl4bD7WfWRIYRj928bZAMexI'
client.detail(place_id="ChIJl4bD7WfWRIYRj928bZAMexI")  # works!

