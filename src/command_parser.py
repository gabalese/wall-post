from pyparsing import *
from commands import *


class InvalidCommand(Exception):
    pass


class CommandParser(object):
    def __init__(self, client_context):
        self.client = client_context
        self.bnf = self.make_bnf()

    def make_bnf(self):
        verb_to_post = oneOf("->")
        verb_to_follow = oneOf("follows")
        verb_to_wall = oneOf("wall")
        user = Word(alphas)
        message = Regex(r'.+')

        user_posts = (user.setResultsName("user") + verb_to_post + message.setResultsName("post")).setParseAction(
            lambda s, l, t: CommandPost(self.client).execute(t["user"], t["post"])
        )

        user_view = (user.setResultsName("user") + LineEnd()).setParseAction(
            lambda quals: CommandUserView(self.client).execute(quals["user"])
        )

        user_follows = (user.setResultsName("user") + verb_to_follow + user.setResultsName("following") + LineEnd()).setParseAction(
            lambda quals: CommandUserFollow(self.client).execute(quals["user"], quals["following"])
        )

        user_wall = (user.setResultsName("user") + verb_to_wall + LineEnd()).setParseAction(
            lambda quals: CommandUserWall(self.client).execute(quals["user"])
        )

        return user_posts | user_view | user_follows | user_wall

    def command_parse(self, string):
        try:
            return self.bnf.parseString(string)
        except ParseException:
            raise InvalidCommand

