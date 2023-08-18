import requests
import base64

class SpotifyConnector:
    """
    Class to interface with Spotify's Web API.

    Attributes:
    -----------
    BASE_TOKEN_URL: str
        Endpoint for Spotify token authentication.
    BASE_API_URL: str
        Base URL for Spotify's Web API.
    app_id: str
        Client ID for the registered Spotify application.
    app_secret: str
        Client Secret for the registered Spotify application.

    Methods:
    --------
    _generate_auth_token():
        Returns an authentication token for Spotify's Web API.
    find(term, kind='track'):
        Searches for a term on Spotify and returns the results.
    """

    BASE_TOKEN_URL = "https://accounts.spotify.com/api/token"
    BASE_API_URL = "https://api.spotify.com/v1/"

    def __init__(self, app_id, app_secret):
        """
        Initializes the SpotifyConnector with app credentials.
        
        Parameters:
        -----------
        app_id : str
            Client ID for the registered Spotify application.
        app_secret : str
            Client Secret for the registered Spotify application.
        """
        self.app_id = app_id
        self.app_secret = app_secret

    def _generate_auth_token(self):
        """Generates and returns an authentication token for Spotify's Web API."""
        credentials = f"{self.app_id}:{self.app_secret}"
        encoded_creds = base64.b64encode(credentials.encode())
        payload = {
            "grant_type": "client_credentials"
        }
        headers = {
            "Authorization": f"Basic {encoded_creds.decode()}"
        }

        response = requests.post(self.BASE_TOKEN_URL, data=payload, headers=headers)
        return response.json().get('access_token', None)

    def find(self, term, kind='track'):
        """
        Searches for a term on Spotify and returns the results.

        Parameters:
        -----------
        term : str
            Search query (e.g., artist name, song title).
        kind : str, optional
            Type of search (e.g., track, artist). Default is 'track'.

        Returns:
        --------
        dict
            A dictionary containing the search results from Spotify's Web API.
        """
        token = self._generate_auth_token()
        request_headers = {
            "Authorization": f"Bearer {token}"
        }
        search_endpoint = f"{self.BASE_API_URL}search?q={term}&type={kind}"
        result = requests.get(search_endpoint, headers=request_headers)
        return result.json()

# Demonstration:
if __name__ == "__main__":
    app_id = "YOUR_APP_ID"
    app_secret = "YOUR_APP_SECRET"
    spotify_connector = SpotifyConnector(app_id, app_secret)
    search_output = spotify_connector.find("Imagine Dragons", kind="artist")
    print(search_output)
