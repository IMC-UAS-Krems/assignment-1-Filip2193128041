"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
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
    def avg_unique_tracks_per_premium_user(self, days=30):
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
        for user_type, durations in type_durations.items():
            avg_duration = sum(durations) / len(durations)
            averages.append((user_type, avg_duration))
        averages.sort(key=lambda x: x[1], reverse=True)
        return averages
    #Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total_minutes = 0.0
        for user in self._users.values():
            if user.__class__.__name__ == 'FamilyAccountUser':
                for sub_user in user.sub_users:
                    if sub_user.age < age_threshold:
                        for session in sub_user.sessions:
                            total_minutes += session.duration_listened_minutes()
        return total_minutes
    #q6:
    def top_artists_by_listening_time(self, n=5):
        artist_minutes = {}
        
        for session in self._sessions:
            track = session.track
            # count Song instances (not podcasts/audiobooks)
            if track.__class__.__name__ == 'Song' or track.__class__.__name__ == 'AlbumTrack' or track.__class__.__name__ == 'SingleRelease':
                artist = track.artist
                if artist not in artist_minutes:
                    artist_minutes[artist] = 0
                artist_minutes[artist] += session.duration_listened_minutes()
        
        sorted_artists = sorted(artist_minutes.items(), key=lambda x: x[1], reverse=True)
        return sorted_artists[:n]
    #Q7
    def user_top_genre(self, user_id):
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None
        genre_time = {}
        total_time = 0
        for session in user.sessions:
            genre = session.track.genre
            minutes = session.duration_listened_minutes()
            if genre not in genre_time:
                genre_time[genre] = 0
            genre_time[genre] += minutes
            total_time += minutes
        if total_time == 0:
            return None
        top_genre = None
        max_time = 0
        for genre, time in genre_time.items():
            if time > max_time:
                max_time = time
                top_genre = genre
        percentage = (max_time / total_time) * 100
        return (top_genre, percentage)
    #Q8:
    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []
        for playlist in self._playlists.values():
            if playlist.__class__.__name__ != 'CollaborativePlaylist':
                continue
            artists = set()
            for track in playlist.tracks:
                if hasattr(track, 'artist'): 
                    artists.add(track.artist)
            #CHECK THIS WHY IT DIDNT RUn
            if len(artists) > threshold:
                result.append(playlist)
        return result
    #Q9: 
    def avg_tracks_per_playlist_type(self):
        playlist_count = 0
        playlist_tracks = 0
        collab_count = 0
        collab_tracks = 0
        for playlist in self._playlists.values():
            if playlist.__class__.__name__ == 'Playlist': #works
                playlist_count += 1
                playlist_tracks += len(playlist.tracks)
            elif playlist.__class__.__name__ == 'CollaborativePlaylist':
                collab_count += 1
                collab_tracks += len(playlist.tracks)
        result = {}
        result['Playlist'] = playlist_tracks / playlist_count if playlist_count > 0 else 0.0
        result['CollaborativePlaylist'] = collab_tracks / collab_count if collab_count > 0 else 0.0
        return result
    #Q10: 
    def users_who_completed_albums(self):
        result = []
        for user in self._users.values():
            completed_albums = []
            #tlistened to
            user_track_ids = set()
            for session in user.sessions:
                user_track_ids.add(session.track.track_id)
            for album in self._albums.values():
                if not album._tracks: 
                    continue
                album_track_ids = album.track_ids()
                if album_track_ids.issubset(user_track_ids):
                    completed_albums.append(album.title)
            if completed_albums:
                result.append((user, completed_albums))
        return result