#note: error,check if it is connected correctly to platform
# used this to understand @property: https://www.geeksforgeeks.org/python/python-property-function/
class Album:
    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self._tracks = []
    @property
    def tracks(self):
        return self._tracks
    def add_track(self, track):
        self._tracks.append(track)
        track.album = self  # 
        self._tracks.sort(key=lambda t: t.track_number)  
    def track_ids(self):
        return {track.track_id for track in self._tracks}
    def duration_seconds(self):
        return sum(track.duration_seconds for track in self._tracks)