import sys
from src.wallpost import *
from src.client import CommandParser, Client

if __name__ == "__main__":
    print "Welcome to WallPost!"
    users = Users()
    client = Client(users)
    command = CommandParser(client)
    while True:
        try:
            user_input = raw_input("> ")
            print command.command_parse(user_input)
        except InvalidCommand:
            print "Sorry, can't understand your command."
        except NoSuchUser:
            print "Sorry, the user does not exist."
        except KeyboardInterrupt:
            sys.exit()
