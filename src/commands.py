from time_format import TimeFormatter


class Command(object):
    def __init__(self, client_context):
        self.client = client_context


class CommandPost(Command):
    def execute(self, username, post):
        self.client.post(username, post)
        return True


class CommandUserView(Command):
    def execute(self, user):
        timeline = self.client.get_user_timeline(user)
        self.format(timeline)

    def format(self, user_wall):
        print ["{} - {} ({})".format(message.username, message.message, TimeFormatter.time_ago(message.timestamp))
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
        print ["{} - {} ({})".format(message.username, message.message, TimeFormatter.time_ago(message.timestamp))
               for message in user_wall]


