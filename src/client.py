from wallpost import *


class Client(object):

    def __init__(self, users_context):
        """

        :param users_context:
        """
        self._users = users_context

    def post(self, username, message):
        user = self._users.getuser(username)
        if user is None:
            new_user = User(username)
            new_user.addpost(Message(username, message))
            self._users.adduser(new_user)
        else:
            user.addpost(Message(username, message))

    def follow(self, username, following):
        user = self._users.getuser(username)
        following = self._users.getuser(following)

        if user is not None and following is not None:
            user.addfollowing(following)
        else:
            raise NoSuchUser

    def get_user_timeline(self, user):
        user = self._users.getuser(user)
        if user is None:
            raise NoSuchUser
        else:
            user_wall = user.getposts()
            return user_wall

    def get_user_wall(self, user):
        user = self._users.getuser(user)
        following = user.getfollowing()
        wall = []
        wall.extend(user.getposts())
        for user in following:
            wall.extend(user.getposts())
        sorted_wall = sorted(wall, key=lambda k: k.timestamp, reverse=True)
        return sorted_wall

    def get_user_profile(self, username):
        user = self._users.getuser(username)
        if not user:
            raise NoSuchUser
        return user
