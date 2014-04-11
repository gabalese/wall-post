from __future__ import print_function
from wallpost import *
from pyparsing import *


class Client(object):
    """

    """

    def __init__(self, users_context):
        """

        :param users_context:
        """
        self._users = users_context

    def _post(self, username, message):
        user = self._users.getuser(username)
        if user is None:
            new_user = User(username)
            new_user.addpost(Message(username, message))
            self._users.adduser(new_user)
        else:
            user.addpost(Message(username, message))

    def _follow(self, username, following):
        user = self._users.getuser(username)
        following = self._users.getuser(following)

        if user is not None and following is not None:
            user.addfollowing(following)
        else:
            raise NoSuchUser

    def _usertimeline(self, user):
        user = self._users.getuser(user)
        if user is None:
            raise NoSuchUser
        else:
            user_wall = user.getposts()
        return ["{} - {} ({})".format(message.username, message.message, time_ago(message.timestamp))
                for message in user_wall]

    def _user_wall(self, user):
        user = self._users.getuser(user)
        following = user.getfollowing()
        wall = []
        wall.extend(user.getposts())
        for user in following:
            wall.extend(user.getposts())

        sorted_wall = sorted(wall, key=lambda k: k.timestamp, reverse=True)
        return ["{} - {} ({})".format(message.username, message.message, time_ago(message.timestamp))
                for message in sorted_wall]


class CommandParser(object):

    def __init__(self, client_context):
        self.client = client_context
        self.bnf = self.makeBNF()

    def makeBNF(self):
        vPost = oneOf("->")
        vFollow = oneOf("follows")
        vWall = oneOf("wall")
        user = Word(alphas)
        message = Regex(r'.+')

        user_posts = (user.setResultsName("user") + vPost + message.setResultsName("post")).setParseAction(
            lambda s, l, t: self.client._post(t["user"], t["post"])
        )

        user_view = (user.setResultsName("user") + LineEnd()).setParseAction(
            lambda quals: self.client._usertimeline(quals["user"])
        )

        user_follows = (user.setResultsName("user") + vFollow + user.setResultsName("following")).setParseAction(
            lambda quals: self.client._follow(quals["user"], quals["following"])
        )

        user_wall = (user.setResultsName("user") + vWall).setParseAction(
            lambda quals: self.client._user_wall(quals["user"])
        )

        return (user_posts | user_view | user_follows | user_wall)

    def command_parse(self, string):
        return self.bnf.parseString(string)


def time_ago(timestamp):
    current_ts = datetime.datetime.now()
    post_ts = datetime.datetime.fromtimestamp(timestamp)
    delta = current_ts - post_ts
    minutes = delta.seconds / 60
    if minutes > 0:
        return "{} minut{} ago".format(minutes, "es" if minutes != 1 else "e")
    else:
        return "{} second{} ago".format(delta.seconds, "s" if delta.seconds != 1 else "")
