class Users(object):

    def __init__(self):
        pass

    def getuser(self, username):
        pass


class User(object):
    def __init__(self):
        pass


class NoSuchUser(Exception):

    def __init__(self, message):
        super(NoSuchUser.__init__(self, message))


class Messages(object):
    pass


class Message(object):
    pass


class Command(object):
    """

    """
    def __init__(self, users_context, messages_context):
        """

        :param users_context:
        :param messages_context:
        """
        pass

    def execute(self, commandstring):
        """

        :param commandstring:
        """
        pass