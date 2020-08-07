# Would like to test importing this new fancy API Client
from client import SpotifyAPIClient

# Get client credentials for authorization
client_id: str = "e99ac0ad2b5c4e329542c2361e28ae40"
client_secret: str = "ce7cca69ac934a868cdcdedf73107cb6"

# Initialize our client class
spotify = SpotifyAPIClient(client_id, client_secret)

# Start using it!
spotify.search({"track": "Time"}, search_type="track")
