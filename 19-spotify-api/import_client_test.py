# Would like to test importing this new fancy API Client
from client import SpotifyAPIClient

# Get client credentials for authorization
client_id: str
client_secret: str

# Initialize our client class
spotify = SpotifyAPIClient(client_id, client_secret)

# Start using it!
spotify.search({"track": "Time"}, search_type="track")
