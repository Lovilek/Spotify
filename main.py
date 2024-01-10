from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "4098291307c6448fa750de31c54f9227"
client_secret = "be76420875c049b3a70cd5ea4ff77d22"
nickname = "hen892ejjs6x3jfc1p8zyvbpg"

date = input("Which year do you want to travel to? Type th date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")
names = [name.getText().strip() for name in soup.select("li ul li h3")]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=nickname,
    )
)
user_id = sp.current_user()["id"]
year = date.split("-")[0]
songs_uri = []
for song in names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.")

playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
playlist_id = playlist['id']
sp.playlist_add_items(playlist_id, songs_uri)
