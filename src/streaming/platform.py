"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from .users import PremiumUser, User
from .tracks import Song

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
    #using datetime and time delta to compare dates and count recent sessions, was having issues understanding how to implement the days parameter
    #https://docs.python.org/3/library/datetime.html = had to go through it using this to understand the library
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = []
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)
        if not premium_users:
            return 0.0
        #calculate the date from days ago
        cutoff_date = datetime.now() - timedelta(days=days)
        total_unique_tracks = 0
        for user in premium_users:
            unique_tracks = set()
            for session in user.sessions:
                #check if session is in those days
                if session.timestamp >= cutoff_date:
                    unique_tracks.add(session.track.track_id)

            total_unique_tracks += len(unique_tracks)
        return round(total_unique_tracks / len(premium_users),2)

    #Q3
    def track_with_most_distinct_listeners(self):
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
        type_durations = {}
        
        for session in self._sessions:
            user_type = session.user.__class__.__name__
            if user_type not in type_durations:
                type_durations[user_type] = []
            type_durations[user_type].append(session.duration_listened_seconds)
        
        result_list = []   
        for user_type in type_durations:
            durations = type_durations[user_type]
            average = sum(durations) / len(durations)
            result_list.append((user_type, average))
        #sort them
        for i in range(len(result_list)):
            for j in range(i + 1, len(result_list)):
                if result_list[i][1] < result_list[j][1]:
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp
        return result_list

    #Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0
        
        for user in self._users.values():
            if user.__class__.__name__ == 'FamilyAccountUser':
                for sub_user in user.sub_users:
                    if sub_user.age < age_threshold:
                        total_seconds += sub_user.total_listening_seconds()
        return total_seconds / 60

    #Q6
    def top_artists_by_listening_time(self, n: int = 5):
        artist_time = {}
        
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                if artist not in artist_time:
                    artist_time[artist] = 0
                artist_time[artist] += session.duration_listened_seconds
        result = []
        for artist in artist_time:
            total_minutes = artist_time[artist] / 60
            result.append((artist, total_minutes))
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                if result[i][1] < result[j][1]:
                    temp = result[i]
                    result[i] = result[j]
                    result[j] = temp
        return result[:n]

    #Q7
    def user_top_genre(self, user_id: str) -> tuple[str, float]:
        user = self._users.get(user_id)
        if user is None:
            return None
        genre_time = {}
        total_time = 0
        for session in user.sessions:
            genre = session.track.genre
            if genre not in genre_time:
                genre_time[genre] = 0
            genre_time[genre] += session.duration_listened_seconds #increment
            total_time += session.duration_listened_seconds
        
        if total_time == 0:
            return None
        top_genre = None
        top_time = 0
        for genre in genre_time:
            if genre_time[genre] > top_time:
                top_time = genre_time[genre]
                top_genre = genre
        
        percentage = (top_time / total_time) * 100
        return (top_genre, percentage)

    #Q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        result = []
        for playlist in self._playlists.values():
            if playlist.__class__.__name__ == 'CollaborativePlaylist': #Find collaborativeplaylist
                artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)
                if len(artists) > threshold:
                    result.append(playlist)
        return result

    #Q9
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        playlist_tracks = 0
        collab_counter = 0
        collab_tracks = 0
        playlist_counter=0

        for playlist in self._playlists.values():
            if playlist.__class__.__name__=="Playlist":
                playlist_counter +=1
                playlist_tracks+=len(playlist.tracks)
            elif playlist.__class__.__name__== "CollaborativePlaylist":
                collab_counter +=1
                collab_tracks+=len(playlist.tracks)
        result= {}
        result['Playlist'] = playlist_tracks/playlist_counter if playlist_counter >0 else 0.0 #why is there an error?
        result['CollaborativePlaylist'] = collab_tracks / collab_counter if collab_counter >0 else 0.0
        return result

    #Q10
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result = []
        
        for user in self._users.values():
            # Get track IDs
            user_track_ids = set()
            for session in user.sessions:
                user_track_ids.add(session.track.track_id)
            
            completed_albums = []
            for album in self._albums.values():
                album_tracks = album.track_ids() if hasattr(album, 'track_ids') else album._tracks
                if not album_tracks:
                    continue
            else:
                 album_track_ids = set(album_tracks)
            if album_track_ids.issubset(user_track_ids):
                    completed_albums.append(album.title)        
            #add if they finished an album
            if completed_albums:
                result.append((user, completed_albums))
        return result