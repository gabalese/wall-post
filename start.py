import sys
from src.wallpost import *

if __name__ == "__main__":
    print "Welcome to WallPost!"
    users = Users()
    prompt = Command(users)
    print prompt.execute.__doc__
    while True:
        try:
            user_input = raw_input("> ")
            status = prompt.execute(user_input)
            if status is not True:
                print "\n".join(status)
        except InvalidCommand:
            print "Sorry, can't understand your command."
        except NoSuchUser:
            print "Sorry, the user does not exist."
        except KeyboardInterrupt:
            sys.exit()

