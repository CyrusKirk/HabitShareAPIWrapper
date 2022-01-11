import requests
import json
from datetime import datetime

#TODO: implement fetching token/cookie with username/password
#      update constructor accordingly

HABITS_URL = 'https://habitshare.herokuapp.com/habits'
FRIENDS_URL = 'https://habitshare.herokuapp.com/api/v3/friends'
MESSAGE_URL = 'https://habitshare.herokuapp.com/messages'
FRIENDHABIT_URL = 'https://habitshare.herokuapp.com/api/v3/users/'

class HabitShare(object):
    def __init__(self,token, cookie):
        """
        habits - authorized user's set of habits and related data including trackers, last checkin, etc
        """
        self.auth_payload = {
            'Authorization': 'Token ' + token,
            'Cookie': 'csrftoken=' + cookie,
            'Content-type':'application/json', 
            'Accept':'application/json'
        }
        self.habits = requests.get(HABITS_URL, headers=self.auth_payload).json()
        self.friends = requests.get(FRIENDS_URL, headers=self.auth_payload).json()
    
    def getFriend(self, friend):
        """
        Return the id of a friend given their exact name in HabitShare.
        """
        usr = [user for user in self.friends if user['name']==friend][0]
        return usr

    def friendLastCheckin(self, friend):
        """
        Return the last overall checkin from a friend.
        """
        usr = self.getFriend(friend)
        return datetime.strptime(usr['lastCheckin'],'%Y-%m-%d')
    
    def message(self, friend, message):
        """
        Send a message from the authorized account to a friend
        """
        friend_id = str(self.getFriend(friend)['id'])
        body = json.dumps({'content': message, 'friendId':friend_id})
        r = requests.post(MESSAGE_URL, headers=self.auth_payload, data=body)
        return r

    def friendHabitTrackers(self, friend):
        """Returns dict of habit data from a friend
        """
        friend_id = str(self.getFriend(friend)['id'])
        fullFriendData = requests.get(FRIENDHABIT_URL+friend_id, headers=self.auth_payload).json()['habits']
        friendTrackers = {}
        for habit in fullFriendData:
            friendTrackers[habit['title']] = habit['trackers']
        return friendTrackers

        