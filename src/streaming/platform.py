"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
#note: had to check how @property and super classes work
class StreamingPlatform:    
    def __init__(self, name):
        self._name = name
        self._catalogue = {}  
        self._users = {}  
        self._artists = {} 
        self._albums = {}    
        self._playlists = {}   
        self._sessions = []    
    def add_track(self, track): 
        self._catalogue[track.track_id] = track
    def add_user(self, user):
        self._users[user.user_id] = user
    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist
    def add_album(self, album):
        self._albums[album.album_id] = album
    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist
    def record_session(self, session):
        self._sessions.append(session)
        session.user.add_session(session)
    def get_track(self, track_id):
        return self._catalogue.get(track_id)
    def get_user(self, user_id):
        return self._users.get(user_id)
    def get_artist(self, artist_id):
        return self._artists.get(artist_id)
    def get_album(self, album_id):
        return self._albums.get(album_id)
    def all_users(self):
        return list(self._users.values())
    def all_tracks(self):
        return list(self._catalogue.values())
    #Q1
    def total_listening_time_minutes(self, start, end):
        total_minutes = 0.0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_minutes += session.duration_listened_minutes()
        return total_minutes
    #Q2
    def avg_unique_tracks_per_premium_user(self, days=30): #check why days not accessed
        premium_users = []
        for user in self._users.values():
            if user.__class__.__name__ == 'PremiumUser':
                premium_users.append(user)
        if not premium_users:
            return 0.0
        total_unique_tracks = 0
        for user in premium_users:
            unique_tracks = set()
            for session in user.sessions:
                unique_tracks.add(session.track.track_id)
            total_unique_tracks += len(unique_tracks)
        
        return total_unique_tracks / len(premium_users)
    #Q3
    def track_with_most_distinct_listeners(self):
        #make a loop if id is not in listeners!!!!
        track_listeners = {}
        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            if track_id not in track_listeners:
                track_listeners[track_id] = set()
            track_listeners[track_id].add(user_id)
        if not track_listeners:
            return None
        max_listeners = 0
        most_popular_track_id = None
        for track_id, listeners in track_listeners.items():
            if len(listeners) > max_listeners:
                max_listeners = len(listeners)
                most_popular_track_id = track_id
        return self._catalogue.get(most_popular_track_id)
    #Q4
    def avg_session_duration_by_user_type(self):
        #note:group
        type_durations = {}
        for session in self._sessions:
            user_type = session.user.__class__.__name__
            if user_type not in type_durations:
                type_durations[user_type] = []
            type_durations[user_type].append(session.duration_listened_seconds)
        averages = []
