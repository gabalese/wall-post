import sys
from src.wallpost import *

if __name__ == "__main__":
    print "Welcome to WallPost!"
    users = Users()
    client = Client(users)
    print client.command_parse.__doc__
    while True:
        try:
            user_input = raw_input("> ")
            print client.command_parse(user_input)
        except InvalidCommand:
            print "Sorry, can't understand your command."
        except NoSuchUser:
            print "Sorry, the user does not exist."
        except KeyboardInterrupt:
            sys.exit()
