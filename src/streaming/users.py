"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
"""
users.py
--------
Implement user classes for the music streaming platform.

Classes to implement:
  - User
  - FreeUser
  - PremiumUser
  - FamilyAccountUser
  - FamilyMember
"""

"""
users.py
--------
Implement user classes for the music streaming platform.

Classes to implement:
  - User
  - FreeUser
  - PremiumUser
  - FamilyAccountUser
  - FamilyMember
"""

class User:
    def __init__(self, user_id:str, name:str, age:int): #had to check with AI if i have to specify if it is str,int etc.. inside the init
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []
    def add_session(self, session):
        self.sessions.append(session)
    def total_listening_seconds(self):
        return sum(session.duration_listened_seconds for session in self.sessions)
    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60
    def unique_tracks_listened(self):
        return {session.track.track_id for session in self.sessions}
class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6
    def __init__(self, user_id:str, name:str, age:int): 
        super().__init__(user_id, name, age)
        self.skips_this_hour = 0
class PremiumUser(User):
    def __init__(self, user_id:str, name:str, age:int, subscription_start:str):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start
class FamilyAccountUser(User):
    def __init__(self, user_id:str, name:str, age:int):
        super().__init__(user_id, name, age)
        self.sub_users = []
    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)
    def all_members(self):
        return [self] + self.sub_users
class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent