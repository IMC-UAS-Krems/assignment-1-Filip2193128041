# playlists.py
# ------------
# Implement playlist classes for organizing tracks.
# 
# Classes to implement:
#   - Playlist
#   - CollaborativePlaylist
class Playlist:
    def __init__(self, playlist_id: str, name: str, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []
    def add_track(self, track):
        if track not in self.tracks: 
            self.tracks.append(track)
    def remove_track(self, track_id: str):
        for i, track in enumerate(self.tracks):
            if track.track_id == track_id:
                self.tracks.pop(i)
                return
    def total_duration_seconds(self):
        return sum(track.duration_seconds for track in self.tracks)
class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, title, owner, **kwargs):
        super().__init__(playlist_id, title, owner, **kwargs)
        self.contributors = [owner] 
    def remove_contributor(self, user):
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)
    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)
