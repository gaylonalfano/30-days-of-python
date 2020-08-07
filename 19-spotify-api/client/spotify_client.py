#!/usr/bin/env python
# coding: utf-8

# In[1]:


import typing as t
import requests
import base64
import datetime
from urllib.parse import urlencode


# In[25]:


# Declare our first class with helper methods
class SpotifyAPIClient(object):
    access_token: str = None
    access_token_expires = datetime.datetime.now()  # or None
    access_token_did_expire: bool = True
    client_id: str = None
    client_secret: str = None
    token_url: str = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        # Call super() so we can call any class we inherit from directly!
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self) -> str:
        """
        Returns a Base 64 encoded string (not bytes!)
        """
        # Need to declare our client_id and client_secret vars
        # The self obj has them but need to update within this
        # method's scope:
        # NOTE ?? Aren't these already available though since we
        # set them inside the __init__ function? I think so but
        # this makes it cleaner so we don't have to {self.client_id}??
        client_id: str = self.client_id
        client_secret: str = self.client_secret

        # Update the client_id and client_secret values
        if client_id is None or client_secret is None:
            raise Exception("You must set client_id and client_secret.")

        # Build the credentials str required by Spotify:
        client_creds: str = f"{client_id}:{client_secret}"
        client_creds_bytes: bytes = client_creds.encode()
        client_creds_b64: bytes = base64.b64encode(client_creds_bytes)
        # NOTE We must .decode() back to 'str' type instead of 'bytes'
        client_creds_b64_decoded: str = client_creds_b64.decode()

        return client_creds_b64_decoded

    def get_token_headers(self) -> t.Dict:
        """
        Pass 'Authorization' header with b64 encoded creds
        "Authorization": "Basic <base64 encoded client_id:client_secret>"
        """
        client_creds_b64_decoded: str = self.get_client_credentials()

        token_headers: t.Dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_creds_b64_decoded}"
        }

        return token_headers
    
    def get_token_data(self) -> t.Dict:
        token_data: t.Dict = {
            "grant_type": "client_credentials",
        }

        return token_data

    def perform_authorization(self) -> bool:
        """
        Extracts the access token and other variables for authorizing
        the client app with Spotify API. It uses helper methods to get
        client credentials, convert to Base 64, get token headers and
        token data. 
        """
        # TODO Re-run authorization if access_token expires
        # Use helper methods to retrieve components for sending request
        token_url: str = self.token_url
        token_data: t.Dict = self.get_token_data()
        token_headers: t.Dict = self.get_token_headers()

        # Now we have everything for authentication so it's time to make the POST request
        r = requests.post(token_url, data=token_data, headers=token_headers)

        if r.status_code not in range(200, 299):
            raise Exception(f"Could not authenticate client: {status_code}")
            # return False

        # Let's store the access token, expires in (seconds), etc.
        data: t.Dict = r.json()
        now = datetime.datetime.now()
        access_token: str = data['access_token']
        expires_in: float = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)

        # Update our class variables with these updated values
        self.access_token = access_token
        self.access_token_expires = expires  # datetime.datetime obj
        self.access_token_did_expire = expires < now  # refetch the token if True

        return True  # authorization successful

    def get_access_token(self) -> str:
        """
        Retrieve the authorized access token for our client app.
        """
        token: str = self.access_token
        expires = self.access_token_expires  # datetime
        now = datetime.datetime.now()

        if expires < now:
            # Retrieve by re-running this exact function!
            self.perform_authorization()
            return self.get_access_token()
        elif token is None:
            self.perform_authorization()
            return self.get_access_token()
        return token
    
    def get_resource_headers(self) -> t.Dict:
        """
        Retrieve the authorized access headers for our client app.
        Specifically, retrieve the Authorization header with the
        Bearer token. This is the header we want/need to pass for
        all of our resources/endpoints we access.
        """
        access_token: str = self.get_access_token()
        headers: t.Dict = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers



    def get_resource(self, lookup_id: str, resource_type: str = "albums", api_version: str = "v1") -> t.Dict:
        """
        Generalized method for retrieving a single artist or album,
        based on the resource type and id value. Must use an
        authorized client in order to access resource type.

        Params:
            _id = ID of the resource
            resource_type = Spotify API endpoint/resource to access
        """
        assert resource_type.lower() in ["artists", "albums"]
        base_url: str = "https://api.spotify.com"
        endpoint: str = f"{base_url}/{api_version}/{resource_type}/{lookup_id}"
        headers: t.Dict = self.get_resource_headers()

        # We have the pieces let's now build our request
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            print(f"Failed request: {r.status_code} : {endpoint}")
            return {}
        return r.json()

    
    def get_album(self, _id: str):
        """
        Search for a single album via Spotify's Albums endpoint:
        https://api.spotify.com/v1/albums/{id}
        """
        # === OLD reference only ===
        # base_url: str = "https://api.spotify.com/"
        # endpoint: str = f"{base_url}/v1/albums/{_id}"
        # r = requests.get(endpoint)
        # if r.status_code not in range(200, 299):
        #     return {}
        # return r.json()

        return self.get_resource(lookup_id=_id, resource_type="albums")

    def get_artist(self, _id: str):
        """
        Search for a single artist via Spotify's Artists endpoint:
        https://api.spotify.com/v1/artists/{id}
        """
        return self.get_resource(lookup_id=_id, resource_type="artists")


    def base_search(self, query_params: str):
        """
        Performs the actual request to API service. The query parameters
        are processed and urlencoded in 'search()' method.

        Params:
            query_params: str = Either a parsed Dict that's been converted
                to string or a simple string.
        """
        assert isinstance(query_params, str)
        headers: t.Dict = self.get_resource_headers()
        endpoint: str = "https://api.spotify.com/v1/search"
        # Let's build/concat our 'lookup_url' for use. Don't forget '?' symbol!
        lookup_url: str = f"{endpoint}?{query_params}"

        # Now that we have the bare minimum requirements, let's make a request
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            print(f"Failed request: {r.status_code} : {lookup_url}")
            return {}
        return r.json()


    def search(self, query: t.Optional[str] = None, operator: t.Optional[str] = None, operator_query: t.Optional[str] = None, search_type: str = 'artist'):
        """
        Parse and construct the query into query_params that can get passed to
        the base_search(query_params) method...??

        Search the Spotify API for various songs, artists,
        albums, etc. Following the "Writing a Query - Guidelines":
        https://developer.spotify.com/documentation/web-api/reference/search/search/

        Params:
            query- Query string that gets url encoded
            search_type - Default='artist'. Type of search to perform in Spotify
        """
        assert search_type.lower() in ["artist", "track", "playlist", "album", "show", "episode"]

        if query is None:
            raise Exception("A query is required.")

        if isinstance(query, dict):
            # Convert query Dict to str.
            # NOTE urlencode() will convert " " to '%20' or '+' hex code
            query: str = " ".join([f"{k}:{v}" for k, v in query.items()])  # 'album:gold artist:abba'

        # Let's check if an operator has been passed for our query
        # === MY VERSION === NOTE Read notes assert vs raise Exception
        # if operator is not None and operator_query is not None:
        #     assert operator.lower() is in {"or", "not"}
        #     assert isinstance(operator_query, str)
        #     # Convert to uppercase per the docs
        #     operator = operator.upper()
        #     # Rebuild our query string with the operator included
        #     # E.g., q=roadhouse%20NOT%20blues
        #     query: str = f"{query} {operator} {operator_query}"
        # === INSTRUCTOR'S VERSION ===
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"

        # We need to pass our 'data/query' within the url string we send our GET request to
        # To make this easier we use urlencode()
        # NOTE Could consider having 'type' be a List or Dict for more options
        query_params: str = urlencode({
            "q": query,
            "type": search_type.lower()  # "Track" -> "track"
        })
        print(query_params)

        return self.base_search(query_params)

