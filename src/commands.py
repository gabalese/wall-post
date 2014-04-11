import datetime


class Command(object):
    def __init__(self, client_context):
        self.client = client_context

    @staticmethod
    def time_ago(timestamp):
        current_ts = datetime.datetime.now()

        post_ts = datetime.datetime.fromtimestamp(timestamp)
        delta = current_ts - post_ts
        minutes = delta.seconds / 60
        if minutes > 0:
            return "{} minut{} ago".format(minutes, "es" if minutes != 1 else "e")
        else:
            return "{} second{} ago".format(delta.seconds, "s" if delta.seconds != 1 else "")


class CommandPost(Command):
    def execute(self, username, post):
        self.client.post(username, post)
        return True


class CommandUserView(Command):
    def execute(self, user):
        timeline = self.client.get_user_timeline(user)
        self.format(timeline)

    def format(self, user_wall):
        print ["{} - {} ({})".format(message.username, message.message, self.time_ago(message.timestamp))
               for message in user_wall]


class CommandUserFollow(Command):
    def execute(self, user, following):
        self.client.follow(user, following)
        return True


class CommandUserWall(Command):
    def execute(self, user):
        timeline = self.client.get_user_wall(user)
        self.format(timeline)

    def format(self, user_wall):
        print ["{} - {} ({})".format(message.username, message.message, self.time_ago(message.timestamp))
               for message in user_wall]


