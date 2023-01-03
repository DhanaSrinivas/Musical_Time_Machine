CLIENT_ID = "cbde9d4dc0a64485949ff92314259c6b"
CLIENT_SECRET = "91762fe11149441cb864363fe249ad6d"

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Scraping Billboard 100 on the date you wanna go back
date = input("Enter the date you wanna travel back in YYYY-MM-DD format: ")
link = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url=link)
file = response.text
soup = BeautifulSoup(file, "html.parser")
titles = []
tags = soup.select(selector=".lrv-u-width-100p #title-of-a-story")

for tag in tags:
    s = tag.string
    if s is not None:
        titles.append(s.replace("\n", "").replace("\t", ""))

titles = titles[:-4]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# Searching Spotify for songs
year = date.split("-")[0]
song_uris = []
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating your private playlist
my_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,
                                      description=f"These are "
                                                  f"the top Billboard songs as of {date}")

# Adding songs to your playlist
sp.playlist_add_items(playlist_id=my_playlist["id"], items=song_uris)
