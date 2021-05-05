# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])


# Shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

# playlists = sp.current_user_playlists()
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# print(sp.playlist('4S7Yk4oYushiMYoChvV6SJ'))
print(sp.pause_playback())