import time


class Users(object):

    def __init__(self):
        self.users = []

    def getuser(self, username):
        for user in self.users:
            if user.username == username:
                return user

    def adduser(self, user_object):
        assert isinstance(user_object, User)
        if user_object.username in [user.username for user in self.users]:
            pass
        else:
            self.users.append(user_object)


class Message(object):
    def __init__(self, user, message):
        self.username = user
        self.message = message
        self.timestamp = time.time()


class User(object):
    def __init__(self, name):
        self.username = name
        self.messages = []
        self._following = []

    def addpost(self, message):
        assert isinstance(message, Message)
        self.messages.append(message)

    def getposts(self):
        return self.messages

    def addfollowing(self, user):
        self._following.append(user)

    def getfollowing(self):
        return self._following


class NoSuchUser(Exception):
    pass
