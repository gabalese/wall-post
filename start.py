import sys
from src.wallpost import *
from src.command_parser import ConsoleCommandParser, InvalidCommand
from src.client import Client

if __name__ == "__main__":
    print "Welcome to WallPost!"
    command = ConsoleCommandParser(Client(Users()))
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
