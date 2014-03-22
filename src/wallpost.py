import datetime


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
        self.timestamp = datetime.datetime.now().strftime("%s")

    @property
    def minutes_ago(self):
        current_ts = datetime.datetime.now()
        post_ts = datetime.datetime.fromtimestamp(int(self.timestamp))
        delta = current_ts - post_ts
        minutes = delta.seconds / 60
        return "{} minut{} ago".format(minutes, "es" if minutes != 1 else "e")


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


class InvalidCommand(Exception):
    pass


class Command(object):
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
            return user.getposts()

    def _user_wall(self, user):
        user = self._users.getuser(user)
        following = user.getfollowing()
        wall = []
        wall.extend(user.getposts())
        for user in following:
            wall.extend(user.getposts())

        sorted_wall = sorted(wall, key=lambda k: k.timestamp, reverse=True)
        return sorted_wall

    def execute(self, commandstring):
        """
        Command examples:
        > <username> -> <message>
        / Posting
        > <username>
        / Reading
        > <username> follows <username>
        Following
        > <username> wall
        Subscription wall

        :param commandstring:
        """
        command = commandstring.split()

        if len(command) == 1:
            # Simple user name
            timeline = self._usertimeline(command[0])
            return ["{} ({})".format(message.message, message.minutes_ago) for message in timeline]
        elif len(command) == 2:
            # User reads his wall
            if command[1] == "wall":
                user_wall = self._user_wall(command[0])
                return ["{} - {} ({})".format(message.username, message.message, message.minutes_ago)
                        for message in user_wall]
            else:
                raise InvalidCommand
        elif len(command) >= 3:
            # user posts or follows someone else
            if command[1] == "->":
                # User posts
                self._post(command[0], " ".join(command[2:]))
                return True
            if command[1] == "follows":
                if len(command[2:]) != 1:
                    raise InvalidCommand
                else:
                    self._follow(command[0], command[2])
                    return True
            else:
                raise InvalidCommand
        else:
            return False
