"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
class ListeningSession:
    def __init__(self,session_id,user,track,daytime,duration_listened_seconds):
        self.session_id=session_id
        self.user=user
        self.track=track
        self.timestamp=daytime
        self.duration_listened_seconds=duration_listened_seconds

    def duration_listened_minutes(self):
        return int(self.duration_listened_seconds)/60